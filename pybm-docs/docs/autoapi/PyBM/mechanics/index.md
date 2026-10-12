<!-- Source: https://docs.app.barge-master.com/autoapi/PyBM/mechanics/index.html -->

# PyBM.mechanics

## Submodules

- [PyBM.mechanics.mechanical_hydraulic_combination](mechanical_hydraulic_combination/index.md)
- [PyBM.mechanics.mechanical_interface](mechanical_interface/index.md)

## Classes

|                                                                                                                                    |                                                                  |
|------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------|
| [`MechanicalHydraulicCombination`](#PyBM.mechanics.MechanicalHydraulicCombination "PyBM.mechanics.MechanicalHydraulicCombination") |                                                                  |
| [`MechanicalInterface`](#PyBM.mechanics.MechanicalInterface "PyBM.mechanics.MechanicalInterface")                                  | Helper class that provides a standard way to create an ABC using |

## Package Contents

*class *PyBM.mechanics.MechanicalHydraulicCombination(*mechanics: [PyBM.mechanics.mechanical_interface.MechanicalInterface](mechanical_interface/index.md#PyBM.mechanics.mechanical_interface.MechanicalInterface "PyBM.mechanics.mechanical_interface.MechanicalInterface")*, *hydraulics: [PyBM.hydraulics.accu_cylinder_combination.AccuCylinderCombination](../hydraulics/accu_cylinder_combination/index.md#PyBM.hydraulics.accu_cylinder_combination.AccuCylinderCombination "PyBM.hydraulics.accu_cylinder_combination.AccuCylinderCombination")*)[](../../../../source-code/PyBM/mechanics/mechanical_hydraulic_combination.py)  
mech  

hyd  

get_force(*Se*)[](../../../../source-code/PyBM/mechanics/mechanical_hydraulic_combination.py)  

\_\_plot(*fcn*, *axes: matplotlib.pyplot.Axes = None*)[](../../../../source-code/PyBM/mechanics/mechanical_hydraulic_combination.py)  

plot_force(*axes: matplotlib.pyplot.Axes = None*)[](../../../../source-code/PyBM/mechanics/mechanical_hydraulic_combination.py)  

plot_error(*design_force*, *axes: matplotlib.pyplot.Axes = None*)[](../../../../source-code/PyBM/mechanics/mechanical_hydraulic_combination.py)  

&nbsp;

*class *PyBM.mechanics.MechanicalInterface(*min_pos*, *max_pos*)[](../../../../source-code/PyBM/mechanics/mechanical_interface.py)  
Bases: `abc.ABC`

Helper class that provides a standard way to create an ABC using inheritance.

min_pos  

max_pos  

*abstractmethod *L_cylinder(*effective_disp*)[](../../../../source-code/PyBM/mechanics/mechanical_interface.py)  
Return cylinder length for given compensation length.

Parameters:  
**effective_disp** – \[m\] Displacement to compensate for.

*abstractmethod *force_ratio(*effective_disp*)[](../../../../source-code/PyBM/mechanics/mechanical_interface.py)  
Return ratio of Cylinder Force / External force for a given position.

Parameters:  
**effective_disp** – \[m\] Displacement to compensate for.
