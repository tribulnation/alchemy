from typing_extensions import Literal, NotRequired, TypedDict
from alchemy.core import Endpoint, validator

AssetChangeKeywords = TypedDict('AssetChangeKeywords', {'from': str | None})
"""
- `from`: Sender address for this asset change.
"""

class AssetChange(AssetChangeKeywords):
  assetType: Literal['NATIVE', 'ERC20', 'ERC721', 'ERC1155', 'SPECIAL_NFT']
  """Type of asset involved in the change."""
  changeType: Literal['TRANSFER', 'APPROVAL']
  """Type of change: token transfer or approval."""
  to: NotRequired[str | None]
  """Recipient address for this asset change."""
  rawAmount: NotRequired[str | None]
  """Unformatted integer amount of the asset change."""
  amount: NotRequired[str | None]
  """Formatted decimal amount of the asset change."""
  contractAddress: NotRequired[str | None]
  """Token contract address; null for native asset (ETH/MATIC)."""
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

AssetChangesParamsKeywords = TypedDict('AssetChangesParamsKeywords', {'from': str})
"""
- `from`: Sender address (20-byte hex).
"""

class AssetChangesParams(AssetChangesParamsKeywords):
  """Unsigned transaction object to simulate."""
  to: str
  """Recipient or contract address (20-byte hex)."""
  value: NotRequired[str]
  """ETH value to send in wei, as a hex string (e.g. '0xDE0B6B3A7640000' for 1 ETH)."""
  data: NotRequired[str]
  """ABI-encoded call data for contract interactions."""
  gas: NotRequired[str]
  """Gas limit for the simulated transaction as a hex string."""

class AssetChangesResponse(TypedDict):
  changes: list[AssetChange]
  """List of asset changes (transfers and approvals) resulting from the simulated transaction."""
  gasUsed: str
  """Hex-encoded gas consumed by the simulated transaction."""
  error: NotRequired[str | None]
  """Error message if the simulation failed; null on success."""

adapter = validator(AssetChangesResponse)

class AssetChanges(Endpoint):
  async def asset_changes(self, params: AssetChangesParams, *, validate: bool | None = None) -> AssetChangesResponse:
    """Simulates a transaction and returns a list of asset changes (token transfers and approvals) without broadcasting via the `alchemy_simulateAssetChanges` JSON-RPC method.

    Args:
      params: Request payload.
      validate: Validation override for this request.

    Returns:
      The validated endpoint response.

    References:
      - [Alchemy API docs](https://www.alchemy.com/docs/reference/simulation-asset-changes)
      """
    r = await self.rpc_request('alchemy_simulateAssetChanges', params, validate=validate)
    return adapter.python(r) if self.should_validate(validate) else r
