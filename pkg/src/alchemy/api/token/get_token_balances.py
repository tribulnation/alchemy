from typing_extensions import Any, NotRequired, TypedDict
from alchemy.core import Endpoint, validator

class Options(TypedDict):
  """Pagination options."""
  pageKey: NotRequired[str]
  """Pagination cursor returned by a previous response."""
  maxCount: NotRequired[int]
  """Maximum number of token balances to return. Capped at 100."""

class TokenBalance(TypedDict):
  contractAddress: str
  """Token contract address."""
  tokenBalance: str | None
  """Hex-encoded token balance, or null if an error occurred fetching this token."""

class Response(TypedDict):
  address: str
  """The queried wallet address."""
  tokenBalances: list[TokenBalance]
  """List of token balances for the wallet."""
  pageKey: NotRequired[str]
  """Pagination cursor for retrieving the next page of balances. Present only when more results exist."""

adapter = validator(Response)

class GetTokenBalances(Endpoint):
  async def get_token_balances(
    self,
    params: list[Any],
    *,
    validate: bool | None = None
  ) -> Response:
    """Returns ERC-20 token balances (or native token balance) for a wallet address via the `alchemy_getTokenBalances` JSON-RPC method.

    Args:
      params: JSON-RPC positional parameters: wallet address, token selection, and optional pagination options.
      validate: Validation override for this request.

    Returns:
      The validated endpoint response.

    References:
      Upstream docs: https://www.alchemy.com/docs/data/token-api/token-api-endpoints/alchemy-get-token-balances"""
    r = await self.rpc_request('alchemy_getTokenBalances', params, validate=validate)
    return adapter.python(r) if self.should_validate(validate) else r
