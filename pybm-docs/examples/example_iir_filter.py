"""Example of IIR filter design and filtering using PyBM.signal module."""

import matplotlib.pyplot as plt

import PyBM.signal  # Add multiply option to scipy TransferFunction class

# System parameters
fs = 100  # [Hz] Sampling frequency
freq_design = 1 / 6  # [Hz] Frequency at which to evaluate filter response


# -------------------------
# Design a Lowpass Butterworth filter
# -------------------------

LP_freq = 8  # [Hz] Low pass filter cutoff frequency
LP_order = 1  # [-] order of filter

# Create filter
LowPass = PyBM.signal.lowpass_iir(LP_freq, fs, order=LP_order)
mag, phase = LowPass.response_at_freqs([freq_design])
LPz_delay = -phase[0]  # [deg] phase delay at design frequency, delay is +

# print discrete low pass filter
print("---------\nButterworth low-pass filter Roll and Pitch")
print(f"Cut-off frequency: {LP_freq:.2f}Hz, filter order: {LP_order:.0f}")
print(f"Phase delay of low-pass filter at {1/freq_design:.2f}s: {LPz_delay:.1f}deg")

# plot filter response
LowPass.plot_response(Name="Low-pass")

# -------------------------
# Create Notch filter
# -------------------------

# Notch filter parameters (see https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.iirnotch.html#scipy.signal.iirnotch)
f_notch = 5  # [Hz] Notch frequency
Q = 1  # [-] Quality factor

Notch = PyBM.signal.notch_iir(f_notch, fs, quality=Q)
mag, phase = Notch.response_at_freqs([freq_design])
notch_delay = -phase[0]  # [deg] phase delay at design frequency, delay is +

print("---------\nNotch filter")
print(f"Notch Freq: {f_notch}Hz")
print(f"Phase delay of notch filter at {freq_design:.2f}Hz: {notch_delay:.2f}deg")
mag, phase = Notch.response_at_freqs([f_notch], db=False)
print(f"Magnitude of notch filter at {f_notch:.2f}Hz: {mag[0]:.2f}")
print(f"Notch filter:\n{Notch}")

# plot filter response
Notch.plot_response(Name="Notch")

# -------------------------
# Combine filters
# -------------------------
Total = LowPass * Notch
Total.plot_response(Name="Total")
plt.legend()
plt.show()
