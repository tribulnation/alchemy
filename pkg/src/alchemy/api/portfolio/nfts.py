from typing_extensions import Literal, NotRequired, TypedDict
from alchemy.core import Endpoint, PaginatedResponse, Timestamp, validator
from alchemy.api.nft.get_nft_metadata import NftCollection
from alchemy.api.nft.get_nft_metadata import NftContract
from alchemy.api.nft.get_nft_metadata import NftImage
from alchemy.api.nft.get_nft_metadata import NftMint
from alchemy.api.nft.get_nft_metadata import NftRawMetadata
from alchemy.api.nft.get_nft_metadata import NftTokenType

class NftAcquiredAt(TypedDict):
  blockTimestamp: NotRequired[Timestamp | None]
  blockNumber: NotRequired[int | None]

class NftsAddress(TypedDict):
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

class PortfolioNft(TypedDict):
  tokenId: str
  balance: str
  acquiredAt: NotRequired[NftAcquiredAt | None]
  network: str
  address: str
  contract: NftContract
  tokenType: NftTokenType
  name: NotRequired[str | None]
  description: NotRequired[str | None]
  tokenUri: NotRequired[str | None]
  image: NotRequired[NftImage | None]
  animation: NotRequired[NftImage | None]
  raw: NotRequired[NftRawMetadata | None]
  collection: NotRequired[NftCollection | None]
  mint: NotRequired[NftMint | None]
  timeLastUpdated: NotRequired[Timestamp | None]

class PortfolioNftsRequest(TypedDict):
  addresses: list[NftsAddress]
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

class PortfolioNftsData(TypedDict):
  ownedNfts: list[PortfolioNft]
  totalCount: int
  pageKey: str | None

class PortfolioNftsResponse(TypedDict):
  data: PortfolioNftsData

adapter = validator(PortfolioNftsResponse)

class Nfts(Endpoint):
  async def __call__(self, request: PortfolioNftsRequest, *, validate: bool | None = None) -> PortfolioNftsResponse:
    """Fetches NFTs held by wallet addresses, with optional metadata and filtering controls.
    
    Args:
      request: Request payload.
      validate: Validation override for this request.
    
    Returns:
      The validated endpoint response.
    
    References:
      - [Alchemy API docs](https://www.alchemy.com/docs/data/portfolio-apis/portfolio-api-endpoints/portfolio-api-endpoints/get-nfts-by-address)
      """
    r = await self.request('POST', '/assets/nfts/by-address', json=request)
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.json(r.text) if self.should_validate(validate) else r.json()

  def paged(
    self, request: PortfolioNftsRequest, *, validate: bool | None = None,
  ) -> PaginatedResponse[PortfolioNft, str]:
    """Fetch NFT pages.

    Args:
      request: Request payload.
      validate: Validation override for each request.

    Returns:
      An async iterable and awaitable paginated response.
    """
    async def next(state: str):
      page_request: PortfolioNftsRequest = {**request}
      if state:
        page_request['pageKey'] = state
      response = await self(page_request, validate=validate)
      return response['data']['ownedNfts'], response['data'].get('pageKey')

    return PaginatedResponse('', next)
