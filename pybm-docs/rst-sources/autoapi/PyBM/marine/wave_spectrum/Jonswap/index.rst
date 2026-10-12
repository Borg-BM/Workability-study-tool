PyBM.marine.wave_spectrum.Jonswap
=================================

.. py:module:: PyBM.marine.wave_spectrum.Jonswap

.. autoapi-nested-parse::

   This document defines the JONSWAP spectrum class.

   CBR 21-06-2023

   References:
    - [1] Offshore Hydromechanics, J.M.J. Journée and W.W. Massie
    - [2] DNV-RP-C205 Environmental Conditions and Environmental Loads, APRIL 2014



Attributes
----------

.. autoapisummary::

   PyBM.marine.wave_spectrum.Jonswap.logger


Classes
-------

.. autoapisummary::

   PyBM.marine.wave_spectrum.Jonswap.Jonswap


Module Contents
---------------

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



