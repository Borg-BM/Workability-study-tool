"""
This document defines the Pierson Moskowitz spectrum class.

CBR 21-06-2023

References:
 - [1] Offshore Hydromechanics, J.M.J. Journée and W.W. Massie
 - [2] DNV-RP-C205 Environmental Conditions and Environmental Loads, APRIL 2014
"""
import logging

import numpy as np
import xarray as xr

from PyBM.marine.wave_spectrum.WaveSpectrum import WaveSpectrum

logger = logging.getLogger(__name__)

class PiersonMoskowitz(WaveSpectrum):
    """
    This class defines the Pierson Moskowitz Frequency spectrum.
    """

    def power_spectrum(self, freqs):
        """
        Compute frequency spectrum for the given frequency points.

        :param freqs: [Hz] list of frequency components
        :return: [m2/Hz] Wave spectral density
        """
        return self._power_spectrum(freqs, self.Tp, self.Hs)

    @staticmethod

    def _power_spectrum(freqs, Tp, Hs):
        """Ref [2] 3.5.5.1

        :param Hs: [m] Significant wave height
        :param Tp: [s] Peak period
        """
        wp = 2 * np.pi / Tp
        w = 2 * np.pi * freqs
        Sw = 5 / 16 * np.square(Hs) * np.power(wp, 4) * np.power(w, -5) * np.exp(-5 / 4 * np.power(w / wp, -4))
        return Sw
