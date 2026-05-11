from typing_extensions import NotRequired, TypedDict
from alchemy.core import Endpoint, PaginatedResponse, validator

class Address(TypedDict):
  address: str
  """Wallet address whose fungible tokens should be fetched."""
  networks: list[str]
  """Networks to query for this wallet address."""

class TokenMetadata(TypedDict):
  decimals: NotRequired[int | None]
  logo: NotRequired[str | None]
  name: NotRequired[str | None]
  symbol: NotRequired[str | None]

class TokenPrice(TypedDict):
  currency: str
  value: str
  lastUpdatedAt: str

class Request(TypedDict):
  addresses: list[Address]
  """Array of wallet addresses and the networks to query them on. The docs state a maximum of 2 addresses and 5 networks per address."""
  withMetadata: NotRequired[bool]
  """Whether to include token metadata such as symbol, name, logo, and decimals."""
  withPrices: NotRequired[bool]
  """Whether to include price snapshots for each returned token."""
  includeNativeTokens: NotRequired[bool]
  """Whether to include the native gas token balance for each requested network."""
  includeErc20Tokens: NotRequired[bool]
  """Whether to include ERC-20 token balances."""
  pageKey: NotRequired[str]
  """Pagination cursor returned by a previous response."""
  pageSize: NotRequired[int]
  """Maximum number of token records to return."""

class Token(TypedDict):
  address: str
  network: str
  tokenAddress: str | None
  tokenBalance: str
  tokenMetadata: NotRequired[TokenMetadata | None]
  tokenPrices: NotRequired[list[TokenPrice] | None]
  error: NotRequired[str | None]

class Data(TypedDict):
  tokens: list[Token]
  pageKey: str | None

class Response(TypedDict):
  data: Data

adapter = validator(Response)

class Tokens(Endpoint):
  async def __call__(self, request: Request, *, validate: bool | None = None) -> Response:
    """Fetches fungible tokens for multiple wallet addresses and networks, optionally including metadata and prices.
    
    Args:
      request: Request payload.
      validate: Validation override for this request.
    
    Returns:
      The validated endpoint response.
    
    References:
      Upstream docs: https://www.alchemy.com/docs/data/portfolio-apis/portfolio-api-endpoints/portfolio-api-endpoints/get-tokens-by-address"""
    r = await self.request('POST', '/assets/tokens/by-address', json=request)
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.json(r.text) if self.should_validate(validate) else r.json()

  def paged(
    self, request: Request, *, validate: bool | None = None,
  ) -> PaginatedResponse[Token, str]:
    """Fetch token pages.

    Args:
      request: Request payload.
      validate: Validation override for each request.

    Returns:
      An async iterable and awaitable paginated response.
    """
    async def next(state: str):
      page_request: Request = {**request}
      if state:
        page_request['pageKey'] = state
      response = await self(page_request, validate=validate)
      return response['data']['tokens'], response['data'].get('pageKey')

    return PaginatedResponse('', next)
