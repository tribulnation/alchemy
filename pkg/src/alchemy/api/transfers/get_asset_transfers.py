from typing_extensions import Literal, NotRequired, TypedDict
from alchemy.core import Endpoint, validator

class Erc1155TransferItem(TypedDict):
  tokenId: NotRequired[str]
  """ERC-1155 token identifier included in the transfer."""
  value: NotRequired[str]
  """Quantity transferred for this ERC-1155 token identifier."""

class TransferMetadata(TypedDict):
  blockTimestamp: NotRequired[str]
  """Timestamp for the block containing this transfer."""

class AssetTransfersParams(TypedDict):
  fromBlock: NotRequired[str | int | Literal['latest', 'indexed']]
  """Inclusive start block. The docs describe this as a hex string, integer, or the `latest` block tag. `indexed` is also documented as a supported block tag in the Transfers overview."""
  toBlock: NotRequired[str | int | Literal['latest', 'indexed']]
  """Inclusive end block. The docs describe this as a hex string, integer, or the `latest` block tag. `indexed` is also documented as a supported block tag in the Transfers overview."""
  fromAddress: NotRequired[str]
  """Filter transfers by sender address."""
  toAddress: NotRequired[str]
  """Filter transfers by recipient address."""
  contractAddresses: NotRequired[list[str]]
  """Filter by contract address. Alchemy documents this as applying to token transfers (`erc20`, `erc721`, and `erc1155`)."""
  category: list[Literal['external', 'internal', 'erc20', 'erc721', 'erc1155', 'specialnft']]
  """Transfer categories to include."""
  excludeZeroValue: NotRequired[bool]
  """Exclude transfers whose value is zero."""
  maxCount: NotRequired[int | str]
  """Maximum number of results to return. The docs state that 1000 (0x3e8) is the maximum per request."""
  pageKey: NotRequired[str]
  """Pagination cursor returned by a previous response."""
  withMetadata: NotRequired[bool]
  """Include transfer metadata such as the block timestamp."""
  order: NotRequired[Literal['asc', 'desc']]
  """Sort order for transfers. The docs say the default order is ascending; set to `desc` for newest to oldest."""

class RawContract(TypedDict):
  value: NotRequired[str | None]
  """Raw on-chain value as returned by Alchemy."""
  address: NotRequired[str | None]
  """Contract address associated with the transferred asset, when applicable."""
  decimal: NotRequired[str | None]
  """Token decimals as returned by Alchemy."""

TransferKeywords = TypedDict('TransferKeywords', {'from': str})
"""
- `from`: Address that sent the asset.
"""

class Transfer(TransferKeywords):
  blockNum: str
  """Hex-encoded block number containing the transfer."""
  uniqueId: str
  """Alchemy-provided unique identifier for this transfer result."""
  hash: str
  """Transaction hash for the transfer."""
  to: str | None
  """Address that received the asset, or null when unavailable."""
  value: NotRequired[float | None]
  """Normalized numeric value for native or fungible token transfers when available."""
  erc721TokenId: NotRequired[str | None]
  """ERC-721 token identifier when the transfer category is `erc721`."""
  erc1155Metadata: NotRequired[list[Erc1155TransferItem] | None]
  """Per-token metadata returned for ERC-1155 transfers, or null for non-ERC-1155 categories."""
  tokenId: NotRequired[str | None]
  """Token identifier when Alchemy returns a single token ID field."""
  asset: NotRequired[str | None]
  """Asset symbol or display name when available."""
  category: Literal['external', 'internal', 'erc20', 'erc721', 'erc1155', 'specialnft']
  """Transfer category matched by this result."""
  rawContract: RawContract
  metadata: NotRequired[TransferMetadata | None]
  """Returned when `withMetadata=true`; otherwise commonly null in live responses."""

class AssetTransfersResponse(TypedDict):
  transfers: list[Transfer]
  """Transfer results matching the requested filters."""
  pageKey: NotRequired[str]
  """Pagination cursor for retrieving the next page of transfers."""

adapter = validator(AssetTransfersResponse)

class GetAssetTransfers(Endpoint):
  async def get_asset_transfers(
    self,
    params: AssetTransfersParams,
    *,
    validate: bool | None = None
  ) -> AssetTransfersResponse:
    """Fetches historical transfers for an address, contract, or block range via the `alchemy_getAssetTransfers` JSON-RPC method.

    Args:
      params: Request payload.
      validate: Validation override for this request.

    Returns:
      The validated endpoint response.

    References:
      - [Alchemy API docs](https://www.alchemy.com/docs/data/transfers-api/transfers-endpoints/alchemy-get-asset-transfers)
      """
    r = await self.rpc_request('alchemy_getAssetTransfers', params, validate=validate)
    return adapter.python(r) if self.should_validate(validate) else r
