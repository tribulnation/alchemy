from alchemy.core import RpcEndpoint
from .get_transaction_receipts import GetTransactionReceipts

class Utility(RpcEndpoint, GetTransactionReceipts):
  ...
