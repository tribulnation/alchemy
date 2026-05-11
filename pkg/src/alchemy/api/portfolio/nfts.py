from typing_extensions import Any, Literal, NotRequired, TypedDict
from alchemy.core import Endpoint, PaginatedResponse, validator

class AcquiredAt(TypedDict):
  blockTimestamp: NotRequired[str | None]
  blockNumber: NotRequired[int | None]

class Address(TypedDict):
  address: str
  """Wallet address whose NFTs should be fetched."""
  networks: list[str]
  """Networks to query for this wallet address."""
  includeFilters: NotRequired[list[str]]
  """Collection filters to include for this wallet query."""
  excludeFilters: NotRequired[list[str]]
  """Collection filters to exclude for this wallet query."""
  spamConfidenceLevel: NotRequired[str]
  """Spam filtering threshold to apply to the returned NFTs."""

class Contract(TypedDict):
  address: str
  name: NotRequired[str | None]
  symbol: NotRequired[str | None]
  totalSupply: NotRequired[str | None]
  tokenType: str
  contractDeployer: NotRequired[str | None]
  deployedBlockNumber: NotRequired[int | None]
  openSeaMetadata: NotRequired[dict[str, Any] | None]
  isSpam: NotRequired[bool | None]
  spamClassifications: NotRequired[list[str]]

class Nft(TypedDict):
  tokenId: str
  balance: str
  acquiredAt: NotRequired[AcquiredAt | None]
  network: str
  address: str
  contract: Contract
  tokenType: str
  name: NotRequired[str | None]
  description: NotRequired[str | None]
  tokenUri: NotRequired[str | None]
  image: NotRequired[dict[str, Any] | None]
  animation: NotRequired[dict[str, Any] | None]
  raw: NotRequired[dict[str, Any] | None]
  collection: NotRequired[dict[str, Any] | None]
  mint: NotRequired[dict[str, Any] | None]
  timeLastUpdated: NotRequired[str | None]

class Request(TypedDict):
  addresses: list[Address]
  withMetadata: NotRequired[bool]
  """Whether to include NFT metadata in each returned item."""
  pageKey: NotRequired[str]
  """Pagination cursor returned by a previous response."""
  pageSize: NotRequired[int]
  """Maximum number of NFT records to return."""
  orderBy: NotRequired[str]
  """Field Alchemy should use to order the returned NFTs."""
  sortOrder: NotRequired[Literal['asc', 'desc']]
  """Sort direction for the selected ordering field."""

class Data(TypedDict):
  ownedNfts: list[Nft]
  totalCount: int
  pageKey: str | None

class Response(TypedDict):
  data: Data

adapter = validator(Response)

class Nfts(Endpoint):
  async def __call__(self, request: Request, *, validate: bool | None = None) -> Response:
    """Fetches NFTs held by wallet addresses, with optional metadata and filtering controls.
    
    Args:
      request: Request payload.
      validate: Validation override for this request.
    
    Returns:
      The validated endpoint response.
    
    References:
      Upstream docs: https://www.alchemy.com/docs/data/portfolio-apis/portfolio-api-endpoints/portfolio-api-endpoints/get-nfts-by-address"""
    r = await self.request('POST', '/assets/nfts/by-address', json=request)
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.json(r.text) if self.should_validate(validate) else r.json()

  def paged(
    self, request: Request, *, validate: bool | None = None,
  ) -> PaginatedResponse[Nft, str]:
    """Fetch NFT pages.

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
      return response['data']['ownedNfts'], response['data'].get('pageKey')

    return PaginatedResponse('', next)
