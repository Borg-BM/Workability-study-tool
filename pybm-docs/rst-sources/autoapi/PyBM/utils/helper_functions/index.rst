PyBM.utils.helper_functions
===========================

.. py:module:: PyBM.utils.helper_functions


Functions
---------

.. autoapisummary::

   PyBM.utils.helper_functions.unwrap_angle
   PyBM.utils.helper_functions.amp_phase_to_complex
   PyBM.utils.helper_functions.disc_area
   PyBM.utils.helper_functions.complex_max
   PyBM.utils.helper_functions.delta
   PyBM.utils.helper_functions.component_absolute
   PyBM.utils.helper_functions.absolute_sum
   PyBM.utils.helper_functions.differentiate


Module Contents
---------------

.. py:function:: unwrap_angle(angle)

   Make sure angle is between 0 and 360.

   :param angle: [deg] angle


.. py:function:: amp_phase_to_complex(amp, phase)

   Convert amplitude / phase representation to complex number

   :param amp: Amplitude
   :param phase: [deg] Phase
   :rtype: Complex


.. py:function:: disc_area(diameter)

   Return area from diameter.

   :param diameter: Diamter of disc
   :return: Area of disc


.. py:function:: complex_max(data: xarray.Dataset, dim)

.. py:function:: delta(steps: numpy.ndarray) -> numpy.ndarray

   Return array of differences, the first value will be 0 to conserve the length.

   :param steps: Array of values
   :type steps: np.ndarray
   :return: Array off diferences
   :rtype: np.ndarray


.. py:function:: component_absolute(x)

   Take the absolute value of the real and imaginary part separatly.

   :param x: Complex number


.. py:function:: absolute_sum(a, b)

   Sum complex numbers as absolute values (to include phase information), for example to get flow from 2 complex velocity signals.
   WARNING: only resulting amplitude is meaningfull.

   :param a: Complex component
   :param b: Complex component
   :return: Magnitude of sum of absolute values. Equivalent to time based: max(abs(signal_a) + abs(signal_b)))


.. py:function:: differentiate(rao, freqs)

   Take the derivate of RAO data

   :param rao: Motion RAO
   :param freqs: [Hz] Frequencies corresponding to the data points
   :return: Time derivative of the data


