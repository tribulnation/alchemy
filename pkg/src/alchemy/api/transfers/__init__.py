from alchemy.core import RpcEndpoint
from .get_asset_transfers import GetAssetTransfers
from alchemy.core.util.paging import PaginatedResponse
from .get_asset_transfers import Params, Response, Transfer

class Transfers(RpcEndpoint, GetAssetTransfers):
  async def transfers(self, params: Params, *, validate: bool | None = None) -> Response:
    """Fetch asset transfers.

    Args:
      params: Transfer filter parameters.
      validate: Validation override for this request.

    Returns:
      The validated transfer response.

    References:
      Upstream docs: https://www.alchemy.com/docs/data/transfers-api/transfers-endpoints/alchemy-get-asset-transfers
    """
    return await self.get_asset_transfers(params, validate=validate)

  def transfers_paged(
    self, params: Params, *, validate: bool | None = None,
  ) -> PaginatedResponse[Transfer, str]:
    """Fetch asset transfers across all pages.

    Args:
      params: Transfer filter parameters.
      validate: Validation override for this request.

    Returns:
      An async iterable and awaitable paginated response.

    References:
      Upstream docs: https://www.alchemy.com/docs/data/transfers-api/transfers-endpoints/alchemy-get-asset-transfers
    """
    state = ''

    async def next(state: str):
      page_params: Params = {**params}
      if state:
        page_params['pageKey'] = state
      r = await self.get_asset_transfers(page_params, validate=validate)
      return r['transfers'], r.get('pageKey')

    return PaginatedResponse(state, next)

  def get_asset_transfers_paged(
    self, params: Params, *, validate: bool | None = None,
  ) -> PaginatedResponse[Transfer, str]:
    """Fetch asset transfers across all pages.

    Args:
      params: Transfer filter parameters.
      validate: Validation override for each request.

    Returns:
      An async iterable and awaitable paginated response.
    """
    return self.transfers_paged(params, validate=validate)
