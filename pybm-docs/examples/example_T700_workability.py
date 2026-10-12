""" Example usage of the workability tools for a T700 machine.

References:
[1] BM-OP970-EN-2006A-Rev0 T700 Holding Load Chart Vineyard validation OLC-1.xlsx (Sheet: Input Reference Systems)

"""

import matplotlib.pyplot as plt
import numpy as np

from PyBM.marine import T700, Jonswap, MotionRAO, directional_workability

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

# Machine
pos = np.array([35.0, 3.1, 6.10 + 3.65])  # [m] position of the machine w.r.t APP/CL/K
pos_wrt_rao = pos - rao.origin
orientation_T700 = 0  # [deg] yaw orientation of the machine w.r.t RAO definitions [1]
machine = T700(pos_wrt_rao, orientation_T700, 35e6)

# Sea state parameters
Tps = np.arange(6, 12, 1)  # [s] wave period
WaveDirs = np.arange(0, 360, 10)  # [deg] wave direction
spreading = 5  # [-] wave spreading
wave = Jonswap(1, Tps, main_direction=WaveDirs, spreading=spreading)

# Compute workability
result = directional_workability(rao, wave, machine)

## ---------------------------------------------
## ---------------- Polar Plots ----------------
plt.figure(figsize=(8, 12))
result.workability.plot_combined_workability(max_hs=4.0)
plt.suptitle("T700 Workability on Marmac400")
# plt.savefig("Figures/Workability.png")
plt.show()

## ---------------------------------------------------------------
## ---------------- Max Hs vs Tp workability plot ----------------
wave_dirs_to_plot = [180, 210, 150]  # Example: change as needed
legend_names = {
    180: "Head seas (180°)",
    210: "+30° (210°)",
    150: "-30° (150°)",
}
plt.figure(figsize=(8, 5))
for wd in wave_dirs_to_plot:
    hs_per_tp = result.min(dim="lim_type").sel(WaveDirection=wd)
    tp_vals = hs_per_tp['Tp'].values
    hs_vals = hs_per_tp.values
    plt.plot(
        tp_vals,
        hs_vals,
        linestyle='-',
        linewidth=2,
        label=legend_names[wd]
    )
    # Print minimum workability for this line
    print(f"Direction {wd}°: {np.nanmin(hs_vals):.1f} m Hs @ Tp = {tp_vals[np.nanargmin(hs_vals)]:.0f} s")
plt.xlabel('Tp [s]', fontsize=12)
plt.ylabel('Max Hs [m]', fontsize=12)
plt.title(f'Max Hs vs Tp', fontsize=14, fontweight='bold')
plt.ylim(0, 5)
plt.grid(True, linestyle='--', alpha=0.7)
plt.xticks(fontsize=11)
plt.yticks(fontsize=11)
plt.legend(title='Wave Direction', loc='lower left', fontsize=11, frameon=True)
plt.tight_layout()
# plt.savefig(f'Figures/Max Hs vs Tp.png')
plt.show()

## --------------------------------------------------------------------------
## ----------- Multi Wave Directions Max Hs vs Tp (Appendices) --------------
wave_dirs = np.arange(0, 360, 10) 
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
        ax.set_title(f'Wave Dir: {wd}°', fontsize=8)
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
    # plt.savefig(f'Figures/Multi_WaveDirections_{fig_idx+1}.png')
    plt.show()
