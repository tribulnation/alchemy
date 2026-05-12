from typing_extensions import Any, Literal, NotRequired, TypedDict
from alchemy.core import Endpoint, Timestamp, validator

NftTokenType = Literal['ERC721', 'ERC1155']

class NftOpenSeaMetadata(TypedDict):
  """OpenSea collection metadata."""
  floorPrice: NotRequired[float | None]
  """Collection floor price when available."""
  collectionName: NotRequired[str | None]
  """OpenSea collection name."""
  collectionSlug: NotRequired[str | None]
  """OpenSea collection slug."""
  safelistRequestStatus: NotRequired[str | None]
  """OpenSea safelist status."""
  imageUrl: NotRequired[str | None]
  """Collection image URL."""
  description: NotRequired[str | None]
  """Collection description."""
  externalUrl: NotRequired[str | None]
  """External collection URL."""
  twitterUsername: NotRequired[str | None]
  """Collection Twitter username."""
  discordUrl: NotRequired[str | None]
  """Collection Discord URL."""
  bannerImageUrl: NotRequired[str | None]
  """Collection banner image URL."""
  lastIngestedAt: NotRequired[Timestamp | None]
  """Last OpenSea metadata ingestion timestamp."""

class NftCollection(TypedDict):
  """NftCollection details."""
  name: NotRequired[str]
  """NftCollection name."""
  slug: NotRequired[str]
  """OpenSea slug."""
  externalUrl: NotRequired[str | None]
  """External collection URL."""
  bannerImageUrl: NotRequired[str | None]
  """Banner image URL."""

class NftContract(TypedDict):
  """NftContract-level metadata."""
  address: NotRequired[str]
  """NftContract address."""
  name: NotRequired[str]
  """NftContract name."""
  symbol: NotRequired[str]
  """NftContract symbol."""
  totalSupply: NotRequired[str]
  """Total token supply."""
  tokenType: NotRequired[NftTokenType]
  """Token standard: ERC721 or ERC1155."""
  contractDeployer: NotRequired[str]
  """Deployer address."""
  deployedBlockNumber: NotRequired[float]
  """Deployment block number."""
  openSeaMetadata: NotRequired[NftOpenSeaMetadata]
  """OpenSea collection metadata."""
  isSpam: NotRequired[bool | None]
  """Whether the contract is classified as spam."""
  spamClassifications: NotRequired[list[str]]
  """Spam classification labels."""

class NftImage(TypedDict):
  """NftImage URLs and metadata."""
  cachedUrl: NotRequired[str | None]
  """Alchemy-cached image URL."""
  thumbnailUrl: NotRequired[str | None]
  """Thumbnail URL."""
  pngUrl: NotRequired[str | None]
  """PNG-converted image URL."""
  contentType: NotRequired[str | None]
  """MIME type of the original image."""
  size: NotRequired[int | None]
  """File size in bytes."""
  originalUrl: NotRequired[str | None]
  """Original image URL from the NFT metadata."""

class NftMint(TypedDict):
  """NftMint information."""
  mintAddress: NotRequired[str | None]
  """Address that minted the token."""
  blockNumber: NotRequired[int | None]
  """Block when minted."""
  timestamp: NotRequired[Timestamp | None]
  """ISO timestamp of mint."""
  transactionHash: NotRequired[str | None]
  """NftMint transaction hash."""

class NftRawMetadata(TypedDict):
  """NftRawMetadata on-chain data."""
  tokenUri: NotRequired[str]
  """Original token URI from the contract."""
  metadata: NotRequired[dict[str, Any] | None]
  """Parsed metadata JSON."""
  error: NotRequired[str | None]
  """Error message if metadata could not be fetched."""

class NftMetadataResponse(TypedDict):
  contract: NotRequired[NftContract]
  tokenId: NotRequired[str]
  """Token ID."""
  tokenType: NotRequired[NftTokenType]
  """Token standard: ERC721 or ERC1155."""
  name: NotRequired[str]
  """NFT name from metadata."""
  description: NotRequired[str | None]
  """NFT description from metadata."""
  image: NotRequired[NftImage]
  raw: NotRequired[NftRawMetadata]
  collection: NotRequired[NftCollection]
  tokenUri: NotRequired[str]
  """Metadata location URI."""
  timeLastUpdated: NotRequired[Timestamp]
  """ISO timestamp of last metadata cache refresh."""
  mint: NotRequired[NftMint]
  owners: NotRequired[list[str] | None]
  """Current owner addresses."""

adapter = validator(NftMetadataResponse)

class GetNftMetadata(Endpoint):
  async def get_nft_metadata(
    self,
    *,
    contract_address: str,
    token_id: str,
    token_type: NftTokenType | None = None,
    token_uri_timeout_in_ms: int | None = None,
    refresh_cache: bool | None = None,
    validate: bool | None = None
  ) -> NftMetadataResponse:
    """Fetches metadata for a specific NFT identified by contract address and token ID.
    
    Args:
      contract_address: NFT contract address (ERC721 or ERC1155).
      token_id: Token ID as a decimal integer string or hex string.
      token_type: Token standard hint to improve response time. One of 'ERC721' or 'ERC1155'.
      token_uri_timeout_in_ms: Timeout in milliseconds for fetching the token URI. Set to 0 for cache-only access.
      refresh_cache: If true, forces a cache refresh and re-fetches metadata from the original source. Defaults to false.
      validate: Validation override for this request.
    
    Returns:
      The validated endpoint response.
    
    References:
      - [Alchemy API docs](https://www.alchemy.com/docs/data/nft-api/api-reference/nft-metadata-endpoints/get-nft-metadata-v-3)
      """
    params: dict = {
      'contractAddress': contract_address,
      'tokenId': token_id,
    }
    if token_type is not None:
      params['tokenType'] = token_type
    if token_uri_timeout_in_ms is not None:
      params['tokenUriTimeoutInMs'] = token_uri_timeout_in_ms
    if refresh_cache is not None:
      params['refreshCache'] = refresh_cache
    r = await self.request('GET', '/getNFTMetadata', params=params)
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.json(r.text) if self.should_validate(validate) else r.json()
