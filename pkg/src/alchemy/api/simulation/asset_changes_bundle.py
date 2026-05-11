from typing_extensions import Literal, NotRequired, TypedDict
from alchemy.core import Endpoint, validator

AssetChangeKeywords = TypedDict('AssetChangeKeywords', {'from': str | None})
"""
- `from`: Sender address for this change.
"""

class AssetChange(AssetChangeKeywords):
  assetType: Literal['NATIVE', 'ERC20', 'ERC721', 'ERC1155', 'SPECIAL_NFT']
  """Type of asset involved."""
  changeType: Literal['TRANSFER', 'APPROVAL']
  """Type of change."""
  to: NotRequired[str | None]
  """Recipient address for this change."""
  rawAmount: NotRequired[str | None]
  """Unformatted integer amount."""
  amount: NotRequired[str | None]
  """Formatted decimal amount."""
  contractAddress: NotRequired[str | None]
  """Token contract address; null for native asset."""
  tokenId: NotRequired[str | None]
  """NFT token ID; null for fungible tokens."""
  decimals: NotRequired[int | None]
  """Token decimal places."""
  symbol: NotRequired[str | None]
  """Token ticker symbol."""
  name: NotRequired[str | None]
  """Token full name."""
  logo: NotRequired[str | None]
  """Token logo URL."""

TransactionKeywords = TypedDict('TransactionKeywords', {'from': str})
"""
- `from`: Sender address (20-byte hex).
"""

class Transaction(TransactionKeywords):
  to: str
  """Recipient or contract address (20-byte hex)."""
  value: NotRequired[str]
  """ETH value to send in wei, as a hex string."""
  data: NotRequired[str]
  """ABI-encoded call data for contract interactions."""

class AssetChangesResult(TypedDict):
  changes: list[AssetChange]
  """List of asset changes from this transaction simulation."""
  gasUsed: str
  """Hex-encoded gas consumed by this simulated transaction."""
  error: NotRequired[str | None]
  """Error message if this transaction simulation failed; null on success."""

adapter = validator(list[AssetChangesResult])

class AssetChangesBundle(Endpoint):
  async def asset_changes_bundle(
    self,
    transactions: list[Transaction],
    *,
    validate: bool | None = None
  ) -> list[AssetChangesResult]:
    """Simulates up to 3 sequential transactions and returns asset changes for each without broadcasting via the `alchemy_simulateAssetChangesBundle` JSON-RPC method.

    Args:
      transactions: Transactions to simulate in order.
      validate: Validation override for this request.

    Returns:
      The validated endpoint response.

    References:
      Upstream docs: https://www.alchemy.com/docs/reference/simulation-bundle"""
    r = await self.rpc_request('alchemy_simulateAssetChangesBundle', transactions, validate=validate)
    return adapter.python(r) if self.should_validate(validate) else r
