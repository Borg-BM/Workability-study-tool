<!-- Source: https://docs.app.barge-master.com/autoapi/PyBM/utils/index.html -->

# PyBM.utils

## Submodules

- [PyBM.utils.data_classes](data_classes/index.md)
- [PyBM.utils.helper_functions](helper_functions/index.md)
- [PyBM.utils.mass_items](mass_items/index.md)
- [PyBM.utils.plot_template](plot_template/index.md)
- [PyBM.utils.windows_helpers](windows_helpers/index.md)

## Classes

|                                                                                  |                                                                             |
|----------------------------------------------------------------------------------|-----------------------------------------------------------------------------|
| [`POI`](#PyBM.utils.POI "PyBM.utils.POI")                                        |                                                                             |
| [`VesselDimensions`](#PyBM.utils.VesselDimensions "PyBM.utils.VesselDimensions") |                                                                             |
| [`massItem`](#PyBM.utils.massItem "PyBM.utils.massItem")                         | Represents a mass item with height, mass, and center of gravity properties. |
| [`Tower`](#PyBM.utils.Tower "PyBM.utils.Tower")                                  | Represents a tower mass item.                                               |
| [`Stack`](#PyBM.utils.Stack "PyBM.utils.Stack")                                  | Abstract base class for a stack of mass items.                              |
| [`VerticalStack`](#PyBM.utils.VerticalStack "PyBM.utils.VerticalStack")          | Represents a vertical stack of mass items.                                  |
| [`HorizontalStack`](#PyBM.utils.HorizontalStack "PyBM.utils.HorizontalStack")    | Represents a horizontal stack of mass items.                                |

## Functions

|                                                                                                          |                                                                                                                                                              |
|----------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [`unwrap_angle`](#PyBM.utils.unwrap_angle "PyBM.utils.unwrap_angle")(angle)                              | Make sure angle is between 0 and 360.                                                                                                                        |
| [`amp_phase_to_complex`](#PyBM.utils.amp_phase_to_complex "PyBM.utils.amp_phase_to_complex")(amp, phase) | Convert amplitude / phase representation to complex number                                                                                                   |
| [`disc_area`](#PyBM.utils.disc_area "PyBM.utils.disc_area")(diameter)                                    | Return area from diameter.                                                                                                                                   |
| [`complex_max`](#PyBM.utils.complex_max "PyBM.utils.complex_max")(data, dim)                             |                                                                                                                                                              |
| [`delta`](#PyBM.utils.delta "PyBM.utils.delta")(→ numpy.ndarray)                                         | Return array of differences, the first value will be 0 to conserve the length.                                                                               |
| [`component_absolute`](#PyBM.utils.component_absolute "PyBM.utils.component_absolute")(x)                | Take the absolute value of the real and imaginary part separatly.                                                                                            |
| [`absolute_sum`](#PyBM.utils.absolute_sum "PyBM.utils.absolute_sum")(a, b)                               | Sum complex numbers as absolute values (to include phase information), for example to get flow from 2 complex velocity signals.                              |
| [`differentiate`](#PyBM.utils.differentiate "PyBM.utils.differentiate")(rao, freqs)                      | Take the derivate of RAO data                                                                                                                                |
| [`isFileLocked`](#PyBM.utils.isFileLocked "PyBM.utils.isFileLocked")(filePath)                           | Source: [https://stackoverflow.com/questions/13371444/python-check-file-is-locked](https://stackoverflow.com/questions/13371444/python-check-file-is-locked) |

## Package Contents

*class *PyBM.utils.POI[](../../../../source-code/PyBM/utils/data_classes.py)  
x*: float = 0.0*  
\[m\] x postion (length)

y*: float = 0.0*  
\[m\] y postion (width)

z*: float = 0.0*  
\[m\] z postion (height)

&nbsp;

*class *PyBM.utils.VesselDimensions[](../../../../source-code/PyBM/utils/data_classes.py)  
Length*: float = 90.0*  
\[m\] length of vessel, from APP

Depth*: float = 13.0*  
\[m\] depth of vessel, keel to deck

Draft*: float = 7.0*  
\[m\] draft of vessel

Breadth*: float = 20.0*  
\[m\] Breadth of vessel

&nbsp;

PyBM.utils.unwrap_angle(*angle*)[](../../../../source-code/PyBM/utils/helper_functions.py)  
Make sure angle is between 0 and 360.

Parameters:  
**angle** – \[deg\] angle

&nbsp;

PyBM.utils.amp_phase_to_complex(*amp*, *phase*)[](../../../../source-code/PyBM/utils/helper_functions.py)  
Convert amplitude / phase representation to complex number

Parameters:  
- **amp** – Amplitude

- **phase** – \[deg\] Phase

Return type:  
Complex

&nbsp;

PyBM.utils.disc_area(*diameter*)[](../../../../source-code/PyBM/utils/helper_functions.py)  
Return area from diameter.

Parameters:  
**diameter** – Diamter of disc

Returns:  
Area of disc

&nbsp;

PyBM.utils.complex_max(*data: xarray.Dataset*, *dim*)[](../../../../source-code/PyBM/utils/helper_functions.py)  

&nbsp;

PyBM.utils.delta(*steps: numpy.ndarray*) → numpy.ndarray[](../../../../source-code/PyBM/utils/helper_functions.py)  
Return array of differences, the first value will be 0 to conserve the length.

Parameters:  
**steps** (*np.ndarray*) – Array of values

Returns:  
Array off diferences

Return type:  
np.ndarray

&nbsp;

PyBM.utils.component_absolute(*x*)[](../../../../source-code/PyBM/utils/helper_functions.py)  
Take the absolute value of the real and imaginary part separatly.

Parameters:  
**x** – Complex number

&nbsp;

PyBM.utils.absolute_sum(*a*, *b*)[](../../../../source-code/PyBM/utils/helper_functions.py)  
Sum complex numbers as absolute values (to include phase information), for example to get flow from 2 complex velocity signals. WARNING: only resulting amplitude is meaningfull.

Parameters:  
- **a** – Complex component

- **b** – Complex component

Returns:  
Magnitude of sum of absolute values. Equivalent to time based: max(abs(signal_a) + abs(signal_b)))

&nbsp;

PyBM.utils.differentiate(*rao*, *freqs*)[](../../../../source-code/PyBM/utils/helper_functions.py)  
Take the derivate of RAO data

Parameters:  
- **rao** – Motion RAO

- **freqs** – \[Hz\] Frequencies corresponding to the data points

Returns:  
Time derivative of the data

&nbsp;

*class *PyBM.utils.massItem[](../../../../source-code/PyBM/utils/mass_items.py)  
Represents a mass item with height, mass, and center of gravity properties.

h*: float*  
\[m\] height

m*: float*  
\[kg\] mass

h_cog*: float = 0*  
\[m\] Height of CoG

x_cog*: float = 0*  
\[m\] Longitudinal offset of CoG

y_cog*: float = 0*  
\[m\] transverse offset of CoG

I*: float = 0*  
Inertia around CoG \[kg.m2\]

get_I() → float[](../../../../source-code/PyBM/utils/mass_items.py)  
\[kg.m2\] Get the inertia around the center of gravity.

set_I(*value: float*)[](../../../../source-code/PyBM/utils/mass_items.py)  
\[kg.m2\] Set the inertia around the center of gravity.

I_shifted(*offset*)[](../../../../source-code/PyBM/utils/mass_items.py)  
Get the inertia around an offset point.

Parameters:  
**offset** – \[m\] distance from stack CoG

Returns:  
Inertia around offset point \[kg.m2\]

&nbsp;

*class *PyBM.utils.Tower[](../../../../source-code/PyBM/utils/mass_items.py)  
Bases: [`massItem`](#PyBM.utils.massItem "PyBM.utils.massItem")

Represents a tower mass item.

D*: float = 0*  
\[m\] Diameter of Tower

*property *I  
Get the inertia around the center of gravity of the tower.

&nbsp;

*class *PyBM.utils.Stack(*items*)[](../../../../source-code/PyBM/utils/mass_items.py)  
Bases: `abc.ABC`

Abstract base class for a stack of mass items.

items  

*property *m  
Get the total mass of the stack.

Returns:  
The total mass of the stack in units of meters \[kg\].

Return type:  
float

*abstractmethod *h()[](../../../../source-code/PyBM/utils/mass_items.py)  
\[m\] Abstract method to get the height of the stack.

*property *h_cog  
\[m\] Get the height of the center of gravity of the stack.

*property *x_cog  
\[m\] Get the longitudinal offset of the center of gravity of the stack.

*property *y_cog  
\[m\] Get the transverse offset of the center of gravity of the stack.

*property *I  
Get the inertia around the center of gravity of the stack.

Returns:  
Inertia around the center of gravity \[kg.m2\]

I_shifted(*offset*)[](../../../../source-code/PyBM/utils/mass_items.py)  
Get the inertia around an offset point.

Parameters:  
**offset** – \[m\] distance from stack CoG

Returns:  
Inertia around offset point \[kg.m2\]

\_\_str\_\_() → str[](../../../../source-code/PyBM/utils/mass_items.py)  
Get a string representation of the stack.

&nbsp;

*class *PyBM.utils.VerticalStack(*items*, *cog_factor=1.0*)[](../../../../source-code/PyBM/utils/mass_items.py)  
Bases: [`Stack`](#PyBM.utils.Stack "PyBM.utils.Stack")

Represents a vertical stack of mass items.

*property *h  
\[m\] Get the height of the vertical stack.

&nbsp;

*class *PyBM.utils.HorizontalStack(*items*, *spacing*, *cog_factor=1.0*)[](../../../../source-code/PyBM/utils/mass_items.py)  
Bases: [`Stack`](#PyBM.utils.Stack "PyBM.utils.Stack")

Represents a horizontal stack of mass items.

*property *h  
\[m\] Get the height of the horizontal stack.

\_\_str\_\_() → str[](../../../../source-code/PyBM/utils/mass_items.py)  
Get a string representation of the horizontal stack.

&nbsp;

PyBM.utils.isFileLocked(*filePath*)[](../../../../source-code/PyBM/utils/windows_helpers.py)  
Source: [https://stackoverflow.com/questions/13371444/python-check-file-is-locked](https://stackoverflow.com/questions/13371444/python-check-file-is-locked) Checks to see if a file is locked. Performs three checks

> 1.  Checks if the file even exists
>
> 2.  Attempts to open the file for reading. This will determine if the file has a write lock.  
>     Write locks occur when the file is being edited or copied to, e.g. a file copy destination
>
> 3.  Attempts to rename the file. If this fails the file is open by some other process for reading. The  
>     file can be read, but not written to or deleted.

Parameters:  
**filePath** – path of file to check
