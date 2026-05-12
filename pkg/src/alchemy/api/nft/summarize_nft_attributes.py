from typing_extensions import NotRequired, TypedDict
from alchemy.core import Endpoint, validator

class NftAttributesSummaryResponse(TypedDict):
  contractAddress: NotRequired[str]
  """The queried contract address."""
  totalSupply: NotRequired[str]
  """Total number of NFTs in the collection."""
  summary: NotRequired[dict[str, dict[str, float]]]
  """Object mapping trait type names to an object of {trait_value: count} occurrences across the collection."""

adapter = validator(NftAttributesSummaryResponse)

class SummarizeNftAttributes(Endpoint):
  async def summarize_nft_attributes(
    self,
    *,
    contract_address: str,
    validate: bool | None = None
  ) -> NftAttributesSummaryResponse:
    """Generates a summary of attribute prevalence across all tokens in a collection.
    
    Args:
      contract_address: NFT contract address (ERC721 or ERC1155).
      validate: Validation override for this request.
    
    Returns:
      The validated endpoint response.
    
    References:
      - [Alchemy API docs](https://www.alchemy.com/docs/reference/nft-api-endpoints/nft-api-endpoints/nft-metadata-endpoints/summarize-nft-attributes-v-3)
      """
    params: dict = {
      'contractAddress': contract_address,
    }
    r = await self.request('GET', '/summarizeNFTAttributes', params=params)
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.json(r.text) if self.should_validate(validate) else r.json()
