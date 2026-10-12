"""
This document defines the JONSWAP spectrum class.

CBR 21-06-2023

References:
 - [1] Offshore Hydromechanics, J.M.J. Journée and W.W. Massie
 - [2] DNV-RP-C205 Environmental Conditions and Environmental Loads, APRIL 2014
"""

import logging

import numpy as np
import xarray as xr

from PyBM.marine.wave_spectrum.PiersonMoskowitz import PiersonMoskowitz
from PyBM.marine.wave_spectrum.WaveSpectrum import WaveSpectrum

logger = logging.getLogger(__name__)

class Jonswap(WaveSpectrum):
    """
    This class defines the JONSWAP Frequency spectrum.

    :param Hs: [m] Significant wave height
    :param Tp: [s] Peak period
    :param main_direction: [deg] Wave direction: 0 is from stern 180 from bow, 90 from starboard
    :param Ndirs: [-] Number of wave directions
    :param spreading: [-] Wave spreading, unidirectional is used if spreading =< 0
    :param gamma: [-] Peakness factor, according to DNV if not specified
    """

    def __init__(self, Hs, Tp, main_direction, Ndirs=11, spreading=4, gamma=None):
        super().__init__(Hs, Tp, main_direction, Ndirs=Ndirs, spreading=spreading)
        if gamma is not None:
            self.gamma = gamma
        else:
            self._gamma = None

    def __str__(self):
        return super().__str__() + f" gamma={self.gamma}"

    @property

    def gamma(self):
        if self._gamma is None:
            return self.compute_gamma()
        else:
            return self._gamma

    @gamma.setter
    def gamma(self, value):
        if isinstance(value, (float, int)):
            self._gamma = xr.DataArray(
                [[value] * len(self.Hs)] * len(self.Tp), dims=("Tp", "Hs"), coords={"Tp": self.Tp, "Hs": self.Hs}
            )
        elif isinstance(value, xr.DataArray):
            assert value.dims == ("Tp", "Hs"), "Gamma must have dimensions (Tp, Hs)"
            self._gamma = value
        else:
            raise ValueError("Gamma must be a float, int or xr.DataArray with dimensions (Tp, Hs)")

    @property

    def Tz(self):
        """Zero up-crossing period [s]"""
        return self.Tp / 1.287  # Ref [1] Eq.5.127

    @staticmethod

    def Tz_to_Tp(Tz):
        """Convert zero up-crossing period to peak period [s]

        :param Tz: Zero up-crossing period [s]
        :return: Peak period [s]
        """
        return Tz * 1.287  # Ref [1] Eq.5.127

    @staticmethod

    def _compute_gamma(Tp, Hs):
        """
        Compute gamma according to DNV regulations [2] 3.5.5.5

        :param Tp: Peak Period [s]
        :param Hs: Significant wave height [m]
        :return: [-] peakedness factor
        """
        X = Tp / np.sqrt(Hs)
        gamma = np.exp(5.75 - 1.15 * (X))
        gamma = np.clip(gamma, 1.0, 5.0)
        return gamma

    def compute_gamma(self):
        return self._compute_gamma(self.Tp, self.Hs)

    def power_spectrum(self, freqs: xr.DataArray):
        """
        Compute frequency spectrum for the given frequency points.

        :param freqs: [Hz] list of frequency components
        :return: [m2/Hz] Wave spectral density
        """
        return self._power_spectrum(freqs, self.gamma, self.Tp, self.Hs)

    @staticmethod

    def _power_spectrum(freqs, gamma, Tp, Hs):
        wp = 2 * np.pi / Tp
        w = 2 * np.pi * freqs
        sigma = xr.where(w > wp, 0.09, 0.07)

        # Jonswap spectrum Ref. [2] 3.5.5.2
        PMsw = PiersonMoskowitz._power_spectrum(freqs, Tp, Hs)
        A_gamma = 1 - 0.287 * np.log(gamma)
        gamma_exponent = np.exp(-0.5 * np.square((w - wp) / (sigma * wp)))
        Sw = A_gamma * PMsw * np.power(gamma, gamma_exponent)
        return Sw
