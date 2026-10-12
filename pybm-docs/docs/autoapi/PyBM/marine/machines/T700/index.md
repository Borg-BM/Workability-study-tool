<!-- Source: https://docs.app.barge-master.com/autoapi/PyBM/marine/machines/T700/index.html -->

# PyBM.marine.machines.T700

T700 System properties to compute workability

References:  
\[1\] RA53967897_AC_1_GEZ_001 \[2\] TWD-2015-006-D-100-REV-1, FOUNDATION -GENERAL ARRANGEMENT \[3\] T700_SystemParameters_Rev0

## Attributes

|                                                                         |     |
|-------------------------------------------------------------------------|-----|
| [`pos`](#PyBM.marine.machines.T700.pos "PyBM.marine.machines.T700.pos") |     |

## Classes

|                                                                            |                                                                  |
|----------------------------------------------------------------------------|------------------------------------------------------------------|
| [`T700`](#PyBM.marine.machines.T700.T700 "PyBM.marine.machines.T700.T700") | Helper class that provides a standard way to create an ABC using |

## Module Contents

*class *PyBM.marine.machines.T700.T700(*position*, *orientation*, *P_passive=35000000.0*)[](../../../../../../source-code/PyBM/marine/machines/T700.py)  
Bases: [`PyBM.marine.machines.machine_interface.Machine_Linear`](../machine_interface/index.md#PyBM.marine.machines.machine_interface.Machine_Linear "PyBM.marine.machines.machine_interface.Machine_Linear")

Helper class that provides a standard way to create an ABC using inheritance.

cd* = 13.8*[](../../../../../../source-code/PyBM/marine/machines/T700.py)  

vmax* = 0.736*[](../../../../../../source-code/PyBM/marine/machines/T700.py)  

vmax_center* = 0.44*[](../../../../../../source-code/PyBM/marine/machines/T700.py)  

stroke* = 2.2*[](../../../../../../source-code/PyBM/marine/machines/T700.py)  

max_flow* = 0.044*[](../../../../../../source-code/PyBM/marine/machines/T700.py)  

bore* = 0.42*[](../../../../../../source-code/PyBM/marine/machines/T700.py)  

rod* = 0.33*[](../../../../../../source-code/PyBM/marine/machines/T700.py)  

rod_center* = 0.26*[](../../../../../../source-code/PyBM/marine/machines/T700.py)  

cylinder[](../../../../../../source-code/PyBM/marine/machines/T700.py)  

CYLINDER_NAMES* = \['c1', 'c2', 'c3'\]*[](../../../../../../source-code/PyBM/marine/machines/T700.py)  

N_CYLINDERS* = 3*[](../../../../../../source-code/PyBM/marine/machines/T700.py)  

POI_NAMES* = \['center', 'c1', 'c2', 'c3'\]*[](../../../../../../source-code/PyBM/marine/machines/T700.py)  

*property *h[](../../../../../../source-code/PyBM/marine/machines/T700.py)  

*property *c1[](../../../../../../source-code/PyBM/marine/machines/T700.py)  

*property *c2[](../../../../../../source-code/PyBM/marine/machines/T700.py)  

*property *c3[](../../../../../../source-code/PyBM/marine/machines/T700.py)  

P_passive* = 35000000.0*[](../../../../../../source-code/PyBM/marine/machines/T700.py)  

cylinder_coordinates[](../../../../../../source-code/PyBM/marine/machines/T700.py)  

workability_checks[](../../../../../../source-code/PyBM/marine/machines/T700.py)  

get_POI()[](../../../../../../source-code/PyBM/marine/machines/T700.py)  
Return cylinder positions w.r.t. RAO definitions.

check_stroke_limit(*motion_at_poi*)[](../../../../../../source-code/PyBM/marine/machines/T700.py)  

check_cylinder_velocity_limit(*motion_at_poi*)[](../../../../../../source-code/PyBM/marine/machines/T700.py)  

check_platform_velocity_limit(*motion_at_poi*)[](../../../../../../source-code/PyBM/marine/machines/T700.py)  

compute_cylinder_forces(*Fz*, *Mx*, *My*)[](../../../../../../source-code/PyBM/marine/machines/T700.py)  

plot(*axs: matplotlib.axes.Axes = None*)[](../../../../../../source-code/PyBM/marine/machines/T700.py)  

&nbsp;

PyBM.marine.machines.T700.pos* = \[10, 20, 0\]*[](../../../../../../source-code/PyBM/marine/machines/T700.py)  
