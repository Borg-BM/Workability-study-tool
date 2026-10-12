<!-- Source: https://docs.app.barge-master.com/autoapi/PyBM/hydraulics/accumulator/index.html -->

# PyBM.hydraulics.accumulator

Python class to compute Accumulator properties

Date: 15-05-2023 Author: CBR Check: —

## Attributes

|                                                                                                        |     |
|--------------------------------------------------------------------------------------------------------|-----|
| [`accu_density`](#PyBM.hydraulics.accumulator.accu_density "PyBM.hydraulics.accumulator.accu_density") |     |

## Classes

|                                                                                                     |     |
|-----------------------------------------------------------------------------------------------------|-----|
| [`Accumulator`](#PyBM.hydraulics.accumulator.Accumulator "PyBM.hydraulics.accumulator.Accumulator") |     |

## Module Contents

PyBM.hydraulics.accumulator.accu_density* = 1000.0*[](../../../../../source-code/PyBM/hydraulics/accumulator.py)  

&nbsp;

*class *PyBM.hydraulics.accumulator.Accumulator(*Vaccu*, *Pmax*)[](../../../../../source-code/PyBM/hydraulics/accumulator.py)  
k* = 1.4*[](../../../../../source-code/PyBM/hydraulics/accumulator.py)  

n2_density* = 1.2506*[](../../../../../source-code/PyBM/hydraulics/accumulator.py)  

Patm* = 101300.0*[](../../../../../source-code/PyBM/hydraulics/accumulator.py)  

V[](../../../../../source-code/PyBM/hydraulics/accumulator.py)  

Pmax[](../../../../../source-code/PyBM/hydraulics/accumulator.py)  

get_p1(*V1*)[](../../../../../source-code/PyBM/hydraulics/accumulator.py)  
Get Pressure for given Volume V1.

Parameters:  
**V1** – Volume \[m3\]

Returns:  
\[Pa\] pressure for V1.

get_pressure_ratio(*V1*)[](../../../../../source-code/PyBM/hydraulics/accumulator.py)  
Ratio of Max Pressure to pressure at point V1

Parameters:  
**V1** – Volume \[m3\]

Returns:  
\[Pa\] pressure for V1.

mass_estimate()[](../../../../../source-code/PyBM/hydraulics/accumulator.py)  
Container Mass estimate based on accu volume

Returns:  
\[kg\] mass

gas_mass()[](../../../../../source-code/PyBM/hydraulics/accumulator.py)  
Get mass of Nitrogen gas.

Returns:  
\[kg\] mass

\_\_str\_\_() → str[](../../../../../source-code/PyBM/hydraulics/accumulator.py)  
