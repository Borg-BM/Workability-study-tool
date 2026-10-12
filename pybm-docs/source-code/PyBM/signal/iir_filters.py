"""
This module contains the tools to create IIR filters.
"""
import numpy as np
from scipy import signal

import PyBM.signal.tf_tools

# def tf_decorator(func):
#     """Decorator to convert the output of the function to a TransferFunction object."""

#     def wrapper(*args, **kwargs):
#         z_b, z_a = func(*args, **kwargs)
#         return signal.TransferFunction(z_b, z_a, dt=1 / kwargs["fs"])

#     return wrapper

# # Decorate the scipy functions
# butter = tf_decorator(signal.butter)
# iirnotch = tf_decorator(signal.iirnotch)

def get_delay_at_freq(filter, freq):
    """
    Get the phase delay at a specific frequency for a given filter.
    :param filter: The filter to analyze.
    :param freq: The frequency at which to evaluate the filter.
    :return: The delay at the specified frequency.
    """
    _, phase = filter.response_at_freqs([freq])
    return -phase[0]

def lead_iir(phase, freq, fs):
    """
    Design a lead IIR filter.
    :param phase: Maximum phase angle of lead filter in degrees.
    :param freq: Frequency where lead filter has maximum phase angle in Hz.
    :param fs: Sampling frequency in Hz.
    """

    freq_Lead = freq  # [Hz] Frequency where lead filter has max phase angle
    freq_unity_gain = freq  # [Hz] Frequency where lead filter has unity gain
    # Calculate ratio between lead time constants from maximum phase angle
    # Source: Franklin, G. F., Powell, J. D. and Emami-Naeini, A. -
    # Feedback control of dynamic systems. New Jersey: Prentice-Hall, 2002
    tau_ratio = (1 + np.sin(np.deg2rad(phase))) / (1 - np.sin(np.deg2rad(phase)))
    tau_den = 1 / (freq_Lead * 2 * np.pi * np.sqrt(tau_ratio))  # Time constant of denominator

    # Lead filter continuous tranfer function
    lead_b = [tau_ratio * tau_den, 1]
    lead_a = [tau_den, 1]
    leadZ_b, LeadZ_a, dt = signal.cont2discrete((lead_b, lead_a), dt=1 / fs, method="tustin")
    Lead = signal.TransferFunction(leadZ_b, LeadZ_a, dt=dt)
    mag, phase = Lead.response_at_freqs([freq_unity_gain], db=False)
    return Lead / mag

def lowpass_iir(cutoff, fs, order=1):
    """
    Design a lowpass IIR filter.
    :param cutoff: Cutoff frequency of the filter in Hz.
    :param fs: Sampling frequency in Hz.
    :param order: Order of the filter.
    """

    # Create filter
    LPz_b, LPz_a = signal.butter(order, cutoff, "low", fs=fs)
    LowPass = signal.TransferFunction(LPz_b, LPz_a, dt=1 / fs)
    return LowPass

def notch_iir(freq, fs, quality=30):
    """
    Design a notch IIR filter.
    :param freq: Center frequency of the notch filter in Hz.
    :param fs: Sampling frequency in Hz.
    :param quality: Quality factor of the filter.
    """

    # Create filter
    NZ_b, NZ_a = signal.iirnotch(freq, quality, fs=fs)
    Notch = signal.TransferFunction(NZ_b, NZ_a, dt=1 / fs)
    return Notch

# notch_b = [1 / (2 * np.pi * f1) ** 2, (2 * beta1) / (2 * np.pi * f1), 1]
# notch_a = [1 / (2 * np.pi * f2) ** 2, (2 * beta2) / (2 * np.pi * f2), 1]
