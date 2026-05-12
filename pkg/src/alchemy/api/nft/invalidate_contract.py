from typing_extensions import NotRequired, TypedDict
from alchemy.core import Endpoint, validator

class InvalidateContractResponse(TypedDict):
  success: NotRequired[bool]
  """True if the contract was successfully invalidated."""
  numTokensInvalidated: NotRequired[float]
  """Number of tokens invalidated. -1 if the token count is unknown."""

adapter = validator(InvalidateContractResponse)

class InvalidateContract(Endpoint):
  async def invalidate_contract(
    self,
    *,
    contract_address: str,
    validate: bool | None = None
  ) -> InvalidateContractResponse:
    """Marks all cached tokens for a contract as stale, ensuring the next query fetches fresh data. Use after collection reveals.
    
    Args:
      contract_address: NFT contract address (ERC721 or ERC1155).
      validate: Validation override for this request.
    
    Returns:
      The validated endpoint response.
    
    References:
      - [Alchemy API docs](https://www.alchemy.com/docs/reference/nft-api-endpoints/nft-api-endpoints/nft-metadata-endpoints/invalidate-contract-v-3)
      """
    params: dict = {
      'contractAddress': contract_address,
    }
    r = await self.request('GET', '/invalidateContract', params=params)
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.json(r.text) if self.should_validate(validate) else r.json()
