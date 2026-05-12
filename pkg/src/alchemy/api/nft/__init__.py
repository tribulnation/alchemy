from typing_extensions import Literal

from alchemy.core import NftEndpoint, PaginatedResponse
from .compute_rarity import ComputeRarity
from .get_collection_metadata import GetCollectionMetadata
from .get_collections_for_owner import GetCollectionsForOwner
from .get_collections_for_owner import OwnerCollection
from .get_contract_metadata import GetContractMetadata
from .get_contract_metadata_batch import GetContractMetadataBatch
from .get_contracts_for_owner import GetContractsForOwner
from .get_contracts_for_owner import OwnerContract
from .get_floor_price import GetFloorPrice
from .get_nft_metadata import GetNftMetadata
from .get_nft_metadata import NftMetadataResponse
from .get_nft_metadata_batch import GetNftMetadataBatch
from .get_nft_sales import GetNftSales
from .get_nft_sales import NftSale
from .get_nfts_for_collection import GetNftsForCollection
from .get_nfts_for_contract import GetNftsForContract
from .get_nfts_for_owner import GetNftsForOwner
from .get_nfts_for_owner import OwnedNft
from .get_owners_for_contract import GetOwnersForContract
from .get_owners_for_contract import ContractOwner
from .get_owners_for_nft import GetOwnersForNft
from .get_owners_for_nft import NftOwnersResponse
from .get_spam_contracts import GetSpamContracts
from .invalidate_contract import InvalidateContract
from .is_airdrop_nft import IsAirdropNft
from .is_holder_of_contract import IsHolderOfContract
from .is_spam_contract import IsSpamContract
from .refresh_nft_metadata import RefreshNftMetadata
from .report_spam import ReportSpam
from .search_contract_metadata import SearchContractMetadata
from .summarize_nft_attributes import SummarizeNftAttributes

