from typing_extensions import NotRequired, TypedDict
from alchemy.core import Endpoint, validator

class Response200(TypedDict):
  owners: NotRequired[list[str]]
  """List of wallet addresses that own the token."""
  pageKey: NotRequired[str | None]
  """Pagination key for additional results."""

adapter = validator(Response200)

class GetOwnersForNft(Endpoint):
  async def get_owners_for_nft(
    self,
    *,
    contract_address: str,
    token_id: str,
    validate: bool | None = None
  ) -> Response200:
    """Retrieves all owner addresses for a specific NFT token.
    
    Args:
      contract_address: NFT contract address (ERC721 or ERC1155).
      token_id: Token ID in hex or decimal format.
      validate: Validation override for this request.
    
    Returns:
      The validated endpoint response.
    
    References:
      Upstream docs: https://www.alchemy.com/docs/reference/nft-api-endpoints/nft-api-endpoints/nft-ownership-endpoints/get-owners-for-nft-v-3"""
    params: dict = {
      'contractAddress': contract_address,
      'tokenId': token_id,
    }
    r = await self.request('GET', '/getOwnersForNFT', params=params)
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.json(r.text) if self.should_validate(validate) else r.json()
