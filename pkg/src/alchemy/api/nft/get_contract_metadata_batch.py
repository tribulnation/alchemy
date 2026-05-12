from typing_extensions import NotRequired, TypedDict
from alchemy.core import Endpoint, validator
from .get_nft_metadata import NftContract

class ContractMetadataBatchRequest(TypedDict):
  contractAddresses: list[str]
  """List of NFT contract addresses."""

class ContractMetadataBatchResponse(TypedDict):
  contracts: NotRequired[list[NftContract]]
  """Array of contract metadata objects, one per input address."""

adapter = validator(ContractMetadataBatchResponse)

class GetContractMetadataBatch(Endpoint):
  async def get_contract_metadata_batch(
    self,
    body: ContractMetadataBatchRequest,
    *,
    validate: bool | None = None
  ) -> ContractMetadataBatchResponse:
    """Fetches collection-level metadata for multiple NFT contracts in a single request.
    
    Args:
      body: List of contract addresses to fetch metadata for.
      validate: Validation override for this request.
    
    Returns:
      The validated endpoint response.
    
    References:
      - [Alchemy API docs](https://www.alchemy.com/docs/reference/nft-api-endpoints/nft-api-endpoints/nft-metadata-endpoints/get-contract-metadata-batch-v-3)
      """
    r = await self.request('POST', '/getContractMetadataBatch', json=body)
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.json(r.text) if self.should_validate(validate) else r.json()
