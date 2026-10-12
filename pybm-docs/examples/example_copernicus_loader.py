"""
Example: Loading hindcast data from Copernicus Marine Service. Perform some analysis and visualization.
"""

import matplotlib.pyplot as plt
import numpy as np
from PyBM.marine.weather_hindcast import Hindcast, CopernicusLoader
from PyBM.marine import Jonswap, T700, MotionRAO, directional_workability

# Define location coordinates
# Example: North Sea location
lat = 54.0   # Latitude (decimal degrees, positive = North)
long = 3.0   # Longitude (decimal degrees, positive = East)

# Define time period (optional, defaults to all available data if not set)
start_date = '2020-01-01'  # Start date in 'YYYY-MM-DD' format
end_date = '2020-12-31'    # End date in 'YYYY-MM-DD' format

# Select product (dataset) from Copernicus Marine Service
# Available products:
#   0: Global Ocean Waves Reanalysis (default, 0.2° resolution, 3-hourly)
#   1: Arctic Ocean Wave Hindcast (3km resolution, hourly)
#   2: Baltic Sea Wave Hindcast (hourly)
#   3: Black Sea Waves Reanalysis (2.5km resolution, hourly)
#   4: Atlantic (Iberian/Biscay/Irish) Ocean Wave Reanalysis (0.027° resolution, hourly)
#   5: Mediterranean Sea Waves Reanalysis (hourly)
#   6: Atlantic (European North West Shelf) Wave Physics Reanalysis (hourly)
product_id = 6 # Since it is a North Sea location

# Create Copernicus loader
loader = CopernicusLoader(
    lat=lat,
    long=long,
    product_id=product_id,
    start_date=start_date,
    end_date=end_date
)

# Create Hindcast object (automatically fetches and processes data)
hindcast = Hindcast(loader)

# =================================
# Typical HindcastTimeSeries Usage
# =================================

# 1. Get Hs statistics - overall and monthly
print("\n=== Hs Statistics ===")
hs_stats_overall = hindcast.get_Hs_stats(period='overall')
print("\nOverall Hs distribution:")
print(hs_stats_overall)

hs_stats_monthly = hindcast.get_Hs_stats(period='monthly', plot=True)
plt.show()

# 2. Get Tp statistics - overall and monthly
print("\n=== Tp Statistics ===")
tp_stats_overall = hindcast.get_Tp_stats(period='overall')
print("\nOverall Tp distribution:")
print(tp_stats_overall)

tp_stats_monthly = hindcast.get_Tp_stats(period='monthly', plot=True)
plt.show()

# 3. Plot Hs vs Tp joint occurrence (2D histogram). Optionally, overlay workability limit curve if available (see at the end).
print("\n=== Plotting Hs-Tp Joint Occurrence ===")
ax = hindcast.plot_Hs_Tp(n_bins_hs=50, n_bins_tp=50)
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

# Calculate overall workability percentage
workability_overall = hindcast.get_workability_percentage(workability_result, period='overall')
# Calculate monthly workability percentage
workability_monthly = hindcast.get_workability_percentage(workability_result, period='monthly')

# Plot monthly workability percentages
fig, ax = plt.subplots(figsize=(8, 6))
workability_monthly.plot.bar(legend=False, ax=ax, color=tuple(np.array([0,173,239])/255), alpha=0.7)
ax.set_xlabel('Month', fontsize=12)
ax.set_ylabel('Workability Percentage [%]', fontsize=12)
ax.set_yticks(np.arange(0, 101, 20))
ax.grid(axis='y', color='lightgray')
ax.set_title(
    f"Monthly Workability: {workability_overall:.2f}%",
    fontsize=14,
    fontweight='bold'
)
plt.show()

# Plot Hs vs Tp with workability limit curve overlaid
print("\n=== Plotting Hs-Tp with Workability Limit ===")
ax = hindcast.plot_Hs_Tp(n_bins_hs=50, n_bins_tp=50, workability_result=workability_result)
plt.show()
