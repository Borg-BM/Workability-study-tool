<!-- Source: https://docs.app.barge-master.com/autoapi/PyBM/marine/machines/MCG30/MCG30_Linear/index.html -->

# PyBM.marine.machines.MCG30.MCG30_Linear

Linearized MCG. Based on the same limits as MCG30.py but with linearized equations according to first-order taylor expansions.

References \[1\] M:EngineeringR&D Projects# PyBMEngineeringLinearization of the MCG DOFS.pptx

## Classes

|                                                                                                                                                        |                                                 |
|--------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------|
| [`MCG30_Linear`](#PyBM.marine.machines.MCG30.MCG30_Linear.MCG30_Linear "PyBM.marine.machines.MCG30.MCG30_Linear.MCG30_Linear")                         | Base class for MCG 3.0 for workability studies. |
| [`MCG30TRANSFER_Linear`](#PyBM.marine.machines.MCG30.MCG30_Linear.MCG30TRANSFER_Linear "PyBM.marine.machines.MCG30.MCG30_Linear.MCG30TRANSFER_Linear") | Base class for MCG 3.0 for workability studies. |
| [`MCG30LIFTING_Linear`](#PyBM.marine.machines.MCG30.MCG30_Linear.MCG30LIFTING_Linear "PyBM.marine.machines.MCG30.MCG30_Linear.MCG30LIFTING_Linear")    | Base class for MCG 3.0 for workability studies. |

## Module Contents

*class *PyBM.marine.machines.MCG30.MCG30_Linear.MCG30_Linear(*position*, *gw_luff_angle_mean*, *gw_slew_angle_mean*, *dp_accuracy=0.5*, *gw_telescope_mean=None*)[](../../../../../../../source-code/PyBM/marine/machines/MCG30/MCG30_Linear.py)  
Bases: [`PyBM.marine.machines.machine_interface.Machine_Linear`](../../machine_interface/index.md#PyBM.marine.machines.machine_interface.Machine_Linear "PyBM.marine.machines.machine_interface.Machine_Linear"), `abc.ABC`

Base class for MCG 3.0 for workability studies. All parameters are from \[2\]

MCGref* = \[0, 0, 0\]*[](../../../../../../../source-code/PyBM/marine/machines/MCG30/MCG30_Linear.py)  

base[](../../../../../../../source-code/PyBM/marine/machines/MCG30/MCG30_Linear.py)  

gw_luff_angle_mean[](../../../../../../../source-code/PyBM/marine/machines/MCG30/MCG30_Linear.py)  

gw_slew_angle_mean[](../../../../../../../source-code/PyBM/marine/machines/MCG30/MCG30_Linear.py)  

gw_telescope_mean* = None*[](../../../../../../../source-code/PyBM/marine/machines/MCG30/MCG30_Linear.py)  

dp_accuracy* = 0.5*[](../../../../../../../source-code/PyBM/marine/machines/MCG30/MCG30_Linear.py)  

pos_tip[](../../../../../../../source-code/PyBM/marine/machines/MCG30/MCG30_Linear.py)  

POI_NAMES* = \['MCGref', 'base', 'tip'\]*[](../../../../../../../source-code/PyBM/marine/machines/MCG30/MCG30_Linear.py)  

poi_coordinates[](../../../../../../../source-code/PyBM/marine/machines/MCG30/MCG30_Linear.py)  

dof_partials[](../../../../../../../source-code/PyBM/marine/machines/MCG30/MCG30_Linear.py)  

workability_checks[](../../../../../../../source-code/PyBM/marine/machines/MCG30/MCG30_Linear.py)  

get_POI()[](../../../../../../../source-code/PyBM/marine/machines/MCG30/MCG30_Linear.py)  
Return POI positions w.r.t. RAO definitions.

translate_linear_dof(*rao*, *name*, *partials*)[](../../../../../../../source-code/PyBM/marine/machines/MCG30/MCG30_Linear.py)  

apply_machine_dofs(*rao*)[](../../../../../../../source-code/PyBM/marine/machines/MCG30/MCG30_Linear.py)  

check_linearized_limit(*limit*, *DOF*, *POI*, *order*)[](../../../../../../../source-code/PyBM/marine/machines/MCG30/MCG30_Linear.py)  

check_telescope_position(*mpe_at_poi*)[](../../../../../../../source-code/PyBM/marine/machines/MCG30/MCG30_Linear.py)  

check_an_luff(*mpe_at_poi*)[](../../../../../../../source-code/PyBM/marine/machines/MCG30/MCG30_Linear.py)  

check_horizontal_acc(*mpe_at_poi*)[](../../../../../../../source-code/PyBM/marine/machines/MCG30/MCG30_Linear.py)  

get_workability_limit(*motion_at_poi*, *\*\*kwargs*)[](../../../../../../../source-code/PyBM/marine/machines/MCG30/MCG30_Linear.py)  

&nbsp;

*class *PyBM.marine.machines.MCG30.MCG30_Linear.MCG30TRANSFER_Linear(*position*, *gw_luff_angle_mean*, *gw_slew_angle_mean*, *dp_accuracy=0.1*, *gw_telescope_mean=None*)[](../../../../../../../source-code/PyBM/marine/machines/MCG30/MCG30_Linear.py)  
Bases: [`MCG30_Linear`](#PyBM.marine.machines.MCG30.MCG30_Linear.MCG30_Linear "PyBM.marine.machines.MCG30.MCG30_Linear.MCG30_Linear"), `abc.ABC`

Base class for MCG 3.0 for workability studies. All parameters are from \[2\]

check_an_luff_world(*mpe_at_poi*)[](../../../../../../../source-code/PyBM/marine/machines/MCG30/MCG30_Linear.py)  

&nbsp;

*class *PyBM.marine.machines.MCG30.MCG30_Linear.MCG30LIFTING_Linear(*position*, *gw_luff_angle_mean*, *gw_slew_angle_mean*, *dp_accuracy=0.1*, *gw_telescope_mean=None*)[](../../../../../../../source-code/PyBM/marine/machines/MCG30/MCG30_Linear.py)  
Bases: [`MCG30_Linear`](#PyBM.marine.machines.MCG30.MCG30_Linear.MCG30_Linear "PyBM.marine.machines.MCG30.MCG30_Linear.MCG30_Linear"), `abc.ABC`

Base class for MCG 3.0 for workability studies. All parameters are from \[2\]

lifting_radius[](../../../../../../../source-code/PyBM/marine/machines/MCG30/MCG30_Linear.py)  
