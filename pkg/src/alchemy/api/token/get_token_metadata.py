from typing_extensions import NotRequired, TypedDict
from alchemy.core import Endpoint, validator

class Response(TypedDict):
  name: NotRequired[str | None]
  """Token full name (e.g. 'USD Coin')."""
  symbol: NotRequired[str | None]
  """Token ticker symbol (e.g. 'USDC')."""
  decimals: NotRequired[int | None]
  """Number of decimal places for the token."""
  logo: NotRequired[str | None]
  """URL of the token logo image; null if unavailable."""

adapter = validator(Response)

class GetTokenMetadata(Endpoint):
  async def get_token_metadata(
    self,
    contract_address: str,
    *,
    validate: bool | None = None
  ) -> Response:
    """Returns name, symbol, decimals, and logo for a token contract via the `alchemy_getTokenMetadata` JSON-RPC method.

    Args:
      contract_address: Token contract address.
      validate: Validation override for this request.

    Returns:
      The validated endpoint response.

    References:
      Upstream docs: https://www.alchemy.com/docs/data/token-api/token-api-endpoints/alchemy-get-token-metadata"""
    r = await self.rpc_request('alchemy_getTokenMetadata', contract_address, validate=validate)
    return adapter.python(r) if self.should_validate(validate) else r
