PyBM.marine.motion_analysis.Response
====================================

.. py:module:: PyBM.marine.motion_analysis.Response

.. autoapi-nested-parse::

   Module to calculate vessel motions in the frequency domain.

   CBR 21-06-2023

   References:
    [1] Offshore Hydromechanics, J.M.J. Journée and W.W. Massie



Functions
---------

.. autoapisummary::

   PyBM.marine.motion_analysis.Response.compute_response
   PyBM.marine.motion_analysis.Response.compute_mpe
   PyBM.marine.motion_analysis.Response.equal_energy_freqs_rao
   PyBM.marine.motion_analysis.Response.apply_directional_spreading


Module Contents
---------------

.. py:function:: compute_response(wave: PyBM.marine.wave_spectrum.WaveSpectrum, rao: PyBM.marine.motion_analysis.RAO, poi=None, Nfreqs=200, f_bounds=None)

   Compute the vessel response based on the given wave spectrum and RAO.

   :param wave: The wave spectrum.
   :type wave: WaveSpectrum
   :param rao: The response amplitude operator.
   :type rao: RAO
   :param poi: The point of interest [x,y,z] in meters, defaults to None.
   :type poi: list, optional
   :param Nfreqs: The number of frequencies to consider, defaults to 200.
   :type Nfreqs: int, optional
   :param f_bounds: The frequency bounds, defaults to None.
   :type f_bounds: tuple, optional
   :return: The computed vessel response.
   :rtype: Response


.. py:function:: compute_mpe(wave: PyBM.marine.wave_spectrum.WaveSpectrum, rao: PyBM.marine.motion_analysis.RAO, poi=None, storm_duration=10800, transfer_function=None)

   Calculate MPE of the given parameter for all points of interest (POI).

   :param poi: [m] (x,y,z) offset of point of interest
   :param storm_duration: [s] duration of the period of interest (usually 3 hours)
   :param transfer_function: ([[a], [b]]) Numerator and Denumerator of continuous transfer function to be applied.
   :return: Statistical extreme value



.. py:function:: equal_energy_freqs_rao(wave: PyBM.marine.wave_spectrum.WaveSpectrum, rao: PyBM.marine.motion_analysis.RAO, Nfreqs, f_bounds=None)

.. py:function:: apply_directional_spreading(wave: PyBM.marine.wave_spectrum.WaveSpectrum, rao: PyBM.marine.motion_analysis.RAO)

