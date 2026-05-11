from typing_extensions import Any, Literal, NotRequired, TypedDict
from alchemy.core import Endpoint, validator

class Item(TypedDict):
  contractAddress: str
  """NFT contract address."""
  tokenId: str
  """Token ID in hex or decimal format."""
  tokenType: NotRequired[Literal['ERC721', 'ERC1155']]
  """Token standard hint (ERC721 or ERC1155) to optimize query."""

class Response200(TypedDict):
  nfts: NotRequired[list[dict[str, Any]]]
  """Array of NFT metadata objects."""

class Body(TypedDict):
  tokens: list[Item]
  """List of token objects to fetch metadata for. Maximum 100."""
  tokenUriTimeoutInMs: NotRequired[int]
  """Timeout for URI resolution in milliseconds."""
  refreshCache: NotRequired[bool]
  """If true, forces metadata re-fetch. Defaults to false."""

adapter = validator(Response200)

class GetNftMetadataBatch(Endpoint):
  async def get_nft_metadata_batch(
    self,
    body: Body,
    *,
    validate: bool | None = None
  ) -> Response200:
    """Fetches metadata for up to 100 NFTs in a single request. Returns an array of NFT objects.
    
    Args:
      body: Batch request payload specifying the tokens to fetch metadata for.
      validate: Validation override for this request.
    
    Returns:
      The validated endpoint response.
    
    References:
      Upstream docs: https://www.alchemy.com/docs/reference/nft-api-endpoints/nft-api-endpoints/nft-metadata-endpoints/get-nft-metadata-batch-v-3"""
    r = await self.request('POST', '/getNFTMetadataBatch', json=body)
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.json(r.text) if self.should_validate(validate) else r.json()
