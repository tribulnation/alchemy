from typing_extensions import Any, Literal, NotRequired, TypedDict, get_type_hints
from dataclasses import dataclass, field
import os

import httpx
from pydantic import TypeAdapter
from typed_core.exceptions import ApiError, AuthError, BadRequest, RateLimited
from typed_core.http import HttpClient

from .util.paths import path_join


ALCHEMY_DATA_API_URL = 'https://api.g.alchemy.com'

ETHEREUM_ALCHEMY_RPC_URL = 'https://eth-mainnet.g.alchemy.com/v2'
BNB_ALCHEMY_RPC_URL = 'https://bnb-mainnet.g.alchemy.com/v2'
POLYGON_ALCHEMY_RPC_URL = 'https://polygon-mainnet.g.alchemy.com/v2'
BASE_ALCHEMY_RPC_URL = 'https://base-mainnet.g.alchemy.com/v2'
AVAX_ALCHEMY_RPC_URL = 'https://avax-mainnet.g.alchemy.com/v2'
OPTIMISM_ALCHEMY_RPC_URL = 'https://opt-mainnet.g.alchemy.com/v2'
ARBITRUM_ALCHEMY_RPC_URL = 'https://arb-mainnet.g.alchemy.com/v2'
GNOSIS_ALCHEMY_RPC_URL = 'https://gnosis-mainnet.g.alchemy.com/v2'
CELO_ALCHEMY_RPC_URL = 'https://celo-mainnet.g.alchemy.com/v2'

ETHEREUM_ALCHEMY_NFT_URL = 'https://eth-mainnet.g.alchemy.com/nft/v3'
BNB_ALCHEMY_NFT_URL = 'https://bnb-mainnet.g.alchemy.com/nft/v3'
POLYGON_ALCHEMY_NFT_URL = 'https://polygon-mainnet.g.alchemy.com/nft/v3'
BASE_ALCHEMY_NFT_URL = 'https://base-mainnet.g.alchemy.com/nft/v3'
AVAX_ALCHEMY_NFT_URL = 'https://avax-mainnet.g.alchemy.com/nft/v3'
OPTIMISM_ALCHEMY_NFT_URL = 'https://opt-mainnet.g.alchemy.com/nft/v3'
ARBITRUM_ALCHEMY_NFT_URL = 'https://arb-mainnet.g.alchemy.com/nft/v3'
GNOSIS_ALCHEMY_NFT_URL = 'https://gnosis-mainnet.g.alchemy.com/nft/v3'
CELO_ALCHEMY_NFT_URL = 'https://celo-mainnet.g.alchemy.com/nft/v3'


class RpcResponse(TypedDict):
  jsonrpc: Literal['2.0']
  id: int | str | None
  result: NotRequired[Any]
  error: NotRequired[Any]


rpc_response_adapter = TypeAdapter(RpcResponse)


def env_api_key(api_key: str | None = None) -> str:
  """Return the explicit API key or load `ALCHEMY_API_KEY`."""
  if api_key is not None:
    return api_key
  try:
    return os.environ['ALCHEMY_API_KEY']
  except KeyError as exc:
    raise ValueError('Either provide `api_key` or set ALCHEMY_API_KEY.') from exc


def authed_url(base_url: str, api_key: str) -> str:
  """Append the API key to an Alchemy base URL."""
  return path_join(base_url, api_key)


