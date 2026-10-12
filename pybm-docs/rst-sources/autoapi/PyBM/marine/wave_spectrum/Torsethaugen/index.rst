PyBM.marine.wave_spectrum.Torsethaugen
======================================

.. py:module:: PyBM.marine.wave_spectrum.Torsethaugen

.. autoapi-nested-parse::

   This document defines the Torsethaugen spectrum class.

   CBR 21-06-2023



Classes
-------

.. autoapisummary::

   PyBM.marine.wave_spectrum.Torsethaugen.Torsethaugen


Module Contents
---------------

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



