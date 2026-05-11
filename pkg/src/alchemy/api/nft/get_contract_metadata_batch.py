from typing_extensions import Any, NotRequired, TypedDict
from alchemy.core import Endpoint, validator

class Body(TypedDict):
  contractAddresses: list[str]
  """List of NFT contract addresses."""

class Response200(TypedDict):
  contracts: NotRequired[list[dict[str, Any]]]
  """Array of contract metadata objects, one per input address."""

adapter = validator(Response200)

class GetContractMetadataBatch(Endpoint):
  async def get_contract_metadata_batch(
    self,
    body: Body,
    *,
    validate: bool | None = None
  ) -> Response200:
    """Fetches collection-level metadata for multiple NFT contracts in a single request.
    
    Args:
      body: List of contract addresses to fetch metadata for.
      validate: Validation override for this request.
    
    Returns:
      The validated endpoint response.
    
    References:
      Upstream docs: https://www.alchemy.com/docs/reference/nft-api-endpoints/nft-api-endpoints/nft-metadata-endpoints/get-contract-metadata-batch-v-3"""
    r = await self.request('POST', '/getContractMetadataBatch', json=body)
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.json(r.text) if self.should_validate(validate) else r.json()
