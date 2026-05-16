from typing_extensions import NotRequired, TypedDict
from alchemy.core import Endpoint, PaginatedResponse, validator
from .get_nft_metadata import NftMetadataResponse

class CollectionNftsResponse(TypedDict):
  nfts: NotRequired[list[NftMetadataResponse]]
  """Array of NFT objects in the collection."""
  pageKey: NotRequired[str]
  """Token ID offset for fetching the next page."""
  nextToken: NotRequired[str]
  """Documented pagination token name for fetching the next page."""

adapter = validator(CollectionNftsResponse)

class GetNftsForCollection(Endpoint):
  def get_nfts_for_collection_paged(
    self, *, contract_address: str | None = None,
    collection_slug: str | None = None, with_metadata: bool | None = None,
    limit: int | None = None, token_uri_timeout_in_ms: int | None = None,
    validate: bool | None = None,
  ) -> PaginatedResponse[NftMetadataResponse, str]:
    """Paged version of get_nfts_for_collection.

    Args:
      contract_address: NFT contract address (ERC721 or ERC1155).
      collection_slug: OpenSea collection slug.
      with_metadata: Include NFT metadata. Defaults to true.
      limit: Number of NFTs to return per page. Defaults to 100.
      token_uri_timeout_in_ms: Timeout for metadata fetching in milliseconds. Set to 0 for cache-only.
      validate: Validation override for each request.

    Returns:
      An async iterable and awaitable paginated response over NFT metadata.

    References:
      - [Alchemy API docs](https://www.alchemy.com/docs/reference/nft-api-endpoints/nft-api-endpoints/nft-metadata-endpoints/get-nf-ts-for-collection-v-3)
    """
    async def next(state: str):
      response = await self.get_nfts_for_collection(
        contract_address=contract_address, collection_slug=collection_slug,
        with_metadata=with_metadata, start_token=state or None,
        limit=limit, token_uri_timeout_in_ms=token_uri_timeout_in_ms,
        validate=validate,
      )
      return response.get('nfts', []), response.get('pageKey') or response.get('nextToken')

    return PaginatedResponse('', next)

  async def get_nfts_for_collection(
    self,
    *,
    contract_address: str | None = None,
    collection_slug: str | None = None,
    with_metadata: bool | None = None,
    start_token: str | None = None,
    limit: int | None = None,
    token_uri_timeout_in_ms: int | None = None,
    validate: bool | None = None
  ) -> CollectionNftsResponse:
    """Retrieves NFTs associated with a specific NFT collection.
    
    Args:
      contract_address: NFT contract address (ERC721 or ERC1155).
      collection_slug: OpenSea collection slug.
      with_metadata: Include NFT metadata. Defaults to true.
      start_token: Token ID offset for pagination (hex or decimal).
      limit: Number of NFTs to return. Defaults to 100.
      token_uri_timeout_in_ms: Timeout for metadata fetching in milliseconds. Set to 0 for cache-only.
      validate: Validation override for this request.
    
    Returns:
      The validated endpoint response.
    
    References:
      - [Alchemy API docs](https://www.alchemy.com/docs/reference/nft-api-endpoints/nft-api-endpoints/nft-metadata-endpoints/get-nf-ts-for-collection-v-3)
      """
    params = {}
    if contract_address is not None:
      params['contractAddress'] = contract_address
    if collection_slug is not None:
      params['collectionSlug'] = collection_slug
    if with_metadata is not None:
      params['withMetadata'] = with_metadata
    if start_token is not None:
      params['startToken'] = start_token
    if limit is not None:
      params['limit'] = limit
    if token_uri_timeout_in_ms is not None:
      params['tokenUriTimeoutInMs'] = token_uri_timeout_in_ms
    r = await self.request('GET', '/getNFTsForCollection', params=params)
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.json(r.text) if self.should_validate(validate) else r.json()
