from typing_extensions import Literal, NotRequired, TypedDict
from alchemy.core import Endpoint, PaginatedResponse, validator
from alchemy.api.nft.get_nft_metadata import NftImage
from alchemy.api.nft.get_nft_metadata import NftOpenSeaMetadata
from alchemy.api.nft.get_nft_metadata import NftTokenType

class NftContractsAddress(TypedDict):
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

class NftContractDisplayNft(TypedDict):
  tokenId: NotRequired[str]
  name: NotRequired[str | None]

class NftContractMetadata(TypedDict):
  address: str
  name: NotRequired[str | None]
  symbol: NotRequired[str | None]
  totalSupply: NotRequired[str | None]
  tokenType: NftTokenType
  contractDeployer: NotRequired[str | None]
  deployedBlockNumber: NotRequired[int | None]
  openSeaMetadata: NotRequired[NftOpenSeaMetadata | None]
  totalBalance: NotRequired[str | None]
  numDistinctTokensOwned: NotRequired[str | None]
  isSpam: NotRequired[bool | None]
  displayNft: NotRequired[NftContractDisplayNft | None]
  image: NotRequired[NftImage | None]

class NftContract(TypedDict):
  contract: NftContractMetadata
  network: str
  address: str

class NftContractsBaseRequest(TypedDict):
  addresses: list[NftContractsAddress]
  withMetadata: NotRequired[bool]
  """Whether to include collection-level metadata in each returned contract."""
  pageSize: NotRequired[int]
  """Maximum number of contract records to return per page."""
  orderBy: NotRequired[str]
  """Field Alchemy should use to order the returned contracts."""
  sortOrder: NotRequired[Literal['asc', 'desc']]
  """Sort direction for the selected ordering field."""

class NftContractsRequest(NftContractsBaseRequest):
  pageKey: NotRequired[str]
  """Pagination cursor returned by a previous response."""

class NftContractsData(TypedDict):
  contracts: list[NftContract]
  totalCount: int
  pageKey: str | None

class NftContractsResponse(TypedDict):
  data: NftContractsData

adapter = validator(NftContractsResponse)

class NftContracts(Endpoint):
  async def __call__(self, request: NftContractsRequest, *, validate: bool | None = None) -> NftContractsResponse:
    """Fetches NFT contracts held by wallet addresses, with aggregate collection-level metadata.
    
    Args:
      request: Request payload.
      validate: Validation override for this request.
    
    Returns:
      The validated endpoint response.
    
    References:
      - [Alchemy API docs](https://www.alchemy.com/docs/data/portfolio-apis/portfolio-api-endpoints/portfolio-api-endpoints/get-nft-contracts-by-address)
      """
    r = await self.request(
      'POST', '/assets/nfts/contracts/by-address',
      json=request
    )
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.json(r.text) if self.should_validate(validate) else r.json()

  def paged(
    self, request: NftContractsBaseRequest, *, validate: bool | None = None,
  ) -> PaginatedResponse[NftContract, str]:
    """Paged version of the NFT contracts endpoint.

    Args:
      request: Request payload.
      validate: Validation override for each request.

    Returns:
      An async iterable and awaitable paginated response over NFT contracts.

    References:
      - [Alchemy API docs](https://www.alchemy.com/docs/data/portfolio-apis/portfolio-api-endpoints/portfolio-api-endpoints/get-nft-contracts-by-address)
    """
    async def next(state: str):
      page_request: NftContractsRequest = {**request}
      if state:
        page_request['pageKey'] = state
      response = await self(page_request, validate=validate)
      return response['data']['contracts'], response['data'].get('pageKey')

    return PaginatedResponse('', next)
