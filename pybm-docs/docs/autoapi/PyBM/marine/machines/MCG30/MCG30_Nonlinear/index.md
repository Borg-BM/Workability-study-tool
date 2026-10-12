<!-- Source: https://docs.app.barge-master.com/autoapi/PyBM/marine/machines/MCG30/MCG30_Nonlinear/index.html -->

# PyBM.marine.machines.MCG30.MCG30_Nonlinear

MCG System properties to compute workability. Based on the old MATLAB utilization calculations.

References:  
\[1\] M:EngineeringDatabaseMatlab scriptsWorkabilityMCGMCG30_Utilization_Rev5.m \[2\] M:EngineeringDatabaseMatlab scriptsWorkabilityMCGMCG30_SystemParameters_Rev4.m

## Classes

|                                                                                                                                                                       |                                                 |
|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------|
| [`MCG30_Nonlinear`](#PyBM.marine.machines.MCG30.MCG30_Nonlinear.MCG30_Nonlinear "PyBM.marine.machines.MCG30.MCG30_Nonlinear.MCG30_Nonlinear")                         | Base class for MCG 3.0 for workability studies. |
| [`MCG30TRANSFER_Nonlinear`](#PyBM.marine.machines.MCG30.MCG30_Nonlinear.MCG30TRANSFER_Nonlinear "PyBM.marine.machines.MCG30.MCG30_Nonlinear.MCG30TRANSFER_Nonlinear") | Base class for MCG 3.0 for workability studies. |
| [`MCG30LIFTING_Nonlinear`](#PyBM.marine.machines.MCG30.MCG30_Nonlinear.MCG30LIFTING_Nonlinear "PyBM.marine.machines.MCG30.MCG30_Nonlinear.MCG30LIFTING_Nonlinear")    | Base class for MCG 3.0 for workability studies. |

## Module Contents

*class *PyBM.marine.machines.MCG30.MCG30_Nonlinear.MCG30_Nonlinear(*position*, *gw_luff_angle_mean*, *gw_slew_angle_mean*, *dp_accuracy=0.5*, *gw_telescope_mean=None*)[](../../../../../../../source-code/PyBM/marine/machines/MCG30/MCG30_Nonlinear.py)  
Bases: [`PyBM.marine.machines.machine_interface.Machine_Nonlinear`](../../machine_interface/index.md#PyBM.marine.machines.machine_interface.Machine_Nonlinear "PyBM.marine.machines.machine_interface.Machine_Nonlinear"), `abc.ABC`

Base class for MCG 3.0 for workability studies. All parameters are from \[2\]

MCGref* = \[0, 0, 0\]*[](../../../../../../../source-code/PyBM/marine/machines/MCG30/MCG30_Nonlinear.py)  

base[](../../../../../../../source-code/PyBM/marine/machines/MCG30/MCG30_Nonlinear.py)  

gw_luff_angle_mean[](../../../../../../../source-code/PyBM/marine/machines/MCG30/MCG30_Nonlinear.py)  

gw_slew_angle_mean[](../../../../../../../source-code/PyBM/marine/machines/MCG30/MCG30_Nonlinear.py)  

gw_telescope_mean* = None*[](../../../../../../../source-code/PyBM/marine/machines/MCG30/MCG30_Nonlinear.py)  

dp_accuracy* = 0.5*[](../../../../../../../source-code/PyBM/marine/machines/MCG30/MCG30_Nonlinear.py)  

pos_tip[](../../../../../../../source-code/PyBM/marine/machines/MCG30/MCG30_Nonlinear.py)  

POI_NAMES* = \['MCGref', 'base', 'tip'\]*[](../../../../../../../source-code/PyBM/marine/machines/MCG30/MCG30_Nonlinear.py)  

poi_coordinates[](../../../../../../../source-code/PyBM/marine/machines/MCG30/MCG30_Nonlinear.py)  

workability_checks[](../../../../../../../source-code/PyBM/marine/machines/MCG30/MCG30_Nonlinear.py)  

get_POI()[](../../../../../../../source-code/PyBM/marine/machines/MCG30/MCG30_Nonlinear.py)  
Return POI positions w.r.t. RAO definitions.

check_telescope_position(*trace: xarray.Dataset*, *stdevs=3.7*)[](../../../../../../../source-code/PyBM/marine/machines/MCG30/MCG30_Nonlinear.py)  

check_v_telescope(*trace: xarray.Dataset*, *stdevs=3.7*)[](../../../../../../../source-code/PyBM/marine/machines/MCG30/MCG30_Nonlinear.py)  

check_an_luff(*trace: xarray.Dataset*, *stdevs=3.7*)[](../../../../../../../source-code/PyBM/marine/machines/MCG30/MCG30_Nonlinear.py)  

check_max_system_pitch(*trace: xarray.Dataset*, *stdevs=3.7*)[](../../../../../../../source-code/PyBM/marine/machines/MCG30/MCG30_Nonlinear.py)  

check_max_system_roll(*trace: xarray.Dataset*, *stdevs=3.7*)[](../../../../../../../source-code/PyBM/marine/machines/MCG30/MCG30_Nonlinear.py)  

check_horizontal_acc(*trace: xarray.Dataset*, *stdevs=3.7*)[](../../../../../../../source-code/PyBM/marine/machines/MCG30/MCG30_Nonlinear.py)  

check_heave_acc(*trace: xarray.Dataset*, *stdevs=3.7*)[](../../../../../../../source-code/PyBM/marine/machines/MCG30/MCG30_Nonlinear.py)  

check_v_luff_cyl(*trace: xarray.Dataset*, *stdevs=3.7*)[](../../../../../../../source-code/PyBM/marine/machines/MCG30/MCG30_Nonlinear.py)  

check_v_slew(*trace: xarray.Dataset*, *stdevs=3.7*)[](../../../../../../../source-code/PyBM/marine/machines/MCG30/MCG30_Nonlinear.py)  

check_duty_cycle(*trace: xarray.Dataset*, *stdevs=3.7*)[](../../../../../../../source-code/PyBM/marine/machines/MCG30/MCG30_Nonlinear.py)  

translate_telescope(*trace: xarray.DataArray*)[](../../../../../../../source-code/PyBM/marine/machines/MCG30/MCG30_Nonlinear.py)  

translate_an_luff_world(*trace: xarray.DataArray*)[](../../../../../../../source-code/PyBM/marine/machines/MCG30/MCG30_Nonlinear.py)  

translate_an_luff(*trace: xarray.DataArray*)[](../../../../../../../source-code/PyBM/marine/machines/MCG30/MCG30_Nonlinear.py)  

translate_an_slew_world(*trace: xarray.DataArray*)[](../../../../../../../source-code/PyBM/marine/machines/MCG30/MCG30_Nonlinear.py)  

translate_an_slew(*trace: xarray.DataArray*)[](../../../../../../../source-code/PyBM/marine/machines/MCG30/MCG30_Nonlinear.py)  

translate_horizontal(*trace: xarray.DataArray*)[](../../../../../../../source-code/PyBM/marine/machines/MCG30/MCG30_Nonlinear.py)  

translate_luf_stroke(*trace: xarray.DataArray*)[](../../../../../../../source-code/PyBM/marine/machines/MCG30/MCG30_Nonlinear.py)  

get_workability_limit(*trace*, *\*\*kwargs*)[](../../../../../../../source-code/PyBM/marine/machines/MCG30/MCG30_Nonlinear.py)  
Get workability limits for the machine. Returns an xarray with Hs limits. (assumes linear scalability of time trace) :param trace: trace to calculate utilizations for. :type trace: xarray.Dataset

plot(*axs: matplotlib.axes.Axes = None*, *vessel: [PyBM.utils.data_classes.VesselDimensions](../../../../utils/data_classes/index.md#PyBM.utils.data_classes.VesselDimensions "PyBM.utils.data_classes.VesselDimensions") = None*, *rao_origin=None*)[](../../../../../../../source-code/PyBM/marine/machines/MCG30/MCG30_Nonlinear.py)  
Plots the MCG in 3 dimensions with either a general vessel or a vessel with given dimensions.

Parameters:  
- **axs** (*Axes*) – Axes to plot onto.

- **vessel** ([*VesselDimensions*](../../../../index.md#PyBM.VesselDimensions "PyBM.VesselDimensions")) – vessel dimensions to plot on figure

- **rao_origin** (*np.array*) – rao origin position \[x,y,z\]

&nbsp;

*class *PyBM.marine.machines.MCG30.MCG30_Nonlinear.MCG30TRANSFER_Nonlinear(*position*, *gw_luff_angle_mean*, *gw_slew_angle_mean*, *dp_accuracy=0.1*, *gw_telescope_mean=None*)[](../../../../../../../source-code/PyBM/marine/machines/MCG30/MCG30_Nonlinear.py)  
Bases: [`MCG30_Nonlinear`](#PyBM.marine.machines.MCG30.MCG30_Nonlinear.MCG30_Nonlinear "PyBM.marine.machines.MCG30.MCG30_Nonlinear.MCG30_Nonlinear"), `abc.ABC`

Base class for MCG 3.0 for workability studies. All parameters are from \[2\]

check_an_slew_world(*trace: xarray.Dataset*, *stdevs=3.7*)[](../../../../../../../source-code/PyBM/marine/machines/MCG30/MCG30_Nonlinear.py)  

check_an_luff_world(*trace: xarray.Dataset*, *stdevs=3.7*)[](../../../../../../../source-code/PyBM/marine/machines/MCG30/MCG30_Nonlinear.py)  

&nbsp;

*class *PyBM.marine.machines.MCG30.MCG30_Nonlinear.MCG30LIFTING_Nonlinear(*position*, *gw_luff_angle_mean*, *gw_slew_angle_mean*, *dp_accuracy=0.1*, *gw_telescope_mean=None*)[](../../../../../../../source-code/PyBM/marine/machines/MCG30/MCG30_Nonlinear.py)  
Bases: [`MCG30_Nonlinear`](#PyBM.marine.machines.MCG30.MCG30_Nonlinear.MCG30_Nonlinear "PyBM.marine.machines.MCG30.MCG30_Nonlinear.MCG30_Nonlinear"), `abc.ABC`

Base class for MCG 3.0 for workability studies. All parameters are from \[2\]

lifting_radius[](../../../../../../../source-code/PyBM/marine/machines/MCG30/MCG30_Nonlinear.py)  

check_v_sys_roll(*trace: xarray.Dataset*, *stdevs=3.7*)[](../../../../../../../source-code/PyBM/marine/machines/MCG30/MCG30_Nonlinear.py)  

check_v_sys_pitch(*trace: xarray.Dataset*, *stdevs=3.7*)[](../../../../../../../source-code/PyBM/marine/machines/MCG30/MCG30_Nonlinear.py)  

check_v_heave(*trace: xarray.Dataset*, *stdevs=3.7*)[](../../../../../../../source-code/PyBM/marine/machines/MCG30/MCG30_Nonlinear.py)  

check_v_tip(*trace: xarray.Dataset*, *stdevs=3.7*)[](../../../../../../../source-code/PyBM/marine/machines/MCG30/MCG30_Nonlinear.py)  
