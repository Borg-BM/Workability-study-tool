<!-- Source: https://docs.app.barge-master.com/autoapi/PyBM/marine/motion_analysis/MotionRAO/index.html -->

# PyBM.marine.motion_analysis.MotionRAO

Motion RAO class. Inherits RAO class and xarray.Dataset Init as Dataset with Three dataarrays: POS (positional RAO values) VEL (velocity RAO values) ACC (acceleration RAO values)

CBR 21-06-2023

References:  
\[1\] Ship Motion Control, Tristan Perez

## Classes

|                                                                                                                   |                                                    |
|-------------------------------------------------------------------------------------------------------------------|----------------------------------------------------|
| [`MotionRAO`](#PyBM.marine.motion_analysis.MotionRAO.MotionRAO "PyBM.marine.motion_analysis.MotionRAO.MotionRAO") | This is the parent class for motion and force RAOs |

## Module Contents

*class *PyBM.marine.motion_analysis.MotionRAO.MotionRAO(*data_vars: xarray.core.types.DataVars \| None = None*, *coords: collections.abc.Mapping\[Any, Any\] \| None = None*, *attrs: collections.abc.Mapping\[Any, Any\] \| None = None*)[](../../../../../../source-code/PyBM/marine/motion_analysis/MotionRAO.py)  
Bases: [`PyBM.marine.motion_analysis.RAO.RAO`](../RAO/index.md#PyBM.marine.motion_analysis.RAO.RAO "PyBM.marine.motion_analysis.RAO.RAO")

This is the parent class for motion and force RAOs

\_\_slots\_\_* = ()*[](../../../../../../source-code/PyBM/marine/motion_analysis/MotionRAO.py)  

translate_rao(*offset*)[](../../../../../../source-code/PyBM/marine/motion_analysis/MotionRAO.py)  
Translates the RAO to a point of interest. Ref\[1\] eq (4.27)

Parameters:  
**offset** – \[m\] (x,y,z) offset of the point of interest

Returns:  
Full vessel motion RAOs around POI