class Nft(NftEndpoint, ComputeRarity, GetCollectionMetadata, GetCollectionsForOwner, GetContractMetadata, GetContractMetadataBatch, GetContractsForOwner, GetFloorPrice, GetNftMetadata, GetNftMetadataBatch, GetNftSales, GetNftsForCollection, GetNftsForContract, GetNftsForOwner, GetOwnersForContract, GetOwnersForNft, GetSpamContracts, InvalidateContract, IsAirdropNft, IsHolderOfContract, IsSpamContract, RefreshNftMetadata, ReportSpam, SearchContractMetadata, SummarizeNftAttributes):
  def get_nfts_for_owner_paged(
    self, *, owner: str, contract_addresses: list[str] | None = None,
    with_metadata: bool | None = None,
    order_by: Literal['transferTime'] | None = None,
    exclude_filters: list[Literal['SPAM', 'AIRDROPS']] | None = None,
    include_filters: list[Literal['SPAM', 'AIRDROPS']] | None = None,
    spam_confidence_level: Literal['VERY_HIGH', 'HIGH', 'MEDIUM', 'LOW'] | None = None,
    token_uri_timeout_in_ms: int | None = None,
    page_size: int | None = None,
    validate: bool | None = None,
  ) -> PaginatedResponse[OwnedNft, str]:
    """Fetch owned NFTs across all pages."""
    async def next(state: str):
      response = await self.get_nfts_for_owner(
        owner=owner, contract_addresses=contract_addresses,
        with_metadata=with_metadata, order_by=order_by,
        exclude_filters=exclude_filters, include_filters=include_filters,
        spam_confidence_level=spam_confidence_level,
        token_uri_timeout_in_ms=token_uri_timeout_in_ms,
        page_key=state or None, page_size=page_size, validate=validate,
      )
      return response.get('ownedNfts', []), response.get('pageKey')

    return PaginatedResponse('', next)

  def get_contracts_for_owner_paged(
    self, *, owner: str, page_size: int | None = None,
    with_metadata: bool | None = None,
    include_filters: list[Literal['SPAM', 'AIRDROPS']] | None = None,
    exclude_filters: list[Literal['SPAM', 'AIRDROPS']] | None = None,
    order_by: Literal['transferTime'] | None = None,
    spam_confidence_level: Literal['VERY_HIGH', 'HIGH', 'MEDIUM', 'LOW'] | None = None,
    validate: bool | None = None,
  ) -> PaginatedResponse[OwnerContract, str]:
    """Fetch owner contract pages."""
    async def next(state: str):
      response = await self.get_contracts_for_owner(
        owner=owner, page_key=state or None, page_size=page_size,
        with_metadata=with_metadata, include_filters=include_filters,
        exclude_filters=exclude_filters, order_by=order_by,
        spam_confidence_level=spam_confidence_level, validate=validate,
      )
      return response.get('contracts', []), response.get('pageKey')

    return PaginatedResponse('', next)

  def get_collections_for_owner_paged(
    self, *, owner: str, page_size: int | None = None,
    with_metadata: bool | None = None,
    include_filters: list[Literal['SPAM', 'AIRDROPS']] | None = None,
    exclude_filters: list[Literal['SPAM', 'AIRDROPS']] | None = None,
    validate: bool | None = None,
  ) -> PaginatedResponse[OwnerCollection, str]:
    """Fetch owner collection pages."""
    async def next(state: str):
      response = await self.get_collections_for_owner(
        owner=owner, page_key=state or None, page_size=page_size,
        with_metadata=with_metadata, include_filters=include_filters,
        exclude_filters=exclude_filters, validate=validate,
      )
      return response.get('collections', []), response.get('pageKey')

    return PaginatedResponse('', next)

  def get_nft_sales_paged(
    self, *, from_block: str | None = None, to_block: str | None = None,
    order: Literal['asc', 'desc'] | None = None,
    marketplace: Literal['seaport', 'wyvern', 'looksrare', 'x2y2', 'blur', 'cryptopunks'] | None = None,
    contract_address: str | None = None,
    token_id: str | None = None,
    buyer_address: str | None = None,
    seller_address: str | None = None,
    taker: Literal['BUYER', 'SELLER'] | None = None,
    limit: int | None = None,
    validate: bool | None = None,
  ) -> PaginatedResponse[NftSale, str]:
    """Fetch NFT sale pages."""
    async def next(state: str):
      response = await self.get_nft_sales(
        from_block=from_block, to_block=to_block, order=order,
        marketplace=marketplace, contract_address=contract_address,
        token_id=token_id, buyer_address=buyer_address,
        seller_address=seller_address, taker=taker, limit=limit,
        page_key=state or None, validate=validate,
      )
      return response.get('nftSales', []), response.get('pageKey')

    return PaginatedResponse('', next)

  def get_nfts_for_collection_paged(
    self, *, contract_address: str | None = None,
    collection_slug: str | None = None, with_metadata: bool | None = None,
    limit: int | None = None, token_uri_timeout_in_ms: int | None = None,
    validate: bool | None = None,
  ) -> PaginatedResponse[NftMetadataResponse, str]:
    """Fetch collection NFT pages."""
    async def next(state: str):
      response = await self.get_nfts_for_collection(
        contract_address=contract_address, collection_slug=collection_slug,
        with_metadata=with_metadata, start_token=state or None,
        limit=limit, token_uri_timeout_in_ms=token_uri_timeout_in_ms,
        validate=validate,
      )
      return response.get('nfts', []), response.get('pageKey') or response.get('nextToken')

    return PaginatedResponse('', next)

  def get_nfts_for_contract_paged(
    self, *, contract_address: str, with_metadata: bool | None = None,
    limit: int | None = None, token_uri_timeout_in_ms: int | None = None,
    validate: bool | None = None,
  ) -> PaginatedResponse[NftMetadataResponse, str]:
    """Fetch contract NFT pages."""
    async def next(state: str):
      response = await self.get_nfts_for_contract(
        contract_address=contract_address, with_metadata=with_metadata,
        start_token=state or None, limit=limit,
        token_uri_timeout_in_ms=token_uri_timeout_in_ms,
        validate=validate,
      )
      return response.get('nfts', []), response.get('pageKey')

    return PaginatedResponse('', next)

  def get_owners_for_contract_paged(
    self, *, contract_address: str, with_token_balances: bool | None = None,
    validate: bool | None = None,
  ) -> PaginatedResponse[ContractOwner, str]:
    """Fetch contract owner pages."""
    async def next(state: str):
      response = await self.get_owners_for_contract(
        contract_address=contract_address,
        with_token_balances=with_token_balances,
        page_key=state or None, validate=validate,
      )
      return response.get('owners', []), response.get('pageKey')

    return PaginatedResponse('', next)

  def get_owners_for_nft_paged(
    self, *, contract_address: str, token_id: str,
    validate: bool | None = None,
  ) -> PaginatedResponse[str, str]:
    """Fetch NFT owner address pages."""
    async def next(state: str):
      response: NftOwnersResponse = await self.get_owners_for_nft(
        contract_address=contract_address,
        token_id=token_id,
        page_key=state or None,
        validate=validate,
      )
      return response.get('owners', []), response.get('pageKey')

    return PaginatedResponse('', next)
