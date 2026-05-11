from alchemy.core import Router
from .nft import Nft
from .portfolio import Portfolio
from .prices import Prices
from .simulation import Simulation
from .token import Token
from .transfers import Transfers
from .utility import Utility

class Api(Router):
  nft: Nft
  portfolio: Portfolio
  prices: Prices
  simulation: Simulation
  token: Token
  transfers: Transfers
  utility: Utility
