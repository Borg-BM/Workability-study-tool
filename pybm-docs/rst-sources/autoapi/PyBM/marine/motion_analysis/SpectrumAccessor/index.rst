PyBM.marine.motion_analysis.SpectrumAccessor
============================================

.. py:module:: PyBM.marine.motion_analysis.SpectrumAccessor

.. autoapi-nested-parse::

   Accessor of Xarray Dataset to implement spectral analysis tools.

   CBR 06-10-2023

   References:
    [1] Offshore Hydromechanics, J.M.J. Journée and W.W. Massie



Classes
-------

.. autoapisummary::

   PyBM.marine.motion_analysis.SpectrumAccessor.SpectralTools
   PyBM.marine.motion_analysis.SpectrumAccessor.EqualEnergySpectrum


Module Contents
---------------

.. py:class:: SpectralTools(xarray_obj)

   Tools to analyse spectra.


   .. py:attribute:: _obj


   .. py:attribute:: _amp
      :value: None



   .. py:attribute:: _m0
      :value: None



   .. py:attribute:: _m1
      :value: None



   .. py:attribute:: _m2
      :value: None



   .. py:property:: m0


   .. py:property:: m1


   .. py:property:: m2


   .. py:property:: amp


   .. py:method:: spectral_moment(order=0)

      Compute nth order spectral moment of a spectrum.
      Ref [1]. Eq (6.81)

      :param order: Order of the moment, defaults to 0
      :type order: int, optional



   .. py:property:: standard_deviation

      Compute the standard deviation from the frequency response.
      Ref. [1] Eq (6.82)

      :param m0: 0th Spectral moment
      :return: Standard deviation



   .. py:property:: zero_crossing_period

      Compute zero-crossing period.
      Ref. [1] Eq (6.84)

      :return: [s] Average zero crossing period.



   .. py:method:: MPE(storm_duration=10800, standard_deviations=None)

      Compute Most Probable Extreme from Rayleigh Distribution based on storm duration and Zero-crossing period.
      Ref [1], Section 11.1 Eq (11.20)

      :param storm_duration: [s] duration of the period of interest (usually 3 hours)
      :return: Most probable extreme.




.. py:class:: EqualEnergySpectrum(xarray_obj)

   Bases: :py:obj:`SpectralTools`


   Tools to analyse spectra optimized for equal energy frequencies.


   .. py:method:: spectral_moment(order=0)

      Compute nth order spectral moment of an equal energy spectrum.
      Ref [1]. Eq (6.81)

      :param order: Order of the moment, defaults to 0
      :type order: int, optional



