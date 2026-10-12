"""
File to calculate workability of the BM Gangway installed on a vessel.

Rev | Author | Date     | Check | Changes
----|--------|----------|-------|-------
0   | XXX    | XX/XX/XX | XXX   | Initial version

"""

import matplotlib.pyplot as plt
import numpy as np
from PyBM.marine import Jonswap, MCG30MTRANSFER_Linear, MotionRAO
from PyBM.marine.workability import directional_workability
from PyBM.utils import VesselDimensions

"""
Note: There are several MCG (linear) classes available in PyBM for transfer purposes:
- MCG30MTRANSFER_Linear: for transfer
- MCG30MTIPLADDER_Linear: for transfer with tip ladder
- MCG30LTRANSFER_Linear: for transfer with long boom
- MCG30LTIPLADDER_Linear: for transfer with long boom and tip ladder

Please choose the appropriate one based on the transfer configuration needed.
"""

# # RAO/trace parameters 
vessel_name = "VESSEL_NAME" # Name of the vessel
loading_condition = "loading_condition_name" # Loading condition
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
Slewing_angle = 270  # [deg] Slewing angle of the MCG. Take note of the Conventions! (90deg PORT side, 270deg STARBOARD side)
Luffing_angle = 0  # [deg] luffing angle of the MCG. Take note of the Conventions!
dp_accuracy = 1  # [m] accuracy of the DP system
# Setting up machine (MCG3.0)
pos_wrt_rao = pos - rao.origin
machine = MCG30MTRANSFER_Linear(pos_wrt_rao, Luffing_angle, Slewing_angle, dp_accuracy=dp_accuracy)
# Plotting machine onto the vessel. Use this to check position and conventions.
machine.plot(vessel=VESSELNAMEVessel, rao_origin=rao.origin)
plt.show()

# Sea state parameters
Tps = np.arange(6, 12, 1)  # [s] wave period
WaveDirs = np.arange(0, 360, 10)  # [deg] wave direction
spreading = 3  # [-] wave spreading
wave = Jonswap(1, Tps, main_direction=WaveDirs, spreading=spreading)

# Compute workability
result = directional_workability(rao, wave, machine)

## ---------------------------------------------
## ---------------- Polar Plots ----------------
plt.figure(figsize=(8, 12))
result.workability.plot_combined_workability(max_hs=4.0)
side = ""
if Slewing_angle == 90:
    side = " - Portside"
elif Slewing_angle == 270:
    side = " - Starboard side"
plt.suptitle(f"VESSEL NAME - Personnel Transfer Workability{side}", fontsize=16)
plt.gcf().legends[0].remove()  # Remove the legend to avoid clutter
plt.tight_layout()
# Save figure
# plt.savefig(f"Figures/Transfer/Personnel Transfer Workability VESSEL NAME{side}.png")
plt.show()

## ---------------------------------------------------------------
## ---------------- Max Hs vs Tp workability plot ----------------
wave_dirs_to_plot = [180, 210, 150]  # Example: change as needed

# Define custom legend names for each wave direction
legend_names = {
    180: "Head seas (180°)",
    210: "+30° (210°)",
    150: "-30° (150°)",
}

plt.figure(figsize=(8, 5))
for wd in wave_dirs_to_plot:
    hs_vs_tp = result.sel(WaveDirection=wd)
    min_hs_per_tp = hs_vs_tp.min(dim='lim_type')
    tp_vals = min_hs_per_tp['Tp'].values
    hs_vals = min_hs_per_tp.values

    plt.plot(
        tp_vals,
        hs_vals,
        linestyle='-',
        linewidth=2,
        label=legend_names.get(wd, f'{wd}°')
    )
    # Print the minimum value for this line
    min_val = np.nanmin(hs_vals)
    min_tp = tp_vals[np.nanargmin(hs_vals)]
    print(f"direction {wd}: {min_val:.1f}m Hs @ Tp = {min_tp:.0f}s")

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
# plt.savefig(f'Figures/Transfer/Transfer - Max Hs vs Tp {side}.png')
plt.show()

## --------------------------------------------------------------------------
## ----------- Multi Wave Directions Max Hs vs Tp (Appendices) --------------

# Determine side info for titles and filenames
side = ""
if Slewing_angle == 90:
    side = "Portside operation"
elif Slewing_angle == 270:
    side = "Starboard operation"

# Move 0 degree to the end of the array
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
        ax.set_ylim(0, 5)
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
    # plt.savefig(f'Figures/Transfer/Transfer_Multi_W¿aveDirections_{fig_idx+1}_{side}.png')
    plt.show()