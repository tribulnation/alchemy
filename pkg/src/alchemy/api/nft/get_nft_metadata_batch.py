from typing_extensions import Literal, NotRequired, TypedDict
from alchemy.core import Endpoint, validator
from .get_nft_metadata import NftMetadataResponse

class NftMetadataBatchToken(TypedDict):
  contractAddress: str
  """NFT contract address."""
  tokenId: str
  """Token ID in hex or decimal format."""
  tokenType: NotRequired[Literal['ERC721', 'ERC1155']]
  """Token standard hint (ERC721 or ERC1155) to optimize query."""

class NftMetadataBatchResponse(TypedDict):
  nfts: NotRequired[list[NftMetadataResponse]]
  """Array of NFT metadata objects."""

class NftMetadataBatchRequest(TypedDict):
  tokens: list[NftMetadataBatchToken]
  """List of token objects to fetch metadata for. Maximum 100."""
  tokenUriTimeoutInMs: NotRequired[int]
  """Timeout for URI resolution in milliseconds."""
  refreshCache: NotRequired[bool]
  """If true, forces metadata re-fetch. Defaults to false."""

adapter = validator(NftMetadataBatchResponse)

class GetNftMetadataBatch(Endpoint):
  async def get_nft_metadata_batch(
    self,
    body: NftMetadataBatchRequest,
    *,
    validate: bool | None = None
  ) -> NftMetadataBatchResponse:
    """Fetches metadata for up to 100 NFTs in a single request. Returns an array of NFT objects.
    
    Args:
      body: Batch request payload specifying the tokens to fetch metadata for.
      validate: Validation override for this request.
    
    Returns:
      The validated endpoint response.
    
    References:
      - [Alchemy API docs](https://www.alchemy.com/docs/reference/nft-api-endpoints/nft-api-endpoints/nft-metadata-endpoints/get-nft-metadata-batch-v-3)
      """
    r = await self.request('POST', '/getNFTMetadataBatch', json=body)
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.json(r.text) if self.should_validate(validate) else r.json()
