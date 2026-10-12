<!-- Source: https://docs.app.barge-master.com/autoapi/PyBM/hydraulics/buckling/index.html -->

# PyBM.hydraulics.buckling

## Functions

|                                                                                                                                                      |                                                                                    |
|------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------|
| [`calculate_cyl_deadlength`](#PyBM.hydraulics.buckling.calculate_cyl_deadlength "PyBM.hydraulics.buckling.calculate_cyl_deadlength")(d_bore)         | Calculate total length of cylinder.                                                |
| [`buckling_check`](#PyBM.hydraulics.buckling.buckling_check "PyBM.hydraulics.buckling.buckling_check")(Fz, d_rod, buckling_length\[, E\])            | Check for buckling of the cylinder rod. (acc. BHO 'template cylinder sizing.xlsx') |
| [`get_min_rod_diameter`](#PyBM.hydraulics.buckling.get_min_rod_diameter "PyBM.hydraulics.buckling.get_min_rod_diameter")(Fz, buckling_length\[, E\]) | Check for buckling of the cylinder rod. (acc. BHO 'template cylinder sizing.xlsx') |

## Module Contents

PyBM.hydraulics.buckling.calculate_cyl_deadlength(*d_bore*)[](../../../../../source-code/PyBM/hydraulics/buckling.py)  
Calculate total length of cylinder. based on rule of thumb calculation by BHO (‘template cylinder sizing.xlsx’)

Parameters:  
- **stroke** – \[m\] Stroke of cylinder

- **diameter** – \[m\] Diameter of cylinder

Returns:  
\[m\] Dead length of cylinder

&nbsp;

PyBM.hydraulics.buckling.buckling_check(*Fz*, *d_rod*, *buckling_length*, *E=210000000000.0*)[](../../../../../source-code/PyBM/hydraulics/buckling.py)  
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

PyBM.hydraulics.buckling.get_min_rod_diameter(*Fz*, *buckling_length*, *E=210000*)[](../../../../../source-code/PyBM/hydraulics/buckling.py)  
Check for buckling of the cylinder rod. (acc. BHO ‘template cylinder sizing.xlsx’)

Parameters:  
- **Fz** – \[N\] Axial force

- **bore** – \[m\] Bore of cylinder

- **rod** – \[m\] Rod of cylinder

- **buckling_length** – \[m\] Length of cylinder rod

- **E** – \[N/mm^2\] Young’s modulus of cylinder

Returns:  
\[bool\] True if buckling occurs
