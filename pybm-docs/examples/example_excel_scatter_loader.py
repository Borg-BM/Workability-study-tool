"""
Example: Loading hindcast scatter table data from Excel file and perform some analysis and visualization.

File Format Requirements:
    - Use the template file format: HindcastScatterTable_template.xlsx
    - Sheet name: 'Hs-Tp' (Hs in rows, Tp in columns) or 'Tp-Hs' (Tp in rows, Hs in columns)
    - Cell A22 must indicate 'relative' (probabilities) or 'absolute' (counts)
    - Bin structure follows the template format
"""

import matplotlib.pyplot as plt
import os
import numpy as np
from pathlib import Path
from PyBM.marine.weather_hindcast import Hindcast, ExcelScatterLoader
from PyBM.marine import Jonswap, T700, MotionRAO, directional_workability

# Path to your Excel scatter table file
# Use the template file as a reference: HindcastScatterTable_template.xlsx
file_path = os.path.dirname(__file__) + "\HindcastScatterTable_template.xlsx"
# Sheet name options:
#   'Hs-Tp': Hs values in rows, Tp values in columns (most common)
#   'Tp-Hs': Tp values in rows, Hs values in columns
sheet_name = 'Hs-Tp'

# Create Excel scatter loader
loader = ExcelScatterLoader(file_path=file_path, sheet_name=sheet_name)

# Create Hindcast object (automatically loads and processes data)
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
