from typing_extensions import NotRequired, TypedDict
from alchemy.core import Endpoint, validator
from .get_nft_metadata import NftContract

class ContractMetadataSearchResponse(TypedDict):
  contracts: NotRequired[list[NftContract]]
  """Array of matching contract metadata objects."""

adapter = validator(ContractMetadataSearchResponse)

class SearchContractMetadata(Endpoint):
  async def search_contract_metadata(
    self,
    *,
    query: str,
    validate: bool | None = None
  ) -> ContractMetadataSearchResponse:
    """Searches contract metadata across ERC-721 and ERC-1155 contracts for a given keyword. Beta.
    
    Args:
      query: Search keyword to match against contract metadata.
      validate: Validation override for this request.
    
    Returns:
      The validated endpoint response.
    
    References:
      - [Alchemy API docs](https://www.alchemy.com/docs/reference/nft-api-endpoints/nft-api-endpoints/nft-metadata-endpoints/search-contract-metadata-v-3)
      """
    params: dict = {
      'query': query,
    }
    r = await self.request('GET', '/searchContractMetadata', params=params)
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.json(r.text) if self.should_validate(validate) else r.json()
