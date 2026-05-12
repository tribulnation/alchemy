from alchemy.core import RpcEndpoint
from alchemy.core.util.paging import PaginatedResponse
from .get_token_allowance import GetTokenAllowance
from .get_token_balances import GetTokenBalances
from .get_token_balances import TokenBalance
from .get_token_balances import TokenBalancesOptions
from .get_token_balances import TokenSpec
from .get_token_metadata import GetTokenMetadata

class Token(RpcEndpoint, GetTokenAllowance, GetTokenBalances, GetTokenMetadata):
  def get_token_balances_paged(
    self, address: str, token_spec: TokenSpec = 'erc20', *,
    options: TokenBalancesOptions | None = None,
    validate: bool | None = None,
  ) -> PaginatedResponse[TokenBalance, str]:
    """Fetch token balance pages.

    Args:
      address: Wallet address to inspect.
      token_spec: Token selection.
      options: Pagination options.
      validate: Validation override for each request.

    Returns:
      An async iterable and awaitable paginated response.
    """
    async def next(state: str):
      page_options: TokenBalancesOptions = {}
      if options is not None:
        page_options.update(options)
      if state:
        page_options['pageKey'] = state
      response = await self.get_token_balances(
        address,
        token_spec,
        options=page_options or None,
        validate=validate,
      )
      return response['tokenBalances'], response.get('pageKey')

    return PaginatedResponse('', next)
