from datetime import datetime
from typing_extensions import NotRequired, TypedDict
from alchemy.core import Endpoint, validator

class PriceEntry(TypedDict):
  currency: str
  """Currency code (e.g. 'usd')."""
  value: str
  """Token price as a decimal string."""
  lastUpdatedAt: datetime
  """ISO 8601 timestamp of when the price was last updated."""

class SymbolPriceResult(TypedDict):
  symbol: str
  """Token ticker symbol."""
  prices: list[PriceEntry]
  """Array of price objects, one per currency."""
  error: NotRequired[str | None]
  """Error message if the symbol could not be resolved, otherwise null."""

class Response(TypedDict):
  data: list[SymbolPriceResult]
  """Array of price results, one per requested symbol."""

adapter = validator(Response)

class BySymbol(Endpoint):
  async def by_symbol(self, *, symbols: list[str], validate: bool | None = None) -> Response:
    """Fetches current prices for up to 25 tokens identified by their ticker symbols.
    
    Args:
      symbols: Array of token ticker symbols to fetch prices for. Maximum 25 symbols per request.
      validate: Validation override for this request.
    
    Returns:
      The validated endpoint response.
    
    References:
      Upstream docs: https://www.alchemy.com/docs/data/prices-api/prices-api-endpoints/prices-api-endpoints/get-token-prices-by-symbol"""
    params: dict = {
      'symbols': symbols,
    }
    r = await self.request('GET', '/tokens/by-symbol', params=params)
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.json(r.text) if self.should_validate(validate) else r.json()
