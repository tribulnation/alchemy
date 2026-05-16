from alchemy.core import RpcEndpoint
from .get_asset_transfers import GetAssetTransfers

class Transfers(RpcEndpoint, GetAssetTransfers):
  ...
