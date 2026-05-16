from typing_extensions import NotRequired, TypedDict
from alchemy.core import Endpoint, PaginatedResponse, validator

class TokensAddress(TypedDict):
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

class TokensBaseRequest(TypedDict):
  addresses: list[TokensAddress]
  """Array of wallet addresses and the networks to query them on. The docs state a maximum of 2 addresses and 5 networks per address."""
  withMetadata: NotRequired[bool]
  """Whether to include token metadata such as symbol, name, logo, and decimals."""
  withPrices: NotRequired[bool]
  """Whether to include price snapshots for each returned token."""
  includeNativeTokens: NotRequired[bool]
  """Whether to include the native gas token balance for each requested network."""
  includeErc20Tokens: NotRequired[bool]
  """Whether to include ERC-20 token balances."""
  pageSize: NotRequired[int]
  """Maximum number of token records to return per page."""

class TokensRequest(TokensBaseRequest):
  pageKey: NotRequired[str]
  """Pagination cursor returned by a previous response."""

class PortfolioToken(TypedDict):
  address: str
  network: str
  tokenAddress: str | None
  tokenBalance: str
  tokenMetadata: NotRequired[TokenMetadata | None]
  tokenPrices: NotRequired[list[TokenPrice] | None]
  error: NotRequired[str | None]

class TokensData(TypedDict):
  tokens: list[PortfolioToken]
  pageKey: str | None

class TokensResponse(TypedDict):
  data: TokensData

adapter = validator(TokensResponse)

class Tokens(Endpoint):
  async def __call__(self, request: TokensRequest, *, validate: bool | None = None) -> TokensResponse:
    """Fetches fungible tokens for multiple wallet addresses and networks, optionally including metadata and prices.
    
    Args:
      request: Request payload.
      validate: Validation override for this request.
    
    Returns:
      The validated endpoint response.
    
    References:
      - [Alchemy API docs](https://www.alchemy.com/docs/data/portfolio-apis/portfolio-api-endpoints/portfolio-api-endpoints/get-tokens-by-address)
      """
    r = await self.request('POST', '/assets/tokens/by-address', json=request)
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.json(r.text) if self.should_validate(validate) else r.json()

  def paged(
    self, request: TokensBaseRequest, *, validate: bool | None = None,
  ) -> PaginatedResponse[PortfolioToken, str]:
    """Paged version of the tokens endpoint.

    Args:
      request: Request payload.
      validate: Validation override for each request.

    Returns:
      An async iterable and awaitable paginated response over tokens.

    References:
      - [Alchemy API docs](https://www.alchemy.com/docs/data/portfolio-apis/portfolio-api-endpoints/portfolio-api-endpoints/get-tokens-by-address)
    """
    async def next(state: str):
      page_request: TokensRequest = {**request}
      if state:
        page_request['pageKey'] = state
      response = await self(page_request, validate=validate)
      return response['data']['tokens'], response['data'].get('pageKey')

    return PaginatedResponse('', next)
