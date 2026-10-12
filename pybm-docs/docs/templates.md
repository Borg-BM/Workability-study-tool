<!-- Source: https://docs.app.barge-master.com/templates.html -->

# Templates

All examples below are available in the templates folder of the repository.

## Motion Analysis

The Motion Analysis tools are largely based on the [Xarray](https://docs.xarray.dev/en/stable/) package, check their docs for details about usage. Theory behind the Motion Analysis tools can be found in the [Theory section](theory.md#theory).

### Frequency domain

[`Download example script file`](../examples/example__frequency_domain.py) (right-click and “Save link as…”)

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

### Time trace generation

[`Download example script file`](../examples/example_time_trace.py) (right-click and “Save link as…”)

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

## Workability

### MCG Linear Workability (Commercial)

#### MCG for Personnel Transfer

[`Download example script file`](../examples/BM_OPXXXX_VESSEL_NAME_Workability_Transfer_Rev0.py) (right-click and “Save link as…”)

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

#### MCG for Lifting Operations

[`Download example script file`](../examples/BM_OPXXXX_VESSEL_NAME_Workability_Lifting_Rev0.py) (right-click and “Save link as…”)

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

### MCG Nonlinear Workability

Use this class only if there are time traces of the vessel motions available.

[`Download example script file`](../examples/example_MCG_workability.py) (right-click and “Save link as…”)

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

### T700 Workability

[`Download example script file`](../examples/example_T700_workability.py) (right-click and “Save link as…”)

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

## Hindcast

### From Excel files (client-provided historical data)

#### Time series format

You can use this CSV template file ([`HindcastTimeSeries_template.csv`](../examples/HindcastTimeSeries_template.csv)) to provide the time series data.

[`Download example script file`](../examples/example_excel_timeseries_loader.py) (right-click and “Save link as…”)

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

#### Scatter table format

You can use this Excel template file ([`HindcastScatterTable_template.xlsx`](../examples/HindcastScatterTable_template.xlsx)) to provide the scatter table data.

[`Download example script file`](../examples/example_excel_scatter_loader.py) (right-click and “Save link as…”)

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

### From Copernicus Marine Service

[`Download example script file`](../examples/example_copernicus_loader.py) (right-click and “Save link as…”)

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

### From NDBC Buoy Data

[`Download example script file`](../examples/example_ndbc_loader.py) (right-click and “Save link as…”)

    """
    Example: Loading hindcast data from NOAA NDBC buoys and perform some analysis and visualization.
    """

    import matplotlib.pyplot as plt
    import numpy as np
    from PyBM.marine.weather_hindcast import Hindcast, NDBCLoader
    from PyBM.marine import Jonswap, T700, MotionRAO, directional_workability

    # ==========================================
    # OPTION 1: Use nearest buoy to coordinates
    # ==========================================

    # Define location coordinates (example: offshore Massachusetts, USA)
    lat = 42.5   # Latitude (decimal degrees, positive = North)
    long = -70.0 # Longitude (decimal degrees, positive = East, negative = West)

    # Define time period (optional, defaults to all available data if not set)
    start_date = '2020-01-01'  # Start date in 'YYYY-MM-DD' format
    end_date = '2020-12-31'    # End date in 'YYYY-MM-DD' format

    loader = NDBCLoader(
        lat=lat,
        long=long,
        start_date=start_date,
        end_date=end_date
    )

    # ==================================================
    # OPTION 2: Use specific buoy ID (uncomment to use)
    # ==================================================
    # # If you know the buoy ID, you can specify it directly
    # # Example buoy IDs:
    # #   - '44013': Boston, MA (16 NM East of Boston)
    # # Find more buoys at: https://www.ndbc.noaa.gov/
    # 
    # buoy_id = '44013'  # Boston buoy
    # 
    # loader = NDBCLoader(
    #     buoy_id=buoy_id,
    #     start_date=start_date,
    #     end_date=end_date
    # )

    # Create Hindcast object (automatically fetches and processes data)
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

### From DNV long-term wave statistics

[`Download example script file`](../examples/example_DNV_weibull_workability.py) (right-click and “Save link as…”)

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

## IIR filters

The following example shows the usage of the IIR filter design tools:

[`Download example script file`](../examples/example_iir_filter.py) (right-click and “Save link as…”)

    """Example of IIR filter design and filtering using PyBM.signal module."""

    import matplotlib.pyplot as plt

    import PyBM.signal  # Add multiply option to scipy TransferFunction class

    # System parameters
    fs = 100  # [Hz] Sampling frequency
    freq_design = 1 / 6  # [Hz] Frequency at which to evaluate filter response

    # -------------------------
    # Design a Lowpass Butterworth filter
    # -------------------------

    LP_freq = 8  # [Hz] Low pass filter cutoff frequency
    LP_order = 1  # [-] order of filter

    # Create filter
    LowPass = PyBM.signal.lowpass_iir(LP_freq, fs, order=LP_order)
    mag, phase = LowPass.response_at_freqs([freq_design])
    LPz_delay = -phase[0]  # [deg] phase delay at design frequency, delay is +

    # print discrete low pass filter
    print("---------\nButterworth low-pass filter Roll and Pitch")
    print(f"Cut-off frequency: {LP_freq:.2f}Hz, filter order: {LP_order:.0f}")
    print(f"Phase delay of low-pass filter at {1/freq_design:.2f}s: {LPz_delay:.1f}deg")

    # plot filter response
    LowPass.plot_response(Name="Low-pass")

    # -------------------------
    # Create Notch filter
    # -------------------------

    # Notch filter parameters (see https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.iirnotch.html#scipy.signal.iirnotch)
    f_notch = 5  # [Hz] Notch frequency
    Q = 1  # [-] Quality factor

    Notch = PyBM.signal.notch_iir(f_notch, fs, quality=Q)
    mag, phase = Notch.response_at_freqs([freq_design])
    notch_delay = -phase[0]  # [deg] phase delay at design frequency, delay is +

    print("---------\nNotch filter")
    print(f"Notch Freq: {f_notch}Hz")
    print(f"Phase delay of notch filter at {freq_design:.2f}Hz: {notch_delay:.2f}deg")
    mag, phase = Notch.response_at_freqs([f_notch], db=False)
    print(f"Magnitude of notch filter at {f_notch:.2f}Hz: {mag[0]:.2f}")
    print(f"Notch filter:\n{Notch}")

    # plot filter response
    Notch.plot_response(Name="Notch")

    # -------------------------
    # Combine filters
    # -------------------------
    Total = LowPass * Notch
    Total.plot_response(Name="Total")
    plt.legend()
    plt.show()

## Heavy Feeder Tower check

The following example shows the usage of Heavy Feeder Tower check tools:

[`Download example script file`](../examples/example_tower_check.py) (right-click and “Save link as…”)

    """
    Heavy feeder capacity check example

    Author: CBR
    Date: 30-03-2023
    """

    from PyBM.machines.heavy_feeder import unity_checks_tower
    from PyBM.utils import HorizontalStack, Tower, VerticalStack

    # Define tower sections
    bottom_split = Tower(h=40, m=700e3, D=9, h_cog=20)
    mid_split = Tower(h=60, m=600e3, D=9, h_cog=30)
    top_split = Tower(h=60, m=500e3, D=8, h_cog=30)

    # Check unity checks for each tower section
    for tower in [bottom_split, mid_split, top_split]:
        print(unity_checks_tower(tower))

    # Stack 2 sections vertically
    bottom_mid = VerticalStack([bottom_split, mid_split])

    # Check unity checks for the stack
    print(unity_checks_tower(bottom_mid))

    # Salt & Pepper setup
    s_p = HorizontalStack([bottom_split, mid_split], spacing=10)
    print(unity_checks_tower(s_p))
