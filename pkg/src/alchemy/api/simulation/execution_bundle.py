from typing_extensions import Any, NotRequired, TypedDict
from alchemy.core import Endpoint, validator

ExecutionBundleCallTraceKeywords = TypedDict('ExecutionBundleCallTraceKeywords', {'from': str})

class ExecutionBundleCallTrace(ExecutionBundleCallTraceKeywords):
  type: NotRequired[str]
  """Call type: CALL, STATICCALL, DELEGATECALL, CREATE, etc."""
  to: NotRequired[str]
  value: NotRequired[str]
  gas: NotRequired[str]
  gasUsed: NotRequired[str]
  input: NotRequired[str]
  output: NotRequired[str]
  error: NotRequired[str | None]
  calls: NotRequired[list[Any]]

class ExecutionBundleDecodedInput(TypedDict):
  name: NotRequired[str]
  type: NotRequired[str]
  value: NotRequired[str]

ExecutionBundleTransactionKeywords = TypedDict('ExecutionBundleTransactionKeywords', {'from': str})
"""
- `from`: Sender address (20-byte hex).
"""

class ExecutionBundleTransaction(ExecutionBundleTransactionKeywords):
  to: str
  """Recipient or contract address (20-byte hex)."""
  value: NotRequired[str]
  """ETH value to send in wei, as a hex string."""
  data: NotRequired[str]
  """ABI-encoded call data for contract interactions."""

class ExecutionBundleDecodedLog(TypedDict):
  name: NotRequired[str]
  inputs: NotRequired[list[ExecutionBundleDecodedInput]]

class ExecutionBundleLog(TypedDict):
  address: NotRequired[str]
  topics: NotRequired[list[str]]
  data: NotRequired[str]
  decoded: NotRequired[ExecutionBundleDecodedLog | None]

class ExecutionResult(TypedDict):
  calls: list[ExecutionBundleCallTrace]
  """Recursive call trace for this transaction."""
  logs: list[ExecutionBundleLog]
  """Event logs emitted during this transaction simulation."""
  gasUsed: str
  """Total hex-encoded gas consumed by this simulated transaction."""
  error: NotRequired[str | None]
  """Error if this transaction simulation failed; null on success."""

adapter = validator(list[ExecutionResult])

class ExecutionBundle(Endpoint):
  async def execution_bundle(
    self,
    transactions: list[ExecutionBundleTransaction],
    *,
    validate: bool | None = None
  ) -> list[ExecutionResult]:
    """Simulates up to 3 sequential transactions and returns execution traces for each without broadcasting via the `alchemy_simulateExecutionBundle` JSON-RPC method.

    Args:
      transactions: Transactions to simulate in order.
      validate: Validation override for this request.

    Returns:
      The validated endpoint response.

    References:
      - [Alchemy API docs](https://www.alchemy.com/docs/reference/simulation-bundle)
      """
    r = await self.rpc_request('alchemy_simulateExecutionBundle', transactions, validate=validate)
    return adapter.python(r) if self.should_validate(validate) else r
