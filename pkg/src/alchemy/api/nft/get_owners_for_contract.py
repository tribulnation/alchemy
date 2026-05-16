from typing_extensions import NotRequired, TypedDict
from alchemy.core import Endpoint, PaginatedResponse, validator

class OwnerTokenBalance(TypedDict):
  tokenId: NotRequired[str]
  """Token ID."""
  balance: NotRequired[str]
  """Quantity held."""

class ContractOwner(TypedDict):
  ownerAddress: NotRequired[str]
  """Wallet address of the NFT holder."""
  tokenBalances: NotRequired[list[OwnerTokenBalance]]
  """Token holdings when withTokenBalances=true."""

class ContractOwnersResponse(TypedDict):
  owners: NotRequired[list[ContractOwner]]
  """List of owner objects."""
  pageKey: NotRequired[str | None]
  """Pagination key for additional results."""

adapter = validator(ContractOwnersResponse)

class GetOwnersForContract(Endpoint):
  def get_owners_for_contract_paged(
    self, *, contract_address: str, with_token_balances: bool | None = None,
    validate: bool | None = None,
  ) -> PaginatedResponse[ContractOwner, str]:
    """Paged version of get_owners_for_contract.

    Args:
      contract_address: NFT contract address.
      with_token_balances: If true, includes per-token balances for each owner.
      validate: Validation override for each request.

    Returns:
      An async iterable and awaitable paginated response over contract owners.

    References:
      - [Alchemy API docs](https://www.alchemy.com/docs/data/nft-api/api-reference/nft-ownership-endpoints/get-owners-for-contract-v-3)
    """
    async def next(state: str):
      response = await self.get_owners_for_contract(
        contract_address=contract_address,
        with_token_balances=with_token_balances,
        page_key=state or None, validate=validate,
      )
      return response.get('owners', []), response.get('pageKey')

    return PaginatedResponse('', next)

  async def get_owners_for_contract(
    self,
    *,
    contract_address: str,
    with_token_balances: bool | None = None,
    page_key: str | None = None,
    validate: bool | None = None
  ) -> ContractOwnersResponse:
    """Retrieves all owners of a given NFT contract. Optionally includes token balances per owner.
    
    Args:
      contract_address: NFT contract address (ERC721 or ERC1155).
      with_token_balances: If true, includes per-token balances for each owner.
      page_key: Pagination cursor for contracts with over 50,000 owners.
      validate: Validation override for this request.
    
    Returns:
      The validated endpoint response.
    
    References:
      - [Alchemy API docs](https://www.alchemy.com/docs/data/nft-api/api-reference/nft-ownership-endpoints/get-owners-for-contract-v-3)
      """
    params: dict = {
      'contractAddress': contract_address,
    }
    if with_token_balances is not None:
      params['withTokenBalances'] = with_token_balances
    if page_key is not None:
      params['pageKey'] = page_key
    r = await self.request('GET', '/getOwnersForContract', params=params)
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.json(r.text) if self.should_validate(validate) else r.json()
