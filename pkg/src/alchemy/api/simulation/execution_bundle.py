from typing_extensions import Any, NotRequired, TypedDict
from alchemy.core import Endpoint, validator

CallTraceKeywords = TypedDict('CallTraceKeywords', {'from': str})

class CallTrace(CallTraceKeywords):
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

class Item(TypedDict):
  name: NotRequired[str]
  type: NotRequired[str]
  value: NotRequired[str]

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

class DecodedLog(TypedDict):
  name: NotRequired[str]
  inputs: NotRequired[list[Item]]

class Log(TypedDict):
  address: NotRequired[str]
  topics: NotRequired[list[str]]
  data: NotRequired[str]
  decoded: NotRequired[DecodedLog | None]

class ExecutionResult(TypedDict):
  calls: list[CallTrace]
  """Recursive call trace for this transaction."""
  logs: list[Log]
  """Event logs emitted during this transaction simulation."""
  gasUsed: str
  """Total hex-encoded gas consumed by this simulated transaction."""
  error: NotRequired[str | None]
  """Error if this transaction simulation failed; null on success."""

adapter = validator(list[ExecutionResult])

class ExecutionBundle(Endpoint):
  async def execution_bundle(
    self,
    transactions: list[Transaction],
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
      Upstream docs: https://www.alchemy.com/docs/reference/simulation-bundle"""
    r = await self.rpc_request('alchemy_simulateExecutionBundle', transactions, validate=validate)
    return adapter.python(r) if self.should_validate(validate) else r
