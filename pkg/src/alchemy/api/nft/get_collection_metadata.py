from typing_extensions import NotRequired, TypedDict
from alchemy.core import Endpoint, validator

class CollectionFloorPrice(TypedDict):
  """Current floor price information."""
  marketplace: NotRequired[str]
  """Marketplace that provided the floor price."""
  floorPrice: NotRequired[float]
  """Floor price amount."""
  priceCurrency: NotRequired[str]
  """Currency of the floor price."""

class CollectionMetadataResponse(TypedDict):
  name: NotRequired[str]
  """Collection name."""
  slug: NotRequired[str]
  """OpenSea collection slug."""
  floorPrice: NotRequired[CollectionFloorPrice]
  description: NotRequired[str]
  """Collection description."""
  externalUrl: NotRequired[str | None]
  """External collection URL."""
  bannerImageUrl: NotRequired[str | None]
  """Collection banner image URL."""
  twitterUsername: NotRequired[str | None]
  """Twitter username."""
  discordUrl: NotRequired[str | None]
  """Discord invite URL."""

adapter = validator(CollectionMetadataResponse)

class GetCollectionMetadata(Endpoint):
  async def get_collection_metadata(
    self,
    *,
    collection_slug: str,
    validate: bool | None = None
  ) -> CollectionMetadataResponse:
    """Retrieves high-level collection metadata for an NFT collection by OpenSea slug.
    
    Args:
      collection_slug: OpenSea collection slug.
      validate: Validation override for this request.
    
    Returns:
      The validated endpoint response.
    
    References:
      - [Alchemy API docs](https://www.alchemy.com/docs/reference/nft-api-endpoints/nft-api-endpoints/nft-metadata-endpoints/get-collection-metadata-v-3)
      """
    params: dict = {
      'collectionSlug': collection_slug,
    }
    r = await self.request('GET', '/getCollectionMetadata', params=params)
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.json(r.text) if self.should_validate(validate) else r.json()
