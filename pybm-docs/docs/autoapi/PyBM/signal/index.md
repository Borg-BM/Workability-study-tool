<!-- Source: https://docs.app.barge-master.com/autoapi/PyBM/signal/index.html -->

# PyBM.signal

## Submodules

- [PyBM.signal.iir_filters](iir_filters/index.md)
- [PyBM.signal.tf_tools](tf_tools/index.md)

## Functions

|                                                                                                                   |                                                                 |
|-------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------|
| [`get_delay_at_freq`](#PyBM.signal.get_delay_at_freq "PyBM.signal.get_delay_at_freq")(filter, freq)               | Get the phase delay at a specific frequency for a given filter. |
| [`lead_iir`](#PyBM.signal.lead_iir "PyBM.signal.lead_iir")(phase, freq, fs)                                       | Design a lead IIR filter.                                       |
| [`lowpass_iir`](#PyBM.signal.lowpass_iir "PyBM.signal.lowpass_iir")(cutoff, fs\[, order\])                        | Design a lowpass IIR filter.                                    |
| [`notch_iir`](#PyBM.signal.notch_iir "PyBM.signal.notch_iir")(freq, fs\[, quality\])                              | Design a notch IIR filter.                                      |
| [`check_sample_times`](#PyBM.signal.check_sample_times "PyBM.signal.check_sample_times")(tf1, tf2)                |                                                                 |
| [`TF_multiply`](#PyBM.signal.TF_multiply "PyBM.signal.TF_multiply")(tf1, tf2)                                     |                                                                 |
| [`TF_divide`](#PyBM.signal.TF_divide "PyBM.signal.TF_divide")(tf1, tf2)                                           |                                                                 |
| [`TF_equals`](#PyBM.signal.TF_equals "PyBM.signal.TF_equals")(tf1, tf2)                                           |                                                                 |
| [`print_TF`](#PyBM.signal.print_TF "PyBM.signal.print_TF")(self)                                                  | Return string of TF coefficients.                               |
| [`response_at_freqs`](#PyBM.signal.response_at_freqs "PyBM.signal.response_at_freqs")(tf, freqs\[, db\])          | Compute magnitude and phase at given frequency points           |
| [`plot_response`](#PyBM.signal.plot_response "PyBM.signal.plot_response")(tf\[, Name, freq_range, mag_ylim, db\]) | Plot the frequency response of a Transfer function              |

## Package Contents

PyBM.signal.get_delay_at_freq(*filter*, *freq*)[](../../../../source-code/PyBM/signal/iir_filters.py)  
Get the phase delay at a specific frequency for a given filter. :param filter: The filter to analyze. :param freq: The frequency at which to evaluate the filter. :return: The delay at the specified frequency.

&nbsp;

PyBM.signal.lead_iir(*phase*, *freq*, *fs*)[](../../../../source-code/PyBM/signal/iir_filters.py)  
Design a lead IIR filter. :param phase: Maximum phase angle of lead filter in degrees. :param freq: Frequency where lead filter has maximum phase angle in Hz. :param fs: Sampling frequency in Hz.

&nbsp;

PyBM.signal.lowpass_iir(*cutoff*, *fs*, *order=1*)[](../../../../source-code/PyBM/signal/iir_filters.py)  
Design a lowpass IIR filter. :param cutoff: Cutoff frequency of the filter in Hz. :param fs: Sampling frequency in Hz. :param order: Order of the filter.

&nbsp;

PyBM.signal.notch_iir(*freq*, *fs*, *quality=30*)[](../../../../source-code/PyBM/signal/iir_filters.py)  
Design a notch IIR filter. :param freq: Center frequency of the notch filter in Hz. :param fs: Sampling frequency in Hz. :param quality: Quality factor of the filter.

&nbsp;

PyBM.signal.check_sample_times(*tf1: scipy.signal.TransferFunction*, *tf2: scipy.signal.TransferFunction*)[](../../../../source-code/PyBM/signal/tf_tools.py)  

&nbsp;

PyBM.signal.TF_multiply(*tf1: scipy.signal.TransferFunction*, *tf2*)[](../../../../source-code/PyBM/signal/tf_tools.py)  

&nbsp;

PyBM.signal.TF_divide(*tf1: scipy.signal.TransferFunction*, *tf2*)[](../../../../source-code/PyBM/signal/tf_tools.py)  

&nbsp;

PyBM.signal.TF_equals(*tf1: scipy.signal.TransferFunction*, *tf2*)[](../../../../source-code/PyBM/signal/tf_tools.py)  

&nbsp;

PyBM.signal.print_TF(*self*)[](../../../../source-code/PyBM/signal/tf_tools.py)  
Return string of TF coefficients.

Return type:  
str

&nbsp;

PyBM.signal.response_at_freqs(*tf: scipy.signal.TransferFunction*, *freqs*, *db=True*)[](../../../../source-code/PyBM/signal/tf_tools.py)  
Compute magnitude and phase at given frequency points

Parameters:  
- **tf** (*spsig.TransferFunction*) – Transfer Function

- **freqs** (*array-like*) – \[Hz\] Frequency points

- **db** (*bool,* *optional*) – True to return Decibels False to return absolute values, defaults to True

Returns:  
tuple (magnitude, phase) WHERE array mag is mgnitude \[db or abs\] array phase \[deg\]

&nbsp;

PyBM.signal.plot_response(*tf: scipy.signal.TransferFunction*, *Name: str = 'IIR Filter'*, *freq_range=(1 / 50, 50)*, *mag_ylim=(-15, 5)*, *db=True*)[](../../../../source-code/PyBM/signal/tf_tools.py)  
Plot the frequency response of a Transfer function

Parameters:  
- **tf** (*spsig.TransferFunction*) – Transfer Function

- **Name** (*str*) – Name of function

- **db** (*bool*) – Use decibels or absolut magnitude