@dataclass(kw_only=True)
class Endpoint:
  """Base Alchemy endpoint with shared HTTP transport and validation defaults."""
  base_url: str
  http: HttpClient = field(default_factory=HttpClient)
  validate: bool = True

  def should_validate(self, validate_param: bool | None = None) -> bool:
    """Resolve per-call validation override against the client default."""
    return self.validate if validate_param is None else validate_param

  async def __aenter__(self):
    await self.http.__aenter__()
    return self

  async def __aexit__(self, exc_type, exc_value, traceback):
    await self.http.__aexit__(exc_type, exc_value, traceback)

  async def request(
    self, method: str, url: str, /, *,
    json: Any | None = None,
    params: dict[str, Any] | None = None,
  ) -> httpx.Response:
    """Send an HTTP request relative to this endpoint base URL."""
    return await self.http.request(
      method,
      self.base_url + url,
      json=json,
      params=params,
    )

  async def rpc_request(
    self, method: str, params: Any | None = None, *,
    id: int = 1, validate: bool | None = None,
  ) -> Any:
    """Send an Alchemy JSON-RPC request and return its result."""
    body: dict[str, Any] = {
      'jsonrpc': '2.0',
      'id': id,
      'method': method,
      'params': [] if params is None else [params],
    }
    r = await self.http.request('POST', self.base_url, json=body)
    if r.status_code != 200:
      self.raise_error(r)
    obj = rpc_response_adapter.validate_json(r.text) if self.should_validate(validate) else r.json()
    if 'error' in obj:
      self.raise_api_error(r.status_code, obj['error'])
    if 'result' not in obj:
      raise ApiError(r.status_code, obj)
    return obj['result']

  def raise_error(self, response: httpx.Response):
    """Raise a typed exception for an unsuccessful HTTP response."""
    try:
      payload: Any = response.json()
    except Exception:
      payload = response.text
    self.raise_api_error(response.status_code, payload)

  def raise_api_error(self, status_code: int, payload: Any):
    """Map Alchemy error payloads to shared typed-core exceptions."""
    if status_code in {401, 403}:
      raise AuthError(status_code, payload)
    if status_code == 429:
      raise RateLimited(status_code, payload)
    if 400 <= status_code < 500:
      raise BadRequest(status_code, payload)
    raise ApiError(status_code, payload)


@dataclass(kw_only=True)
class Router(Endpoint):
  """Router that instantiates typed child endpoint groups."""

  def __post_init__(self):
    for field_name, cls in get_type_hints(type(self)).items():
      if isinstance(cls, type) and issubclass(cls, Endpoint):
        setattr(
          self,
          field_name,
          cls(base_url=self.base_url, http=self.http, validate=self.validate),
        )


class PortfolioEndpoint(Endpoint):
  """Portfolio REST API endpoint group."""

  @classmethod
  def new(
    cls, *, api_key: str | None = None, validate: bool = True,
    http: HttpClient | None = None, base_url: str | None = None,
  ):
    """Create a Portfolio API client."""
    key = env_api_key(api_key)
    url = base_url or authed_url(path_join(ALCHEMY_DATA_API_URL, 'data/v1'), key)
    return cls(base_url=url, http=http or HttpClient(), validate=validate)


class PricesEndpoint(Endpoint):
  """Prices REST API endpoint group."""

  @classmethod
  def new(
    cls, *, api_key: str | None = None, validate: bool = True,
    http: HttpClient | None = None, base_url: str | None = None,
  ):
    """Create a Prices API client."""
    key = env_api_key(api_key)
    url = base_url or authed_url(path_join(ALCHEMY_DATA_API_URL, 'prices/v1'), key)
    return cls(base_url=url, http=http or HttpClient(), validate=validate)


class NftEndpoint(Endpoint):
  """NFT REST API endpoint group."""

  @classmethod
  def new(
    cls, node_url: str = ETHEREUM_ALCHEMY_NFT_URL, *,
    api_key: str | None = None, validate: bool = True,
    http: HttpClient | None = None, base_url: str | None = None,
  ):
    """Create an NFT API client."""
    key = env_api_key(api_key)
    url = base_url or authed_url(node_url, key)
    return cls(base_url=url, http=http or HttpClient(), validate=validate)


class RpcEndpoint(Endpoint):
  """Alchemy JSON-RPC endpoint group."""

  @classmethod
  def new(
    cls, node_url: str = ETHEREUM_ALCHEMY_RPC_URL, *,
    api_key: str | None = None, validate: bool = True,
    http: HttpClient | None = None, base_url: str | None = None,
  ):
    """Create a JSON-RPC API client."""
    key = env_api_key(api_key)
    url = base_url or authed_url(node_url, key)
    return cls(base_url=url, http=http or HttpClient(), validate=validate)
