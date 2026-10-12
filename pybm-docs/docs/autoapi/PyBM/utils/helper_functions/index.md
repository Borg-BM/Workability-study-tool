<!-- Source: https://docs.app.barge-master.com/autoapi/PyBM/utils/helper_functions/index.html -->

# PyBM.utils.helper_functions

## Functions

|                                                                                                                                            |                                                                                                                                 |
|--------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------|
| [`unwrap_angle`](#PyBM.utils.helper_functions.unwrap_angle "PyBM.utils.helper_functions.unwrap_angle")(angle)                              | Make sure angle is between 0 and 360.                                                                                           |
| [`amp_phase_to_complex`](#PyBM.utils.helper_functions.amp_phase_to_complex "PyBM.utils.helper_functions.amp_phase_to_complex")(amp, phase) | Convert amplitude / phase representation to complex number                                                                      |
| [`disc_area`](#PyBM.utils.helper_functions.disc_area "PyBM.utils.helper_functions.disc_area")(diameter)                                    | Return area from diameter.                                                                                                      |
| [`complex_max`](#PyBM.utils.helper_functions.complex_max "PyBM.utils.helper_functions.complex_max")(data, dim)                             |                                                                                                                                 |
| [`delta`](#PyBM.utils.helper_functions.delta "PyBM.utils.helper_functions.delta")(→ numpy.ndarray)                                         | Return array of differences, the first value will be 0 to conserve the length.                                                  |
| [`component_absolute`](#PyBM.utils.helper_functions.component_absolute "PyBM.utils.helper_functions.component_absolute")(x)                | Take the absolute value of the real and imaginary part separatly.                                                               |
| [`absolute_sum`](#PyBM.utils.helper_functions.absolute_sum "PyBM.utils.helper_functions.absolute_sum")(a, b)                               | Sum complex numbers as absolute values (to include phase information), for example to get flow from 2 complex velocity signals. |
| [`differentiate`](#PyBM.utils.helper_functions.differentiate "PyBM.utils.helper_functions.differentiate")(rao, freqs)                      | Take the derivate of RAO data                                                                                                   |

## Module Contents

PyBM.utils.helper_functions.unwrap_angle(*angle*)[](../../../../../source-code/PyBM/utils/helper_functions.py)  
Make sure angle is between 0 and 360.

Parameters:  
**angle** – \[deg\] angle

&nbsp;

PyBM.utils.helper_functions.amp_phase_to_complex(*amp*, *phase*)[](../../../../../source-code/PyBM/utils/helper_functions.py)  
Convert amplitude / phase representation to complex number

Parameters:  
- **amp** – Amplitude

- **phase** – \[deg\] Phase

Return type:  
Complex

&nbsp;

PyBM.utils.helper_functions.disc_area(*diameter*)[](../../../../../source-code/PyBM/utils/helper_functions.py)  
Return area from diameter.

Parameters:  
**diameter** – Diamter of disc

Returns:  
Area of disc

&nbsp;

PyBM.utils.helper_functions.complex_max(*data: xarray.Dataset*, *dim*)[](../../../../../source-code/PyBM/utils/helper_functions.py)  

&nbsp;

PyBM.utils.helper_functions.delta(*steps: numpy.ndarray*) → numpy.ndarray[](../../../../../source-code/PyBM/utils/helper_functions.py)  
Return array of differences, the first value will be 0 to conserve the length.

Parameters:  
**steps** (*np.ndarray*) – Array of values

Returns:  
Array off diferences

Return type:  
np.ndarray

&nbsp;

PyBM.utils.helper_functions.component_absolute(*x*)[](../../../../../source-code/PyBM/utils/helper_functions.py)  
Take the absolute value of the real and imaginary part separatly.

Parameters:  
**x** – Complex number

&nbsp;

PyBM.utils.helper_functions.absolute_sum(*a*, *b*)[](../../../../../source-code/PyBM/utils/helper_functions.py)  
Sum complex numbers as absolute values (to include phase information), for example to get flow from 2 complex velocity signals. WARNING: only resulting amplitude is meaningfull.

Parameters:  
- **a** – Complex component

- **b** – Complex component

Returns:  
Magnitude of sum of absolute values. Equivalent to time based: max(abs(signal_a) + abs(signal_b)))

&nbsp;

PyBM.utils.helper_functions.differentiate(*rao*, *freqs*)[](../../../../../source-code/PyBM/utils/helper_functions.py)  
Take the derivate of RAO data

Parameters:  
- **rao** – Motion RAO

- **freqs** – \[Hz\] Frequencies corresponding to the data points

Returns:  
Time derivative of the data
