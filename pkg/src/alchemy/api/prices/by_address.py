from datetime import datetime
from typing_extensions import NotRequired, TypedDict
from alchemy.core import Endpoint, validator

class TokenPriceEntry(TypedDict):
  currency: str
  """Currency code (e.g. 'usd')."""
  value: str
  """Token price as a decimal string."""
  lastUpdatedAt: datetime
  """ISO 8601 timestamp of when the price was last updated."""

class TokenAddress(TypedDict):
  network: str
  """Network identifier (e.g. 'eth-mainnet', 'base-mainnet')."""
  address: str
  """ERC-20 token contract address."""

class TokenAddressPriceResult(TypedDict):
  network: str
  """Network identifier for this result."""
  address: str
  """Token contract address."""
  prices: list[TokenPriceEntry]
  """Array of price objects, one per currency."""
  error: NotRequired[str | None]
  """Error message if the address could not be resolved, otherwise null."""

class TokenPricesByAddressRequest(TypedDict):
  addresses: list[TokenAddress]
  """Array of token contract address objects. Maximum 25 addresses across a maximum of 3 distinct networks."""

class TokenPricesByAddressResponse(TypedDict):
  data: list[TokenAddressPriceResult]
  """Array of price results, one per requested address."""

adapter = validator(TokenPricesByAddressResponse)

class ByAddress(Endpoint):
  async def by_address(self, request: TokenPricesByAddressRequest, *, validate: bool | None = None) -> TokenPricesByAddressResponse:
    """Fetches current prices for up to 25 ERC-20 token contracts identified by network and address.
    
    Args:
      request: Request payload.
      validate: Validation override for this request.
    
    Returns:
      The validated endpoint response.
    
    References:
      - [Alchemy API docs](https://www.alchemy.com/docs/data/prices-api/prices-api-endpoints/prices-api-endpoints/get-token-prices-by-address)
      """
    r = await self.request('POST', '/tokens/by-address', json=request)
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.json(r.text) if self.should_validate(validate) else r.json()
