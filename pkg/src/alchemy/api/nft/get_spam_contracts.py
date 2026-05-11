from typing_extensions import NotRequired, TypedDict
from alchemy.core import Endpoint, validator

class Response200(TypedDict):
  contractAddresses: NotRequired[list[str]]
  """List of contract addresses marked as spam."""

adapter = validator(Response200 | str)

class GetSpamContracts(Endpoint):
  async def get_spam_contracts(self, *, validate: bool | None = None) -> Response200 | str:
    """Returns all NFT contract addresses currently marked as spam by Alchemy. Requires Growth plan or higher.
    
    Args:
      validate: Validation override for this request.
    
    Returns:
      The validated endpoint response.
    
    References:
      Upstream docs: https://www.alchemy.com/docs/reference/nft-api-endpoints/nft-api-endpoints/nft-spam-endpoints/get-spam-contracts-v-3"""
    r = await self.request('GET', '/getSpamContracts')
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.json(r.text) if self.should_validate(validate) else r.json()
