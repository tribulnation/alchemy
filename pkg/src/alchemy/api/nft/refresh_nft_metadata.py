from typing_extensions import NotRequired, TypedDict
from alchemy.core import Endpoint, validator

class Body(TypedDict):
  contractAddress: str
  """Contract address of the token to refresh."""
  tokenId: str
  """Token ID of the token to refresh."""

class Response200(TypedDict):
  status: NotRequired[str]
  """Returns 'Queued' when successfully queued for refresh."""
  estimatedMsToRefresh: NotRequired[float]
  """Estimated milliseconds until the metadata refresh completes."""

adapter = validator(Response200)

class RefreshNftMetadata(Endpoint):
  async def refresh_nft_metadata(
    self,
    body: Body,
    *,
    validate: bool | None = None
  ) -> Response200:
    """Queues a cache refresh for a specific NFT token's metadata.
    
    Args:
      body: Token to refresh.
      validate: Validation override for this request.
    
    Returns:
      The validated endpoint response.
    
    References:
      Upstream docs: https://www.alchemy.com/docs/reference/nft-api-endpoints/nft-api-endpoints/nft-metadata-endpoints/refresh-nft-metadata-v-3"""
    r = await self.request('POST', '/refreshNftMetadata', json=body)
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.json(r.text) if self.should_validate(validate) else r.json()
