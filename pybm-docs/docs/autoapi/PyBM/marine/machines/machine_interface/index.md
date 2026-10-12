<!-- Source: https://docs.app.barge-master.com/autoapi/PyBM/marine/machines/machine_interface/index.html -->

# PyBM.marine.machines.machine_interface

Generic Interface for BM machine to compute workability

## Classes

|                                                                                                                                             |                                                                  |
|---------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------|
| [`Machine_Linear`](#PyBM.marine.machines.machine_interface.Machine_Linear "PyBM.marine.machines.machine_interface.Machine_Linear")          | Helper class that provides a standard way to create an ABC using |
| [`Machine_Nonlinear`](#PyBM.marine.machines.machine_interface.Machine_Nonlinear "PyBM.marine.machines.machine_interface.Machine_Nonlinear") | Helper class that provides a standard way to create an ABC using |

## Module Contents

*class *PyBM.marine.machines.machine_interface.Machine_Linear(*position*, *orientation*)[](../../../../../../source-code/PyBM/marine/machines/machine_interface.py)  
Bases: `abc.ABC`

Helper class that provides a standard way to create an ABC using inheritance.

pos[](../../../../../../source-code/PyBM/marine/machines/machine_interface.py)  

orient[](../../../../../../source-code/PyBM/marine/machines/machine_interface.py)  

rotation[](../../../../../../source-code/PyBM/marine/machines/machine_interface.py)  

apply_transform(*point: numpy.array*) → numpy.array[](../../../../../../source-code/PyBM/marine/machines/machine_interface.py)  
Apply rotation then translation to 3D point

Parameters:  
**point** (*np.array*) – 3D vector \[x,y,z\]

Returns:  
Transformed position

Return type:  
np.array

get_rao_at_poi(*rao*) → [PyBM.marine.motion_analysis.MotionRAO.MotionRAO](../../motion_analysis/MotionRAO/index.md#PyBM.marine.motion_analysis.MotionRAO.MotionRAO "PyBM.marine.motion_analysis.MotionRAO.MotionRAO")[](../../../../../../source-code/PyBM/marine/machines/machine_interface.py)  
Get the Motion RAOs at the POI

*abstractmethod *get_POI() → dict[](../../../../../../source-code/PyBM/marine/machines/machine_interface.py)  

apply_machine_dofs(*rao*) → [PyBM.marine.motion_analysis.MotionRAO.MotionRAO](../../motion_analysis/MotionRAO/index.md#PyBM.marine.motion_analysis.MotionRAO.MotionRAO "PyBM.marine.motion_analysis.MotionRAO.MotionRAO")[](../../../../../../source-code/PyBM/marine/machines/machine_interface.py)  

get_workability_limit(*motion_at_poi*, *\*\*kwargs*)[](../../../../../../source-code/PyBM/marine/machines/machine_interface.py)  

\_\_str\_\_() → str[](../../../../../../source-code/PyBM/marine/machines/machine_interface.py)  

&nbsp;

*class *PyBM.marine.machines.machine_interface.Machine_Nonlinear(*position*, *orientation*)[](../../../../../../source-code/PyBM/marine/machines/machine_interface.py)  
Bases: `abc.ABC`

Helper class that provides a standard way to create an ABC using inheritance.

pos[](../../../../../../source-code/PyBM/marine/machines/machine_interface.py)  

orient[](../../../../../../source-code/PyBM/marine/machines/machine_interface.py)  

rotation[](../../../../../../source-code/PyBM/marine/machines/machine_interface.py)  

apply_transform(*point: numpy.array*) → numpy.array[](../../../../../../source-code/PyBM/marine/machines/machine_interface.py)  
Apply rotation then translation to 3D point

Parameters:  
**point** (*np.array*) – 3D vector \[x,y,z\]

Returns:  
Transformed position

Return type:  
np.array

*abstractmethod *get_POI() → dict[](../../../../../../source-code/PyBM/marine/machines/machine_interface.py)  
