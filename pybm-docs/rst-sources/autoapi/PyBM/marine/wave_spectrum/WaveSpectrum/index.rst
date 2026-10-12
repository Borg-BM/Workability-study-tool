PyBM.marine.wave_spectrum.WaveSpectrum
======================================

.. py:module:: PyBM.marine.wave_spectrum.WaveSpectrum


Classes
-------

.. autoapisummary::

   PyBM.marine.wave_spectrum.WaveSpectrum.WaveSpectrum


Functions
---------

.. autoapisummary::

   PyBM.marine.wave_spectrum.WaveSpectrum.wrap


Module Contents
---------------

.. py:function:: wrap(angle)

.. py:class:: WaveSpectrum(Hs, Tp, main_direction, Ndirs=11, spreading=4.0)

   Bases: :py:obj:`abc.ABC`


   Helper class that provides a standard way to create an ABC using
   inheritance.


   .. py:property:: Hs


   .. py:property:: Tp


   .. py:property:: main_direction

      [deg] Main direction of wave.



   .. py:attribute:: spreading
      :value: 4.0



   .. py:property:: Ndirs

      [-] Number of wave directions to use (should be odd).



   .. py:method:: __str__()


   .. py:method:: power_spectrum(freqs)
      :abstractmethod:


      Compute frequency spectrum for the given frequency points.

      :param freqs: [Hz] list of frequency components
      :param plot: True to plot spectrum
      :return: [m2/(rad/s)] Wave spectral density



   .. py:method:: wave_spectrum(freqs)

      Compute frequency spectrum for the given frequency points.

      :param freqs: [Hz] list of frequency components
      :param plot: True to plot spectrum
      :return: [m2/(rad/s)] Wave spectral density



   .. py:method:: equal_energy_frequencies(bounds, df=None, Nfreqs=100)

      Numeric method to calculate frequencies at equal energies.

      :param Nfreqs: NUmber of frequency components to generate, defaults to 100
      :type Nfreqs: int, optional



   .. py:method:: equal_energy_directions(Ndirs=None)

      Compute the directions to use for equal energy directional spreading.

      :param Ndirs: [-] number of directions (must be odd)
      :return: [deg] Vector of directions



   .. py:method:: equal_energy_method(func_power_spectrum, bounds, N)
      :staticmethod:


      Numeric equal area method.
      :param func_power_spectrum: Function that outputs the power spectrum, such as a wave spectrum power spectrum or a spreading function. Must accept array of x coordinates, and output either a xr.DataArray or an array of y.
      :param bounds: bounds of X, as an array or tuple: (xmin, xmax)
      :param N: Number of X to divide energy over



   .. py:method:: directional_wave_spectrum(freqs, Rel_Dirs)

      Compute combined directional wave spectrum.

      :param freqs: [Hz] list of frequency components
      :param Rel_Dirs: [deg] list of wave directions relative to main direction (between -180 and 180 degrees).

      :return: [m2/Hz] Wave spectral density



   .. py:method:: abs_directions(Rel_Dirs)


   .. py:method:: equal_energy_directional_wave_spectrum(freqs, Ndirs=None)

      Compute directional wave spectrim with spreading using equal energy directions.

      :param freqs: [Hz] Vector of frequency points
      :param Ndirs: [-] Number of directions (must be odd)
      :return: Directional wave Spectrum



   .. py:method:: equal_energy_directional_spreading(Ndirs=None)

      Compute directional wave spreading using equal energy directions.

      :param Ndirs: [-] Number of directions (must be odd)
      :param plot: plots the spectrum if True
      :return: Directional wave spreading



   .. py:method:: directional_spreading(relative_dirs)

      Compute directional spreading factors for the given directions.

      Function is based on the Cos^n function defined in the Orcaflex documentation.

      :param relative_dirs: [deg] list of wave directions relative to main direction (between -180 and 180 degrees).
      :param plot: True to plot directional spreading
      :return: [-] spreading factor corresponding to each direction



   .. py:method:: shift_direction(wave_data, angle_shift)
      :staticmethod:



   .. py:method:: plot(freqs, Rel_Dirs, ax=None)


