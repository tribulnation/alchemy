from typing_extensions import NotRequired, TypedDict
from alchemy.core import Endpoint, validator

class LooksRareFloorPrice(TypedDict):
  """Floor price data from LooksRareFloorPrice."""
  floorPrice: NotRequired[float]
  """Floor price value."""
  priceCurrency: NotRequired[str]
  """Currency denomination (typically ETH)."""
  collectionUrl: NotRequired[str]
  """Link to the collection on LooksRareFloorPrice."""
  retrievedAt: NotRequired[str]
  """UTC timestamp when the floor price was fetched."""
  error: NotRequired[str | None]
  """Error message if retrieval failed; null on success."""

class OpenSeaFloorPrice(TypedDict):
  """Floor price data from OpenSeaFloorPrice."""
  floorPrice: NotRequired[float]
  """Floor price value."""
  priceCurrency: NotRequired[str]
  """Currency denomination (typically ETH)."""
  collectionUrl: NotRequired[str]
  """Link to the collection on OpenSeaFloorPrice."""
  retrievedAt: NotRequired[str]
  """UTC timestamp when the floor price was fetched."""
  error: NotRequired[str | None]
  """Error message if retrieval failed; null on success."""

class FloorPriceResponse(TypedDict):
  """Object with one key per supported marketplace."""
  openSea: NotRequired[OpenSeaFloorPrice]
  looksRare: NotRequired[LooksRareFloorPrice]

adapter = validator(FloorPriceResponse)

class GetFloorPrice(Endpoint):
  async def get_floor_price(
    self,
    *,
    contract_address: str,
    collection_slug: str | None = None,
    validate: bool | None = None
  ) -> FloorPriceResponse:
    """Retrieves the floor price of an NFT collection on OpenSeaFloorPrice and LooksRareFloorPrice marketplaces. Ethereum Mainnet only.
    
    Args:
      contract_address: NFT contract address (ERC721 or ERC1155).
      collection_slug: OpenSeaFloorPrice collection slug for the collection.
      validate: Validation override for this request.
    
    Returns:
      The validated endpoint response.
    
    References:
      - [Alchemy API docs](https://www.alchemy.com/docs/reference/nft-api-endpoints/nft-api-endpoints/nft-sales-endpoints/get-floor-price-v-3)
      """
    params: dict = {
      'contractAddress': contract_address,
    }
    if collection_slug is not None:
      params['collectionSlug'] = collection_slug
    r = await self.request('GET', '/getFloorPrice', params=params)
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.json(r.text) if self.should_validate(validate) else r.json()
