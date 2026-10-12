<!-- Source: https://docs.app.barge-master.com/autoapi/PyBM/marine/machines/HeavyFeeder/index.html -->

# PyBM.marine.machines.HeavyFeeder

Heavy Feeder class to compute workability

References:

> \[1\] TWD-NL-2021-512-D-010-REV-2, General Arrangement CYLINDER NUMBERING \[2\] NL002692-02-50-2000-HYD-0001-RAF Hydraulic diagram Roll Pitch Cylinder assembly_AB

## Classes

|                                                                                                               |                                                                  |
|---------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------|
| [`HeavyFeeder`](#PyBM.marine.machines.HeavyFeeder.HeavyFeeder "PyBM.marine.machines.HeavyFeeder.HeavyFeeder") | Helper class that provides a standard way to create an ABC using |

## Module Contents

*class *PyBM.marine.machines.HeavyFeeder.HeavyFeeder(*position*, *orientation*, *comp_point=\[0, 0, 0\]*)[](../../../../../../source-code/PyBM/marine/machines/HeavyFeeder.py)  
Bases: [`PyBM.marine.machines.machine_interface.Machine_Linear`](../machine_interface/index.md#PyBM.marine.machines.machine_interface.Machine_Linear "PyBM.marine.machines.machine_interface.Machine_Linear")

Helper class that provides a standard way to create an ABC using inheritance.

cyl_arm_roll* = 10.409*[](../../../../../../source-code/PyBM/marine/machines/HeavyFeeder.py)  

cyl_arm_pitch* = 7.327*[](../../../../../../source-code/PyBM/marine/machines/HeavyFeeder.py)  

tds_arm_roll* = 11.43*[](../../../../../../source-code/PyBM/marine/machines/HeavyFeeder.py)  

tds_arm_pitch* = 8*[](../../../../../../source-code/PyBM/marine/machines/HeavyFeeder.py)  

cb_to_tbic_top* = 6.42*[](../../../../../../source-code/PyBM/marine/machines/HeavyFeeder.py)  

vmax* = 0.455*[](../../../../../../source-code/PyBM/marine/machines/HeavyFeeder.py)  

bore* = 0.47*[](../../../../../../source-code/PyBM/marine/machines/HeavyFeeder.py)  

rod* = 0.23*[](../../../../../../source-code/PyBM/marine/machines/HeavyFeeder.py)  

stroke* = 1.1*[](../../../../../../source-code/PyBM/marine/machines/HeavyFeeder.py)  

p_hpu* = 31500000.0*[](../../../../../../source-code/PyBM/marine/machines/HeavyFeeder.py)  

p_hold_bot* = 35000000.0*[](../../../../../../source-code/PyBM/marine/machines/HeavyFeeder.py)  

p_hold_rod* = 42000000.0*[](../../../../../../source-code/PyBM/marine/machines/HeavyFeeder.py)  

comp_point_max_horizontal_motion* = 2.0*[](../../../../../../source-code/PyBM/marine/machines/HeavyFeeder.py)  

cylinder[](../../../../../../source-code/PyBM/marine/machines/HeavyFeeder.py)  

CYLINDER_NAMES* = \['c1', 'c2'\]*[](../../../../../../source-code/PyBM/marine/machines/HeavyFeeder.py)  

N_CYLINDERS* = 2*[](../../../../../../source-code/PyBM/marine/machines/HeavyFeeder.py)  

POI_NAMES* = \['central_bearing', 'comp_point'\]*[](../../../../../../source-code/PyBM/marine/machines/HeavyFeeder.py)  

*property *c1[](../../../../../../source-code/PyBM/marine/machines/HeavyFeeder.py)  

*property *c2[](../../../../../../source-code/PyBM/marine/machines/HeavyFeeder.py)  

cylinder_coordinates[](../../../../../../source-code/PyBM/marine/machines/HeavyFeeder.py)  

comp_point_wrt_cb[](../../../../../../source-code/PyBM/marine/machines/HeavyFeeder.py)  

comp_point[](../../../../../../source-code/PyBM/marine/machines/HeavyFeeder.py)  

workability_checks[](../../../../../../source-code/PyBM/marine/machines/HeavyFeeder.py)  

get_POI()[](../../../../../../source-code/PyBM/marine/machines/HeavyFeeder.py)  
Return cylinder positions w.r.t. RAO definitions.

apply_machine_dofs(*rao*)[](../../../../../../source-code/PyBM/marine/machines/HeavyFeeder.py)  

check_stroke_limit(*motion_at_poi*)[](../../../../../../source-code/PyBM/marine/machines/HeavyFeeder.py)  

check_cylinder_velocity_limit(*motion_at_poi*)[](../../../../../../source-code/PyBM/marine/machines/HeavyFeeder.py)  

check_horizontal_motion_no_comp(*motion_at_poi*)[](../../../../../../source-code/PyBM/marine/machines/HeavyFeeder.py)  

check_horizontal_motion(*motion_at_poi*)[](../../../../../../source-code/PyBM/marine/machines/HeavyFeeder.py)  

plot(*axs: matplotlib.axes.Axes = None*)[](../../../../../../source-code/PyBM/marine/machines/HeavyFeeder.py)  
