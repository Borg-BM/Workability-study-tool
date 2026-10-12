"""
File to calculate workability of the BM Gangway installed on a vessel.

Rev | Author | Date     | Check | Changes
----|--------|----------|-------|-------
0   | XXX    | XX/XX/XX | XXX   | Initial version

"""

import matplotlib.pyplot as plt
import numpy as np
from PyBM.marine import Jonswap, MCG30MHIGHLOAD_Linear, MCG30MLOWLOAD_Linear, MCG30LHIGHLOAD_Linear, MCG30LLOWLOAD_Linear, MotionRAO
from PyBM.marine.workability import directional_workability
from PyBM.utils import VesselDimensions

"""
Note: There are several MCG (linear) classes available in PyBM for lifting purposes:
- MCG30MHIGHLOAD_Linear: for high load lifting (1000 kg)
- MCG30MLOWLOAD_Linear: for low load lifting (500 kg)
- MCG30LHIGHLOAD_Linear: for high load lifting with long boom (1000 kg)
- MCG30LLOWLOAD_Linear: for low load lifting with long boom (500 kg)

Please choose the appropriate one based on the lifting capacity needed.
"""

# # RAO/trace parameters 
vessel_name = "Kasteelborg" # Name of the vessel
loading_condition = "Draft_5.08" # Loading condition
# Revision = 1
# (OLD RAO IMPORTING METHOD - TO BE DEPRECATED)
# nc_file = MotionRAO.default_rao_path(vessel_name, Revision)
# rao = MotionRAO.load_rao(nc_file, loading_condition)

# NEW IMPORTING METHOD FOR RAOS
# This will load all available time traces from API (will trigger authentication flow, if needed)
rao = MotionRAO.from_api(vessel_name, loading_condition)
# Vessel parameters (for advanced plotting)
VESSELNAMEVessel = VesselDimensions(Length=82.5, Breadth=18.83, Depth=7.6, Draft=4.35)

# Machine parameters
pos = np.array([21.1, -2.32, 20.9])  # [m] position of the machine's center of slewing joint (MCGref) w.r.t APP/CL/K
Slewing_angle = 90  # [deg] Slewing angle of the MCG. Take note of the Conventions! (90deg PORT side, 270deg STARBOARD side)
Luffing_angle = 15  # [deg] luffing angle of the MCG. Take note of the Conventions!
dp_accuracy = 1  # [m] accuracy of the DP system
lifting_radius = 18  # [m] Lifting radius of the MCG30, used for workability calculations
gw_telescope_mean = lifting_radius/np.cos(np.radians(Luffing_angle))  # [m] Mean telescope length of the MCG30, used for workability calculations
# Setting up machine (MCG3.0)
pos_wrt_rao = pos - rao.origin
machine = MCG30MHIGHLOAD_Linear(pos_wrt_rao, Luffing_angle, Slewing_angle, dp_accuracy=dp_accuracy, gw_telescope_mean=gw_telescope_mean)
# Plotting machine onto the vessel. Use this to check position and conventions.
machine.plot(vessel=VESSELNAMEVessel, rao_origin=rao.origin)
plt.show()

# Sea state parameters
Tps = np.arange(6, 12, 1)  # [s] wave period
WaveDirs = np.arange(0, 360, 10)  # [deg] wave direction
spreading = 3  # [-] wave spreading
wave = Jonswap(1, Tps, main_direction=WaveDirs, spreading=spreading)

# Number of standard deviations for the workability limit
# For highload (1000 kg), keep it at 2.3 for engineered lifts
# For lowload (500 kg), keep it at 3
n_sigma = 2.3

# Compute workability
result = directional_workability(rao, wave, machine, standard_deviations=n_sigma)

## ---------------------------------------------
## ---------------- Polar Plots ----------------
plt.figure(figsize=(8, 12))
result.workability.plot_combined_workability(max_hs=3.0)
print(f"Workability for heading +/-30 deg: {result.sel(WaveDirection=[330,340,350,0,10,20,30]).min(['lim_type','Tp', 'WaveDirection'])}")
print(f"Workability for all headings: {result.min(['lim_type','Tp', 'WaveDirection'])}")
side = ""
if Slewing_angle == 90:
    side = " - Portside"
elif Slewing_angle == 270:
    side = " - Starboard side"
