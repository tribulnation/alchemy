from datetime import datetime
from typing_extensions import Literal, NotRequired, TypedDict
from alchemy.core import Endpoint, validator

class HistoricalTokenPricePoint(TypedDict):
  value: str
  """Token price at this timestamp as a decimal string."""
  timestamp: datetime
  """ISO 8601 timestamp of the data point."""
  marketCap: NotRequired[str]
  """Market capitalization at this timestamp (only present when `withMarketData=true`)."""
  totalVolume: NotRequired[str]
  """Total trading volume at this timestamp (only present when `withMarketData=true`)."""

class HistoricalTokenPricesRequest(TypedDict):
  symbol: NotRequired[str]
  """Token ticker symbol (e.g. 'ETH'). Required if `network` and `address` are not provided."""
  network: NotRequired[str]
  """Network identifier (e.g. 'eth-mainnet'). Required together with `address` if `symbol` is not provided."""
  address: NotRequired[str]
  """Token contract address. Required together with `network` if `symbol` is not provided."""
  startTime: int
  """Unix timestamp (seconds) for the start of the time range."""
  endTime: int
  """Unix timestamp (seconds) for the end of the time range."""
  interval: NotRequired[Literal['5m', '1h', '1d']]
  """Granularity of price data points. One of '5m', '1h', '1d'. Defaults to '1d'."""
  withMarketData: NotRequired[bool]
  """Whether to include market cap and total volume for each data point."""

class HistoricalTokenPricesResponse(TypedDict):
  symbol: NotRequired[str]
  """Token symbol (present when queried by symbol)."""
  network: NotRequired[str]
  """Network identifier (present when queried by address)."""
  address: NotRequired[str]
  """Token contract address (present when queried by address)."""
  currency: str
  """Currency of price data (e.g. 'usd')."""
  data: list[HistoricalTokenPricePoint]
  """Array of historical price data points."""

adapter = validator(HistoricalTokenPricesResponse)

class Historical(Endpoint):
  async def historical(self, request: HistoricalTokenPricesRequest, *, validate: bool | None = None) -> HistoricalTokenPricesResponse:
    """Fetches historical price data for a token identified either by symbol or by network and contract address.
    
    Args:
      request: Request payload.
      validate: Validation override for this request.
    
    Returns:
      The validated endpoint response.
    
    References:
      - [Alchemy API docs](https://www.alchemy.com/docs/data/prices-api/prices-api-endpoints/prices-api-endpoints/get-historical-token-prices)
      """
    r = await self.request('POST', '/tokens/historical', json=request)
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.json(r.text) if self.should_validate(validate) else r.json()
