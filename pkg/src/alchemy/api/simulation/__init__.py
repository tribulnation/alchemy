from alchemy.core import RpcEndpoint
from .asset_changes import AssetChanges
from .asset_changes_bundle import AssetChangesBundle
from .execution import Execution
from .execution_bundle import ExecutionBundle

class Simulation(RpcEndpoint, AssetChanges, AssetChangesBundle, Execution, ExecutionBundle):
  ...
