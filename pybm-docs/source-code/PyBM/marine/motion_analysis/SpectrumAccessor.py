"""
Accessor of Xarray Dataset to implement spectral analysis tools.

CBR 06-10-2023

References:
 [1] Offshore Hydromechanics, J.M.J. Journée and W.W. Massie
"""
import numpy as np
import xarray as xr

@xr.register_dataarray_accessor("spectral")
@xr.register_dataset_accessor("spectral")

class SpectralTools:
    """Tools to analyse spectra."""

    def __init__(self, xarray_obj):
        if not "Frequency" in xarray_obj.coords:
            raise AttributeError("DataArray must have Frequency coordinate for Spectral tools to work.")

        self._obj = xarray_obj

        self._amp = None

        self._m0 = None

        self._m1 = None

        self._m2 = None

    @property

    def m0(self):
        if self._m0 is None:
            self._m0 = self.spectral_moment(0)
        return self._m0

    @property

    def m1(self):
        if self._m1 is None:
            self._m1 = self.spectral_moment(1)
        return self._m1

    @property

    def m2(self):
        if self._m2 is None:
            self._m2 = self.spectral_moment(2)
        return self._m2

    @property

    def amp(self):
        if self._amp is None:
            self._amp = np.abs(self._obj)
        return self._amp

    def spectral_moment(self, order=0):
        """Compute nth order spectral moment of a spectrum.
        Ref [1]. Eq (6.81)

        :param order: Order of the moment, defaults to 0
        :type order: int, optional
        """
        freqs = self._obj.Frequency * 2 * np.pi
        if order != 0:
            moment = self.amp * np.power(freqs, order)
        else:
            moment = self.amp
        return xr.apply_ufunc(np.trapz, moment, freqs, input_core_dims=[["Frequency"], ["Frequency"]], vectorize=True)

    @property

    def standard_deviation(self):
        """
        Compute the standard deviation from the frequency response.
        Ref. [1] Eq (6.82)

        :param m0: 0th Spectral moment
        :return: Standard deviation
        """
        return np.sqrt(self.m0)

    @property

    def zero_crossing_period(self):
        """Compute zero-crossing period.
        Ref. [1] Eq (6.84)

        :return: [s] Average zero crossing period.
        """
        return 2 * np.pi * np.sqrt(self.m0 / self.m2)

    def MPE(self, storm_duration=10800, standard_deviations=None):
        """
        Compute Most Probable Extreme from Rayleigh Distribution based on storm duration and Zero-crossing period.
        Ref [1], Section 11.1 Eq (11.20)

        :param storm_duration: [s] duration of the period of interest (usually 3 hours)
        :return: Most probable extreme.

        """
        n = storm_duration / self.zero_crossing_period  # Ref. [1] Eq (8.86)
        factor = np.sqrt(2 * np.log(n))  # Default = 3.71 for 1000 cycles Ref [1] Eq (11.20)
        if standard_deviations != None:
            factor = standard_deviations
        return self.standard_deviation * factor

@xr.register_dataarray_accessor("spectral_equal_energy")
@xr.register_dataset_accessor("spectral_equal_energy")

class EqualEnergySpectrum(SpectralTools):
    """Tools to analyse spectra optimized for equal energy frequencies."""

    def spectral_moment(self, order=0):
        """Compute nth order spectral moment of an equal energy spectrum.
        Ref [1]. Eq (6.81)

        :param order: Order of the moment, defaults to 0
        :type order: int, optional
        """
        if order != 0:
            moment = (self._obj * np.power(self._obj.Frequency * 2 * np.pi, order)).sum(dim="Frequency")
        else:
            moment = self._obj.sum(dim="Frequency")
        return moment
