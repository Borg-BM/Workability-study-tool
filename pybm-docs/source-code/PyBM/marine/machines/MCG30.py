from .mcg30_helper import (
    MCG30LHIGHLOAD_Params,
    MCG30LLOWLOAD_Params,
    MCG30LTIPLADDER_Params,
    MCG30LTRANSFER_Params,
    MCG30MHIGHLOAD_Params,
    MCG30MLOWLOAD_Params,
    MCG30MTIPLADDER_Params,
    MCG30MTRANSFER_Params,
)
from .MCG30_Linear import MCG30_Linear, MCG30LIFTING_Linear, MCG30TRANSFER_Linear
from .MCG30_Nonlinear import (
    MCG30_Nonlinear,
    MCG30LIFTING_Nonlinear,
    MCG30TRANSFER_Nonlinear,
)

# Create a class like the one below for every combination of linear and non-linear machines as imported above

class MCG30LHIGHLOAD_Linear(MCG30LHIGHLOAD_Params, MCG30LIFTING_Linear):
    pass

class MCG30LLOWLOAD_Linear(MCG30LLOWLOAD_Params, MCG30LIFTING_Linear):
    pass

class MCG30LTRANSFER_Linear(MCG30LTRANSFER_Params, MCG30TRANSFER_Linear):
    pass

class MCG30LTIPLADDER_Linear(MCG30LTIPLADDER_Params, MCG30TRANSFER_Linear):
    pass

class MCG30MHIGHLOAD_Linear(MCG30MHIGHLOAD_Params, MCG30LIFTING_Linear):
    pass

class MCG30MLOWLOAD_Linear(MCG30MLOWLOAD_Params, MCG30LIFTING_Linear):
    pass

class MCG30MTRANSFER_Linear(MCG30MTRANSFER_Params, MCG30TRANSFER_Linear):
    pass

class MCG30MTIPLADDER_Linear(MCG30MTIPLADDER_Params, MCG30TRANSFER_Linear):
    pass

class MCG30LHIGHLOAD_Nonlinear(MCG30LHIGHLOAD_Params, MCG30LIFTING_Nonlinear):
    pass

class MCG30LLOWLOAD_Nonlinear(MCG30LLOWLOAD_Params, MCG30LIFTING_Nonlinear):
    pass

class MCG30LTRANSFER_Nonlinear(MCG30LTRANSFER_Params, MCG30TRANSFER_Nonlinear):
    pass

class MCG30LTIPLADDER_Nonlinear(MCG30LTIPLADDER_Params, MCG30TRANSFER_Nonlinear):
    pass

class MCG30MHIGHLOAD_Nonlinear(MCG30MHIGHLOAD_Params, MCG30LIFTING_Nonlinear):
    pass

class MCG30MLOWLOAD_Nonlinear(MCG30MLOWLOAD_Params, MCG30LIFTING_Nonlinear):
    pass

class MCG30MTRANSFER_Nonlinear(MCG30MTRANSFER_Params, MCG30TRANSFER_Nonlinear):
    pass

class MCG30MTIPLADDER_Nonlinear(MCG30MTIPLADDER_Params, MCG30TRANSFER_Nonlinear):
    pass

# Add the classes to the __all__ list
__all__ = [
    "MCG30LHIGHLOAD_Linear",
    "MCG30LLOWLOAD_Linear",
    "MCG30LTRANSFER_Linear",
    "MCG30LTIPLADDER_Linear",
    "MCG30MHIGHLOAD_Linear",
    "MCG30MLOWLOAD_Linear",
    "MCG30MTRANSFER_Linear",
    "MCG30MTIPLADDER_Linear",
    "MCG30LHIGHLOAD_Nonlinear",
    "MCG30LLOWLOAD_Nonlinear",
    "MCG30LTRANSFER_Nonlinear",
    "MCG30LTIPLADDER_Nonlinear",
    "MCG30MHIGHLOAD_Nonlinear",
    "MCG30MLOWLOAD_Nonlinear",
    "MCG30MTRANSFER_Nonlinear",
    "MCG30MTIPLADDER_Nonlinear",
]
