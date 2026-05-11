from alchemy.core import Router, PortfolioEndpoint
from .nft_contracts import NftContracts
from .nfts import Nfts
from .token_balances import TokenBalances
from .tokens import Tokens
from .transactions import Transactions

class Portfolio(Router, PortfolioEndpoint):
  nft_contracts: NftContracts
  nfts: Nfts
  token_balances: TokenBalances
  tokens: Tokens
  transactions: Transactions
