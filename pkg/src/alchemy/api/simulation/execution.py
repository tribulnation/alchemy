from typing_extensions import Any, NotRequired, TypedDict
from alchemy.core import Endpoint, validator

CallTraceKeywords = TypedDict('CallTraceKeywords', {'from': str})
"""
- `from`: Caller address.
"""

class CallTrace(CallTraceKeywords):
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

class Item(TypedDict):
  name: NotRequired[str]
  type: NotRequired[str]
  value: NotRequired[str]

ParamsKeywords = TypedDict('ParamsKeywords', {'from': str})
"""
- `from`: Sender address (20-byte hex).
"""

class Params(ParamsKeywords):
  """Unsigned transaction object to simulate."""
  to: str
  """Recipient or contract address (20-byte hex)."""
  value: NotRequired[str]
  """ETH value to send in wei, as a hex string."""
  data: NotRequired[str]
  """ABI-encoded call data for contract interactions."""

class DecodedLog(TypedDict):
  name: NotRequired[str]
  """Event name."""
  inputs: NotRequired[list[Item]]
  """Decoded event parameters."""

class Log(TypedDict):
  address: NotRequired[str]
  """Address of the contract that emitted this log."""
  topics: NotRequired[list[str]]
  """Log topics."""
  data: NotRequired[str]
  """ABI-encoded log data."""
  decoded: NotRequired[DecodedLog | None]
  """ABI-decoded log data when Alchemy can resolve the event ABI; null otherwise."""

class Response(TypedDict):
  calls: list[CallTrace]
  """Recursive call trace. Each entry may contain nested subcalls."""
  logs: list[Log]
  """Event logs emitted during the simulated transaction."""
  gasUsed: str
  """Total hex-encoded gas consumed by the simulated transaction."""
  error: NotRequired[str | None]
  """Top-level error if the simulation failed; null on success."""

adapter = validator(Response)

class Execution(Endpoint):
  async def execution(self, params: Params, *, validate: bool | None = None) -> Response:
    """Simulates a transaction and returns decoded execution traces and event logs without broadcasting via the `alchemy_simulateExecution` JSON-RPC method.

    Args:
      params: Request payload.
      validate: Validation override for this request.

    Returns:
      The validated endpoint response.

    References:
      Upstream docs: https://www.alchemy.com/docs/reference/simulation-execution"""
    r = await self.rpc_request('alchemy_simulateExecution', params, validate=validate)
    return adapter.python(r) if self.should_validate(validate) else r
