<!-- Source: https://docs.app.barge-master.com/autoapi/PyBM/marine/machines/index.html -->

# PyBM.marine.machines

## Submodules

- [PyBM.marine.machines.HeavyFeeder](HeavyFeeder/index.md)
- [PyBM.marine.machines.HeavyFeederSurgeSway](HeavyFeederSurgeSway/index.md)
- [PyBM.marine.machines.MCG30](MCG30/index.md)
- [PyBM.marine.machines.T700](T700/index.md)
- [PyBM.marine.machines.machine_interface](machine_interface/index.md)

## Classes

|                                                                                                                              |                                                                  |
|------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------|
| [`HeavyFeeder`](#PyBM.marine.machines.HeavyFeeder "PyBM.marine.machines.HeavyFeeder")                                        | Helper class that provides a standard way to create an ABC using |
| [`HeavyFeederSurgeSway`](#PyBM.marine.machines.HeavyFeederSurgeSway "PyBM.marine.machines.HeavyFeederSurgeSway")             | Helper class that provides a standard way to create an ABC using |
| [`Machine_Linear`](#PyBM.marine.machines.Machine_Linear "PyBM.marine.machines.Machine_Linear")                               | Helper class that provides a standard way to create an ABC using |
| [`Machine_Nonlinear`](#PyBM.marine.machines.Machine_Nonlinear "PyBM.marine.machines.Machine_Nonlinear")                      | Helper class that provides a standard way to create an ABC using |
| [`MCG30LHIGHLOAD_Linear`](#PyBM.marine.machines.MCG30LHIGHLOAD_Linear "PyBM.marine.machines.MCG30LHIGHLOAD_Linear")          | Helper class that provides a standard way to create an ABC using |
| [`MCG30LHIGHLOAD_Nonlinear`](#PyBM.marine.machines.MCG30LHIGHLOAD_Nonlinear "PyBM.marine.machines.MCG30LHIGHLOAD_Nonlinear") | Helper class that provides a standard way to create an ABC using |
| [`MCG30LLOWLOAD_Linear`](#PyBM.marine.machines.MCG30LLOWLOAD_Linear "PyBM.marine.machines.MCG30LLOWLOAD_Linear")             | Helper class that provides a standard way to create an ABC using |
| [`MCG30LLOWLOAD_Nonlinear`](#PyBM.marine.machines.MCG30LLOWLOAD_Nonlinear "PyBM.marine.machines.MCG30LLOWLOAD_Nonlinear")    | Helper class that provides a standard way to create an ABC using |
| [`MCG30LTRANSFER_Linear`](#PyBM.marine.machines.MCG30LTRANSFER_Linear "PyBM.marine.machines.MCG30LTRANSFER_Linear")          | Helper class that provides a standard way to create an ABC using |
| [`MCG30LTRANSFER_Nonlinear`](#PyBM.marine.machines.MCG30LTRANSFER_Nonlinear "PyBM.marine.machines.MCG30LTRANSFER_Nonlinear") | Helper class that provides a standard way to create an ABC using |
| [`MCG30MHIGHLOAD_Linear`](#PyBM.marine.machines.MCG30MHIGHLOAD_Linear "PyBM.marine.machines.MCG30MHIGHLOAD_Linear")          | Helper class that provides a standard way to create an ABC using |
| [`MCG30MHIGHLOAD_Nonlinear`](#PyBM.marine.machines.MCG30MHIGHLOAD_Nonlinear "PyBM.marine.machines.MCG30MHIGHLOAD_Nonlinear") | Helper class that provides a standard way to create an ABC using |
| [`MCG30MLOWLOAD_Linear`](#PyBM.marine.machines.MCG30MLOWLOAD_Linear "PyBM.marine.machines.MCG30MLOWLOAD_Linear")             | Helper class that provides a standard way to create an ABC using |
| [`MCG30MLOWLOAD_Nonlinear`](#PyBM.marine.machines.MCG30MLOWLOAD_Nonlinear "PyBM.marine.machines.MCG30MLOWLOAD_Nonlinear")    | Helper class that provides a standard way to create an ABC using |
| [`MCG30MTRANSFER_Linear`](#PyBM.marine.machines.MCG30MTRANSFER_Linear "PyBM.marine.machines.MCG30MTRANSFER_Linear")          | Helper class that provides a standard way to create an ABC using |
| [`MCG30MTRANSFER_Nonlinear`](#PyBM.marine.machines.MCG30MTRANSFER_Nonlinear "PyBM.marine.machines.MCG30MTRANSFER_Nonlinear") | Helper class that provides a standard way to create an ABC using |
| [`T700`](#PyBM.marine.machines.T700 "PyBM.marine.machines.T700")                                                             | Helper class that provides a standard way to create an ABC using |

## Package Contents

*class *PyBM.marine.machines.HeavyFeeder(*position*, *orientation*, *comp_point=\[0, 0, 0\]*)[](../../../../../source-code/PyBM/marine/machines/HeavyFeeder.py)  
Bases: [`PyBM.marine.machines.machine_interface.Machine_Linear`](machine_interface/index.md#PyBM.marine.machines.machine_interface.Machine_Linear "PyBM.marine.machines.machine_interface.Machine_Linear")

Helper class that provides a standard way to create an ABC using inheritance.

cyl_arm_roll* = 10.409*  

cyl_arm_pitch* = 7.327*  

tds_arm_roll* = 11.43*  

tds_arm_pitch* = 8*  

cb_to_tbic_top* = 6.42*  

vmax* = 0.455*  

bore* = 0.47*  

rod* = 0.23*  

stroke* = 1.1*  

p_hpu* = 31500000.0*  

p_hold_bot* = 35000000.0*  

p_hold_rod* = 42000000.0*  

comp_point_max_horizontal_motion* = 2.0*  

cylinder  

CYLINDER_NAMES* = \['c1', 'c2'\]*  

N_CYLINDERS* = 2*  

POI_NAMES* = \['central_bearing', 'comp_point'\]*  

*property *c1  

*property *c2  

cylinder_coordinates  

comp_point_wrt_cb  

comp_point  

workability_checks  

get_POI()[](../../../../../source-code/PyBM/marine/machines/HeavyFeeder.py)  
Return cylinder positions w.r.t. RAO definitions.

apply_machine_dofs(*rao*)[](../../../../../source-code/PyBM/marine/machines/HeavyFeeder.py)  

check_stroke_limit(*motion_at_poi*)[](../../../../../source-code/PyBM/marine/machines/HeavyFeeder.py)  

check_cylinder_velocity_limit(*motion_at_poi*)[](../../../../../source-code/PyBM/marine/machines/HeavyFeeder.py)  

check_horizontal_motion_no_comp(*motion_at_poi*)[](../../../../../source-code/PyBM/marine/machines/HeavyFeeder.py)  

check_horizontal_motion(*motion_at_poi*)[](../../../../../source-code/PyBM/marine/machines/HeavyFeeder.py)  

plot(*axs: matplotlib.axes.Axes = None*)[](../../../../../source-code/PyBM/marine/machines/HeavyFeeder.py)  

&nbsp;

*class *PyBM.marine.machines.HeavyFeederSurgeSway(*position*, *orientation*, *comp_point=\[0, 0, 0\]*)[](../../../../../source-code/PyBM/marine/machines/HeavyFeederSurgeSway.py)  
Bases: [`PyBM.marine.machines.HeavyFeeder.HeavyFeeder`](HeavyFeeder/index.md#PyBM.marine.machines.HeavyFeeder.HeavyFeeder "PyBM.marine.machines.HeavyFeeder.HeavyFeeder")

Helper class that provides a standard way to create an ABC using inheritance.

workability_checks  

get_POI()[](../../../../../source-code/PyBM/marine/machines/HeavyFeederSurgeSway.py)  
Return cylinder positions w.r.t. RAO definitions.

apply_machine_dofs(*rao*)[](../../../../../source-code/PyBM/marine/machines/HeavyFeederSurgeSway.py)  

check_stroke_limit(*motion_at_poi*)[](../../../../../source-code/PyBM/marine/machines/HeavyFeederSurgeSway.py)  

&nbsp;

*class *PyBM.marine.machines.Machine_Linear(*position*, *orientation*)[](../../../../../source-code/PyBM/marine/machines/machine_interface.py)  
Bases: `abc.ABC`

Helper class that provides a standard way to create an ABC using inheritance.

pos  

orient  

rotation  

apply_transform(*point: numpy.array*) → numpy.array[](../../../../../source-code/PyBM/marine/machines/machine_interface.py)  
Apply rotation then translation to 3D point

Parameters:  
**point** (*np.array*) – 3D vector \[x,y,z\]

Returns:  
Transformed position

Return type:  
np.array

get_rao_at_poi(*rao*) → [PyBM.marine.motion_analysis.MotionRAO.MotionRAO](../motion_analysis/MotionRAO/index.md#PyBM.marine.motion_analysis.MotionRAO.MotionRAO "PyBM.marine.motion_analysis.MotionRAO.MotionRAO")[](../../../../../source-code/PyBM/marine/machines/machine_interface.py)  
Get the Motion RAOs at the POI

*abstractmethod *get_POI() → dict[](../../../../../source-code/PyBM/marine/machines/machine_interface.py)  

apply_machine_dofs(*rao*) → [PyBM.marine.motion_analysis.MotionRAO.MotionRAO](../motion_analysis/MotionRAO/index.md#PyBM.marine.motion_analysis.MotionRAO.MotionRAO "PyBM.marine.motion_analysis.MotionRAO.MotionRAO")[](../../../../../source-code/PyBM/marine/machines/machine_interface.py)  

get_workability_limit(*motion_at_poi*, *\*\*kwargs*)[](../../../../../source-code/PyBM/marine/machines/machine_interface.py)  

\_\_str\_\_() → str[](../../../../../source-code/PyBM/marine/machines/machine_interface.py)  

&nbsp;

*class *PyBM.marine.machines.Machine_Nonlinear(*position*, *orientation*)[](../../../../../source-code/PyBM/marine/machines/machine_interface.py)  
Bases: `abc.ABC`

Helper class that provides a standard way to create an ABC using inheritance.

pos  

orient  

rotation  

apply_transform(*point: numpy.array*) → numpy.array[](../../../../../source-code/PyBM/marine/machines/machine_interface.py)  
Apply rotation then translation to 3D point

Parameters:  
**point** (*np.array*) – 3D vector \[x,y,z\]

Returns:  
Transformed position

Return type:  
np.array

*abstractmethod *get_POI() → dict[](../../../../../source-code/PyBM/marine/machines/machine_interface.py)  

&nbsp;

*class *PyBM.marine.machines.MCG30LHIGHLOAD_Linear(*position*, *gw_luff_angle_mean*, *gw_slew_angle_mean*, *dp_accuracy=0.1*, *gw_telescope_mean=None*)[](../../../../../source-code/PyBM/marine/machines/MCG30.py)  
Bases: `mcg30_helper.MCG30LHIGHLOAD_Params`, `MCG30_Linear.MCG30LIFTING_Linear`

Helper class that provides a standard way to create an ABC using inheritance.

&nbsp;

*class *PyBM.marine.machines.MCG30LHIGHLOAD_Nonlinear(*position*, *gw_luff_angle_mean*, *gw_slew_angle_mean*, *dp_accuracy=0.1*, *gw_telescope_mean=None*)[](../../../../../source-code/PyBM/marine/machines/MCG30.py)  
Bases: `mcg30_helper.MCG30LHIGHLOAD_Params`, `MCG30_Nonlinear.MCG30LIFTING_Nonlinear`

Helper class that provides a standard way to create an ABC using inheritance.

&nbsp;

*class *PyBM.marine.machines.MCG30LLOWLOAD_Linear(*position*, *gw_luff_angle_mean*, *gw_slew_angle_mean*, *dp_accuracy=0.1*, *gw_telescope_mean=None*)[](../../../../../source-code/PyBM/marine/machines/MCG30.py)  
Bases: `mcg30_helper.MCG30LLOWLOAD_Params`, `MCG30_Linear.MCG30LIFTING_Linear`

Helper class that provides a standard way to create an ABC using inheritance.

&nbsp;

*class *PyBM.marine.machines.MCG30LLOWLOAD_Nonlinear(*position*, *gw_luff_angle_mean*, *gw_slew_angle_mean*, *dp_accuracy=0.1*, *gw_telescope_mean=None*)[](../../../../../source-code/PyBM/marine/machines/MCG30.py)  
Bases: `mcg30_helper.MCG30LLOWLOAD_Params`, `MCG30_Nonlinear.MCG30LIFTING_Nonlinear`

Helper class that provides a standard way to create an ABC using inheritance.

&nbsp;

*class *PyBM.marine.machines.MCG30LTRANSFER_Linear(*position*, *gw_luff_angle_mean*, *gw_slew_angle_mean*, *dp_accuracy=0.1*, *gw_telescope_mean=None*)[](../../../../../source-code/PyBM/marine/machines/MCG30.py)  
Bases: `mcg30_helper.MCG30LTRANSFER_Params`, `MCG30_Linear.MCG30TRANSFER_Linear`

Helper class that provides a standard way to create an ABC using inheritance.

&nbsp;

*class *PyBM.marine.machines.MCG30LTRANSFER_Nonlinear(*position*, *gw_luff_angle_mean*, *gw_slew_angle_mean*, *dp_accuracy=0.1*, *gw_telescope_mean=None*)[](../../../../../source-code/PyBM/marine/machines/MCG30.py)  
Bases: `mcg30_helper.MCG30LTRANSFER_Params`, `MCG30_Nonlinear.MCG30TRANSFER_Nonlinear`

Helper class that provides a standard way to create an ABC using inheritance.

&nbsp;

*class *PyBM.marine.machines.MCG30MHIGHLOAD_Linear(*position*, *gw_luff_angle_mean*, *gw_slew_angle_mean*, *dp_accuracy=0.1*, *gw_telescope_mean=None*)[](../../../../../source-code/PyBM/marine/machines/MCG30.py)  
Bases: `mcg30_helper.MCG30MHIGHLOAD_Params`, `MCG30_Linear.MCG30LIFTING_Linear`

Helper class that provides a standard way to create an ABC using inheritance.

&nbsp;

*class *PyBM.marine.machines.MCG30MHIGHLOAD_Nonlinear(*position*, *gw_luff_angle_mean*, *gw_slew_angle_mean*, *dp_accuracy=0.1*, *gw_telescope_mean=None*)[](../../../../../source-code/PyBM/marine/machines/MCG30.py)  
Bases: `mcg30_helper.MCG30MHIGHLOAD_Params`, `MCG30_Nonlinear.MCG30LIFTING_Nonlinear`

Helper class that provides a standard way to create an ABC using inheritance.

&nbsp;

*class *PyBM.marine.machines.MCG30MLOWLOAD_Linear(*position*, *gw_luff_angle_mean*, *gw_slew_angle_mean*, *dp_accuracy=0.1*, *gw_telescope_mean=None*)[](../../../../../source-code/PyBM/marine/machines/MCG30.py)  
Bases: `mcg30_helper.MCG30MLOWLOAD_Params`, `MCG30_Linear.MCG30LIFTING_Linear`

Helper class that provides a standard way to create an ABC using inheritance.

&nbsp;

*class *PyBM.marine.machines.MCG30MLOWLOAD_Nonlinear(*position*, *gw_luff_angle_mean*, *gw_slew_angle_mean*, *dp_accuracy=0.1*, *gw_telescope_mean=None*)[](../../../../../source-code/PyBM/marine/machines/MCG30.py)  
Bases: `mcg30_helper.MCG30MLOWLOAD_Params`, `MCG30_Nonlinear.MCG30LIFTING_Nonlinear`

Helper class that provides a standard way to create an ABC using inheritance.

&nbsp;

*class *PyBM.marine.machines.MCG30MTRANSFER_Linear(*position*, *gw_luff_angle_mean*, *gw_slew_angle_mean*, *dp_accuracy=0.1*, *gw_telescope_mean=None*)[](../../../../../source-code/PyBM/marine/machines/MCG30.py)  
Bases: `mcg30_helper.MCG30MTRANSFER_Params`, `MCG30_Linear.MCG30TRANSFER_Linear`

Helper class that provides a standard way to create an ABC using inheritance.

&nbsp;

*class *PyBM.marine.machines.MCG30MTRANSFER_Nonlinear(*position*, *gw_luff_angle_mean*, *gw_slew_angle_mean*, *dp_accuracy=0.1*, *gw_telescope_mean=None*)[](../../../../../source-code/PyBM/marine/machines/MCG30.py)  
Bases: `mcg30_helper.MCG30MTRANSFER_Params`, `MCG30_Nonlinear.MCG30TRANSFER_Nonlinear`

Helper class that provides a standard way to create an ABC using inheritance.

&nbsp;

*class *PyBM.marine.machines.T700(*position*, *orientation*, *P_passive=35000000.0*)[](../../../../../source-code/PyBM/marine/machines/T700.py)  
Bases: [`PyBM.marine.machines.machine_interface.Machine_Linear`](machine_interface/index.md#PyBM.marine.machines.machine_interface.Machine_Linear "PyBM.marine.machines.machine_interface.Machine_Linear")

Helper class that provides a standard way to create an ABC using inheritance.

cd* = 13.8*  

vmax* = 0.736*  

vmax_center* = 0.44*  

stroke* = 2.2*  

max_flow* = 0.044*  

bore* = 0.42*  

rod* = 0.33*  

rod_center* = 0.26*  

cylinder  

CYLINDER_NAMES* = \['c1', 'c2', 'c3'\]*  

N_CYLINDERS* = 3*  

POI_NAMES* = \['center', 'c1', 'c2', 'c3'\]*  

*property *h  

*property *c1  

*property *c2  

*property *c3  

P_passive* = 35000000.0*  

cylinder_coordinates  

workability_checks  

get_POI()[](../../../../../source-code/PyBM/marine/machines/T700.py)  
Return cylinder positions w.r.t. RAO definitions.

check_stroke_limit(*motion_at_poi*)[](../../../../../source-code/PyBM/marine/machines/T700.py)  

check_cylinder_velocity_limit(*motion_at_poi*)[](../../../../../source-code/PyBM/marine/machines/T700.py)  

check_platform_velocity_limit(*motion_at_poi*)[](../../../../../source-code/PyBM/marine/machines/T700.py)  

compute_cylinder_forces(*Fz*, *Mx*, *My*)[](../../../../../source-code/PyBM/marine/machines/T700.py)  

plot(*axs: matplotlib.axes.Axes = None*)[](../../../../../source-code/PyBM/marine/machines/T700.py)  
