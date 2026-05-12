from typing_extensions import Any, NotRequired, TypedDict
from alchemy.core import Endpoint, validator

ExecutionCallTraceKeywords = TypedDict('ExecutionCallTraceKeywords', {'from': str})
"""
- `from`: Caller address.
"""

class ExecutionCallTrace(ExecutionCallTraceKeywords):
  type: NotRequired[str]
  """Call type: CALL, STATICCALL, DELEGATECALL, CREATE, etc."""
  to: NotRequired[str]
  """Callee address."""
  value: NotRequired[str]
  """Value transferred in wei (hex)."""
  gas: NotRequired[str]
  """Gas limit for this call (hex)."""
  gasUsed: NotRequired[str]
  """Gas consumed by this call (hex)."""
  input: NotRequired[str]
  """ABI-encoded input data."""
  output: NotRequired[str]
  """ABI-encoded return data."""
  error: NotRequired[str | None]
  """Revert reason if this call frame failed; null on success."""
  calls: NotRequired[list[Any]]
  """Nested subcalls made from this call frame."""

class DecodedInput(TypedDict):
  name: NotRequired[str]
  type: NotRequired[str]
  value: NotRequired[str]

ExecutionParamsKeywords = TypedDict('ExecutionParamsKeywords', {'from': str})
"""
- `from`: Sender address (20-byte hex).
"""

class ExecutionParams(ExecutionParamsKeywords):
  """Unsigned transaction object to simulate."""
  to: str
  """Recipient or contract address (20-byte hex)."""
  value: NotRequired[str]
  """ETH value to send in wei, as a hex string."""
  data: NotRequired[str]
  """ABI-encoded call data for contract interactions."""

class DecodedExecutionLog(TypedDict):
  name: NotRequired[str]
  """Event name."""
  inputs: NotRequired[list[DecodedInput]]
  """Decoded event parameters."""

class ExecutionLog(TypedDict):
  address: NotRequired[str]
  """Address of the contract that emitted this log."""
  topics: NotRequired[list[str]]
  """ExecutionLog topics."""
  data: NotRequired[str]
  """ABI-encoded log data."""
  decoded: NotRequired[DecodedExecutionLog | None]
  """ABI-decoded log data when Alchemy can resolve the event ABI; null otherwise."""

class ExecutionResponse(TypedDict):
  calls: list[ExecutionCallTrace]
  """Recursive call trace. Each entry may contain nested subcalls."""
  logs: list[ExecutionLog]
  """Event logs emitted during the simulated transaction."""
  gasUsed: str
  """Total hex-encoded gas consumed by the simulated transaction."""
  error: NotRequired[str | None]
  """Top-level error if the simulation failed; null on success."""

adapter = validator(ExecutionResponse)

class Execution(Endpoint):
  async def execution(self, params: ExecutionParams, *, validate: bool | None = None) -> ExecutionResponse:
    """Simulates a transaction and returns decoded execution traces and event logs without broadcasting via the `alchemy_simulateExecution` JSON-RPC method.

    Args:
      params: Request payload.
      validate: Validation override for this request.

    Returns:
      The validated endpoint response.

    References:
      - [Alchemy API docs](https://www.alchemy.com/docs/reference/simulation-execution)
      """
    r = await self.rpc_request('alchemy_simulateExecution', params, validate=validate)
    return adapter.python(r) if self.should_validate(validate) else r
