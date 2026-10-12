PyBM.marine.wave_spectrum
=========================

.. py:module:: PyBM.marine.wave_spectrum


Submodules
----------

.. toctree::
   :maxdepth: 1

   /autoapi/PyBM/marine/wave_spectrum/Jonswap/index
   /autoapi/PyBM/marine/wave_spectrum/PiersonMoskowitz/index
   /autoapi/PyBM/marine/wave_spectrum/Torsethaugen/index
   /autoapi/PyBM/marine/wave_spectrum/WaveSpectrum/index


Attributes
----------

.. autoapisummary::

   PyBM.marine.wave_spectrum.logger
   PyBM.marine.wave_spectrum.logger


Classes
-------

.. autoapisummary::

   PyBM.marine.wave_spectrum.PiersonMoskowitz
   PyBM.marine.wave_spectrum.WaveSpectrum
   PyBM.marine.wave_spectrum.Jonswap
   PyBM.marine.wave_spectrum.WaveSpectrum
   PyBM.marine.wave_spectrum.PiersonMoskowitz
   PyBM.marine.wave_spectrum.WaveSpectrum
   PyBM.marine.wave_spectrum.Torsethaugen
   PyBM.marine.wave_spectrum.WaveSpectrum


Functions
---------

.. autoapisummary::

   PyBM.marine.wave_spectrum.wrap


Package Contents
----------------

.. py:class:: PiersonMoskowitz(Hs, Tp, main_direction, Ndirs=11, spreading=4.0)

   Bases: :py:obj:`PyBM.marine.wave_spectrum.WaveSpectrum.WaveSpectrum`


   This class defines the Pierson Moskowitz Frequency spectrum.


   .. py:method:: power_spectrum(freqs)

      Compute frequency spectrum for the given frequency points.

      :param freqs: [Hz] list of frequency components
      :return: [m2/Hz] Wave spectral density



   .. py:method:: _power_spectrum(freqs, Tp, Hs)
      :staticmethod:


      Ref [2] 3.5.5.1

      :param Hs: [m] Significant wave height
      :param Tp: [s] Peak period



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


.. py:data:: logger

.. py:class:: Jonswap(Hs, Tp, main_direction, Ndirs=11, spreading=4, gamma=None)

   Bases: :py:obj:`PyBM.marine.wave_spectrum.WaveSpectrum.WaveSpectrum`


   This class defines the JONSWAP Frequency spectrum.

   :param Hs: [m] Significant wave height
   :param Tp: [s] Peak period
   :param main_direction: [deg] Wave direction: 0 is from stern 180 from bow, 90 from starboard
   :param Ndirs: [-] Number of wave directions
   :param spreading: [-] Wave spreading, unidirectional is used if spreading =< 0
   :param gamma: [-] Peakness factor, according to DNV if not specified


   .. py:method:: __str__()


   .. py:property:: gamma


   .. py:property:: Tz

      Zero up-crossing period [s]



   .. py:method:: Tz_to_Tp(Tz)
      :staticmethod:


      Convert zero up-crossing period to peak period [s]

      :param Tz: Zero up-crossing period [s]
      :return: Peak period [s]



   .. py:method:: _compute_gamma(Tp, Hs)
      :staticmethod:


      Compute gamma according to DNV regulations [2] 3.5.5.5

      :param Tp: Peak Period [s]
      :param Hs: Significant wave height [m]
      :return: [-] peakedness factor



   .. py:method:: compute_gamma()


   .. py:method:: power_spectrum(freqs: xarray.DataArray)

      Compute frequency spectrum for the given frequency points.

      :param freqs: [Hz] list of frequency components
      :return: [m2/Hz] Wave spectral density



   .. py:method:: _power_spectrum(freqs, gamma, Tp, Hs)
      :staticmethod:



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


.. py:data:: logger

.. py:class:: PiersonMoskowitz(Hs, Tp, main_direction, Ndirs=11, spreading=4.0)

   Bases: :py:obj:`PyBM.marine.wave_spectrum.WaveSpectrum.WaveSpectrum`


   This class defines the Pierson Moskowitz Frequency spectrum.


   .. py:method:: power_spectrum(freqs)

      Compute frequency spectrum for the given frequency points.

      :param freqs: [Hz] list of frequency components
      :return: [m2/Hz] Wave spectral density



   .. py:method:: _power_spectrum(freqs, Tp, Hs)
      :staticmethod:


      Ref [2] 3.5.5.1

      :param Hs: [m] Significant wave height
      :param Tp: [s] Peak period



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


.. py:class:: Torsethaugen(Hs, Tp, main_direction, Ndirs=11, spreading=4, offset=0)

   Bases: :py:obj:`PyBM.marine.wave_spectrum.WaveSpectrum.WaveSpectrum`


   This class defines the Torsethaugen Frequency spectrum.


   .. py:attribute:: offset
      :value: 0



   .. py:method:: power_spectrum(freqs)

      Compute frequency spectrum for the given frequency points.

      :param freqs: [Hz] list of frequency components
      :param Npeak: [0, 1 or 2] 0: use full Torsethaugen spectrum. 1: use first peak only. 2: use second peak only
      :return: [m2/Hz] Wave spectral density



   .. py:method:: _power_spectrum_parameters(Tp, Hs)
      :staticmethod:


      Compute power spectral parameters for the Torsethaugen double peak spectrum
      :param Tp: peak wave period
      :param Hs: significant wave height
      :return: [H1, Tp1, H2, Tp2, y, winddominated]



   .. py:method:: _power_spectrum(freqs, Tp, Hs)
      :staticmethod:


      Calculate the double peaked power spectrum of the Torsethaugen paper (simplified)
      :params freqs: frequencies of the spectral density result
      :param Tp: peak wave period
      :param Hs: significant wave height
      :return: [H1, Tp1, H2, Tp2, y, winddominated]



   .. py:method:: dual_equal_energy_directional_wave_spectrum(freqs, offset=90, Ndirs=None)

      Compute dual peak, combined directional wave spectrum. Uses two JONSWAP spectrums offset by 90 deg or whatever specified.

      :param freqs: [Hz] Vector of frequency points
      :param offset: [deg] directionality offset between first peak spectrum and second peak spectrum
      :param Ndirs: [-] Number of directions (must be odd)
      :return: Directional wave Spectrum



   .. py:method:: equal_energy_directional_wave_spectrum(freqs, Ndirs=None)

      Compute directional wave spectrim with spreading using equal energy directions.

      :param freqs: [Hz] Vector of frequency points
      :param Ndirs: [-] Number of directions (must be odd)
      :return: Directional wave Spectrum



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


