from typing_extensions import NotRequired, TypedDict
from alchemy.core import Endpoint, PaginatedResponse, validator

class TokenBalancesAddress(TypedDict):
  address: str
  """Wallet address whose balances should be fetched."""
  networks: list[str]
  """Networks to query for this wallet address."""

class PortfolioTokenBalance(TypedDict):
  address: str
  """Wallet address this balance belongs to."""
  network: str
  """Network the balance was fetched from."""
  tokenAddress: str | None
  """PortfolioTokenBalance contract address, or null for native tokens."""
  tokenBalance: str
  """Raw token balance as returned by Alchemy."""

class TokenBalancesData(TypedDict):
  tokens: list[PortfolioTokenBalance]
  pageKey: str | None
  """Pagination cursor for the next page, or null when there are no more results."""

class TokenBalancesBaseRequest(TypedDict):
  addresses: list[TokenBalancesAddress]
  """Wallet addresses and networks to query for balances."""
  includeNativeTokens: NotRequired[bool]
  """Whether to include the native gas token balance for each requested network."""
  includeErc20Tokens: NotRequired[bool]
  """Whether to include ERC-20 token balances."""
  pageSize: NotRequired[int]
  """Maximum number of balance records to return per page."""

class TokenBalancesRequest(TokenBalancesBaseRequest):
  pageKey: NotRequired[str]
  """Pagination cursor returned by a previous response."""

class TokenBalancesResponse(TypedDict):
  data: TokenBalancesData

adapter = validator(TokenBalancesResponse)

class TokenBalances(Endpoint):
  async def __call__(self, request: TokenBalancesRequest, *, validate: bool | None = None) -> TokenBalancesResponse:
    """Fetches fungible token balances for multiple wallet addresses and networks.
    
    Args:
      request: Request payload.
      validate: Validation override for this request.
    
    Returns:
      The validated endpoint response.
    
    References:
      - [Alchemy API docs](https://www.alchemy.com/docs/data/portfolio-apis/portfolio-api-endpoints/portfolio-api-endpoints/get-token-balances-by-address)
      """
    r = await self.request(
      'POST', '/assets/tokens/balances/by-address',
      json=request
    )
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.json(r.text) if self.should_validate(validate) else r.json()

  def paged(
    self, request: TokenBalancesBaseRequest, *, validate: bool | None = None,
  ) -> PaginatedResponse[PortfolioTokenBalance, str]:
    """Paged version of the token balances endpoint.

    Args:
      request: Request payload.
      validate: Validation override for each request.

    Returns:
      An async iterable and awaitable paginated response over token balances.

    References:
      - [Alchemy API docs](https://www.alchemy.com/docs/data/portfolio-apis/portfolio-api-endpoints/portfolio-api-endpoints/get-token-balances-by-address)
    """
    async def next(state: str):
      page_request: TokenBalancesRequest = {**request}
      if state:
        page_request['pageKey'] = state
      response = await self(page_request, validate=validate)
      return response['data']['tokens'], response['data'].get('pageKey')

    return PaginatedResponse('', next)
