import numpy as np
import xarray as xr

def unwrap_angle(angle):
    """Make sure angle is between 0 and 360.

    :param angle: [deg] angle
    """
    return angle % 360

def amp_phase_to_complex(amp, phase):
    """Convert amplitude / phase representation to complex number

    :param amp: Amplitude
    :param phase: [deg] Phase
    :rtype: Complex
    """
    return amp * (np.cos(np.deg2rad(phase)) + 1j * np.sin(np.deg2rad(phase)))

def disc_area(diameter):
    """Return area from diameter.

    :param diameter: Diamter of disc
    :return: Area of disc
    """
    return 0.25 * np.pi * np.square(diameter)

def complex_max(data: xr.Dataset, dim):
    return data[np.abs(data).argmax(dim=dim)]

def delta(steps: np.ndarray) -> np.ndarray:
    """Return array of differences, the first value will be 0 to conserve the length.

    :param steps: Array of values
    :type steps: np.ndarray
    :return: Array off diferences
    :rtype: np.ndarray
    """
    diff = np.zeros(len(steps))
    diff[1:] = steps[1:] - steps[:-1]
    return diff

def component_absolute(x):
    """Take the absolute value of the real and imaginary part separatly.

    :param x: Complex number
    """
    return np.abs(np.real(x)) + np.abs(np.imag(x)) * 1j

def absolute_sum(a, b):
    """Sum complex numbers as absolute values (to include phase information), for example to get flow from 2 complex velocity signals.
    WARNING: only resulting amplitude is meaningfull.

    :param a: Complex component
    :param b: Complex component
    :return: Magnitude of sum of absolute values. Equivalent to time based: max(abs(signal_a) + abs(signal_b)))
    """
    return np.abs(component_absolute(a) + component_absolute(b))

def differentiate(rao, freqs):
    """Take the derivate of RAO data

    :param rao: Motion RAO
    :param freqs: [Hz] Frequencies corresponding to the data points
    :return: Time derivative of the data
    """
    return rao * freqs * 2 * np.pi * 1j
