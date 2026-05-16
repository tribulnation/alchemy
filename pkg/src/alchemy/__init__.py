from dataclasses import dataclass, field
from typing_extensions import Literal

from typed_core.exceptions import (
  Error as Error,
  NetworkError as NetworkError,
  ValidationError as ValidationError,
  ApiError as ApiError,
  BadRequest as BadRequest,
  AuthError as AuthError,
  RateLimited as RateLimited,
  LogicError as LogicError,
)
from typed_core.http import HttpClient as _HttpClient

from .api.nft import Nft as Nft
from .api.portfolio import Portfolio as Portfolio
from .api.prices import Prices as Prices
from .api.simulation import Simulation as Simulation
from .api.token import Token as Token
from .api.transfers import Transfers as Transfers
from .api.utility import Utility as Utility
from .core import (
  ALCHEMY_DATA_API_URL,
  ETHEREUM_ALCHEMY_RPC_URL,
  BNB_ALCHEMY_RPC_URL,
  POLYGON_ALCHEMY_RPC_URL,
  BASE_ALCHEMY_RPC_URL,
  AVAX_ALCHEMY_RPC_URL,
  OPTIMISM_ALCHEMY_RPC_URL,
  ARBITRUM_ALCHEMY_RPC_URL,
  GNOSIS_ALCHEMY_RPC_URL,
  CELO_ALCHEMY_RPC_URL,
  ETHEREUM_ALCHEMY_NFT_URL,
  BNB_ALCHEMY_NFT_URL,
  POLYGON_ALCHEMY_NFT_URL,
  BASE_ALCHEMY_NFT_URL,
  AVAX_ALCHEMY_NFT_URL,
  OPTIMISM_ALCHEMY_NFT_URL,
  ARBITRUM_ALCHEMY_NFT_URL,
  GNOSIS_ALCHEMY_NFT_URL,
  CELO_ALCHEMY_NFT_URL,
)
from .core.mixin import authed_url as _authed_url, env_api_key as _env_api_key
from .core.util.paths import path_join as _path_join


Network = Literal[
  'ethereum', 'bnb', 'polygon', 'base', 'avalanche',
  'optimism', 'arbitrum', 'gnosis', 'celo',
]

RPC_URLS: dict[Network, str] = {
  'ethereum': ETHEREUM_ALCHEMY_RPC_URL,
  'bnb': BNB_ALCHEMY_RPC_URL,
  'polygon': POLYGON_ALCHEMY_RPC_URL,
  'base': BASE_ALCHEMY_RPC_URL,
  'avalanche': AVAX_ALCHEMY_RPC_URL,
  'optimism': OPTIMISM_ALCHEMY_RPC_URL,
  'arbitrum': ARBITRUM_ALCHEMY_RPC_URL,
  'gnosis': GNOSIS_ALCHEMY_RPC_URL,
  'celo': CELO_ALCHEMY_RPC_URL,
}

NFT_URLS: dict[Network, str] = {
  'ethereum': ETHEREUM_ALCHEMY_NFT_URL,
  'bnb': BNB_ALCHEMY_NFT_URL,
  'polygon': POLYGON_ALCHEMY_NFT_URL,
  'base': BASE_ALCHEMY_NFT_URL,
  'avalanche': AVAX_ALCHEMY_NFT_URL,
  'optimism': OPTIMISM_ALCHEMY_NFT_URL,
  'arbitrum': ARBITRUM_ALCHEMY_NFT_URL,
  'gnosis': GNOSIS_ALCHEMY_NFT_URL,
  'celo': CELO_ALCHEMY_NFT_URL,
}


@dataclass
class Alchemy:
  """Composite Alchemy client for Portfolio, Prices, NFT, and JSON-RPC APIs.

  Global API groups are exposed as direct properties. Network-scoped API groups
  are selected with an explicit network literal, such as
  `client.transfers('ethereum')`.
  """
  api_key: str = field(repr=False)
  validate: bool = True
  data_url: str | None = None
  prices_url: str | None = None
  http: _HttpClient = field(default_factory=_HttpClient)

  @classmethod
  def new(
    cls, *, api_key: str | None = None, validate: bool = True,
    data_url: str | None = None, prices_url: str | None = None,
    http: _HttpClient | None = None,
  ):
    """Create an Alchemy client.

    Args:
      api_key: Alchemy API key. If omitted, falls back to `ALCHEMY_API_KEY`.
      validate: Validate responses by default.
      data_url: Fully-qualified Portfolio API base URL override.
      prices_url: Fully-qualified Prices API base URL override.
      http: Shared HTTP client override.
    """
    return cls(
      api_key=_env_api_key(api_key),
      validate=validate,
      data_url=data_url,
      prices_url=prices_url,
      http=http or _HttpClient(),
    )

  @property
  def portfolio(self) -> Portfolio:
    """Access the Portfolio API group."""
    url = self.data_url or _authed_url(_path_join(ALCHEMY_DATA_API_URL, 'data/v1'), self.api_key)
    return Portfolio(base_url=url, http=self.http, validate=self.validate)

  @property
  def prices(self) -> Prices:
    """Access the Prices API group."""
    url = self.prices_url or _authed_url(_path_join(ALCHEMY_DATA_API_URL, 'prices/v1'), self.api_key)
    return Prices(base_url=url, http=self.http, validate=self.validate)

  def nft(self, network: Network, *, base_url: str | None = None) -> Nft:
    """Access the NFT API group for a network.

    Args:
      network: Supported Alchemy network.
      base_url: Fully-qualified NFT API base URL override.
    """
    url = base_url or _authed_url(NFT_URLS[network], self.api_key)
    return Nft(base_url=url, http=self.http, validate=self.validate)

  def token(self, network: Network, *, base_url: str | None = None) -> Token:
    """Access the Token JSON-RPC API group for a network.

    Args:
      network: Supported Alchemy network.
      base_url: Fully-qualified JSON-RPC API base URL override.
    """
    url = base_url or _authed_url(RPC_URLS[network], self.api_key)
    return Token(base_url=url, http=self.http, validate=self.validate)

  def transfers(self, network: Network, *, base_url: str | None = None) -> Transfers:
    """Access the Transfers JSON-RPC API group for a network.

    Args:
      network: Supported Alchemy network.
      base_url: Fully-qualified JSON-RPC API base URL override.
    """
    url = base_url or _authed_url(RPC_URLS[network], self.api_key)
    return Transfers(base_url=url, http=self.http, validate=self.validate)

  def utility(self, network: Network, *, base_url: str | None = None) -> Utility:
    """Access the Utility JSON-RPC API group for a network.

    Args:
      network: Supported Alchemy network.
      base_url: Fully-qualified JSON-RPC API base URL override.
    """
    url = base_url or _authed_url(RPC_URLS[network], self.api_key)
    return Utility(base_url=url, http=self.http, validate=self.validate)

  def simulation(self, network: Network, *, base_url: str | None = None) -> Simulation:
    """Access the Simulation JSON-RPC API group for a network.

    Args:
      network: Supported Alchemy network.
      base_url: Fully-qualified JSON-RPC API base URL override.
    """
    url = base_url or _authed_url(RPC_URLS[network], self.api_key)
    return Simulation(base_url=url, http=self.http, validate=self.validate)

  async def __aenter__(self):
    await self.http.__aenter__()
    return self

  async def __aexit__(self, exc_type, exc_value, traceback):
    await self.http.__aexit__(exc_type, exc_value, traceback)
