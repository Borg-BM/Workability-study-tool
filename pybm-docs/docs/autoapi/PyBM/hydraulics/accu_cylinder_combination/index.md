<!-- Source: https://docs.app.barge-master.com/autoapi/PyBM/hydraulics/accu_cylinder_combination/index.html -->

# PyBM.hydraulics.accu_cylinder_combination

Python class to compute Accumulator properties

Date: 15-05-2023 Author: CBR Check: —

## Classes

|                                                                                                                                                                     |     |
|---------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----|
| [`AccuCylinderCombination`](#PyBM.hydraulics.accu_cylinder_combination.AccuCylinderCombination "PyBM.hydraulics.accu_cylinder_combination.AccuCylinderCombination") |     |

## Module Contents

*class *PyBM.hydraulics.accu_cylinder_combination.AccuCylinderCombination(*Vaccu*, *Pmax*, *Acyl*, *stroke*)[](../../../../../source-code/PyBM/hydraulics/accu_cylinder_combination.py)  
accu[](../../../../../source-code/PyBM/hydraulics/accu_cylinder_combination.py)  

cyl[](../../../../../source-code/PyBM/hydraulics/accu_cylinder_combination.py)  

get_V1(*Pcyl*)[](../../../../../source-code/PyBM/hydraulics/accu_cylinder_combination.py)  
Volume of Accu at point Pcyl

Parameters:  
**Pcyl** – \[m\] Cylinder position (0 is retracted).

Returns:  
\[m3\] Volume at point Pcyl

get_p1(*Pcyl*)[](../../../../../source-code/PyBM/hydraulics/accu_cylinder_combination.py)  
Get Pressure at at point Pcyl.

Parameters:  
**Pcyl** – \[m\] Cylinder position (0 is retracted).

Returns:  
\[Pa\] pressure for Pcyl.

get_cyl_force(*Pcyl*)[](../../../../../source-code/PyBM/hydraulics/accu_cylinder_combination.py)  
Cylinder force at point Pcyl

Parameters:  
**Pcyl** – \[m\] Cylinder position (0 is retracted).

Returns:  
\[N\] Force for Pcyl.

get_pressure_ratio(*Pcyl*)[](../../../../../source-code/PyBM/hydraulics/accu_cylinder_combination.py)  
Ratio of Max Pressure to pressure at point Pcyl

Parameters:  
**Pcyl** – \[m\] Cylinder position (0 is retracted).

Returns:  
\[Pa\] pressure for Pcyl.

mass_estimate()[](../../../../../source-code/PyBM/hydraulics/accu_cylinder_combination.py)  
Total mass estimate.

Returns:  
\[kg\] mass

\_\_str\_\_() → str[](../../../../../source-code/PyBM/hydraulics/accu_cylinder_combination.py)  

*classmethod *from_pressure_ratio_and_1_point(*pressure_ratio*, *L1*, *Acyl*, *P2*, *stroke*, *Max_Vaccu=np.inf*)[](../../../../../source-code/PyBM/hydraulics/accu_cylinder_combination.py)  

*classmethod *from_pressure_ratio_and_2_points(*pressure_ratio*, *L2*, *L1*, *Acyl*, *P2*, *stroke*, *Max_Vaccu=np.inf*)[](../../../../../source-code/PyBM/hydraulics/accu_cylinder_combination.py)  
Create class based on pressure ratio at 2 desired points.

Parameters:  
- **pressure_ratio** – \[-\] P1/P2 ratio off desired pressures

- **L2** – \[m\] Length of cylinder at position 2 (corresponding to P2)

- **L1** – \[m\] Length of cylinder at position 1 (corresponding to P1)

- **A** – \[m2\] Cylinder Area

- **P2** – \[Pa\] Pressure at Point 2 of Accumulator

*classmethod *from_pressure_ratio_and_V2(*pressure_ratio*, *L1*, *V2*, *Fcyl*, *stroke*, *Max_P2=np.inf*)[](../../../../../source-code/PyBM/hydraulics/accu_cylinder_combination.py)  
Create class based on pressure ratio and V2

Parameters:  
- **pressure_ratio** – \[-\] P1/P2 ratio off desired pressures

- **L1** – \[m\] Length of cylinder at position 1 (corresponding to P1)

- **V2** – \[m3\] Volume of accumulator

- **Fcyl** – \[N\] maximum force of Cylinder

plot_force(*axs=None*)[](../../../../../source-code/PyBM/hydraulics/accu_cylinder_combination.py)  
Plot properties of the combination.

Parameters:  
**axs** – Axes to plot on, defaults to None
