"""
This document defines the Torsethaugen spectrum class.

CBR 21-06-2023
"""
import numpy as np
import xarray as xr

from PyBM.marine.wave_spectrum.WaveSpectrum import WaveSpectrum

class Torsethaugen(WaveSpectrum):
    """
    This class defines the Torsethaugen Frequency spectrum.
    """

    def __init__(self, Hs, Tp, main_direction, Ndirs=11, spreading=4, offset=0):
        """_summary_

        :param Hs: [m] Significant wave height
        :param Tp: [s] Peak period
        :param main_direction: [deg] Wave direction: 0 is from stern 180 from bow, 90 from starboard
        :param Ndirs: [-] Number of wave directions
        :param spreading: [-] Wave spreading, unidirectional is used if spreading =< 0
        :param offset: [deg] directional offset of peak 2 w.r.t. peak 1, defaults to 0
        """
        super().__init__(Hs, Tp, main_direction, Ndirs, spreading)

        self.offset = offset

    def power_spectrum(self, freqs):
        """
        Compute frequency spectrum for the given frequency points.

        :param freqs: [Hz] list of frequency components
        :param Npeak: [0, 1 or 2] 0: use full Torsethaugen spectrum. 1: use first peak only. 2: use second peak only
        :return: [m2/Hz] Wave spectral density
        """
        S, __, __ = self._power_spectrum(freqs, self.Tp, self.Hs)
        return S

    
    @staticmethod

    def _power_spectrum_parameters(Tp, Hs):
        """
        Compute power spectral parameters for the Torsethaugen double peak spectrum
        :param Tp: peak wave period
        :param Hs: significant wave height
        :return: [H1, Tp1, H2, Tp2, y, winddominated]
        """
        # Empirical parameter values
        af = 6.6  # sm^(-1/3)
        ae = 2.0  # sm^(-1/2)
        au = 25  # s
        a10 = 0.7
        a1 = 0.5
        kg = 35  # *(1+3.5*np.exp(-Hs)) #35.0
        b1 = 2.0  # s
        a20 = 0.6
        a2 = 0.3
        a3 = 6
        g = 9.81
        # Check for swell or wind dominated sea
        Tpf = af * Hs ** (1 / 3)
        winddominated = Tp <= Tpf

        # upper and lower limnits wave period scale factors
        Tl = ae * Hs ** (1 / 2)
        Tu = au
        # non-dimensional scales for the spectral peak period
        el = (Tpf - Tp) / (Tpf - Tl)
        eu = (Tp - Tpf) / (Tu - Tpf)

        # wind dominated spectral parameters
        Rw = (1 - a10) * np.exp(-((el / a1) ** 2)) + a10
        Hw1 = Rw * Hs
        Tpw1 = Tp
        sp = (2 * np.pi / g) * Hw1 / (Tpw1**2)
        yw = kg * sp ** (6 / 7)
        Hw2 = (1 - Rw**2) ** (1 / 2) * Hs
        Tpw2 = Tpf + b1
        # swell dominated spectral parameters
        Rs = (1 - a20) * np.exp(-((eu / a2) ** 2)) + a20
        Hs1 = Rs * Hs
        Tps1 = Tp
        sf = (2 * np.pi / g) * Hs / (Tpf**2)
        yf = kg * sf ** (6 / 7)
        ys = yf * (1 + a3 * eu)
        Hs2 = (1 - Rs**2) ** (1 / 2) * Hs
        Tps2 = af * Hs2 ** (1 / 3)

        lc = lambda w, s: xr.where(winddominated, w, s)
        H1 = lc(Hw1, Hs1)
        Tp1 = lc(Tpw1, Tps1)
        H2 = lc(Hw2, Hs2)
        Tp2 = lc(Tpw2, Tps2)
        gamma = lc(yw, ys)

        return [H1, Tp1, H2, Tp2, gamma, winddominated]

    @staticmethod

    def _power_spectrum(freqs, Tp, Hs):
        """
        Calculate the double peaked power spectrum of the Torsethaugen paper (simplified)
        :params freqs: frequencies of the spectral density result
        :param Tp: peak wave period
        :param Hs: significant wave height
        :return: [H1, Tp1, H2, Tp2, y, winddominated]
        """
        fm = 1 / Tp
        if fm < 1:
            sigma = 0.07
        else:
            sigma = 0.09
        H1, Tp1, H2, Tp2, gamma, _ = Torsethaugen._power_spectrum_parameters(Tp, Hs)

        f1n = freqs * Tp1
        f2n = freqs * Tp2
        G0 = 3.26
        Ay = (1 + 1.1 * np.log(gamma) ** 1.19) / gamma
        E1 = (1 / 16) * H1**2 * Tp1
        E2 = (1 / 16) * H2**2 * Tp2
        S1n = G0 * Ay * f1n**-4 * np.exp(-(f1n**-4)) * gamma ** (np.exp(-(1 / (2 * sigma**2)) * (f1n - 1) ** 2))
        S2n = G0 * f2n**-4 * np.exp(-(f2n**-4))

        Sw = E1 * S1n + E2 * S2n
        return [Sw, E1 * S1n, E2 * S2n]

    def dual_equal_energy_directional_wave_spectrum(self, freqs, offset=90, Ndirs=None):
        """
        Compute dual peak, combined directional wave spectrum. Uses two JONSWAP spectrums offset by 90 deg or whatever specified.

        :param freqs: [Hz] Vector of frequency points
        :param offset: [deg] directionality offset between first peak spectrum and second peak spectrum
        :param Ndirs: [-] Number of directions (must be odd)
        :return: Directional wave Spectrum
        """
        Rel_Dirs = self.equal_energy_directions(Ndirs)
        Sd1 = self.directional_spreading(Rel_Dirs)
        __, Sw1, Sw2 = [self._power_spectrum(freqs, Tp, self.Hs) for Tp in self.Tp]
        S1 = Sw1 * Sd1
        Sd2 = self.directional_spreading(Rel_Dirs, self.main_direction + offset)
        S2 = Sw2 * Sd2
        S1e = xr.concat(
            [S1, S1.interp(dict(Direction=S2.coords["Direction"].values)).fillna(0)],
            dim="Direction",
        )
        S2e = S2.interp(dict(Direction=S1e.coords["Direction"].values)).fillna(0)

        Stot = S1e + S2e
        Stot = Stot.sortby("Direction")
        Stot = Stot.assign_coords(
            dict(
                Relative_Direction=(
                    "Direction",
                    ((Stot["Direction"].values + 180) % 360 - 180),
                )
            )
        )
        return Stot

    def equal_energy_directional_wave_spectrum(self, freqs, Ndirs=None):
        return self.dual_equal_energy_directional_wave_spectrum(freqs, self.offset, Ndirs)
