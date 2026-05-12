from typing_extensions import NotRequired, TypedDict
from alchemy.core import Endpoint, validator

class ContractHolderCheckResponse(TypedDict):
  isHolderOfContract: NotRequired[bool]
  """True if the wallet owns at least one token in the contract."""

adapter = validator(ContractHolderCheckResponse)

class IsHolderOfContract(Endpoint):
  async def is_holder_of_contract(
    self,
    *,
    wallet: str,
    contract_address: str,
    validate: bool | None = None
  ) -> ContractHolderCheckResponse:
    """Checks whether a given wallet owns any token in a specified NFT contract.
    
    Args:
      wallet: Wallet address to check.
      contract_address: NFT contract address (ERC721 or ERC1155).
      validate: Validation override for this request.
    
    Returns:
      The validated endpoint response.
    
    References:
      - [Alchemy API docs](https://www.alchemy.com/docs/reference/nft-api-endpoints/nft-api-endpoints/nft-ownership-endpoints/is-holder-of-contract-v-3)
      """
    params: dict = {
      'wallet': wallet,
      'contractAddress': contract_address,
    }
    r = await self.request('GET', '/isHolderOfContract', params=params)
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.json(r.text) if self.should_validate(validate) else r.json()
