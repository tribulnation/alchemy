from typing_extensions import Any, Literal, NotRequired, TypedDict
from alchemy.core import Endpoint, PaginatedResponse, validator

class Address(TypedDict):
  address: str
  """Wallet address whose NFT contracts should be fetched."""
  networks: list[str]
  """Networks to query for this wallet address."""
  includeFilters: NotRequired[list[str]]
  """Collection filters to include for this wallet query."""
  excludeFilters: NotRequired[list[str]]
  """Collection filters to exclude for this wallet query."""
  spamConfidenceLevel: NotRequired[str]
  """Spam filtering threshold to apply to the returned contracts."""

class ItemContract(TypedDict):
  address: str
  name: NotRequired[str | None]
  symbol: NotRequired[str | None]
  totalSupply: NotRequired[str | None]
  tokenType: str
  contractDeployer: NotRequired[str | None]
  deployedBlockNumber: NotRequired[int | None]
  openSeaMetadata: NotRequired[dict[str, Any] | None]
  totalBalance: NotRequired[str | None]
  numDistinctTokensOwned: NotRequired[str | None]
  isSpam: NotRequired[bool | None]
  displayNft: NotRequired[dict[str, Any] | None]
  image: NotRequired[dict[str, Any] | None]

class Contract(TypedDict):
  contract: ItemContract
  network: str
  address: str

class Request(TypedDict):
  addresses: list[Address]
  withMetadata: NotRequired[bool]
  """Whether to include collection-level metadata in each returned contract."""
  pageKey: NotRequired[str]
  """Pagination cursor returned by a previous response."""
  pageSize: NotRequired[int]
  """Maximum number of contract records to return."""
  orderBy: NotRequired[str]
  """Field Alchemy should use to order the returned contracts."""
  sortOrder: NotRequired[Literal['asc', 'desc']]
  """Sort direction for the selected ordering field."""

class Data(TypedDict):
  contracts: list[Contract]
  totalCount: int
  pageKey: str | None

class Response(TypedDict):
  data: Data

adapter = validator(Response)

class NftContracts(Endpoint):
  async def __call__(self, request: Request, *, validate: bool | None = None) -> Response:
    """Fetches NFT contracts held by wallet addresses, with aggregate collection-level metadata.
    
    Args:
      request: Request payload.
      validate: Validation override for this request.
    
    Returns:
      The validated endpoint response.
    
    References:
      Upstream docs: https://www.alchemy.com/docs/data/portfolio-apis/portfolio-api-endpoints/portfolio-api-endpoints/get-nft-contracts-by-address"""
    r = await self.request(
      'POST', '/assets/nfts/contracts/by-address',
      json=request
    )
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.json(r.text) if self.should_validate(validate) else r.json()

  def paged(
    self, request: Request, *, validate: bool | None = None,
  ) -> PaginatedResponse[Contract, str]:
    """Fetch NFT contract pages.

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
      return response['data']['contracts'], response['data'].get('pageKey')

    return PaginatedResponse('', next)
