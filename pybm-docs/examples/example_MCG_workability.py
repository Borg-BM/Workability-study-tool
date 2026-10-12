""" File to calculate workability of the BM Gangway installed on a vessel, using time traces."""

import matplotlib.pyplot as plt
import numpy as np

from PyBM.marine import Jonswap, MCG30MTRANSFER_Nonlinear, TimeDomain
from PyBM.marine.workability import directional_workability_timetrace
from PyBM.utils import VesselDimensions

# RAO/trace parameters
Revision = 1
vessel_name = "Sartor"

# Vessel parameters (for advanced plotting)
SartorVessel = VesselDimensions(Length=82.5, Breadth=18.83, Depth=7.6, Draft=4.35)

# Machine parameters
pos = np.array([35.0, 3.1, 6.3 + 1.2])  # [m] position of the machine's center of slewing joint (MCGref) w.r.t APP/CL/K
Slewing_angle = 90  # [deg] Slewing angle of the MCG. Take note of the Conventions! (90deg PORT side, 270deg STARBOARD side)
Luffing_angle = 0  # [deg] luffing angle of the MCG. Take note of the Conventions!
dp_accuracy = 0.5  # [m] accuracy of the DP system

# Sea state parameters
Tps = np.arange(7, 10, 1)  # [s] wave period

# This will load all available time traces, either .nc, if present, or .mat.
trace = TimeDomain.load_all_default_time_traces(vessel_name, Revision)
trace = trace.sel(Tp=Tps)  # Select chosen wave periods

# define pos wrt trace
pos_wrt_trace = pos - trace.origin

# Loading RAO, setting up machine (MCG3.0)
machine = MCG30MTRANSFER_Nonlinear(pos_wrt_trace, Luffing_angle, Slewing_angle, dp_accuracy=dp_accuracy)
# Plotting machine onto a vessel (sartor). Use this to check position and conventions.
machine.plot(vessel=SartorVessel, rao_origin=trace.origin)
plt.show()

# Compute workability
result = directional_workability_timetrace(trace, machine, stdevs=3.7)
result.workability.plot_detailed_workability(max_hs=4)
plt.suptitle("MCG30 Workability on Sartor")
# plt.savefig("workability.png")
plt.show()
