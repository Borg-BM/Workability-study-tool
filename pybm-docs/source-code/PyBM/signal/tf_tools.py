"""
Tools to augment Scipy.signal.TransferFunction function class.

Date: 24-11-2023
Author: CBR
Check: ---
"""

import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as spsig
from numpy.polynomial import Polynomial

def check_sample_times(tf1: spsig.TransferFunction, tf2: spsig.TransferFunction):
    if tf1.dt != tf2.dt:
        raise ValueError(
            f"Trying to perform math operation on discrete TFs with different sample times: tf1={tf1.dt}s and tf2={tf2.dt}s"
        )

def TF_multiply(tf1: spsig.TransferFunction, tf2):
    if isinstance(tf2, spsig.TransferFunction):
        check_sample_times(tf1, tf2)
        b = Polynomial(tf1.num) * Polynomial(tf2.num)
        a = Polynomial(tf1.den) * Polynomial(tf2.den)
        return spsig.TransferFunction(b.coef, a.coef, dt=tf1.dt)
    return spsig.TransferFunction(tf1.num * tf2, tf1.den, dt=tf1.dt)

def TF_divide(tf1: spsig.TransferFunction, tf2):
    if isinstance(tf2, spsig.TransferFunction):
        check_sample_times(tf1, tf2)
        b = Polynomial(tf1.num) * Polynomial(tf2.den)
        a = Polynomial(tf1.den) * Polynomial(tf2.num)
        return spsig.TransferFunction(b.coef, a.coef, dt=tf1.dt)
    return spsig.TransferFunction(tf1.num / tf2, tf1.den, dt=tf1.dt)

def TF_equals(tf1: spsig.TransferFunction, tf2):
    return np.allclose(tf1.num, tf2.num) and np.allclose(tf1.den, tf2.den) and np.allclose(tf1.dt, tf2.dt)

def print_TF(self):
    """Return string of TF coefficients.

    :rtype: str
    """
    st = ""
    for i, b in enumerate(self.num):
        st += f"b{i} = {b}\n"
    for i, a in enumerate(self.den):
        st += f"a{i} = {a}\n"
    return st

def response_at_freqs(tf: spsig.TransferFunction, freqs, db=True):
    """Compute magnitude and phase at given frequency points

    :param tf: Transfer Function
    :type tf: spsig.TransferFunction
    :param freqs: [Hz] Frequency points
    :type freqs: array-like
    :param db: True to return Decibels False to return absolute values, defaults to True
    :type db: bool, optional
    :return: tuple (magnitude, phase)
        WHERE
        array mag is mgnitude [db or abs]
        array phase [deg]
    """
    __, h = spsig.freqz(tf.num, tf.den, worN=freqs, fs=1 / tf.dt)
    mag = np.abs(h)
    if db:
        mag = 20 * np.log10(mag)
    phase = np.rad2deg(np.angle(h))
    return mag, phase

def plot_response(
    tf: spsig.TransferFunction,
    Name: str = "IIR Filter",
    freq_range=(1 / 50, 50),
    mag_ylim=(-15, 5),
    db=True,
):
    """Plot the frequency response of a Transfer function

    :param tf: Transfer Function
    :type tf: spsig.TransferFunction
    :param Name: Name of function
    :type Name: str
    :param db: Use decibels or absolut magnitude
    :type db: bool
    """
    freqs = np.logspace(np.log10(freq_range[0]), np.log10(freq_range[1]), 1000)
    mag, phase = tf.response_at_freqs(freqs, db=db)
    ax1 = plt.subplot(2, 1, 1)
    ax1.semilogx(freqs, mag)
    ax1.set_ylim(mag_ylim) if db else 0
    ax1.set_title("Bode Plot")
    ax1.set_ylabel(f"Amplitude ({'dB' if db else 'abs'})")
    ax1.grid(True)
    ax2 = plt.subplot(2, 1, 2)
    ax2.semilogx(freqs, phase, label=Name)
    ax2.set_ylim([-30, 10])
    ax2.set_ylabel("Angle (degrees)")
    ax2.set_xlabel("Frequency (Hz)")
    ax2.grid(True)

spsig.TransferFunction.__mul__ = TF_multiply
spsig.TransferFunction.__truediv__ = TF_divide
spsig.TransferFunction.__eq__ = TF_equals
spsig.TransferFunction.__str__ = print_TF
spsig.TransferFunction.response_at_freqs = response_at_freqs
spsig.TransferFunction.plot_response = plot_response
