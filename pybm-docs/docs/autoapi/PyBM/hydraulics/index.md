<!-- Source: https://docs.app.barge-master.com/autoapi/PyBM/hydraulics/index.html -->

# PyBM.hydraulics

## Submodules

- [PyBM.hydraulics.VariablePressureAccumulator](VariablePressureAccumulator/index.md)
- [PyBM.hydraulics.accu_cylinder_combination](accu_cylinder_combination/index.md)
- [PyBM.hydraulics.accumulator](accumulator/index.md)
- [PyBM.hydraulics.buckling](buckling/index.md)
- [PyBM.hydraulics.cylinder](cylinder/index.md)

## Classes

|                                                                                                                             |              |
|-----------------------------------------------------------------------------------------------------------------------------|--------------|
| [`AccuCylinderCombination`](#PyBM.hydraulics.AccuCylinderCombination "PyBM.hydraulics.AccuCylinderCombination")             |              |
| [`Accumulator`](#PyBM.hydraulics.Accumulator "PyBM.hydraulics.Accumulator")                                                 |              |
| [`Cylinder`](#PyBM.hydraulics.Cylinder "PyBM.hydraulics.Cylinder")                                                          |              |
| [`DoubleActingCylinder`](#PyBM.hydraulics.DoubleActingCylinder "PyBM.hydraulics.DoubleActingCylinder")                      |              |
| [`TripleChamberCylinder`](#PyBM.hydraulics.TripleChamberCylinder "PyBM.hydraulics.TripleChamberCylinder")                   |              |
| [`VariablePressureAccumulator`](#PyBM.hydraulics.VariablePressureAccumulator "PyBM.hydraulics.VariablePressureAccumulator") | All symbols: |

## Functions

|                                                                                                                                    |                                                                                    |
|------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------|
| [`buckling_check`](#PyBM.hydraulics.buckling_check "PyBM.hydraulics.buckling_check")(Fz, d_rod, buckling_length\[, E\])            | Check for buckling of the cylinder rod. (acc. BHO 'template cylinder sizing.xlsx') |
| [`calculate_cyl_deadlength`](#PyBM.hydraulics.calculate_cyl_deadlength "PyBM.hydraulics.calculate_cyl_deadlength")(d_bore)         | Calculate total length of cylinder.                                                |
| [`get_min_rod_diameter`](#PyBM.hydraulics.get_min_rod_diameter "PyBM.hydraulics.get_min_rod_diameter")(Fz, buckling_length\[, E\]) | Check for buckling of the cylinder rod. (acc. BHO 'template cylinder sizing.xlsx') |

## Package Contents

*class *PyBM.hydraulics.AccuCylinderCombination(*Vaccu*, *Pmax*, *Acyl*, *stroke*)[](../../../../source-code/PyBM/hydraulics/accu_cylinder_combination.py)  
accu  

cyl  

get_V1(*Pcyl*)[](../../../../source-code/PyBM/hydraulics/accu_cylinder_combination.py)  
Volume of Accu at point Pcyl

Parameters:  
**Pcyl** – \[m\] Cylinder position (0 is retracted).

Returns:  
\[m3\] Volume at point Pcyl

get_p1(*Pcyl*)[](../../../../source-code/PyBM/hydraulics/accu_cylinder_combination.py)  
Get Pressure at at point Pcyl.

Parameters:  
**Pcyl** – \[m\] Cylinder position (0 is retracted).

Returns:  
\[Pa\] pressure for Pcyl.

get_cyl_force(*Pcyl*)[](../../../../source-code/PyBM/hydraulics/accu_cylinder_combination.py)  
Cylinder force at point Pcyl

Parameters:  
**Pcyl** – \[m\] Cylinder position (0 is retracted).

Returns:  
\[N\] Force for Pcyl.

get_pressure_ratio(*Pcyl*)[](../../../../source-code/PyBM/hydraulics/accu_cylinder_combination.py)  
Ratio of Max Pressure to pressure at point Pcyl

Parameters:  
**Pcyl** – \[m\] Cylinder position (0 is retracted).

Returns:  
\[Pa\] pressure for Pcyl.

mass_estimate()[](../../../../source-code/PyBM/hydraulics/accu_cylinder_combination.py)  
Total mass estimate.

Returns:  
\[kg\] mass

\_\_str\_\_() → str[](../../../../source-code/PyBM/hydraulics/accu_cylinder_combination.py)  

*classmethod *from_pressure_ratio_and_1_point(*pressure_ratio*, *L1*, *Acyl*, *P2*, *stroke*, *Max_Vaccu=np.inf*)[](../../../../source-code/PyBM/hydraulics/accu_cylinder_combination.py)  

*classmethod *from_pressure_ratio_and_2_points(*pressure_ratio*, *L2*, *L1*, *Acyl*, *P2*, *stroke*, *Max_Vaccu=np.inf*)[](../../../../source-code/PyBM/hydraulics/accu_cylinder_combination.py)  
Create class based on pressure ratio at 2 desired points.

Parameters:  
- **pressure_ratio** – \[-\] P1/P2 ratio off desired pressures

- **L2** – \[m\] Length of cylinder at position 2 (corresponding to P2)

- **L1** – \[m\] Length of cylinder at position 1 (corresponding to P1)

- **A** – \[m2\] Cylinder Area

- **P2** – \[Pa\] Pressure at Point 2 of Accumulator

*classmethod *from_pressure_ratio_and_V2(*pressure_ratio*, *L1*, *V2*, *Fcyl*, *stroke*, *Max_P2=np.inf*)[](../../../../source-code/PyBM/hydraulics/accu_cylinder_combination.py)  
Create class based on pressure ratio and V2

Parameters:  
- **pressure_ratio** – \[-\] P1/P2 ratio off desired pressures

- **L1** – \[m\] Length of cylinder at position 1 (corresponding to P1)

- **V2** – \[m3\] Volume of accumulator

- **Fcyl** – \[N\] maximum force of Cylinder

plot_force(*axs=None*)[](../../../../source-code/PyBM/hydraulics/accu_cylinder_combination.py)  
Plot properties of the combination.

Parameters:  
**axs** – Axes to plot on, defaults to None

&nbsp;

*class *PyBM.hydraulics.Accumulator(*Vaccu*, *Pmax*)[](../../../../source-code/PyBM/hydraulics/accumulator.py)  
k* = 1.4*  

n2_density* = 1.2506*  

Patm* = 101300.0*  

V  

Pmax  

get_p1(*V1*)[](../../../../source-code/PyBM/hydraulics/accumulator.py)  
Get Pressure for given Volume V1.

Parameters:  
**V1** – Volume \[m3\]

Returns:  
\[Pa\] pressure for V1.

get_pressure_ratio(*V1*)[](../../../../source-code/PyBM/hydraulics/accumulator.py)  
Ratio of Max Pressure to pressure at point V1

Parameters:  
**V1** – Volume \[m3\]

Returns:  
\[Pa\] pressure for V1.

mass_estimate()[](../../../../source-code/PyBM/hydraulics/accumulator.py)  
Container Mass estimate based on accu volume

Returns:  
\[kg\] mass

gas_mass()[](../../../../source-code/PyBM/hydraulics/accumulator.py)  
Get mass of Nitrogen gas.

Returns:  
\[kg\] mass

\_\_str\_\_() → str[](../../../../source-code/PyBM/hydraulics/accumulator.py)  

&nbsp;

PyBM.hydraulics.buckling_check(*Fz*, *d_rod*, *buckling_length*, *E=210000000000.0*)[](../../../../source-code/PyBM/hydraulics/buckling.py)  
Check for buckling of the cylinder rod. (acc. BHO ‘template cylinder sizing.xlsx’)

Parameters:  
- **Fz** – \[N\] Axial force

- **bore** – \[m\] Bore of cylinder

- **rod** – \[m\] Rod of cylinder

- **buckling_length** – \[m\] Length of cylinder rod

- **E** – \[Pa\] Young’s modulus of cylinder

Returns:  
\[bool\] True if buckling occurs

&nbsp;

PyBM.hydraulics.calculate_cyl_deadlength(*d_bore*)[](../../../../source-code/PyBM/hydraulics/buckling.py)  
Calculate total length of cylinder. based on rule of thumb calculation by BHO (‘template cylinder sizing.xlsx’)

Parameters:  
- **stroke** – \[m\] Stroke of cylinder

- **diameter** – \[m\] Diameter of cylinder

Returns:  
\[m\] Dead length of cylinder

&nbsp;

PyBM.hydraulics.get_min_rod_diameter(*Fz*, *buckling_length*, *E=210000*)[](../../../../source-code/PyBM/hydraulics/buckling.py)  
Check for buckling of the cylinder rod. (acc. BHO ‘template cylinder sizing.xlsx’)

Parameters:  
- **Fz** – \[N\] Axial force

- **bore** – \[m\] Bore of cylinder

- **rod** – \[m\] Rod of cylinder

- **buckling_length** – \[m\] Length of cylinder rod

- **E** – \[N/mm^2\] Young’s modulus of cylinder

Returns:  
\[bool\] True if buckling occurs

&nbsp;

*class *PyBM.hydraulics.Cylinder(*piston_area*, *stroke*, *max_pressure*, *minLength=None*)[](../../../../source-code/PyBM/hydraulics/cylinder.py)  
A  

stroke  

minLength* = None*  

Pmax  

max_vel  

*property *Dia  
Diameter of cylinder \[m\].

*property *Maxforce  
Maximum force of cylinder \[N\].

*property *Maxflow  
Maximum flow of cylinder \[m3/s\].

get_stroke(*Lcyl*)[](../../../../source-code/PyBM/hydraulics/cylinder.py)  
Get cylinder stroke from cylinder length

Parameters:  
**Lcyl** – \[m\] Total required length of cylinder

\_\_str\_\_() → str[](../../../../source-code/PyBM/hydraulics/cylinder.py)  

mass_estimate()[](../../../../source-code/PyBM/hydraulics/cylinder.py)  
Cylinder and manifold mass estimate based HF cylinder mass.

Returns:  
\[kg\] Mass estimate of cylinder and manifold.

cylinder_mass_estimate()[](../../../../source-code/PyBM/hydraulics/cylinder.py)  
Give cylinder mass estimate scaled based on HF cylinder area. return: \[kg\] mass estimate.

manifold_mass_estimate()[](../../../../source-code/PyBM/hydraulics/cylinder.py)  
Manifold mass scaled based on HF cylinder flow.

Returns:  
\[m3\] manifold mass estimate.

&nbsp;

*class *PyBM.hydraulics.DoubleActingCylinder(*piston_area*, *ring_area*, *stroke*, *max_pressure*, *minLength=None*)[](../../../../source-code/PyBM/hydraulics/cylinder.py)  
Bases: [`Cylinder`](#PyBM.hydraulics.Cylinder "PyBM.hydraulics.Cylinder")

ring_area  

max_pulling_force()[](../../../../source-code/PyBM/hydraulics/cylinder.py)  
Maximum pulling force.

Returns:  
\[N\] pulling force

\_\_str\_\_() → str[](../../../../source-code/PyBM/hydraulics/cylinder.py)  

&nbsp;

*class *PyBM.hydraulics.TripleChamberCylinder(*piston_area*, *ring_area*, *inner_rod_area*, *stroke*, *max_pressure*, *max_passive_pressure=None*, *minLength=None*)[](../../../../source-code/PyBM/hydraulics/cylinder.py)  
Bases: [`DoubleActingCylinder`](#PyBM.hydraulics.DoubleActingCylinder "PyBM.hydraulics.DoubleActingCylinder")

max_passive_pressure  

passive_area  

max_passive_force()[](../../../../source-code/PyBM/hydraulics/cylinder.py)  
Maximum force of the passive chamber.

Returns:  
\[N\] passive force

\_\_str\_\_() → str[](../../../../source-code/PyBM/hydraulics/cylinder.py)  

&nbsp;

*class *PyBM.hydraulics.VariablePressureAccumulator(*\*extra_eq1*, *Ploss_iso=200000.0*, *Ploss_accu=200000.0*, *Ploss_valve=300000.0*, *Ploss_tank=500000.0*, *Floss_ex=0*, *num_solve=False*, *guesses=False*, *\*\*kwargs*)[](../../../../source-code/PyBM/hydraulics/VariablePressureAccumulator.py)  
All symbols: Pnitro - Nitrogen pressure in the accumulator at midpoint Fact - Max active cylinder force c_f - Contingency factor of required active force, meant for control delay, or pumping pressure loss/gain in the VPA. Usually 1.2 Fdyn - Dynamic forces on cylinder, as required active force. Floss - Extra active force required to overcome losses in the VPA r_acc - Nitrogen pressure loss/gain (ratio) over full stroke of accu (+/-) Fmax - Maximum force of the active + passive cylinder Fmin - Minimum force of the active + passive cylinder Apass - Area of the passive cylinder/chamber P1_loss - Pressure loss in V1 of the VPA P2_loss - Pressure loss in V2 of the VPA P3_loss - Pressure loss in V3 of the VPA P4_loss - Pressure loss in V4 of the VPA Ppas_max - Maximum passive pressure A1 - Area of the tandem cylinder in V1 and V4 in the VPA A2 - Area of the tandem cylinder in V2 and V3 in the VPA

\_syms  

all_eqs  

properties  

*static *syms(*k*)  

prop_dict()[](../../../../source-code/PyBM/hydraulics/VariablePressureAccumulator.py)  

*static *calc_accu_volume(*A1*, *A2*, *stroke_vpa*, *n_pumps=3*)[](../../../../source-code/PyBM/hydraulics/VariablePressureAccumulator.py)  

*static *calc_nitro_loss(*A1*, *A2*, *stroke_vpa*, *V_nitro=V_nitro_T700*, *n_pumps=3*)[](../../../../source-code/PyBM/hydraulics/VariablePressureAccumulator.py)  

*static *calc_accu_stroke(*A1*, *A2*, *stroke_vpa*, *d_accu=d_accu_T700*, *n_pumps=3*, *temp_range=\[273.15, 293.15\]*, *r_accu_fill_inaccuracy=0.04*)[](../../../../source-code/PyBM/hydraulics/VariablePressureAccumulator.py)  

get_passive_force_steps()[](../../../../source-code/PyBM/hydraulics/VariablePressureAccumulator.py)  
