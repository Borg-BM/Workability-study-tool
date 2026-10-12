"""
Example: Loading hindcast time series data from Excel or CSV file and perform some analysis and visualization.

File Format Requirements:
    - Use the template file format: HindcastTimeSeries_template.csv
    - All data in the first sheet
    - Headers in the first row, in the following order: Date, Hs, Tp
    - Date column must be in a consistent format (see date_format parameter)
"""

import matplotlib.pyplot as plt
import os
import numpy as np
from pathlib import Path
from PyBM.marine.weather_hindcast import Hindcast, ExcelTimeSeriesLoader
from PyBM.marine import Jonswap, T700, MotionRAO, directional_workability

# Path to your Excel or CSV file
# Use the template file as a reference for the expected format
file_path = os.path.dirname(__file__) + "\HindcastTimeSeries_template.csv"  # or .xls, .xlsx

# Date format in the file (adjust if your file uses a different format)
# Common formats:
#   '%m/%d/%Y %H:%M'  - Example: 01/15/2020 14:30
#   '%Y-%m-%d %H:%M:%S' - Example: 2020-01-15 14:30:00
#   '%d-%m-%Y %H:%M'  - Example: 15-01-2020 14:30
date_format = '%m/%d/%Y %H:%M'

# Create Excel time series loader
loader = ExcelTimeSeriesLoader(
    file_path=file_path,
    date_format=date_format
)

# Create Hindcast object (automatically loads and processes data)
hindcast = Hindcast(loader)

# ==================================
# Typical HindcastTimeSeries Usage
# ==================================

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
