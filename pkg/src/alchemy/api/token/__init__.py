from alchemy.core import RpcEndpoint
from .get_token_allowance import GetTokenAllowance
from .get_token_balances import GetTokenBalances
from .get_token_metadata import GetTokenMetadata

class Token(RpcEndpoint, GetTokenAllowance, GetTokenBalances, GetTokenMetadata):
  ...
