PyBM.signal.iir_filters
=======================

.. py:module:: PyBM.signal.iir_filters

.. autoapi-nested-parse::

   This module contains the tools to create IIR filters.



Functions
---------

.. autoapisummary::

   PyBM.signal.iir_filters.get_delay_at_freq
   PyBM.signal.iir_filters.lead_iir
   PyBM.signal.iir_filters.lowpass_iir
   PyBM.signal.iir_filters.notch_iir


Module Contents
---------------

.. py:function:: get_delay_at_freq(filter, freq)

   Get the phase delay at a specific frequency for a given filter.
   :param filter: The filter to analyze.
   :param freq: The frequency at which to evaluate the filter.
   :return: The delay at the specified frequency.


.. py:function:: lead_iir(phase, freq, fs)

   Design a lead IIR filter.
   :param phase: Maximum phase angle of lead filter in degrees.
   :param freq: Frequency where lead filter has maximum phase angle in Hz.
   :param fs: Sampling frequency in Hz.


.. py:function:: lowpass_iir(cutoff, fs, order=1)

   Design a lowpass IIR filter.
   :param cutoff: Cutoff frequency of the filter in Hz.
   :param fs: Sampling frequency in Hz.
   :param order: Order of the filter.


.. py:function:: notch_iir(freq, fs, quality=30)

   Design a notch IIR filter.
   :param freq: Center frequency of the notch filter in Hz.
   :param fs: Sampling frequency in Hz.
   :param quality: Quality factor of the filter.


