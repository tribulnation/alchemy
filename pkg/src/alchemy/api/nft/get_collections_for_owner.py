from typing_extensions import Literal, NotRequired, TypedDict
from alchemy.core import Endpoint, PaginatedResponse, validator
from .get_contracts_for_owner import OwnerDisplayNft
from .get_nft_metadata import NftContract
from .get_nft_metadata import NftImage

class CollectionFloorPrice(TypedDict):
  """Collection floor price data."""
  marketplace: NotRequired[str | None]
  """Marketplace for the floor price."""
  price: NotRequired[float | None]
  """Floor price amount."""
  currency: NotRequired[str | None]
  """Floor price currency."""

class OwnerCollection(TypedDict):
  name: NotRequired[str]
  """Collection name."""
  slug: NotRequired[str]
  """OpenSea human-readable slug."""
  externalUrl: NotRequired[str | None]
  """External URL for the collection."""
  bannerImageUrl: NotRequired[str | None]
  """Banner image URL."""
  floorPrice: NotRequired[CollectionFloorPrice]
  """Floor price data including marketplace, price, and currency."""
  contract: NotRequired[NftContract]
  """Contract address and metadata."""
  totalBalance: NotRequired[str]
  """Sum of NFT balances across token IDs."""
  numDistinctTokensOwned: NotRequired[str]
  """Count of distinct token IDs held."""
  displayNft: NotRequired[OwnerDisplayNft]
  """Representative NFT (tokenId, name)."""
  image: NotRequired[NftImage]
  """Collection image URLs."""

class OwnerCollectionsResponse(TypedDict):
  collections: NotRequired[list[OwnerCollection]]
  """Array of collection objects held by the owner."""
  pageKey: NotRequired[str]
  """Cursor for next page."""
  totalCount: NotRequired[int]
  """Total number of collections held."""

adapter = validator(OwnerCollectionsResponse)

class GetCollectionsForOwner(Endpoint):
  def get_collections_for_owner_paged(
    self,
    *,
    owner: str,
    page_size: int | None = None,
    with_metadata: bool | None = None,
    include_filters: list[Literal['SPAM', 'AIRDROPS']] | None = None,
    exclude_filters: list[Literal['SPAM', 'AIRDROPS']] | None = None,
    validate: bool | None = None,
  ) -> PaginatedResponse[OwnerCollection, str]:
    """Paged version of get_collections_for_owner.

    Args:
      owner: Wallet address. Supports ENS format on Eth Mainnet.
      page_size: Collections per page. Maximum 100. Defaults to 100.
      with_metadata: Include NFT metadata. Defaults to true.
      include_filters: Include only tokens matching SPAM or AIRDROPS.
      exclude_filters: Exclude tokens matching SPAM or AIRDROPS.
      validate: Validation override for each request.

    Returns:
      An async iterable and awaitable paginated response over owner collections.

    References:
      - [Alchemy API docs](https://www.alchemy.com/docs/reference/nft-api-endpoints/nft-api-endpoints/nft-ownership-endpoints/get-collections-for-owner-v-3)
      """
    async def next(state: str):
      response = await self.get_collections_for_owner(
        owner=owner, page_key=state or None, page_size=page_size,
        with_metadata=with_metadata, include_filters=include_filters,
        exclude_filters=exclude_filters, validate=validate,
      )
      return response.get('collections', []), response.get('pageKey')

    return PaginatedResponse('', next)

  async def get_collections_for_owner(
    self,
    *,
    owner: str,
    page_key: str | None = None,
    page_size: int | None = None,
    with_metadata: bool | None = None,
    include_filters: list[Literal['SPAM', 'AIRDROPS']] | None = None,
    exclude_filters: list[Literal['SPAM', 'AIRDROPS']] | None = None,
    validate: bool | None = None
  ) -> OwnerCollectionsResponse:
    """Returns all NFT collections held by a given wallet address, with collection-level metadata and floor prices.

    Args:
      owner: Wallet address. Supports ENS format on Eth Mainnet.
      page_key: Pagination cursor from previous response.
      page_size: Collections per page. Maximum 100. Defaults to 100.
      with_metadata: Include NFT metadata. Defaults to true.
      include_filters: Include only tokens matching SPAM or AIRDROPS.
      exclude_filters: Exclude tokens matching SPAM or AIRDROPS.
      validate: Validation override for this request.

    Returns:
      The validated endpoint response.

    References:
      - [Alchemy API docs](https://www.alchemy.com/docs/reference/nft-api-endpoints/nft-api-endpoints/nft-ownership-endpoints/get-collections-for-owner-v-3)
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
    r = await self.request('GET', '/getCollectionsForOwner', params=params)

    if r.status_code != 200:
      self.raise_error(r)
    return adapter.json(r.text) if self.should_validate(validate) else r.json()
