"""
Module to calculate vessel motions in the frequency domain.

CBR 21-06-2023

References:
 [1] Offshore Hydromechanics, J.M.J. Journée and W.W. Massie
"""

import numpy as np

from PyBM import OutofBoundsError
from PyBM.marine.motion_analysis import RAO
from PyBM.marine.wave_spectrum import WaveSpectrum

def compute_response(wave: WaveSpectrum, rao: RAO, poi=None, Nfreqs=200, f_bounds=None):
    """
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
    """
    if not (poi is None):
        assert len(poi) == 3, "POI must be a list of 3 coordinates [x,y,z] in meters."
        rao = rao.translate_rao(poi)
    if wave.spreading > 0:
        rao = apply_directional_spreading(wave, rao)
    else:
        rao = rao.interp(Direction=wave.main_direction)
    rao = equal_energy_freqs_rao(wave, rao, Nfreqs, f_bounds)
    Resp = (np.square(wave.Hs) / (16 * Nfreqs)) * np.square(np.abs(rao))
    if wave.spreading > 0:
        Resp = Resp.sum(dim="Direction") / len(Resp.Direction)
    return Resp

def compute_mpe(wave: WaveSpectrum, rao: RAO, poi=None, storm_duration=10800, transfer_function=None):
    """
    Calculate MPE of the given parameter for all points of interest (POI).

    :param poi: [m] (x,y,z) offset of point of interest
    :param storm_duration: [s] duration of the period of interest (usually 3 hours)
    :param transfer_function: ([[a], [b]]) Numerator and Denumerator of continuous transfer function to be applied.
    :return: Statistical extreme value

    """
    response = compute_response(wave, rao, poi)
    # if not (transfer_function is None):
    #     response = frequency_response(response, transfer_function)
    return response.spectral_equal_energy.MPE(storm_duration)

def equal_energy_freqs_rao(wave: WaveSpectrum, rao: RAO, Nfreqs, f_bounds=None):
    if f_bounds is None:
        f_bounds = (rao.Frequency[0], rao.Frequency[-1])
    freqs = wave.equal_energy_frequencies(f_bounds, Nfreqs=Nfreqs)
    if (freqs.isel(Frequency=0) < rao.Frequency[0]).any() or (freqs.isel(Frequency=-1) > rao.Frequency[-1]).any():
        raise OutofBoundsError("wave frequency bounds out of bounds for the vessel RAO")
    return rao.interp(Frequency=freqs, assume_sorted=True)

# def frequency_response(response, transfer_function):
#     tf = sig.TransferFunction(transfer_function[0], transfer_function[1])
#     w = response.Frequency.values * 2 * np.pi
#     w, H = sig.freqresp(tf, w)
#     H = xr.DataArray(H, coords=[response.Frequency.values], dims="Frequency")
#     freq_response = H * response
#     return freq_response

def apply_directional_spreading(wave: WaveSpectrum, rao: RAO):
    wave_dirs = wave.abs_directions(wave.equal_energy_directions())
    rao = rao.interp(Direction=wave_dirs)
    return rao
