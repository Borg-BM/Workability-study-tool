""" Example usage of the motion analysis tools in frequency domain. """

import matplotlib.pyplot as plt
import numpy as np
import xarray as xr

from PyBM.marine import Jonswap, MotionRAO, compute_mpe

# RAO importing
vessel_name = "FPW"
loading_condition = "FULLLOAD"
# Revision = 1
# OLD RAO IMPORTING METHOD (TO BE DEPRECATED)
# nc_file = MotionRAO.default_rao_path(vessel_name, Revision)
# rao = MotionRAO.load_rao(nc_file, loading_condition)

# NEW IMPORTING METHOD FOR RAOS
# This will load all available time traces from API (will trigger authentication flow, if needed)
rao = MotionRAO.from_api(vessel_name, loading_condition)

# Define Wave Conditions
Hs = 2.0  # Significant wave height [m]
Tp = 8.0  # Peak wave period [s]
WaveDir = 0.0  # Wave direction [degrees]
wave = Jonswap(Hs, Tp, WaveDir, spreading=8)

# Compute the response
poi = [0, 0, 0]  # Point of interest [m] [x,y,z] w.r.t. to the RAO origin
mpe = compute_mpe(wave, rao, poi=poi)
print(f"\nMPE Heave: {mpe['POS'].sel(DOF='Z').values} [m]")

# Parameters can be defined using arrays so that several conditions are computed at once
Hs = 2.0  # Significant wave height [m]
Tps = np.arange(5, 15, 1)  # Peak wave period [s]
WaveDirs = np.arange(0, 360, 10)  # Wave direction [degrees]
wave = Jonswap(Hs, Tps, WaveDirs, spreading=8)
mpe = compute_mpe(wave, rao, poi=poi)
# Maximum heave response over all wave directions and periods
max_heave = mpe["POS"].sel(DOF="Z").max(dim=["WaveDirection", "Tp"])

# Plot the heave response for various wave directions
WaveDir = np.arange(0, 360, 15)
wave = Jonswap(Hs, Tp, WaveDir, spreading=8)
mpe = compute_mpe(wave, rao, poi=poi)
mpe["POS"].sel(DOF="Z").squeeze().plot.line(x="WaveDirection")
plt.show()
