PyBM.signal.tf_tools
====================

.. py:module:: PyBM.signal.tf_tools

.. autoapi-nested-parse::

   Tools to augment Scipy.signal.TransferFunction function class.

   Date: 24-11-2023
   Author: CBR
   Check: ---



Functions
---------

.. autoapisummary::

   PyBM.signal.tf_tools.check_sample_times
   PyBM.signal.tf_tools.TF_multiply
   PyBM.signal.tf_tools.TF_divide
   PyBM.signal.tf_tools.TF_equals
   PyBM.signal.tf_tools.print_TF
   PyBM.signal.tf_tools.response_at_freqs
   PyBM.signal.tf_tools.plot_response


Module Contents
---------------

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


