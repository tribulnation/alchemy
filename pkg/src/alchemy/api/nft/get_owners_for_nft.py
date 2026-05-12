from typing_extensions import NotRequired, TypedDict
from alchemy.core import Endpoint, validator

class NftOwnersResponse(TypedDict):
  owners: NotRequired[list[str]]
  """List of wallet addresses that own the token."""
  pageKey: NotRequired[str | None]
  """Pagination key for additional results."""

adapter = validator(NftOwnersResponse)

class GetOwnersForNft(Endpoint):
  async def get_owners_for_nft(
    self,
    *,
    contract_address: str,
    token_id: str,
    page_key: str | None = None,
    validate: bool | None = None
  ) -> NftOwnersResponse:
    """Retrieves all owner addresses for a specific NFT token.
    
    Args:
      contract_address: NFT contract address (ERC721 or ERC1155).
      token_id: Token ID in hex or decimal format.
      page_key: Pagination cursor returned by a previous response.
      validate: Validation override for this request.
    
    Returns:
      The validated endpoint response.
    
    References:
      - [Alchemy API docs](https://www.alchemy.com/docs/reference/nft-api-endpoints/nft-api-endpoints/nft-ownership-endpoints/get-owners-for-nft-v-3)
      """
    params: dict = {
      'contractAddress': contract_address,
      'tokenId': token_id,
    }
    if page_key is not None:
      params['pageKey'] = page_key
    r = await self.request('GET', '/getOwnersForNFT', params=params)
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.json(r.text) if self.should_validate(validate) else r.json()
