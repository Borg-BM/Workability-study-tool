PyBM.signal
===========

.. py:module:: PyBM.signal


Submodules
----------

.. toctree::
   :maxdepth: 1

   /autoapi/PyBM/signal/iir_filters/index
   /autoapi/PyBM/signal/tf_tools/index


Functions
---------

.. autoapisummary::

   PyBM.signal.get_delay_at_freq
   PyBM.signal.lead_iir
   PyBM.signal.lowpass_iir
   PyBM.signal.notch_iir
   PyBM.signal.check_sample_times
   PyBM.signal.TF_multiply
   PyBM.signal.TF_divide
   PyBM.signal.TF_equals
   PyBM.signal.print_TF
   PyBM.signal.response_at_freqs
   PyBM.signal.plot_response


Package Contents
----------------

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


.. py:function:: check_sample_times(tf1: scipy.signal.TransferFunction, tf2: scipy.signal.TransferFunction)

.. py:function:: TF_multiply(tf1: scipy.signal.TransferFunction, tf2)

.. py:function:: TF_divide(tf1: scipy.signal.TransferFunction, tf2)

.. py:function:: TF_equals(tf1: scipy.signal.TransferFunction, tf2)

.. py:function:: print_TF(self)

   Return string of TF coefficients.

   :rtype: str


.. py:function:: response_at_freqs(tf: scipy.signal.TransferFunction, freqs, db=True)

   Compute magnitude and phase at given frequency points

   :param tf: Transfer Function
   :type tf: spsig.TransferFunction
   :param freqs: [Hz] Frequency points
   :type freqs: array-like
   :param db: True to return Decibels False to return absolute values, defaults to True
   :type db: bool, optional
   :return: tuple (magnitude, phase)
       WHERE
       array mag is mgnitude [db or abs]
       array phase [deg]


.. py:function:: plot_response(tf: scipy.signal.TransferFunction, Name: str = 'IIR Filter', freq_range=(1 / 50, 50), mag_ylim=(-15, 5), db=True)

   Plot the frequency response of a Transfer function

   :param tf: Transfer Function
   :type tf: spsig.TransferFunction
   :param Name: Name of function
   :type Name: str
   :param db: Use decibels or absolut magnitude
   :type db: bool


