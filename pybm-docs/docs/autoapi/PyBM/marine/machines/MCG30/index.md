<!-- Source: https://docs.app.barge-master.com/autoapi/PyBM/marine/machines/MCG30/index.html -->

# PyBM.marine.machines.MCG30

## Submodules

- [PyBM.marine.machines.MCG30.MCG30_Linear](MCG30_Linear/index.md)
- [PyBM.marine.machines.MCG30.MCG30_Nonlinear](MCG30_Nonlinear/index.md)
- [PyBM.marine.machines.MCG30.mcg30_helper](mcg30_helper/index.md)

## Classes

|                                                                                                                                             |                                                                                       |
|---------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------|
| [`MCG30LHIGHLOAD_Linear`](#PyBM.marine.machines.MCG30.MCG30LHIGHLOAD_Linear "PyBM.marine.machines.MCG30.MCG30LHIGHLOAD_Linear")             | Helper class that provides a standard way to create an ABC using                      |
| [`MCG30LLOWLOAD_Linear`](#PyBM.marine.machines.MCG30.MCG30LLOWLOAD_Linear "PyBM.marine.machines.MCG30.MCG30LLOWLOAD_Linear")                | Helper class that provides a standard way to create an ABC using                      |
| [`MCG30LTRANSFER_Linear`](#PyBM.marine.machines.MCG30.MCG30LTRANSFER_Linear "PyBM.marine.machines.MCG30.MCG30LTRANSFER_Linear")             | Helper class that provides a standard way to create an ABC using                      |
| [`MCG30LTIPLADDER_Linear`](#PyBM.marine.machines.MCG30.MCG30LTIPLADDER_Linear "PyBM.marine.machines.MCG30.MCG30LTIPLADDER_Linear")          | For the tip ladder the standard deviation limits are reduced by multiplying them with |
| [`MCG30MHIGHLOAD_Linear`](#PyBM.marine.machines.MCG30.MCG30MHIGHLOAD_Linear "PyBM.marine.machines.MCG30.MCG30MHIGHLOAD_Linear")             | Helper class that provides a standard way to create an ABC using                      |
| [`MCG30MLOWLOAD_Linear`](#PyBM.marine.machines.MCG30.MCG30MLOWLOAD_Linear "PyBM.marine.machines.MCG30.MCG30MLOWLOAD_Linear")                | Helper class that provides a standard way to create an ABC using                      |
| [`MCG30MTRANSFER_Linear`](#PyBM.marine.machines.MCG30.MCG30MTRANSFER_Linear "PyBM.marine.machines.MCG30.MCG30MTRANSFER_Linear")             | Helper class that provides a standard way to create an ABC using                      |
| [`MCG30MTIPLADDER_Linear`](#PyBM.marine.machines.MCG30.MCG30MTIPLADDER_Linear "PyBM.marine.machines.MCG30.MCG30MTIPLADDER_Linear")          | For the tip ladder the standard deviation limits are reduced by multiplying them with |
| [`MCG30LHIGHLOAD_Nonlinear`](#PyBM.marine.machines.MCG30.MCG30LHIGHLOAD_Nonlinear "PyBM.marine.machines.MCG30.MCG30LHIGHLOAD_Nonlinear")    | Helper class that provides a standard way to create an ABC using                      |
| [`MCG30LLOWLOAD_Nonlinear`](#PyBM.marine.machines.MCG30.MCG30LLOWLOAD_Nonlinear "PyBM.marine.machines.MCG30.MCG30LLOWLOAD_Nonlinear")       | Helper class that provides a standard way to create an ABC using                      |
| [`MCG30LTRANSFER_Nonlinear`](#PyBM.marine.machines.MCG30.MCG30LTRANSFER_Nonlinear "PyBM.marine.machines.MCG30.MCG30LTRANSFER_Nonlinear")    | Helper class that provides a standard way to create an ABC using                      |
| [`MCG30LTIPLADDER_Nonlinear`](#PyBM.marine.machines.MCG30.MCG30LTIPLADDER_Nonlinear "PyBM.marine.machines.MCG30.MCG30LTIPLADDER_Nonlinear") | For the tip ladder the standard deviation limits are reduced by multiplying them with |
| [`MCG30MHIGHLOAD_Nonlinear`](#PyBM.marine.machines.MCG30.MCG30MHIGHLOAD_Nonlinear "PyBM.marine.machines.MCG30.MCG30MHIGHLOAD_Nonlinear")    | Helper class that provides a standard way to create an ABC using                      |
| [`MCG30MLOWLOAD_Nonlinear`](#PyBM.marine.machines.MCG30.MCG30MLOWLOAD_Nonlinear "PyBM.marine.machines.MCG30.MCG30MLOWLOAD_Nonlinear")       | Helper class that provides a standard way to create an ABC using                      |
| [`MCG30MTRANSFER_Nonlinear`](#PyBM.marine.machines.MCG30.MCG30MTRANSFER_Nonlinear "PyBM.marine.machines.MCG30.MCG30MTRANSFER_Nonlinear")    | Helper class that provides a standard way to create an ABC using                      |
| [`MCG30MTIPLADDER_Nonlinear`](#PyBM.marine.machines.MCG30.MCG30MTIPLADDER_Nonlinear "PyBM.marine.machines.MCG30.MCG30MTIPLADDER_Nonlinear") | For the tip ladder the standard deviation limits are reduced by multiplying them with |

## Package Contents

*class *PyBM.marine.machines.MCG30.MCG30LHIGHLOAD_Linear(*position*, *gw_luff_angle_mean*, *gw_slew_angle_mean*, *dp_accuracy=0.1*, *gw_telescope_mean=None*)[](../../../../../../source-code/PyBM/marine/machines/MCG30.py)  
Bases: [`mcg30_helper.MCG30LHIGHLOAD_Params`](mcg30_helper/index.md#PyBM.marine.machines.MCG30.mcg30_helper.MCG30LHIGHLOAD_Params "PyBM.marine.machines.MCG30.mcg30_helper.MCG30LHIGHLOAD_Params"), [`MCG30_Linear.MCG30LIFTING_Linear`](MCG30_Linear/index.md#PyBM.marine.machines.MCG30.MCG30_Linear.MCG30LIFTING_Linear "PyBM.marine.machines.MCG30.MCG30_Linear.MCG30LIFTING_Linear")

Helper class that provides a standard way to create an ABC using inheritance.

&nbsp;

*class *PyBM.marine.machines.MCG30.MCG30LLOWLOAD_Linear(*position*, *gw_luff_angle_mean*, *gw_slew_angle_mean*, *dp_accuracy=0.1*, *gw_telescope_mean=None*)[](../../../../../../source-code/PyBM/marine/machines/MCG30.py)  
Bases: [`mcg30_helper.MCG30LLOWLOAD_Params`](mcg30_helper/index.md#PyBM.marine.machines.MCG30.mcg30_helper.MCG30LLOWLOAD_Params "PyBM.marine.machines.MCG30.mcg30_helper.MCG30LLOWLOAD_Params"), [`MCG30_Linear.MCG30LIFTING_Linear`](MCG30_Linear/index.md#PyBM.marine.machines.MCG30.MCG30_Linear.MCG30LIFTING_Linear "PyBM.marine.machines.MCG30.MCG30_Linear.MCG30LIFTING_Linear")

Helper class that provides a standard way to create an ABC using inheritance.

&nbsp;

*class *PyBM.marine.machines.MCG30.MCG30LTRANSFER_Linear(*position*, *gw_luff_angle_mean*, *gw_slew_angle_mean*, *dp_accuracy=0.1*, *gw_telescope_mean=None*)[](../../../../../../source-code/PyBM/marine/machines/MCG30.py)  
Bases: [`mcg30_helper.MCG30LTRANSFER_Params`](mcg30_helper/index.md#PyBM.marine.machines.MCG30.mcg30_helper.MCG30LTRANSFER_Params "PyBM.marine.machines.MCG30.mcg30_helper.MCG30LTRANSFER_Params"), [`MCG30_Linear.MCG30TRANSFER_Linear`](MCG30_Linear/index.md#PyBM.marine.machines.MCG30.MCG30_Linear.MCG30TRANSFER_Linear "PyBM.marine.machines.MCG30.MCG30_Linear.MCG30TRANSFER_Linear")

Helper class that provides a standard way to create an ABC using inheritance.

&nbsp;

*class *PyBM.marine.machines.MCG30.MCG30LTIPLADDER_Linear(*position*, *gw_luff_angle_mean*, *gw_slew_angle_mean*, *dp_accuracy=0.1*, *gw_telescope_mean=None*)[](../../../../../../source-code/PyBM/marine/machines/MCG30.py)  
Bases: [`mcg30_helper.MCG30LTIPLADDER_Params`](mcg30_helper/index.md#PyBM.marine.machines.MCG30.mcg30_helper.MCG30LTIPLADDER_Params "PyBM.marine.machines.MCG30.mcg30_helper.MCG30LTIPLADDER_Params"), [`MCG30_Linear.MCG30TRANSFER_Linear`](MCG30_Linear/index.md#PyBM.marine.machines.MCG30.MCG30_Linear.MCG30TRANSFER_Linear "PyBM.marine.machines.MCG30.MCG30_Linear.MCG30TRANSFER_Linear")

For the tip ladder the standard deviation limits are reduced by multiplying them with  
- stroke 70%

- velocity 35%

&nbsp;

*class *PyBM.marine.machines.MCG30.MCG30MHIGHLOAD_Linear(*position*, *gw_luff_angle_mean*, *gw_slew_angle_mean*, *dp_accuracy=0.1*, *gw_telescope_mean=None*)[](../../../../../../source-code/PyBM/marine/machines/MCG30.py)  
Bases: [`mcg30_helper.MCG30MHIGHLOAD_Params`](mcg30_helper/index.md#PyBM.marine.machines.MCG30.mcg30_helper.MCG30MHIGHLOAD_Params "PyBM.marine.machines.MCG30.mcg30_helper.MCG30MHIGHLOAD_Params"), [`MCG30_Linear.MCG30LIFTING_Linear`](MCG30_Linear/index.md#PyBM.marine.machines.MCG30.MCG30_Linear.MCG30LIFTING_Linear "PyBM.marine.machines.MCG30.MCG30_Linear.MCG30LIFTING_Linear")

Helper class that provides a standard way to create an ABC using inheritance.

&nbsp;

*class *PyBM.marine.machines.MCG30.MCG30MLOWLOAD_Linear(*position*, *gw_luff_angle_mean*, *gw_slew_angle_mean*, *dp_accuracy=0.1*, *gw_telescope_mean=None*)[](../../../../../../source-code/PyBM/marine/machines/MCG30.py)  
Bases: [`mcg30_helper.MCG30MLOWLOAD_Params`](mcg30_helper/index.md#PyBM.marine.machines.MCG30.mcg30_helper.MCG30MLOWLOAD_Params "PyBM.marine.machines.MCG30.mcg30_helper.MCG30MLOWLOAD_Params"), [`MCG30_Linear.MCG30LIFTING_Linear`](MCG30_Linear/index.md#PyBM.marine.machines.MCG30.MCG30_Linear.MCG30LIFTING_Linear "PyBM.marine.machines.MCG30.MCG30_Linear.MCG30LIFTING_Linear")

Helper class that provides a standard way to create an ABC using inheritance.

&nbsp;

*class *PyBM.marine.machines.MCG30.MCG30MTRANSFER_Linear(*position*, *gw_luff_angle_mean*, *gw_slew_angle_mean*, *dp_accuracy=0.1*, *gw_telescope_mean=None*)[](../../../../../../source-code/PyBM/marine/machines/MCG30.py)  
Bases: [`mcg30_helper.MCG30MTRANSFER_Params`](mcg30_helper/index.md#PyBM.marine.machines.MCG30.mcg30_helper.MCG30MTRANSFER_Params "PyBM.marine.machines.MCG30.mcg30_helper.MCG30MTRANSFER_Params"), [`MCG30_Linear.MCG30TRANSFER_Linear`](MCG30_Linear/index.md#PyBM.marine.machines.MCG30.MCG30_Linear.MCG30TRANSFER_Linear "PyBM.marine.machines.MCG30.MCG30_Linear.MCG30TRANSFER_Linear")

Helper class that provides a standard way to create an ABC using inheritance.

&nbsp;

*class *PyBM.marine.machines.MCG30.MCG30MTIPLADDER_Linear(*position*, *gw_luff_angle_mean*, *gw_slew_angle_mean*, *dp_accuracy=0.1*, *gw_telescope_mean=None*)[](../../../../../../source-code/PyBM/marine/machines/MCG30.py)  
Bases: [`mcg30_helper.MCG30MTIPLADDER_Params`](mcg30_helper/index.md#PyBM.marine.machines.MCG30.mcg30_helper.MCG30MTIPLADDER_Params "PyBM.marine.machines.MCG30.mcg30_helper.MCG30MTIPLADDER_Params"), [`MCG30_Linear.MCG30TRANSFER_Linear`](MCG30_Linear/index.md#PyBM.marine.machines.MCG30.MCG30_Linear.MCG30TRANSFER_Linear "PyBM.marine.machines.MCG30.MCG30_Linear.MCG30TRANSFER_Linear")

For the tip ladder the standard deviation limits are reduced by multiplying them with  
- stroke 70%

- velocity 35%

&nbsp;

*class *PyBM.marine.machines.MCG30.MCG30LHIGHLOAD_Nonlinear(*position*, *gw_luff_angle_mean*, *gw_slew_angle_mean*, *dp_accuracy=0.1*, *gw_telescope_mean=None*)[](../../../../../../source-code/PyBM/marine/machines/MCG30.py)  
Bases: [`mcg30_helper.MCG30LHIGHLOAD_Params`](mcg30_helper/index.md#PyBM.marine.machines.MCG30.mcg30_helper.MCG30LHIGHLOAD_Params "PyBM.marine.machines.MCG30.mcg30_helper.MCG30LHIGHLOAD_Params"), [`MCG30_Nonlinear.MCG30LIFTING_Nonlinear`](MCG30_Nonlinear/index.md#PyBM.marine.machines.MCG30.MCG30_Nonlinear.MCG30LIFTING_Nonlinear "PyBM.marine.machines.MCG30.MCG30_Nonlinear.MCG30LIFTING_Nonlinear")

Helper class that provides a standard way to create an ABC using inheritance.

&nbsp;

*class *PyBM.marine.machines.MCG30.MCG30LLOWLOAD_Nonlinear(*position*, *gw_luff_angle_mean*, *gw_slew_angle_mean*, *dp_accuracy=0.1*, *gw_telescope_mean=None*)[](../../../../../../source-code/PyBM/marine/machines/MCG30.py)  
Bases: [`mcg30_helper.MCG30LLOWLOAD_Params`](mcg30_helper/index.md#PyBM.marine.machines.MCG30.mcg30_helper.MCG30LLOWLOAD_Params "PyBM.marine.machines.MCG30.mcg30_helper.MCG30LLOWLOAD_Params"), [`MCG30_Nonlinear.MCG30LIFTING_Nonlinear`](MCG30_Nonlinear/index.md#PyBM.marine.machines.MCG30.MCG30_Nonlinear.MCG30LIFTING_Nonlinear "PyBM.marine.machines.MCG30.MCG30_Nonlinear.MCG30LIFTING_Nonlinear")

Helper class that provides a standard way to create an ABC using inheritance.

&nbsp;

*class *PyBM.marine.machines.MCG30.MCG30LTRANSFER_Nonlinear(*position*, *gw_luff_angle_mean*, *gw_slew_angle_mean*, *dp_accuracy=0.1*, *gw_telescope_mean=None*)[](../../../../../../source-code/PyBM/marine/machines/MCG30.py)  
Bases: [`mcg30_helper.MCG30LTRANSFER_Params`](mcg30_helper/index.md#PyBM.marine.machines.MCG30.mcg30_helper.MCG30LTRANSFER_Params "PyBM.marine.machines.MCG30.mcg30_helper.MCG30LTRANSFER_Params"), [`MCG30_Nonlinear.MCG30TRANSFER_Nonlinear`](MCG30_Nonlinear/index.md#PyBM.marine.machines.MCG30.MCG30_Nonlinear.MCG30TRANSFER_Nonlinear "PyBM.marine.machines.MCG30.MCG30_Nonlinear.MCG30TRANSFER_Nonlinear")

Helper class that provides a standard way to create an ABC using inheritance.

&nbsp;

*class *PyBM.marine.machines.MCG30.MCG30LTIPLADDER_Nonlinear(*position*, *gw_luff_angle_mean*, *gw_slew_angle_mean*, *dp_accuracy=0.1*, *gw_telescope_mean=None*)[](../../../../../../source-code/PyBM/marine/machines/MCG30.py)  
Bases: [`mcg30_helper.MCG30LTIPLADDER_Params`](mcg30_helper/index.md#PyBM.marine.machines.MCG30.mcg30_helper.MCG30LTIPLADDER_Params "PyBM.marine.machines.MCG30.mcg30_helper.MCG30LTIPLADDER_Params"), [`MCG30_Nonlinear.MCG30TRANSFER_Nonlinear`](MCG30_Nonlinear/index.md#PyBM.marine.machines.MCG30.MCG30_Nonlinear.MCG30TRANSFER_Nonlinear "PyBM.marine.machines.MCG30.MCG30_Nonlinear.MCG30TRANSFER_Nonlinear")

For the tip ladder the standard deviation limits are reduced by multiplying them with  
- stroke 70%

- velocity 35%

&nbsp;

*class *PyBM.marine.machines.MCG30.MCG30MHIGHLOAD_Nonlinear(*position*, *gw_luff_angle_mean*, *gw_slew_angle_mean*, *dp_accuracy=0.1*, *gw_telescope_mean=None*)[](../../../../../../source-code/PyBM/marine/machines/MCG30.py)  
Bases: [`mcg30_helper.MCG30MHIGHLOAD_Params`](mcg30_helper/index.md#PyBM.marine.machines.MCG30.mcg30_helper.MCG30MHIGHLOAD_Params "PyBM.marine.machines.MCG30.mcg30_helper.MCG30MHIGHLOAD_Params"), [`MCG30_Nonlinear.MCG30LIFTING_Nonlinear`](MCG30_Nonlinear/index.md#PyBM.marine.machines.MCG30.MCG30_Nonlinear.MCG30LIFTING_Nonlinear "PyBM.marine.machines.MCG30.MCG30_Nonlinear.MCG30LIFTING_Nonlinear")

Helper class that provides a standard way to create an ABC using inheritance.

&nbsp;

*class *PyBM.marine.machines.MCG30.MCG30MLOWLOAD_Nonlinear(*position*, *gw_luff_angle_mean*, *gw_slew_angle_mean*, *dp_accuracy=0.1*, *gw_telescope_mean=None*)[](../../../../../../source-code/PyBM/marine/machines/MCG30.py)  
Bases: [`mcg30_helper.MCG30MLOWLOAD_Params`](mcg30_helper/index.md#PyBM.marine.machines.MCG30.mcg30_helper.MCG30MLOWLOAD_Params "PyBM.marine.machines.MCG30.mcg30_helper.MCG30MLOWLOAD_Params"), [`MCG30_Nonlinear.MCG30LIFTING_Nonlinear`](MCG30_Nonlinear/index.md#PyBM.marine.machines.MCG30.MCG30_Nonlinear.MCG30LIFTING_Nonlinear "PyBM.marine.machines.MCG30.MCG30_Nonlinear.MCG30LIFTING_Nonlinear")

Helper class that provides a standard way to create an ABC using inheritance.

&nbsp;

*class *PyBM.marine.machines.MCG30.MCG30MTRANSFER_Nonlinear(*position*, *gw_luff_angle_mean*, *gw_slew_angle_mean*, *dp_accuracy=0.1*, *gw_telescope_mean=None*)[](../../../../../../source-code/PyBM/marine/machines/MCG30.py)  
Bases: [`mcg30_helper.MCG30MTRANSFER_Params`](mcg30_helper/index.md#PyBM.marine.machines.MCG30.mcg30_helper.MCG30MTRANSFER_Params "PyBM.marine.machines.MCG30.mcg30_helper.MCG30MTRANSFER_Params"), [`MCG30_Nonlinear.MCG30TRANSFER_Nonlinear`](MCG30_Nonlinear/index.md#PyBM.marine.machines.MCG30.MCG30_Nonlinear.MCG30TRANSFER_Nonlinear "PyBM.marine.machines.MCG30.MCG30_Nonlinear.MCG30TRANSFER_Nonlinear")

Helper class that provides a standard way to create an ABC using inheritance.

&nbsp;

*class *PyBM.marine.machines.MCG30.MCG30MTIPLADDER_Nonlinear(*position*, *gw_luff_angle_mean*, *gw_slew_angle_mean*, *dp_accuracy=0.1*, *gw_telescope_mean=None*)[](../../../../../../source-code/PyBM/marine/machines/MCG30.py)  
Bases: [`mcg30_helper.MCG30MTIPLADDER_Params`](mcg30_helper/index.md#PyBM.marine.machines.MCG30.mcg30_helper.MCG30MTIPLADDER_Params "PyBM.marine.machines.MCG30.mcg30_helper.MCG30MTIPLADDER_Params"), [`MCG30_Nonlinear.MCG30TRANSFER_Nonlinear`](MCG30_Nonlinear/index.md#PyBM.marine.machines.MCG30.MCG30_Nonlinear.MCG30TRANSFER_Nonlinear "PyBM.marine.machines.MCG30.MCG30_Nonlinear.MCG30TRANSFER_Nonlinear")

For the tip ladder the standard deviation limits are reduced by multiplying them with  
- stroke 70%

- velocity 35%
