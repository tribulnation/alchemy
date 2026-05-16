from typing_extensions import Literal, NotRequired, TypedDict
from alchemy.core import Endpoint, PaginatedResponse, Timestamp, validator

class NftSaleFee(TypedDict):
  """Token payment amount in an NFT sale."""
  amount: NotRequired[str]
  """Raw token amount."""
  tokenAddress: NotRequired[str]
  """Payment token contract address."""
  symbol: NotRequired[str]
  """Payment token symbol."""
  decimals: NotRequired[int]
  """Payment token decimals."""

class NftSaleValidAt(TypedDict):
  """Block context at which the sales response was computed."""
  blockNumber: NotRequired[int]
  """Block number used for the response."""
  blockHash: NotRequired[str]
  """Block hash used for the response."""
  blockTimestamp: NotRequired[Timestamp]
  """Block timestamp used for the response."""

class NftSale(TypedDict):
  marketplace: NotRequired[str]
  """Marketplace where the sale occurred."""
  marketplaceAddress: NotRequired[str]
  """Contract address of the marketplace."""
  contractAddress: NotRequired[str]
  """NFT contract address."""
  tokenId: NotRequired[str]
  """Decimal token ID."""
  quantity: NotRequired[str]
  """Number of tokens sold."""
  buyerAddress: NotRequired[str]
  """Buyer wallet address."""
  sellerAddress: NotRequired[str]
  """Seller wallet address."""
  taker: NotRequired[str]
  """Whether the buyer or seller was the price taker."""
  sellerFee: NotRequired[NftSaleFee]
  """Payment from buyer to seller (amount, tokenAddress, symbol, decimals)."""
  protocolFee: NotRequired[NftSaleFee]
  """Payment from buyer to marketplace protocol."""
  royaltyFee: NotRequired[NftSaleFee]
  """Payment from buyer to royalty collector."""
  blockNumber: NotRequired[int]
  """Block number of the sale."""
  logIndex: NotRequired[int]
  """Log index of the sale event within the block."""
  bundleIndex: NotRequired[int]
  """Index within the sale bundle (for bundle sales)."""
  transactionHash: NotRequired[str]
  """Transaction hash of the sale."""

class NftSalesResponse(TypedDict):
  nftSales: NotRequired[list[NftSale]]
  """Array of NFT sale events."""
  pageKey: NotRequired[str | None]
  """Cursor for next page. Null if no more results."""
  validAt: NotRequired[NftSaleValidAt]
  """Block context at which the data is valid."""

adapter = validator(NftSalesResponse)

class GetNftSales(Endpoint):
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
    """Paged version of get_nft_sales.

    Args:
      from_block: Start block number.
      to_block: End block number.
      order: Sort direction from fromBlock.
      marketplace: Filter by marketplace.
      contract_address: Filter by NFT contract address.
      token_id: Filter by token ID.
      buyer_address: Filter by buyer wallet address.
      seller_address: Filter by seller wallet address.
      taker: Filter by price taker role.
      limit: Max results to return per page.
      validate: Validation override for each request.

    Returns:
      An async iterable and awaitable paginated response over NFT sales.

    References:
      - [Alchemy API docs](https://www.alchemy.com/docs/reference/nft-api-endpoints/nft-api-endpoints/nft-sales-endpoints/get-nft-sales-v-3)
    """
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

  async def get_nft_sales(
    self,
    *,
    from_block: str | None = None,
    to_block: str | None = None,
    order: Literal['asc', 'desc'] | None = None,
    marketplace: Literal['seaport', 'wyvern', 'looksrare', 'x2y2', 'blur', 'cryptopunks'] | None = None,
    contract_address: str | None = None,
    token_id: str | None = None,
    buyer_address: str | None = None,
    seller_address: str | None = None,
    taker: Literal['BUYER', 'SELLER'] | None = None,
    limit: int | None = None,
    page_key: str | None = None,
    validate: bool | None = None
  ) -> NftSalesResponse:
    """Retrieves NFT sales data from on-chain marketplaces with rich filtering options.
    
    Args:
      from_block: Start block number (decimal, hex, or 'latest'). Defaults to '0'.
      to_block: End block number (decimal, hex, or 'latest'). Defaults to 'latest'.
      order: Sort direction from fromBlock: 'asc' or 'desc'. Defaults to 'desc'.
      marketplace: Filter by marketplace. One of: seaport, wyvern, looksrare, x2y2, blur, cryptopunks.
      contract_address: Filter by NFT contract address.
      token_id: Filter by token ID within the contractAddress collection.
      buyer_address: Filter by buyer wallet address.
      seller_address: Filter by seller wallet address.
      taker: Filter by price taker role: BUYER or SELLER.
      limit: Max results to return. Maximum 1000. Defaults to 1000.
      page_key: Pagination cursor from a previous response.
      validate: Validation override for this request.
    
    Returns:
      The validated endpoint response.
    
    References:
      - [Alchemy API docs](https://www.alchemy.com/docs/reference/nft-api-endpoints/nft-api-endpoints/nft-sales-endpoints/get-nft-sales-v-3)
      """
    params = {}
    if from_block is not None:
      params['fromBlock'] = from_block
    if to_block is not None:
      params['toBlock'] = to_block
    if order is not None:
      params['order'] = order
    if marketplace is not None:
      params['marketplace'] = marketplace
    if contract_address is not None:
      params['contractAddress'] = contract_address
    if token_id is not None:
      params['tokenId'] = token_id
    if buyer_address is not None:
      params['buyerAddress'] = buyer_address
    if seller_address is not None:
      params['sellerAddress'] = seller_address
    if taker is not None:
      params['taker'] = taker
    if limit is not None:
      params['limit'] = limit
    if page_key is not None:
      params['pageKey'] = page_key
    r = await self.request('GET', '/getNFTSales', params=params)
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.json(r.text) if self.should_validate(validate) else r.json()
