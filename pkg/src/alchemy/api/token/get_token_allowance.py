from typing_extensions import TypedDict
from alchemy.core import Endpoint, validator

class TokenAllowanceRequest(TypedDict):
  contract: str
  """ERC-20 token contract address."""
  owner: str
  """Wallet address that owns the tokens."""
  spender: str
  """Address approved to spend tokens from the owner."""

adapter = validator(str)

class GetTokenAllowance(Endpoint):
  async def get_token_allowance(
    self,
    token_allowance_request: TokenAllowanceRequest,
    *,
    validate: bool | None = None
  ) -> str:
    """Returns the ERC-20 token allowance for a spender and owner via the `alchemy_getTokenAllowance` JSON-RPC method.

    Args:
      token_allowance_request: Request payload.
      validate: Validation override for this request.

    Returns:
      The validated endpoint response.

    References:
      Upstream docs: https://www.alchemy.com/docs/data/token-api/token-api-endpoints/alchemy-get-token-allowance"""
    r = await self.rpc_request('alchemy_getTokenAllowance', token_allowance_request, validate=validate)
    return adapter.python(r) if self.should_validate(validate) else r
