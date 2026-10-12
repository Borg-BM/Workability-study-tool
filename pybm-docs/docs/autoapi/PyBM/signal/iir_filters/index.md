<!-- Source: https://docs.app.barge-master.com/autoapi/PyBM/signal/iir_filters/index.html -->

# PyBM.signal.iir_filters

This module contains the tools to create IIR filters.

## Functions

|                                                                                                                             |                                                                 |
|-----------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------|
| [`get_delay_at_freq`](#PyBM.signal.iir_filters.get_delay_at_freq "PyBM.signal.iir_filters.get_delay_at_freq")(filter, freq) | Get the phase delay at a specific frequency for a given filter. |
| [`lead_iir`](#PyBM.signal.iir_filters.lead_iir "PyBM.signal.iir_filters.lead_iir")(phase, freq, fs)                         | Design a lead IIR filter.                                       |
| [`lowpass_iir`](#PyBM.signal.iir_filters.lowpass_iir "PyBM.signal.iir_filters.lowpass_iir")(cutoff, fs\[, order\])          | Design a lowpass IIR filter.                                    |
| [`notch_iir`](#PyBM.signal.iir_filters.notch_iir "PyBM.signal.iir_filters.notch_iir")(freq, fs\[, quality\])                | Design a notch IIR filter.                                      |

## Module Contents

PyBM.signal.iir_filters.get_delay_at_freq(*filter*, *freq*)[](../../../../../source-code/PyBM/signal/iir_filters.py)  
Get the phase delay at a specific frequency for a given filter. :param filter: The filter to analyze. :param freq: The frequency at which to evaluate the filter. :return: The delay at the specified frequency.

&nbsp;

PyBM.signal.iir_filters.lead_iir(*phase*, *freq*, *fs*)[](../../../../../source-code/PyBM/signal/iir_filters.py)  
Design a lead IIR filter. :param phase: Maximum phase angle of lead filter in degrees. :param freq: Frequency where lead filter has maximum phase angle in Hz. :param fs: Sampling frequency in Hz.

&nbsp;

PyBM.signal.iir_filters.lowpass_iir(*cutoff*, *fs*, *order=1*)[](../../../../../source-code/PyBM/signal/iir_filters.py)  
Design a lowpass IIR filter. :param cutoff: Cutoff frequency of the filter in Hz. :param fs: Sampling frequency in Hz. :param order: Order of the filter.

&nbsp;

PyBM.signal.iir_filters.notch_iir(*freq*, *fs*, *quality=30*)[](../../../../../source-code/PyBM/signal/iir_filters.py)  
Design a notch IIR filter. :param freq: Center frequency of the notch filter in Hz. :param fs: Sampling frequency in Hz. :param quality: Quality factor of the filter.
