from typing_extensions import Any, Literal, NotRequired, TypedDict
from alchemy.core import Endpoint, validator

class Collection(TypedDict):
  """Collection details."""
  name: NotRequired[str]
  """Collection name."""
  slug: NotRequired[str]
  """OpenSea slug."""
  externalUrl: NotRequired[str | None]
  """External collection URL."""
  bannerImageUrl: NotRequired[str]
  """Banner image URL."""

class Contract(TypedDict):
  """Contract-level metadata."""
  address: NotRequired[str]
  """Contract address."""
  name: NotRequired[str]
  """Contract name."""
  symbol: NotRequired[str]
  """Contract symbol."""
  totalSupply: NotRequired[str]
  """Total token supply."""
  tokenType: NotRequired[str]
  """Token standard: ERC721 or ERC1155."""
  contractDeployer: NotRequired[str]
  """Deployer address."""
  deployedBlockNumber: NotRequired[float]
  """Deployment block number."""
  openSeaMetadata: NotRequired[dict[str, Any]]
  """OpenSea collection metadata."""
  isSpam: NotRequired[bool]
  """Whether the contract is classified as spam."""
  spamClassifications: NotRequired[list[str]]
  """Spam classification labels."""

class Image(TypedDict):
  """Image URLs and metadata."""
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

class Mint(TypedDict):
  """Mint information."""
  mintAddress: NotRequired[str | None]
  """Address that minted the token."""
  blockNumber: NotRequired[int | None]
  """Block when minted."""
  timestamp: NotRequired[str | None]
  """ISO timestamp of mint."""
  transactionHash: NotRequired[str | None]
  """Mint transaction hash."""

class Raw(TypedDict):
  """Raw on-chain data."""
  tokenUri: NotRequired[str]
  """Original token URI from the contract."""
  metadata: NotRequired[dict[str, Any]]
  """Parsed metadata JSON."""
  error: NotRequired[str | None]
  """Error message if metadata could not be fetched."""

class Response200(TypedDict):
  contract: NotRequired[Contract]
  tokenId: NotRequired[str]
  """Token ID."""
  tokenType: NotRequired[str]
  """Token standard: ERC721 or ERC1155."""
  name: NotRequired[str]
  """NFT name from metadata."""
  description: NotRequired[str | None]
  """NFT description from metadata."""
  image: NotRequired[Image]
  raw: NotRequired[Raw]
  collection: NotRequired[Collection]
  tokenUri: NotRequired[str]
  """Metadata location URI."""
  timeLastUpdated: NotRequired[str]
  """ISO timestamp of last metadata cache refresh."""
  mint: NotRequired[Mint]
  owners: NotRequired[list[str] | None]
  """Current owner addresses."""

adapter = validator(Response200)

class GetNftMetadata(Endpoint):
  async def get_nft_metadata(
    self,
    *,
    contract_address: str,
    token_id: str,
    token_type: Literal['ERC721', 'ERC1155'] | None = None,
    token_uri_timeout_in_ms: int | None = None,
    refresh_cache: bool | None = None,
    validate: bool | None = None
  ) -> Response200:
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
      Upstream docs: https://www.alchemy.com/docs/data/nft-api/api-reference/nft-metadata-endpoints/get-nft-metadata-v-3"""
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