plt.suptitle(f"VESSEL NAME - Lifting Workability{side}", fontsize=16)
plt.gcf().legends[0].remove()  # Remove the legend to avoid clutter
plt.tight_layout()
# Save figure
# plt.savefig(f"Figures/Lifting/Lifting Workability VESSEL NAME{side} lift_radius{lifting_radius}.png")
plt.show()

## ---------------------------------------------------------------
## ---------------- Max Hs vs Tp workability plot ----------------
wave_dirs_to_plot = [180, 210, 150]  # Example: change as needed

# Define custom legend names for each wave direction
legend_names = {
    180: "Head seas (180°)",
    150: "-30° (150°)",
    210: "+30° (210°)"
}

plt.figure(figsize=(8, 5))
for wd in wave_dirs_to_plot:
    hs_vs_tp = result.sel(WaveDirection=wd)
    min_hs_per_tp = hs_vs_tp.min(dim='lim_type')
    plt.plot(
        min_hs_per_tp['Tp'],
        min_hs_per_tp.values,
        linestyle='-',
        linewidth=2,
        label=legend_names.get(wd, f'{wd}°')
    )
    # Print the minimum value for this line
    min_val = np.nanmin(min_hs_per_tp.values)
    min_tp = min_hs_per_tp['Tp'].values[np.nanargmin(min_hs_per_tp.values)]
    print(f"Wave Dir {wd}°: Min Hs = {min_val:.2f} m at Tp = {min_tp:.1f} s")

plt.xlabel('Tp [s]', fontsize=12)
plt.ylabel('Max Hs [m]', fontsize=12)
# Add side info to the title
side = ""
if Slewing_angle == 90:
    side = " (Portside operation)"
elif Slewing_angle == 270:
    side = " (Starboard side operation)"
plt.title(f'Max Hs vs Tp {side}', fontsize=14, fontweight='bold')
plt.ylim(0, 5)
plt.grid(True, linestyle='--', alpha=0.7)
plt.xticks(fontsize=11)
plt.yticks(fontsize=11)
plt.legend(title='Wave Direction', loc='upper right', fontsize=11, frameon=True)
plt.tight_layout()
# plt.savefig(f'Figures/Lifting/Lifting - Max Hs vs Tp {side}.png')
plt.show()

## --------------------------------------------------------------------------
## ----------- Multi Wave Directions Max Hs vs Tp (Appendices) --------------

# Determine side info for titles and filenames
side = ""
if Slewing_angle == 90:
    side = "Portside operation"
elif Slewing_angle == 270:
    side = "Starboard operation"

# Divide the wave directions into two groups for two figures, including 0 deg
wave_dirs = np.arange(0, 360, 10)  # 180 to 350
split_idx = len(wave_dirs) // 2
wave_dirs_groups = [wave_dirs[:split_idx], wave_dirs[split_idx:]]

for fig_idx, dirs in enumerate(wave_dirs_groups):
    n_plots = len(dirs)
    n_cols = 3
    n_rows = int(np.ceil(n_plots / n_cols))
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(8.27, 11.69))  # A4 size in inches (portrait)
    axes = axes.flatten()

    for idx, wd in enumerate(dirs):
        ax = axes[idx]
        hs_vs_tp = result.sel(WaveDirection=wd)
        min_hs_per_tp = hs_vs_tp.min(dim='lim_type')
        ax.plot(
            min_hs_per_tp['Tp'],
            min_hs_per_tp.values,
            linestyle='-',
            linewidth=2,
            color='tab:blue'
        )
        ax.set_title(f'Wave Dir: {wd}° ({side})', fontsize=8)
        ax.set_ylim(0, 3)
        ax.set_xlabel('Tp [s]')
        ax.set_ylabel('Max Hs [m]')
        ax.grid(True, linestyle='--', alpha=0.7)
        tp_vals = min_hs_per_tp['Tp'].values
        ax.set_xticks(tp_vals)
        ax.set_xticklabels([f"{tp:.0f}" for tp in tp_vals])
        ax.tick_params(axis='both', which='both', labelsize=10)

    # Hide any unused subplots
    for idx in range(n_plots, len(axes)):
        fig.delaxes(axes[idx])

    plt.tight_layout(rect=[0, 0, 1, 1]) # type: ignore
    # plt.savefig(f'Figures/Lifting/Lifting_Multi_WaveDirections_{fig_idx+1}_{side}.png')
    plt.show()