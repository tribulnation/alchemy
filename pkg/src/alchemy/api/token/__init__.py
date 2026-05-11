from alchemy.core import RpcEndpoint
from .get_token_allowance import GetTokenAllowance
from .get_token_balances import GetTokenBalances
from .get_token_balances import TokenBalance
from alchemy.core.util.paging import PaginatedResponse
from .get_token_metadata import GetTokenMetadata

class Token(RpcEndpoint, GetTokenAllowance, GetTokenBalances, GetTokenMetadata):
  def get_token_balances_paged(
    self, params: list, *, validate: bool | None = None,
  ) -> PaginatedResponse[TokenBalance, str]:
    """Fetch token balance pages.

    Args:
      params: JSON-RPC positional parameters.
      validate: Validation override for each request.

    Returns:
      An async iterable and awaitable paginated response.
    """
    async def next(state: str):
      page_params = list(params)
      if state:
        options = dict(page_params[2]) if len(page_params) > 2 and isinstance(page_params[2], dict) else {}
        options['pageKey'] = state
        if len(page_params) > 2:
          page_params[2] = options
        else:
          page_params.append(options)
      response = await self.get_token_balances(page_params, validate=validate)
      return response['tokenBalances'], response.get('pageKey')

    return PaginatedResponse('', next)
