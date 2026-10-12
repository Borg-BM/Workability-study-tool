import math
from abc import ABC, abstractmethod
from collections.abc import Iterable

import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
from scipy import integrate

def wrap(angle):
    return (angle + 360) % (360)

class WaveSpectrum(ABC):
    def __init__(self, Hs, Tp, main_direction, Ndirs=11, spreading=4.0):
        """Abstract class for wave spectra. Units of the spectrum are m^2/(rad/s)

        :param Hs: [m] Significant wave height
        :param Tp: [s] Peak period
        :param main_direction: [deg] Wave direction: 0 is from stern 180 from bow, 90 from starboard
        :param Ndirs: [-] Number of wave directions
        :param spreading: [-] Wave spreading, unidirectional is used if spreading =< 0
        """
        self.Hs = Hs
        self.Tp = Tp
        self.main_direction = main_direction

        self.spreading = spreading

        self.Ndirs = Ndirs

    def __str__(self):
        return f"{self.__class__.__name__} Spectrum: Hs=\n{self.Hs}m, Tp=\n{self.Tp}s, Direction={self.main_direction:.0f}deg, Spreading={self.spreading:.1f}"

    @property

    def main_direction(self):
        """[deg] Main direction of wave."""
        return self._main_direction

    @main_direction.setter
    def main_direction(self, value):
        if not isinstance(value, Iterable):
            value = [value]
        self._main_direction = xr.DataArray(value, dims=("WaveDirection"), coords={"WaveDirection": value})
        self._main_direction = self._main_direction % 360

    @property

    def Hs(self):
        return self._Hs

    @Hs.setter
    def Hs(self, value):
        if not isinstance(value, Iterable):
            value = [value]
        self._Hs = xr.DataArray(value, dims=("Hs"), coords={"Hs": value})

    @property

    def Tp(self):
        return self._Tp

    @Tp.setter
    def Tp(self, value):
        if not isinstance(value, Iterable):
            value = [value]
        self._Tp = xr.DataArray(value, dims=("Tp"), coords={"Tp": value})

    @property

    def Ndirs(self):
        """[-] Number of wave directions to use (should be odd)."""
        return self._Ndirs

    @Ndirs.setter
    def Ndirs(self, value):
        if (value % 2 == 0) or (value < 4):
            raise ValueError("Number of directions should be odd and larger than 3")
        self._Ndirs = value

    @abstractmethod

    def power_spectrum(self, freqs):
        """
        Compute frequency spectrum for the given frequency points.

        :param freqs: [Hz] list of frequency components
        :param plot: True to plot spectrum
        :return: [m2/(rad/s)] Wave spectral density
        """
        pass

    def wave_spectrum(self, freqs):
        """
        Compute frequency spectrum for the given frequency points.

        :param freqs: [Hz] list of frequency components
        :param plot: True to plot spectrum
        :return: [m2/(rad/s)] Wave spectral density
        """
        if self.spreading <= 0:
            Sw = self.power_spectrum(freqs).expand_dims(dim={"Direction": [self.main_direction]})
            return Sw.assign_coords(Relative_Direction=("Direction", [0]))
        else:
            return self.equal_energy_directional_wave_spectrum(freqs)

    def equal_energy_frequencies(self, bounds, df=None, Nfreqs=100):
        """Numeric method to calculate frequencies at equal energies.

        :param Nfreqs: NUmber of frequency components to generate, defaults to 100
        :type Nfreqs: int, optional
        """
        fmin = bounds[0]
        fmax = bounds[1]
        if df == None:
            df = (fmax - fmin) / Nfreqs
        if Nfreqs == None:
            Nfreqs = (fmax - fmin) / df

        x_c, _ = WaveSpectrum.equal_energy_method(self.power_spectrum, (fmin, fmax), Nfreqs)
        return x_c.rename(idx="Frequency")

    def equal_energy_directions(self, Ndirs=None):
        """
        Compute the directions to use for equal energy directional spreading.

        :param Ndirs: [-] number of directions (must be odd)
        :return: [deg] Vector of directions
        """
        if Ndirs == None:
            Ndirs = self.Ndirs
        else:
            self.Ndirs = Ndirs
        if self.spreading <= 0:
            raise ValueError("Cannot have equal energy direction without spreading.")

        def spreading(x):
            return np.power(np.cos(x), self.spreading)

        xs_c, _ = WaveSpectrum.equal_energy_method(spreading, (-np.pi / 2, np.pi / 2), Ndirs)
        Rel_Dirs = xs_c * 180 / np.pi
        Rel_Dirs = Rel_Dirs.rename(idx="Direction")
        return Rel_Dirs.assign_coords(Relative_Direction=Rel_Dirs)

    @staticmethod

    def equal_energy_method(func_power_spectrum, bounds, N):
        """
        Numeric equal area method.
        :param func_power_spectrum: Function that outputs the power spectrum, such as a wave spectrum power spectrum or a spreading function. Must accept array of x coordinates, and output either a xr.DataArray or an array of y.
        :param bounds: bounds of X, as an array or tuple: (xmin, xmax)
        :param N: Number of X to divide energy over
        """
        # Make sure that bounds are passed to linspace as floats, not dataArray. 
        b0 = bounds[0].item() if hasattr(bounds[0], 'item') else bounds[0]
        b1 = bounds[1].item() if hasattr(bounds[1], 'item') else bounds[1]
        x = np.linspace(b0, b1, N * 100)
        x = xr.DataArray(x, coords={"x": x})
        y = func_power_spectrum(x)

        y_cum = xr.apply_ufunc(integrate.cumulative_trapezoid, y, kwargs=dict(x=y["x"], initial=0))
        PSsum = y_cum.isel(x=-1, drop=True)
        energy_func = lambda x: np.linspace(0, x, 2 * N + 1, axis=-1)
        Energies = xr.apply_ufunc(energy_func, PSsum, output_core_dims=[["E"]])

        def get_freqs(x, freqs, energies):
            return np.interp(energies, x, freqs)
        
        eq_idx = xr.apply_ufunc(get_freqs, y_cum, y_cum.x, Energies, input_core_dims=[["x"], ["x"], ["E"]], output_core_dims=[["idx"]], vectorize=True)

        xs_b = eq_idx.isel(idx=slice(0,len(eq_idx.idx),2))
        xs_c = eq_idx.isel(idx=slice(1,-1,2))
        return xs_c, xs_b

    def directional_wave_spectrum(self, freqs, Rel_Dirs):
        """
        Compute combined directional wave spectrum.

        :param freqs: [Hz] list of frequency components
        :param Rel_Dirs: [deg] list of wave directions relative to main direction (between -180 and 180 degrees).

        :return: [m2/Hz] Wave spectral density
        """
        Sd = self.directional_spreading(Rel_Dirs)
        Sw = self.power_spectrum(freqs)
        return Sw * Sd

    def abs_directions(self, Rel_Dirs):
        abs_dirs = wrap(Rel_Dirs + self.main_direction)
        sorted = abs_dirs.groupby("WaveDirection", squeeze=False).map(np.sort)
        return sorted

    def equal_energy_directional_wave_spectrum(self, freqs, Ndirs=None):
        """
        Compute directional wave spectrim with spreading using equal energy directions.

        :param freqs: [Hz] Vector of frequency points
        :param Ndirs: [-] Number of directions (must be odd)
        :return: Directional wave Spectrum
        """
        Rel_Dirs = self.equal_energy_directions(Ndirs)
        return self.directional_wave_spectrum(freqs, Rel_Dirs)

    def equal_energy_directional_spreading(self, Ndirs=None):
        """
        Compute directional wave spreading using equal energy directions.

        :param Ndirs: [-] Number of directions (must be odd)
        :param plot: plots the spectrum if True
        :return: Directional wave spreading
        """
        Rel_Dirs = self.equal_energy_directions(Ndirs)
        Sd = self.directional_spreading(Rel_Dirs)
        return Sd

    def directional_spreading(self, relative_dirs):
        """
        Compute directional spreading factors for the given directions.

        Function is based on the Cos^n function defined in the Orcaflex documentation.

        :param relative_dirs: [deg] list of wave directions relative to main direction (between -180 and 180 degrees).
        :param plot: True to plot directional spreading
        :return: [-] spreading factor corresponding to each direction
        """
        if np.any([relative_dirs < -180, relative_dirs > 180]):
            raise ValueError(
                f"Relative wave directions should be in the -180 to 180 degree range. \nReceived: {relative_dirs}"
            )

        relative_dirs, _ = xr.broadcast(relative_dirs, self.main_direction)

        # Compute spreading factor
        K = math.gamma(self.spreading / 2 + 1) / (np.sqrt(np.pi) * math.gamma(self.spreading / 2 + 1 / 2))
        Sd = K * np.power(np.cos(np.deg2rad(relative_dirs)), self.spreading)

        # Set directional spreading to 0 outside of +-90 deg range
        Sd = xr.where(relative_dirs < -90, 0, Sd)
        Sd = xr.where(relative_dirs > 90, 0, Sd)

        Dirs = wrap(relative_dirs + self.main_direction)
        Sd = Sd.assign_coords(Direction=Dirs)
        return Sd

    @staticmethod

    def shift_direction(wave_data, angle_shift):
        wave_data["Direction"] = wrap(wave_data["Direction"] + angle_shift)
        return wave_data

    def plot(self, freqs, Rel_Dirs, ax=None):
        Spectrum = self.directional_wave_spectrum(freqs, Rel_Dirs)
        self.plot(Spectrum, ax)

    @staticmethod
    def plot(Spectrum, ax=None):
        ax = ax or plt.figure().add_subplot(projection="3d")
        Data = Spectrum.squeeze().sortby(Spectrum.Direction)
        Data.plot.surface(ax=ax)
        # plt.ylabel('Wave direction [deg]')
        # plt.xlabel('Frequency [Hz]')
        plt.title("Directional wave spectrum: Main direction{}")
