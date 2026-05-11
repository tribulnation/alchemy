from alchemy.core import PricesEndpoint
from .by_address import ByAddress
from .by_symbol import BySymbol
from .historical import Historical

class Prices(PricesEndpoint, ByAddress, BySymbol, Historical):
  ...
