from typing_extensions import NotRequired, TypedDict
from alchemy.core import Endpoint, validator

class Response200(TypedDict):
  isSpamContract: NotRequired[bool]
  """True if the contract is marked as spam, false if it is considered valid."""

adapter = validator(Response200)

class IsSpamContract(Endpoint):
  async def is_spam_contract(
    self,
    *,
    contract_address: str,
    validate: bool | None = None
  ) -> Response200:
    """Checks whether a given NFT contract is classified as spam by Alchemy.
    
    Args:
      contract_address: NFT contract address (ERC721 or ERC1155).
      validate: Validation override for this request.
    
    Returns:
      The validated endpoint response.
    
    References:
      Upstream docs: https://www.alchemy.com/docs/reference/nft-api-endpoints/nft-api-endpoints/nft-spam-endpoints/is-spam-contract-v-3"""
    params: dict = {
      'contractAddress': contract_address,
    }
    r = await self.request('GET', '/isSpamContract', params=params)
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.json(r.text) if self.should_validate(validate) else r.json()
