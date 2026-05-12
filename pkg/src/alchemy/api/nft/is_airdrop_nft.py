from typing_extensions import NotRequired, TypedDict
from alchemy.core import Endpoint, validator

class AirdropNftCheckResponse(TypedDict):
  isAirdrop: NotRequired[bool]
  """True if the token was airdropped, false otherwise."""

adapter = validator(AirdropNftCheckResponse)

class IsAirdropNft(Endpoint):
  async def is_airdrop_nft(
    self,
    *,
    contract_address: str,
    token_id: str,
    validate: bool | None = None
  ) -> AirdropNftCheckResponse:
    """Checks whether a specific NFT token was airdropped (minted by an address different from the recipient).
    
    Args:
      contract_address: NFT contract address (ERC721 or ERC1155).
      token_id: Token ID in hex or decimal format.
      validate: Validation override for this request.
    
    Returns:
      The validated endpoint response.
    
    References:
      - [Alchemy API docs](https://www.alchemy.com/docs/data/nft-api/api-reference/nft-spam-endpoints/is-airdrop-nft-v-3)
      """
    params: dict = {
      'contractAddress': contract_address,
      'tokenId': token_id,
    }
    r = await self.request('GET', '/isAirdropNFT', params=params)
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.json(r.text) if self.should_validate(validate) else r.json()
