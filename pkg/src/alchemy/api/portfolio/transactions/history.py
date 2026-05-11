from typing_extensions import NotRequired, TypedDict
from alchemy.core import Endpoint, PaginatedResponse, validator

class Address(TypedDict):
  address: str
  """Wallet address whose transaction history should be fetched."""
  networks: list[str]
  """Networks to query for this wallet address."""

class Transaction(TypedDict):
  network: NotRequired[str]
  hash: NotRequired[str]
  timeStamp: NotRequired[str]
  blockNumber: NotRequired[int]
  blockHash: NotRequired[str]
  nonce: NotRequired[int]
  transactionIndex: NotRequired[int]
  fromAddress: NotRequired[str]
  toAddress: NotRequired[str | None]

class Request(TypedDict):
  addresses: list[Address]
  """Array of address and networks pairs. The docs say this endpoint is currently limited to 1 address pair and at most 2 networks."""
  before: NotRequired[str]
  """Cursor pointing to the previous set of results."""
  after: NotRequired[str]
  """Cursor pointing to the end of the current set of results."""
  limit: NotRequired[int]
  """Maximum number of transactions to return in this page."""
  pageKey: NotRequired[str]
  """Pagination cursor returned by a previous response."""

class Response(TypedDict):
  transactions: list[Transaction]
  before: NotRequired[str | None]
  after: str | None
  totalCount: int | None

adapter = validator(Response)

class History(Endpoint):
  async def history(self, request: Request, *, validate: bool | None = None) -> Response:
    """Fetches historical transactions for wallet addresses across supported networks. Alchemy documents this endpoint as beta and recommends migrating to `alchemy_getAssetTransfers`.
    
    Args:
      request: Request payload.
      validate: Validation override for this request.
    
    Returns:
      The validated endpoint response.
    
    References:
      Upstream docs: https://www.alchemy.com/docs/data/portfolio-apis/portfolio-api-endpoints/portfolio-api-endpoints/get-transaction-history-by-address"""
    r = await self.request('POST', '/transactions/history/by-address', json=request)
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.json(r.text) if self.should_validate(validate) else r.json()

  def history_paged(
    self, request: Request, *, validate: bool | None = None,
  ) -> PaginatedResponse[Transaction, str]:
    """Fetch transaction history pages.

    Args:
      request: Request payload.
      validate: Validation override for each request.

    Returns:
      An async iterable and awaitable paginated response.
    """
    async def next(state: str):
      page_request: Request = {**request}
      if state:
        page_request['after'] = state
      response = await self.history(page_request, validate=validate)
      return response['transactions'], response.get('after')

    return PaginatedResponse('', next)
