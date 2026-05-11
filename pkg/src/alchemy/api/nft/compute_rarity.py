from typing_extensions import NotRequired, TypedDict
from alchemy.core import Endpoint, validator

class Item(TypedDict):
  traitType: NotRequired[str]
  """Name of the trait category (e.g., Hat, Color, Face)."""
  value: NotRequired[str]
  """Value for the trait (e.g., White Cap, Blue)."""
  prevalence: NotRequired[float]
  """Float from 0 to 1 representing what fraction of the collection has this trait value."""

class Response200(TypedDict):
  rarities: NotRequired[list[Item]]
  """Array of trait rarity entries for each attribute of the NFT."""

adapter = validator(Response200)

class ComputeRarity(Endpoint):
  async def compute_rarity(
    self,
    *,
    contract_address: str,
    token_id: str,
    validate: bool | None = None
  ) -> Response200:
    """Computes the rarity of each trait attribute for a specific NFT token within its collection.
    
    Args:
      contract_address: NFT contract address (ERC721 or ERC1155).
      token_id: Token ID in hex or decimal format.
      validate: Validation override for this request.
    
    Returns:
      The validated endpoint response.
    
    References:
      Upstream docs: https://www.alchemy.com/docs/reference/nft-api-endpoints/nft-api-endpoints/nft-metadata-endpoints/compute-rarity-v-3"""
    params: dict = {
      'contractAddress': contract_address,
      'tokenId': token_id,
    }
    r = await self.request('GET', '/computeRarity', params=params)
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.json(r.text) if self.should_validate(validate) else r.json()
