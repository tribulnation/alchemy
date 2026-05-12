from typing_extensions import Literal, NotRequired, TypedDict
from alchemy.core import Endpoint, validator

class TransactionReceiptLog(TypedDict):
  address: NotRequired[str]
  """Address of the contract that emitted this log."""
  topics: NotRequired[list[str]]
  """TransactionReceiptLog topics."""
  data: NotRequired[str]
  """ABI-encoded log data."""
  blockNumber: NotRequired[str]
  """Hex-encoded block number."""
  blockHash: NotRequired[str]
  """Block hash."""
  transactionHash: NotRequired[str]
  """Transaction hash."""
  transactionIndex: NotRequired[str]
  """Hex-encoded transaction index."""
  logIndex: NotRequired[str]
  """Hex-encoded log index within the block."""
  removed: NotRequired[bool]
  """True if this log was removed due to a chain reorganization."""

class TransactionReceiptsParams(TypedDict):
  """Provide exactly one of blockNumber or blockHash."""
  blockNumber: NotRequired[str]
  """Hex-encoded block number to fetch receipts for (e.g. '0xF1D1C6')."""
  blockHash: NotRequired[str]
  """32-byte block hash to fetch receipts for."""

TransactionReceiptKeywords = TypedDict('TransactionReceiptKeywords', {'from': str})
"""
- `from`: Sender address.
"""

class TransactionReceipt(TransactionReceiptKeywords):
  blockHash: str
  """Hash of the block containing this transaction."""
  blockNumber: str
  """Hex-encoded block number."""
  transactionHash: str
  """Hash of this transaction."""
  transactionIndex: str
  """Hex-encoded index of this transaction within the block."""
  to: NotRequired[str | None]
  """Recipient address, or null for contract creation transactions."""
  contractAddress: NotRequired[str | None]
  """Deployed contract address for contract creation transactions; null otherwise."""
  gasUsed: str
  """Hex-encoded gas used by this transaction."""
  cumulativeGasUsed: str
  """Hex-encoded cumulative gas used up to and including this transaction in the block."""
  effectiveGasPrice: NotRequired[str]
  """Hex-encoded effective gas price paid in wei."""
  logsBloom: str
  """Bloom filter for the logs in this transaction."""
  logs: list[TransactionReceiptLog]
  """Event logs emitted by this transaction."""
  status: Literal['0x0', '0x1']
  """Transaction status: '0x1' for success, '0x0' for failure."""
  type: str
  """Transaction type hex string (e.g. '0x2' for EIP-1559)."""
  root: NotRequired[str | None]
  """Pre-Byzantium state root; null for post-Byzantium transactions."""

class TransactionReceiptsResponse(TypedDict):
  receipts: list[TransactionReceipt]
  """All transaction receipts for the block."""

adapter = validator(TransactionReceiptsResponse)

class GetTransactionReceipts(Endpoint):
  async def get_transaction_receipts(
    self,
    params: TransactionReceiptsParams,
    *,
    validate: bool | None = None
  ) -> TransactionReceiptsResponse:
    """Returns all transaction receipts for a block identified by block number or block hash via the `alchemy_getTransactionReceipts` JSON-RPC method.

    Args:
      params: Request payload.
      validate: Validation override for this request.

    Returns:
      The validated endpoint response.

    References:
      - [Alchemy API docs](https://www.alchemy.com/docs/data/utility-apis/transactions-receipts-endpoints/alchemy-get-transaction-receipts)
      """
    r = await self.rpc_request('alchemy_getTransactionReceipts', params, validate=validate)
    return adapter.python(r) if self.should_validate(validate) else r
