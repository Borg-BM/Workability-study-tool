<!-- Source: https://docs.app.barge-master.com/autoapi/PyBM/signal/tf_tools/index.html -->

# PyBM.signal.tf_tools

Tools to augment Scipy.signal.TransferFunction function class.

Date: 24-11-2023 Author: CBR Check: —

## Functions

|                                                                                                                                     |                                                       |
|-------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------|
| [`check_sample_times`](#PyBM.signal.tf_tools.check_sample_times "PyBM.signal.tf_tools.check_sample_times")(tf1, tf2)                |                                                       |
| [`TF_multiply`](#PyBM.signal.tf_tools.TF_multiply "PyBM.signal.tf_tools.TF_multiply")(tf1, tf2)                                     |                                                       |
| [`TF_divide`](#PyBM.signal.tf_tools.TF_divide "PyBM.signal.tf_tools.TF_divide")(tf1, tf2)                                           |                                                       |
| [`TF_equals`](#PyBM.signal.tf_tools.TF_equals "PyBM.signal.tf_tools.TF_equals")(tf1, tf2)                                           |                                                       |
| [`print_TF`](#PyBM.signal.tf_tools.print_TF "PyBM.signal.tf_tools.print_TF")(self)                                                  | Return string of TF coefficients.                     |
| [`response_at_freqs`](#PyBM.signal.tf_tools.response_at_freqs "PyBM.signal.tf_tools.response_at_freqs")(tf, freqs\[, db\])          | Compute magnitude and phase at given frequency points |
| [`plot_response`](#PyBM.signal.tf_tools.plot_response "PyBM.signal.tf_tools.plot_response")(tf\[, Name, freq_range, mag_ylim, db\]) | Plot the frequency response of a Transfer function    |

## Module Contents

PyBM.signal.tf_tools.check_sample_times(*tf1: scipy.signal.TransferFunction*, *tf2: scipy.signal.TransferFunction*)[](../../../../../source-code/PyBM/signal/tf_tools.py)  

&nbsp;

PyBM.signal.tf_tools.TF_multiply(*tf1: scipy.signal.TransferFunction*, *tf2*)[](../../../../../source-code/PyBM/signal/tf_tools.py)  

&nbsp;

PyBM.signal.tf_tools.TF_divide(*tf1: scipy.signal.TransferFunction*, *tf2*)[](../../../../../source-code/PyBM/signal/tf_tools.py)  

&nbsp;

PyBM.signal.tf_tools.TF_equals(*tf1: scipy.signal.TransferFunction*, *tf2*)[](../../../../../source-code/PyBM/signal/tf_tools.py)  

&nbsp;

PyBM.signal.tf_tools.print_TF(*self*)[](../../../../../source-code/PyBM/signal/tf_tools.py)  
Return string of TF coefficients.

Return type:  
str

&nbsp;

PyBM.signal.tf_tools.response_at_freqs(*tf: scipy.signal.TransferFunction*, *freqs*, *db=True*)[](../../../../../source-code/PyBM/signal/tf_tools.py)  
Compute magnitude and phase at given frequency points

Parameters:  
- **tf** (*spsig.TransferFunction*) – Transfer Function

- **freqs** (*array-like*) – \[Hz\] Frequency points

- **db** (*bool,* *optional*) – True to return Decibels False to return absolute values, defaults to True

Returns:  
tuple (magnitude, phase) WHERE array mag is mgnitude \[db or abs\] array phase \[deg\]

&nbsp;

PyBM.signal.tf_tools.plot_response(*tf: scipy.signal.TransferFunction*, *Name: str = 'IIR Filter'*, *freq_range=(1 / 50, 50)*, *mag_ylim=(-15, 5)*, *db=True*)[](../../../../../source-code/PyBM/signal/tf_tools.py)  
Plot the frequency response of a Transfer function

Parameters:  
- **tf** (*spsig.TransferFunction*) – Transfer Function

- **Name** (*str*) – Name of function

- **db** (*bool*) – Use decibels or absolut magnitude
