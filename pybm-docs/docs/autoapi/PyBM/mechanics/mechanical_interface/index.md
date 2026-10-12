<!-- Source: https://docs.app.barge-master.com/autoapi/PyBM/mechanics/mechanical_interface/index.html -->

# PyBM.mechanics.mechanical_interface

## Classes

|                                                                                                                                             |                                                                  |
|---------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------|
| [`MechanicalInterface`](#PyBM.mechanics.mechanical_interface.MechanicalInterface "PyBM.mechanics.mechanical_interface.MechanicalInterface") | Helper class that provides a standard way to create an ABC using |

## Module Contents

*class *PyBM.mechanics.mechanical_interface.MechanicalInterface(*min_pos*, *max_pos*)[](../../../../../source-code/PyBM/mechanics/mechanical_interface.py)  
Bases: `abc.ABC`

Helper class that provides a standard way to create an ABC using inheritance.

min_pos[](../../../../../source-code/PyBM/mechanics/mechanical_interface.py)  

max_pos[](../../../../../source-code/PyBM/mechanics/mechanical_interface.py)  

*abstractmethod *L_cylinder(*effective_disp*)[](../../../../../source-code/PyBM/mechanics/mechanical_interface.py)  
Return cylinder length for given compensation length.

Parameters:  
**effective_disp** – \[m\] Displacement to compensate for.

*abstractmethod *force_ratio(*effective_disp*)[](../../../../../source-code/PyBM/mechanics/mechanical_interface.py)  
Return ratio of Cylinder Force / External force for a given position.

Parameters:  
**effective_disp** – \[m\] Displacement to compensate for.
