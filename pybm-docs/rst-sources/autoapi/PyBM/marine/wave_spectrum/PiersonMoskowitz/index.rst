PyBM.marine.wave_spectrum.PiersonMoskowitz
==========================================

.. py:module:: PyBM.marine.wave_spectrum.PiersonMoskowitz

.. autoapi-nested-parse::

   This document defines the Pierson Moskowitz spectrum class.

   CBR 21-06-2023

   References:
    - [1] Offshore Hydromechanics, J.M.J. Journée and W.W. Massie
    - [2] DNV-RP-C205 Environmental Conditions and Environmental Loads, APRIL 2014



Attributes
----------

.. autoapisummary::

   PyBM.marine.wave_spectrum.PiersonMoskowitz.logger


Classes
-------

.. autoapisummary::

   PyBM.marine.wave_spectrum.PiersonMoskowitz.PiersonMoskowitz


Module Contents
---------------

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



