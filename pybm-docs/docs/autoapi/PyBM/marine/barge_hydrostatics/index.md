<!-- Source: https://docs.app.barge-master.com/autoapi/PyBM/marine/barge_hydrostatics/index.html -->

# PyBM.marine.barge_hydrostatics

Python class to compute barge hydrostatics

Date: 15-05-2023 Author: CBR Check: JHO

## Classes

|                                                                                         |     |
|-----------------------------------------------------------------------------------------|-----|
| [`Barge`](#PyBM.marine.barge_hydrostatics.Barge "PyBM.marine.barge_hydrostatics.Barge") |     |

## Module Contents

*class *PyBM.marine.barge_hydrostatics.Barge(*L*, *B*, *Depth*, *Draft*, *KG*, *name=None*)[](../../../../../source-code/PyBM/marine/barge_hydrostatics.py)  
name* = None*[](../../../../../source-code/PyBM/marine/barge_hydrostatics.py)  

L[](../../../../../source-code/PyBM/marine/barge_hydrostatics.py)  

B[](../../../../../source-code/PyBM/marine/barge_hydrostatics.py)  

Depth[](../../../../../source-code/PyBM/marine/barge_hydrostatics.py)  

Draft[](../../../../../source-code/PyBM/marine/barge_hydrostatics.py)  

KG[](../../../../../source-code/PyBM/marine/barge_hydrostatics.py)  

KB[](../../../../../source-code/PyBM/marine/barge_hydrostatics.py)  

\_disp* = None*[](../../../../../source-code/PyBM/marine/barge_hydrostatics.py)  

\_Ixx* = None*[](../../../../../source-code/PyBM/marine/barge_hydrostatics.py)  

\_Iyy* = None*[](../../../../../source-code/PyBM/marine/barge_hydrostatics.py)  

*property *Awl[](../../../../../source-code/PyBM/marine/barge_hydrostatics.py)  

*property *disp[](../../../../../source-code/PyBM/marine/barge_hydrostatics.py)  

*property *mass[](../../../../../source-code/PyBM/marine/barge_hydrostatics.py)  

*property *Iyy[](../../../../../source-code/PyBM/marine/barge_hydrostatics.py)  
Momement of intertia around y-axis (pitch inertia) based on solid cuboid.

Returns:  
\[kg.m2\]

*property *Ixx[](../../../../../source-code/PyBM/marine/barge_hydrostatics.py)  
Momement of intertia around x-axis (roll inertia) based on solid cuboid.

Returns:  
\[kg.m2\]

*property *heave_stiffness[](../../../../../source-code/PyBM/marine/barge_hydrostatics.py)  
Compute hydrostatic Heave stiffness of barge.

Returns:  
Heave stiffness \[N/m\]

Return type:  
float

*property *heave_period[](../../../../../source-code/PyBM/marine/barge_hydrostatics.py)  
Natural period of Heave.

Returns:  
\[s\]

*property *pitch_stiffness[](../../../../../source-code/PyBM/marine/barge_hydrostatics.py)  
Compute hydrostatic pitch stiffness of barge (for small angles).

Returns:  
Pitch stiffness \[Nm/rad\]

Return type:  
float

*property *roll_stiffness[](../../../../../source-code/PyBM/marine/barge_hydrostatics.py)  
Compute hydrostatic roll stiffness of barge (for small angles).

Returns:  
Roll stiffness \[Nm/rad\]

Return type:  
float

*property *pitch_period[](../../../../../source-code/PyBM/marine/barge_hydrostatics.py)  
Natural period of pitch.

Returns:  
\[s\]

*property *roll_period[](../../../../../source-code/PyBM/marine/barge_hydrostatics.py)  
Natural period of Roll.

Returns:  
\[s\]

*property *Rxx[](../../../../../source-code/PyBM/marine/barge_hydrostatics.py)  
Radius of gyration in Roll.

Returns:  
\[m\]

*property *Ryy[](../../../../../source-code/PyBM/marine/barge_hydrostatics.py)  
Radius of gyration in Pitch.

Returns:  
\[m\]

\_radii_of_gyration(*Inertia*)[](../../../../../source-code/PyBM/marine/barge_hydrostatics.py)  

heave_stiffness_at_POI(*POI: Barge.heave_stiffness_at_POI.POI*) → float[](../../../../../source-code/PyBM/marine/barge_hydrostatics.py)  
Get heave stiffness at POI.

Parameters:  
**POI** – position of POI from barge center point.

Returns:  
\[N/m\] heave stiffness of POI.

\_\_str\_\_() → str[](../../../../../source-code/PyBM/marine/barge_hydrostatics.py)  

roll_stats() → str[](../../../../../source-code/PyBM/marine/barge_hydrostatics.py)  
