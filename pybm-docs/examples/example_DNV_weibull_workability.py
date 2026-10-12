"""
Example: Using DNV Weibull parameters to generate scatter diagram and perform some analysis and visualization.

References:
    DNV-RP-C205 Environmental Conditions and Environmental Loads (2014-04)
    Appendix C, Table C-1 contains Weibull parameters for various global locations
"""

import matplotlib.pyplot as plt
import numpy as np
from PyBM.marine.weather_hindcast import Hindcast, DNVLoader
from PyBM.marine import Jonswap, T700, MotionRAO, directional_workability

# Example Weibull parameters for North Sea (Sector 11)
# These are illustrative values - consult DNV-RP-C205 Appendix B and C 
# for actual parameters for your specific location
weibull_params = {
    'alpha_s': 2.19,    # Weibull scale parameter for Hs
    'beta_s': 1.26,     # Weibull shape parameter for Hs
    'a1': 0.935,         # Conditional distribution parameter
    'a2': 0.222,         # Conditional distribution parameter  
    'b1': 0.1386,         # Conditional distribution parameter
    'b2': -0.0208,        # Conditional distribution parameter
    'a0': 0.7,         # Default conditional distribution parameter
    'b0': 0.07,        # Default conditional distribution parameter
    'gamma_s': 0.0     # Location parameter (typically 0)
}

# Optional: Define custom bin ranges for Hs and Tp
# If not provided, defaults to Hs: 0.5-10.5m (0.5m steps), Tp: 1-20s (1s steps)
custom_Hs_bins = np.arange(0.5, 8.0, 0.5)  # Up to 8m in 0.5m increments
custom_Tp_bins = np.arange(2.0, 16.0, 1.0)  # 2-15s in 1s increments

# Create DNV loader with Weibull parameters
loader = DNVLoader(
    **weibull_params,
    Hs_bins=custom_Hs_bins,
    Tp_bins=custom_Tp_bins
)

# Create Hindcast object (automatically generates scatter table)
hindcast = Hindcast(loader)

# ====================================
# Typical HindcastScatterTable Usage
# ====================================

# 1. Get Hs statistics (only 'overall' available for scatter table data)
print("\n=== Hs Statistics ===")
hs_stats_df, ax = hindcast.get_Hs_stats(period='overall', plot=True, min_span=1.0, n_bins=5)
plt.show()

# 2. Get Tp statistics (only 'overall' available for scatter table data)
print("\n=== Tp Statistics ===")
tp_stats_df = hindcast.get_Tp_stats(period='overall', plot=True, min_span=2.0, n_bins=10)
plt.show()

# 3. Plot Hs vs Tp joint occurrence (heatmap from scatter table). Optionally, overlay workability limit curve if available (see at the end).
print("\n=== Plotting Hs-Tp Joint Occurrence ===")
ax = hindcast.plot_Hs_Tp()
plt.show()

# 4. Calculate workability percentage (requires workability result from workability analysis)
# You can load a workability result. We generate a dummy workability example here.
Tp = np.arange(2, 16, 1)
WaveDirs = np.arange(0, 360, 10)
wave = Jonswap(1, Tp, main_direction=WaveDirs, spreading=10)
rao = MotionRAO.from_api("FPW", "FULLLOAD") # example RAO loading
machine = T700(np.array([35.0, 3.1, 6.10 + 3.65]) - rao.origin, 0)
workability_result = directional_workability(rao, wave, machine)
workability_result = workability_result.min(["lim_type", "WaveDirection"])

# Calculate overall workability percentage (only 'overall' available for scatter table)
workability_overall = hindcast.get_workability_percentage(workability_result, period='overall')
print(f"\nOverall workability: {workability_overall:.2f}%")

# Plot Hs vs Tp with workability limit curve overlaid
print("\n=== Plotting Hs-Tp with Workability Limit ===")
ax = hindcast.plot_Hs_Tp(workability_result=workability_result)
plt.show()
