<!-- Source: https://docs.app.barge-master.com/autoapi/PyBM/hydraulics/cylinder/index.html -->

# PyBM.hydraulics.cylinder

Python class to compute Cylinder properties

Date: 15-05-2023 Author: CBR Check: —

References:  
\[1\]: NL002692-02-50-2100-ADM-0001-RAI RA98725531

## Attributes

|                                                                                                                    |     |
|--------------------------------------------------------------------------------------------------------------------|-----|
| [`HF_cylinder_bore`](#PyBM.hydraulics.cylinder.HF_cylinder_bore "PyBM.hydraulics.cylinder.HF_cylinder_bore")       |     |
| [`HF_cylinder_area`](#PyBM.hydraulics.cylinder.HF_cylinder_area "PyBM.hydraulics.cylinder.HF_cylinder_area")       |     |
| [`HF_cylinder_stroke`](#PyBM.hydraulics.cylinder.HF_cylinder_stroke "PyBM.hydraulics.cylinder.HF_cylinder_stroke") |     |
| [`HF_cylinder_mass`](#PyBM.hydraulics.cylinder.HF_cylinder_mass "PyBM.hydraulics.cylinder.HF_cylinder_mass")       |     |
| [`HF_cylinder_volume`](#PyBM.hydraulics.cylinder.HF_cylinder_volume "PyBM.hydraulics.cylinder.HF_cylinder_volume") |     |
| [`HF_manifold_mass`](#PyBM.hydraulics.cylinder.HF_manifold_mass "PyBM.hydraulics.cylinder.HF_manifold_mass")       |     |
| [`HF_max_vel`](#PyBM.hydraulics.cylinder.HF_max_vel "PyBM.hydraulics.cylinder.HF_max_vel")                         |     |
| [`HF_max_flow`](#PyBM.hydraulics.cylinder.HF_max_flow "PyBM.hydraulics.cylinder.HF_max_flow")                      |     |

## Classes

|                                                                                                                             |     |
|-----------------------------------------------------------------------------------------------------------------------------|-----|
| [`Cylinder`](#PyBM.hydraulics.cylinder.Cylinder "PyBM.hydraulics.cylinder.Cylinder")                                        |     |
| [`DoubleActingCylinder`](#PyBM.hydraulics.cylinder.DoubleActingCylinder "PyBM.hydraulics.cylinder.DoubleActingCylinder")    |     |
| [`TripleChamberCylinder`](#PyBM.hydraulics.cylinder.TripleChamberCylinder "PyBM.hydraulics.cylinder.TripleChamberCylinder") |     |

## Module Contents

PyBM.hydraulics.cylinder.HF_cylinder_bore* = 0.47*[](../../../../../source-code/PyBM/hydraulics/cylinder.py)  

&nbsp;

PyBM.hydraulics.cylinder.HF_cylinder_area[](../../../../../source-code/PyBM/hydraulics/cylinder.py)  

&nbsp;

PyBM.hydraulics.cylinder.HF_cylinder_stroke* = 1.47*[](../../../../../source-code/PyBM/hydraulics/cylinder.py)  

&nbsp;

PyBM.hydraulics.cylinder.HF_cylinder_mass* = 6959*[](../../../../../source-code/PyBM/hydraulics/cylinder.py)  

&nbsp;

PyBM.hydraulics.cylinder.HF_cylinder_volume[](../../../../../source-code/PyBM/hydraulics/cylinder.py)  

&nbsp;

PyBM.hydraulics.cylinder.HF_manifold_mass* = 3508*[](../../../../../source-code/PyBM/hydraulics/cylinder.py)  

&nbsp;

PyBM.hydraulics.cylinder.HF_max_vel* = 0.455*[](../../../../../source-code/PyBM/hydraulics/cylinder.py)  

&nbsp;

PyBM.hydraulics.cylinder.HF_max_flow[](../../../../../source-code/PyBM/hydraulics/cylinder.py)  

&nbsp;

*class *PyBM.hydraulics.cylinder.Cylinder(*piston_area*, *stroke*, *max_pressure*, *minLength=None*)[](../../../../../source-code/PyBM/hydraulics/cylinder.py)  
A[](../../../../../source-code/PyBM/hydraulics/cylinder.py)  

stroke[](../../../../../source-code/PyBM/hydraulics/cylinder.py)  

minLength* = None*[](../../../../../source-code/PyBM/hydraulics/cylinder.py)  

Pmax[](../../../../../source-code/PyBM/hydraulics/cylinder.py)  

max_vel[](../../../../../source-code/PyBM/hydraulics/cylinder.py)  

*property *Dia[](../../../../../source-code/PyBM/hydraulics/cylinder.py)  
Diameter of cylinder \[m\].

*property *Maxforce[](../../../../../source-code/PyBM/hydraulics/cylinder.py)  
Maximum force of cylinder \[N\].

*property *Maxflow[](../../../../../source-code/PyBM/hydraulics/cylinder.py)  
Maximum flow of cylinder \[m3/s\].

get_stroke(*Lcyl*)[](../../../../../source-code/PyBM/hydraulics/cylinder.py)  
Get cylinder stroke from cylinder length

Parameters:  
**Lcyl** – \[m\] Total required length of cylinder

\_\_str\_\_() → str[](../../../../../source-code/PyBM/hydraulics/cylinder.py)  

mass_estimate()[](../../../../../source-code/PyBM/hydraulics/cylinder.py)  
Cylinder and manifold mass estimate based HF cylinder mass.

Returns:  
\[kg\] Mass estimate of cylinder and manifold.

cylinder_mass_estimate()[](../../../../../source-code/PyBM/hydraulics/cylinder.py)  
Give cylinder mass estimate scaled based on HF cylinder area. return: \[kg\] mass estimate.

manifold_mass_estimate()[](../../../../../source-code/PyBM/hydraulics/cylinder.py)  
Manifold mass scaled based on HF cylinder flow.

Returns:  
\[m3\] manifold mass estimate.

&nbsp;

*class *PyBM.hydraulics.cylinder.DoubleActingCylinder(*piston_area*, *ring_area*, *stroke*, *max_pressure*, *minLength=None*)[](../../../../../source-code/PyBM/hydraulics/cylinder.py)  
Bases: [`Cylinder`](#PyBM.hydraulics.cylinder.Cylinder "PyBM.hydraulics.cylinder.Cylinder")

ring_area[](../../../../../source-code/PyBM/hydraulics/cylinder.py)  

max_pulling_force()[](../../../../../source-code/PyBM/hydraulics/cylinder.py)  
Maximum pulling force.

Returns:  
\[N\] pulling force

\_\_str\_\_() → str[](../../../../../source-code/PyBM/hydraulics/cylinder.py)  

&nbsp;

*class *PyBM.hydraulics.cylinder.TripleChamberCylinder(*piston_area*, *ring_area*, *inner_rod_area*, *stroke*, *max_pressure*, *max_passive_pressure=None*, *minLength=None*)[](../../../../../source-code/PyBM/hydraulics/cylinder.py)  
Bases: [`DoubleActingCylinder`](#PyBM.hydraulics.cylinder.DoubleActingCylinder "PyBM.hydraulics.cylinder.DoubleActingCylinder")

max_passive_pressure[](../../../../../source-code/PyBM/hydraulics/cylinder.py)  

passive_area[](../../../../../source-code/PyBM/hydraulics/cylinder.py)  

max_passive_force()[](../../../../../source-code/PyBM/hydraulics/cylinder.py)  
Maximum force of the passive chamber.

Returns:  
\[N\] passive force

\_\_str\_\_() → str[](../../../../../source-code/PyBM/hydraulics/cylinder.py)  
