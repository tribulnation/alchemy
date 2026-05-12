from typing_extensions import Literal, NotRequired, TypedDict
from alchemy.core import Endpoint, validator
from .get_nft_metadata import NftImage
from .get_nft_metadata import NftOpenSeaMetadata
from .get_nft_metadata import NftTokenType

class OwnerDisplayNft(TypedDict):
  """Representative NFT for display."""
  tokenId: NotRequired[str]
  """Token ID."""
  name: NotRequired[str | None]
  """NFT name."""

class OwnerContract(TypedDict):
  address: NotRequired[str]
  """Contract address."""
  name: NotRequired[str]
  """Contract name."""
  symbol: NotRequired[str]
  """Contract symbol."""
  totalSupply: NotRequired[str]
  """Total supply in the collection."""
  tokenType: NotRequired[NftTokenType]
  """Token standard (ERC721, ERC1155)."""
  totalBalance: NotRequired[str]
  """Sum of NFT balances held by owner."""
  numDistinctTokensOwned: NotRequired[str]
  """Count of distinct token IDs held."""
  isSpam: NotRequired[bool]
  """Whether the contract is classified as spam."""
  displayNft: NotRequired[OwnerDisplayNft]
  """Representative NFT for display."""
  image: NotRequired[NftImage]
  """Contract image URLs."""
  openSeaMetadata: NotRequired[NftOpenSeaMetadata]
  """OpenSea collection metadata."""

class OwnerContractsResponse(TypedDict):
  contracts: NotRequired[list[OwnerContract]]
  """List of NFT contract objects held by the owner."""
  pageKey: NotRequired[str]
  """Cursor for next page."""
  totalCount: NotRequired[int]
  """Total number of contracts held."""

adapter = validator(OwnerContractsResponse)

class GetContractsForOwner(Endpoint):
  async def get_contracts_for_owner(
    self,
    *,
    owner: str,
    page_key: str | None = None,
    page_size: int | None = None,
    with_metadata: bool | None = None,
    include_filters: list[Literal['SPAM', 'AIRDROPS']] | None = None,
    exclude_filters: list[Literal['SPAM', 'AIRDROPS']] | None = None,
    order_by: Literal['transferTime'] | None = None,
    spam_confidence_level: Literal['VERY_HIGH', 'HIGH', 'MEDIUM', 'LOW'] | None = None,
    validate: bool | None = None
  ) -> OwnerContractsResponse:
    """Lists all NFT contracts (collections) for which a given wallet holds at least one token.
    
    Args:
      owner: Wallet address. Supports ENS format on Eth Mainnet.
      page_key: Pagination cursor from previous response.
      page_size: Contracts per page. Maximum 100. Defaults to 100.
      with_metadata: Include contract metadata. Defaults to true.
      include_filters: Include only tokens matching SPAM or AIRDROPS filters.
      exclude_filters: Exclude tokens matching SPAM or AIRDROPS filters.
      order_by: Sort order. 'transferTime' sorts by most recent transfer first.
      spam_confidence_level: Spam threshold (paid tier). One of: VERY_HIGH, HIGH, MEDIUM, LOW.
      validate: Validation override for this request.
    
    Returns:
      The validated endpoint response.
    
    References:
      - [Alchemy API docs](https://www.alchemy.com/docs/reference/nft-api-endpoints/nft-api-endpoints/nft-ownership-endpoints/get-contracts-for-owner-v-3)
      """
    params: dict = {
      'owner': owner,
    }
    if page_key is not None:
      params['pageKey'] = page_key
    if page_size is not None:
      params['pageSize'] = page_size
    if with_metadata is not None:
      params['withMetadata'] = with_metadata
    if include_filters is not None:
      params['includeFilters[]'] = include_filters
    if exclude_filters is not None:
      params['excludeFilters[]'] = exclude_filters
    if order_by is not None:
      params['orderBy'] = order_by
    if spam_confidence_level is not None:
      params['spamConfidenceLevel'] = spam_confidence_level
    r = await self.request('GET', '/getContractsForOwner', params=params)
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.json(r.text) if self.should_validate(validate) else r.json()
