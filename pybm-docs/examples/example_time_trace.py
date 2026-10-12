""" Example usage of the motion analysis tools in time domain. """

import os

import matplotlib.pyplot as plt
import numpy as np
import xarray as xr

from PyBM.marine import Jonswap, MotionRAO, TimeDomain

# RAO importing
vessel_name = "FPW"
loading_condition = "FULLLOAD"
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

# Generate time traces
dt = 0.1  # Time step [s]
duration = 3 * 60 * 60  # Duration of time trace [s]
folder = "Traces"
time_domain = TimeDomain(wave=wave, rao=rao, vesselCoG=[0, 0, 0])
time_domain.generate_time_traces(folder, dt, duration, wave)
