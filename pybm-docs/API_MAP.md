# PyBM API map (generated from the source code in `source-code/`)

One line per public class/function: first line of its docstring. Full docs: `docs/autoapi/<module path>/index.md`; full code: `source-code/<module path>.py`.


## `PyBM.constants`

- `g = 9.81`
- `rho = 1025`

## `PyBM.exceptions`
Custom PyBM exceptions

- **class `OutofBoundsError`**(Exception) — 

## `PyBM.hydraulics.VariablePressureAccumulator`

- `guesser(symbols: list)` — 
- **class `VariablePressureAccumulator`** — All symbols:
  - methods: `syms`, `prop_dict`, `calc_accu_volume`, `calc_nitro_loss`, `calc_accu_stroke`, `get_passive_force_steps`

## `PyBM.hydraulics.accu_cylinder_combination`
Python class to compute Accumulator properties

- **class `AccuCylinderCombination`** — 
  - methods: `get_V1`, `get_p1`, `get_cyl_force`, `get_pressure_ratio`, `mass_estimate`, `from_pressure_ratio_and_1_point`, `from_pressure_ratio_and_2_points`, `from_pressure_ratio_and_V2`, `plot_force`

## `PyBM.hydraulics.accumulator`
Python class to compute Accumulator properties

- **class `Accumulator`** — 
  - methods: `get_p1`, `get_pressure_ratio`, `mass_estimate`, `gas_mass`

## `PyBM.hydraulics.buckling`

- `calculate_cyl_deadlength(d_bore)` — Calculate total length of cylinder.
- `buckling_check(Fz, d_rod, buckling_length, E=210000000000.0)` — Check for buckling of the cylinder rod. (acc. BHO 'template cylinder sizing.xlsx')
- `get_min_rod_diameter(Fz, buckling_length, E=210000)` — Check for buckling of the cylinder rod. (acc. BHO 'template cylinder sizing.xlsx')

## `PyBM.hydraulics.cylinder`
Python class to compute Cylinder properties

- **class `Cylinder`** — 
  - methods: `Dia`, `Maxforce`, `Maxflow`, `get_stroke`, `mass_estimate`, `cylinder_mass_estimate`, `manifold_mass_estimate`
- **class `DoubleActingCylinder`**(Cylinder) — 
  - methods: `max_pulling_force`
- **class `TripleChamberCylinder`**(DoubleActingCylinder) — 
  - methods: `max_passive_force`

## `PyBM.machines.heavy_feeder.tower_check`
Date: 20-03-2023

- `unity_checks_tower(tower: massItem, tbic: massItem=None, lifting_tool: massItem=None, Hs: float=None)` — Calculate unity checks of a different tower w.r.t. the heavy feeder design conditions.

## `PyBM.machines.standard_feeder.tower_check`
Date: 06-05-2024

- `unity_checks_tower(tower: massItem, tbic: massItem=None, lifting_tool: massItem=None, Hs_transit: float=None, Hs_operational: float=None, d…)` — 

## `PyBM.marine.barge_hydrostatics`
Python class to compute barge hydrostatics

- **class `Barge`** — 
  - methods: `Awl`, `disp`, `disp`, `mass`, `Iyy`, `Iyy`, `Ixx`, `Ixx`, `heave_stiffness`, `heave_period`, `pitch_stiffness`, `roll_stiffness`, `pitch_period`, `roll_period`, `Rxx`, `Ryy`, `heave_stiffness_at_POI`, `roll_stats`

## `PyBM.marine.machines.HeavyFeeder`
Heavy Feeder class to compute workability

- **class `HeavyFeeder`**(Machine_Linear) — 
  - methods: `c1`, `c2`, `get_POI`, `apply_machine_dofs`, `check_stroke_limit`, `check_cylinder_velocity_limit`, `check_horizontal_motion_no_comp`, `check_horizontal_motion`, `plot`

## `PyBM.marine.machines.HeavyFeederSurgeSway`
Heavy Feeder class to compensate Surge and Sway motion of a POI

- **class `HeavyFeederSurgeSway`**(HeavyFeeder) — 
  - methods: `get_POI`, `apply_machine_dofs`, `check_stroke_limit`

## `PyBM.marine.machines.MCG30`

- **class `MCG30LHIGHLOAD_Linear`**(MCG30LHIGHLOAD_Params, MCG30LIFTING_Linear) — 
- **class `MCG30LLOWLOAD_Linear`**(MCG30LLOWLOAD_Params, MCG30LIFTING_Linear) — 
- **class `MCG30LTRANSFER_Linear`**(MCG30LTRANSFER_Params, MCG30TRANSFER_Linear) — 
- **class `MCG30LTIPLADDER_Linear`**(MCG30LTIPLADDER_Params, MCG30TRANSFER_Linear) — 
- **class `MCG30MHIGHLOAD_Linear`**(MCG30MHIGHLOAD_Params, MCG30LIFTING_Linear) — 
- **class `MCG30MLOWLOAD_Linear`**(MCG30MLOWLOAD_Params, MCG30LIFTING_Linear) — 
- **class `MCG30MTRANSFER_Linear`**(MCG30MTRANSFER_Params, MCG30TRANSFER_Linear) — 
- **class `MCG30MTIPLADDER_Linear`**(MCG30MTIPLADDER_Params, MCG30TRANSFER_Linear) — 
- **class `MCG30LHIGHLOAD_Nonlinear`**(MCG30LHIGHLOAD_Params, MCG30LIFTING_Nonlinear) — 
- **class `MCG30LLOWLOAD_Nonlinear`**(MCG30LLOWLOAD_Params, MCG30LIFTING_Nonlinear) — 
- **class `MCG30LTRANSFER_Nonlinear`**(MCG30LTRANSFER_Params, MCG30TRANSFER_Nonlinear) — 
- **class `MCG30LTIPLADDER_Nonlinear`**(MCG30LTIPLADDER_Params, MCG30TRANSFER_Nonlinear) — 
- **class `MCG30MHIGHLOAD_Nonlinear`**(MCG30MHIGHLOAD_Params, MCG30LIFTING_Nonlinear) — 
- **class `MCG30MLOWLOAD_Nonlinear`**(MCG30MLOWLOAD_Params, MCG30LIFTING_Nonlinear) — 
- **class `MCG30MTRANSFER_Nonlinear`**(MCG30MTRANSFER_Params, MCG30TRANSFER_Nonlinear) — 
- **class `MCG30MTIPLADDER_Nonlinear`**(MCG30MTIPLADDER_Params, MCG30TRANSFER_Nonlinear) — 

## `PyBM.marine.machines.MCG30.MCG30_Linear`
Linearized MCG. Based on the same limits as MCG30.py but with linearized equations according to first-order taylor expansions.

- **class `MCG30_Linear`**(Machine_Linear, ABC) — Base class for MCG 3.0 for workability studies.
  - methods: `get_POI`, `translate_linear_dof`, `apply_machine_dofs`, `check_linearized_limit`, `check_telescope_position`, `check_an_luff`, `check_horizontal_acc`, `get_workability_limit`
- **class `MCG30TRANSFER_Linear`**(MCG30_Linear, ABC) — 
  - methods: `check_an_luff_world`
- **class `MCG30LIFTING_Linear`**(MCG30_Linear, ABC) — 

## `PyBM.marine.machines.MCG30.MCG30_Nonlinear`
MCG System properties to compute workability. Based on the old MATLAB utilization calculations.

- **class `MCG30_Nonlinear`**(Machine_Nonlinear, ABC) — Base class for MCG 3.0 for workability studies.
  - methods: `get_POI`, `check_telescope_position`, `check_v_telescope`, `check_an_luff`, `check_max_system_pitch`, `check_max_system_roll`, `check_horizontal_acc`, `check_heave_acc`, `check_v_luff_cyl`, `check_v_slew`, `check_duty_cycle`, `translate_telescope`, `translate_an_luff_world`, `translate_an_luff`, `translate_an_slew_world`, `translate_an_slew`, `translate_horizontal`, `translate_luf_stroke`, `get_workability_limit`, `plot`
- **class `MCG30TRANSFER_Nonlinear`**(MCG30_Nonlinear, ABC) — 
  - methods: `check_an_slew_world`, `check_an_luff_world`
- **class `MCG30LIFTING_Nonlinear`**(MCG30_Nonlinear, ABC) — 
  - methods: `check_v_sys_roll`, `check_v_sys_pitch`, `check_v_heave`, `check_v_tip`

## `PyBM.marine.machines.MCG30.mcg30_helper`

- `partials_telescope(pos_tip, base)` — Calculate the partial derivatives of the telescope position with respect to the response DOFs [ X, Y, Z, Rx, Ry, Rz ].
- `partials_luff_world(pos_tip, base)` — 
- `partials_luff(pos_tip, base, slew_angle)` — 
- `partials_slew_world(pos_tip, base)` — 
- `partials_slew(pos_tip, base)` — Calculate the partial derivatives of the slew angle with respect to the response DOFs [ X, Y, Z, Rx, Ry, Rz ].
- `partials_luff_cyl(pos_tip, base, slew_angle, luff_angle, lc0, l0, l1)` — Calculate the partial derivatives of the luffing cylinder length with respect to the response DOFs [ X, Y, Z, Rx, Ry, Rz ].
- `partials_v_tip(luff_angle, gw_L, slew_angle)` — 
- `p2ds(partials)` — Convert partials to a dataset with POS, VEL and ACC
- **class `MCG30_Params`**(ABC) — 
  - methods: `plot`
- **class `MCG30L_Params`**(MCG30_Params, ABC) — 
- **class `MCG30M_Params`**(MCG30_Params, ABC) — 
- **class `MCG30TRANSFER_Params`**(MCG30_Params, ABC) — 
- **class `MCG30HIGHLOAD_Params`**(MCG30_Params, ABC) — 
  - methods: `tip_v_threshold`
- **class `MCG30LOWLOAD_Params`**(MCG30_Params, ABC) — 
  - methods: `tip_v_threshold`
- `MCG30TIPLADDER_FACTORY(MCG_Size_Params_Class)` — 
- **class `MCG30MTRANSFER_Params`**(MCG30M_Params, MCG30TRANSFER_Params, ABC) — 
- **class `MCG30MHIGHLOAD_Params`**(MCG30M_Params, MCG30HIGHLOAD_Params, ABC) — 
- **class `MCG30MLOWLOAD_Params`**(MCG30M_Params, MCG30LOWLOAD_Params, ABC) — 
- **class `MCG30LTRANSFER_Params`**(MCG30L_Params, MCG30TRANSFER_Params, ABC) — 
- **class `MCG30LHIGHLOAD_Params`**(MCG30L_Params, MCG30HIGHLOAD_Params, ABC) — 
- **class `MCG30LLOWLOAD_Params`**(MCG30L_Params, MCG30LOWLOAD_Params, ABC) — 

## `PyBM.marine.machines.T700`
T700 System properties to compute workability

- **class `T700`**(Machine_Linear) — 
  - methods: `h`, `c1`, `c2`, `c3`, `get_POI`, `check_stroke_limit`, `check_cylinder_velocity_limit`, `check_platform_velocity_limit`, `compute_cylinder_forces`, `plot`

## `PyBM.marine.machines.machine_interface`
Generic Interface for BM machine to compute workability

- **class `Machine_Linear`**(ABC) — 
  - methods: `apply_transform`, `get_rao_at_poi`, `get_POI`, `apply_machine_dofs`, `get_workability_limit`
- **class `Machine_Nonlinear`**(ABC) — 
  - methods: `apply_transform`, `get_POI`

## `PyBM.marine.motion_analysis.MotionRAO`
Motion RAO class. Inherits RAO class and xarray.Dataset

- **class `MotionRAO`**(RAO) — 
  - methods: `translate_rao`

## `PyBM.marine.motion_analysis.RAO`
Base class for RAOs of Vessels. Inherits xarray.Dataset.

- **class `SurgeDir`**(Enum) — Enum for Surge direction
- **class `SwayDir`**(Enum) — Enum for Sway direction
- **class `HeaveDir`**(Enum) — Enum for Heave direction
- **class `RollDir`**(Enum) — Enum for Roll direction
- **class `PitchDir`**(Enum) — Enum for Pitch direction
- **class `YawDir`**(Enum) — Enum for Yaw direction
- **class `WaveOrigin`**(Enum) — Enum for Wave direction
- **class `RotationUnit`**(Enum) — Enum for Rotation unit
- **class `RAO`**(xr.Dataset, ABC) — This is the parent class for motion and force RAOs
  - methods: `translate_rao`, `default_rao_path`, `group_name`, `group`, `modify_conventions`, `load_rao`, `from_api`, `save_rao`, `get_roll_period`, `plot`

## `PyBM.marine.motion_analysis.Response`
Module to calculate vessel motions in the frequency domain.

- `compute_response(wave: WaveSpectrum, rao: RAO, poi=None, Nfreqs=200, f_bounds=None)` — Compute the vessel response based on the given wave spectrum and RAO.
- `compute_mpe(wave: WaveSpectrum, rao: RAO, poi=None, storm_duration=10800, transfer_function=None)` — Calculate MPE of the given parameter for all points of interest (POI).
- `equal_energy_freqs_rao(wave: WaveSpectrum, rao: RAO, Nfreqs, f_bounds=None)` — 
- `apply_directional_spreading(wave: WaveSpectrum, rao: RAO)` — 

## `PyBM.marine.motion_analysis.SpectrumAccessor`
Accessor of Xarray Dataset to implement spectral analysis tools.

- **class `SpectralTools`** — Tools to analyse spectra.
  - methods: `m0`, `m1`, `m2`, `amp`, `spectral_moment`, `standard_deviation`, `zero_crossing_period`, `MPE`
- **class `EqualEnergySpectrum`**(SpectralTools) — Tools to analyse spectra optimized for equal energy frequencies.
  - methods: `spectral_moment`

## `PyBM.marine.motion_analysis.TimeDomain`
Time domain tools

- **class `TimeDomainTools`** — Tools for time domain traces in xarray.DataArray type
  - methods: `translate_trace`, `translate_trace_smallangle`
- **class `TimeDomain`** — 
  - methods: `time_vector`, `generate_mat_time_traces`, `generate_time_traces`, `save_mat_file`, `save_nc_file`, `default_trace_path`, `load_time_trace`, `load_all_default_time_traces`, `load_all_time_traces`, `load_mat_time_trace`, `load_nc_time_trace`, `mat_file_name`, `nc_file_name`, `time_trace_from_rao_and_wave`, `multi_directional_time_trace`, `single_direction_time_trace`, `compute_deltas`, `zero_crossing_period`

## `PyBM.marine.tools.CSV_to_Xarray`
convert CSV and CSV-like formats to useful xarray

- `parse_csv_sections(filename)` — Split the .csv file into sections by '&buildg -csv' / 'END'.
- `parse_section(section_text)` — Parse a single amplitude or phase section.
- `extract_dof_name(section_text)` — Extract DOF name like 'Surge', 'Sway', etc. from the section header.
- `decode_RAO_CSV(filename, mirror)` — 
- `load_CSV(filename, mirror)` — 
- `CSV_to_RAO(filename, VesselName, Vessel_LC, origin, mirror=False)` — Convert CSV file to Xarray RAO object

## `PyBM.marine.tools.LIS_to_Xarray`
tools to read AQWA RAO files (*.LIS)

- `get_cog(filename)` — 
- `get_n_freqs(filename)` — 
- `get_draft(filename)` — 
- `decode_RAO(filename, rao_type, n_freqs)` — 
- `load_LIS(filename)` — 
- `LIS_to_RAO(filename, VesselName, Vessel_LC)` — Convert LIS data to MotionRAO object.

## `PyBM.marine.tools.TXT_to_Xarray`
convert TXT Orcaflex formats to useful xarray

- `parse_TXT(filename)` — Parse OrcaFlex .txt file into structured blocks per direction.
- `decode_RAO_TXT(filename, mirror=False)` — Decode OrcaFlex .txt file to xarray DataArray.
- `load_TXT(filename, mirror=False)` — 
- `TXT_to_RAO(filename, VesselName, Vessel_LC, origin, mirror=False)` — Convert OrcaFlex .txt file to MotionRAO object.

## `PyBM.marine.tools.XLS_to_Xarray`
convert XLS format to useful xarray

- `decode_RAO_XLS(filename, mirror)` — 
- `load_XLS(filename, mirror)` — 
- `XLS_to_RAO(filename, VesselName, Vessel_LC, origin, mirror=False)` — Convert excel file to Xarray RAO object

## `PyBM.marine.tools.api.api_calls`

- `get_raos(session=None)` — Get RAOs from API (auto-authenticates if needed)
- `get_rao_loadcases(VesselName: str, session=None)` — Get loadcases for a specific RAO from API (auto-authenticates if needed)
- `get_rao_loadcase(VesselName: str, Vessel_LC: str, session=None)` — Get specific loadcase details for a RAO from API (auto-authenticates if needed)

## `PyBM.marine.tools.api.oauth_session`
Created by CVE, 05-11-2025, together with Copilot <3

- **class `TokenCache`** — 
  - methods: `save`, `load`
- **class `OAuth2CallbackHandler`**(BaseHTTPRequestHandler) — 
  - methods: `do_GET`, `log_message`
- `get_authenticated_session()` — Get authenticated session using OAuth2 (browser-based, tokens cached locally)

## `PyBM.marine.tools.import_octopus_rao`

- `Octopus_to_RAO(octopus_file, VesselName, Vessel_LC, speed=0)` — 
- `get_rao_parameter(file_iterator, param_string)` — 
- `read_data_line(line)` — 
- `get_origin(file_iterator)` — 
- `get_wave_directions(file_iterator)` — 
- `get_speeds(file_iterator)` — 
- `get_wave_frequencies(file_iterator, speed)` — 
- `get_rao(file_iterator, desired_speed)` — 

## `PyBM.marine.tools.read_res`
This file reads .res output files from aNySIM and returns a dictionary with all the data

- `resample(data, new_dt, data_dt)` — 
- `read_res(filename, dt=0, read_invalid=True)` — Read a text .res file with time traces.
- `write_pickle(filename, data_dict)` — 
- `write_res(filename, data_dict)` — Write a data dictionary to a .res text file.

## `PyBM.marine.wave_spectrum.Jonswap`
This document defines the JONSWAP spectrum class.

- **class `Jonswap`**(WaveSpectrum) — This class defines the JONSWAP Frequency spectrum.
  - methods: `gamma`, `gamma`, `Tz`, `Tz_to_Tp`, `compute_gamma`, `power_spectrum`

## `PyBM.marine.wave_spectrum.PiersonMoskowitz`
This document defines the Pierson Moskowitz spectrum class.

- **class `PiersonMoskowitz`**(WaveSpectrum) — This class defines the Pierson Moskowitz Frequency spectrum.
  - methods: `power_spectrum`

## `PyBM.marine.wave_spectrum.Torsethaugen`
This document defines the Torsethaugen spectrum class.

- **class `Torsethaugen`**(WaveSpectrum) — This class defines the Torsethaugen Frequency spectrum.
  - methods: `power_spectrum`, `dual_equal_energy_directional_wave_spectrum`, `equal_energy_directional_wave_spectrum`

## `PyBM.marine.wave_spectrum.WaveSpectrum`

- `wrap(angle)` — 
- **class `WaveSpectrum`**(ABC) — 
  - methods: `main_direction`, `main_direction`, `Hs`, `Hs`, `Tp`, `Tp`, `Ndirs`, `Ndirs`, `power_spectrum`, `wave_spectrum`, `equal_energy_frequencies`, `equal_energy_directions`, `equal_energy_method`, `directional_wave_spectrum`, `abs_directions`, `equal_energy_directional_wave_spectrum`, `equal_energy_directional_spreading`, `directional_spreading`, `shift_direction`, `plot`, `plot`

## `PyBM.marine.weather_hindcast.Hindcast`
Hindcast analysis framework with pluggable data sources.

- **class `HindcastBase`**(ABC) — Abstract internal base with shared attributes and polymorphic abstract methods.
  - methods: `get_Hs_stats`, `get_Tp_stats`, `plot_Hs_Tp`, `get_workability_percentage`
- **class `HindcastScatterTable`**(HindcastBase) — Analysis class for scatter table format hindcast data.
  - methods: `get_Hs_stats`, `get_Tp_stats`, `plot_Hs_Tp`, `get_workability_percentage`
- **class `HindcastTimeSeries`**(HindcastBase) — Analysis class for time series format hindcast data.
  - methods: `get_Hs_stats`, `get_Tp_stats`, `plot_Hs_Tp`, `get_workability_percentage`
- **class `Hindcast`** — Factory class for creating appropriate hindcast analysis objects.

## `PyBM.marine.weather_hindcast.HindcastLoader`
Hindcast data loaders for various sources.

- **class `HindcastLoader`**(ABC) — Abstract base class for all hindcast data loaders.
  - methods: `fetch`
- **class `CopernicusLoader`**(HindcastLoader) — Class to load hindcast data from Copernicus Marine API. [3], [4]
  - methods: `fetch`
- **class `NDBCLoader`**(HindcastLoader) — Class to load hindcast data from NOAA NDBC buoys. [1], [2]
  - methods: `fetch`
- **class `ExcelTimeSeriesLoader`**(HindcastLoader) — Load hindcast time series data from Excel or CSV file.
  - methods: `fetch`
- **class `ExcelScatterLoader`**(HindcastLoader) — Load hindcast scatter table from Excel file.
  - methods: `fetch`
- **class `DNVLoader`**(HindcastLoader) — Load hindcast scatter table from DNV long-term wave statistics using Weibull distribution.
  - methods: `fetch`

## `PyBM.marine.weather_hindcast.ScatterDiagram`

- `from_weibull(Hs, Tz, alpha_s, beta_s, a1, a2, b1, b2, a0=0.7, b0=0.07, lambda_s=0)` — calculate Hs-Tz scatter according to
- `percentage_from_workability_weibull(Hs_workability, alpha_s, beta_s, a1, a2, b1, b2, a0=0.7, b0=0.07, lambda_s=0)` — Warning: Weibull distributions are extremely conservative from a sales perspective.

## `PyBM.marine.weather_hindcast.utils`
Utility functions for hindcast analysis.

- `adaptive_bins(coord_values, min_span, n_bins)` — Create adaptive statistics bins based on scatter_data coordinates.
- `from_weibull(Hs, Tz, alpha_s, beta_s, a1, a2, b1, b2, a0=0.7, b0=0.07, gamma_s=0)` — Calculate Hs-Tz scatter according to DNV-RP-C205 2014-04 Formula 3.6.3.4.

## `PyBM.marine.workability.workability_limits`

- **class `workability_accessor`** — 
  - methods: `table`, `byscatter`, `plot_detailed_workability`, `plot_combined_workability`
- `directional_workability(rao: MotionRAO, wave: WaveSpectrum, machine: Machine_Linear, **kwargs)` — Compute the workability of the machine for the given wave directions.
- `directional_workability_timetrace(trace: xr.DataArray, machine: MCG30_Nonlinear, **kwargs)` — Compute the workability of the machine using the time trace supplied (MCG)
- `multicolored_line(ax: plt.Axes, Tp_result)` — 
- `multiple_lines(ax: plt.Axes, Tp_result)` — 
- `set_polar_plot_params(ax: plt.Axes, max_y, Tp)` — 
- `plot_ship(ax: plt.Axes, plot_diameter=1.0)` — Plot a ship contour on the given axis.

## `PyBM.mechanics.mechanical_hydraulic_combination`

- **class `MechanicalHydraulicCombination`** — 
  - methods: `get_force`, `plot_force`, `plot_error`

## `PyBM.mechanics.mechanical_interface`

- **class `MechanicalInterface`**(ABC) — 
  - methods: `L_cylinder`, `force_ratio`

## `PyBM.signal.iir_filters`
This module contains the tools to create IIR filters.

- `get_delay_at_freq(filter, freq)` — Get the phase delay at a specific frequency for a given filter.
- `lead_iir(phase, freq, fs)` — Design a lead IIR filter.
- `lowpass_iir(cutoff, fs, order=1)` — Design a lowpass IIR filter.
- `notch_iir(freq, fs, quality=30)` — Design a notch IIR filter.

## `PyBM.signal.tf_tools`
Tools to augment Scipy.signal.TransferFunction function class.

- `check_sample_times(tf1: spsig.TransferFunction, tf2: spsig.TransferFunction)` — 
- `TF_multiply(tf1: spsig.TransferFunction, tf2)` — 
- `TF_divide(tf1: spsig.TransferFunction, tf2)` — 
- `TF_equals(tf1: spsig.TransferFunction, tf2)` — 
- `print_TF(self)` — Return string of TF coefficients.
- `response_at_freqs(tf: spsig.TransferFunction, freqs, db=True)` — Compute magnitude and phase at given frequency points
- `plot_response(tf: spsig.TransferFunction, Name: str='IIR Filter', freq_range=(1 / 50, 50), mag_ylim=(-15, 5), db=True)` — Plot the frequency response of a Transfer function

## `PyBM.utils.data_classes`

- **class `POI`** — 
- **class `VesselDimensions`** — 

## `PyBM.utils.helper_functions`

- `unwrap_angle(angle)` — Make sure angle is between 0 and 360.
- `amp_phase_to_complex(amp, phase)` — Convert amplitude / phase representation to complex number
- `disc_area(diameter)` — Return area from diameter.
- `complex_max(data: xr.Dataset, dim)` — 
- `delta(steps: np.ndarray)` — Return array of differences, the first value will be 0 to conserve the length.
- `component_absolute(x)` — Take the absolute value of the real and imaginary part separatly.
- `absolute_sum(a, b)` — Sum complex numbers as absolute values (to include phase information), for example to get flow from 2 complex velocity signals.
- `differentiate(rao, freqs)` — Take the derivate of RAO data

## `PyBM.utils.mass_items`

- **class `massItem`** — Represents a mass item with height, mass, and center of gravity properties.
  - methods: `get_I`, `set_I`, `I_shifted`
- **class `Tower`**(massItem) — Represents a tower mass item.
  - methods: `I`, `I`
- **class `Stack`**(ABC) — Abstract base class for a stack of mass items.
  - methods: `m`, `h`, `h_cog`, `x_cog`, `y_cog`, `I`, `I_shifted`
- **class `VerticalStack`**(Stack) — Represents a vertical stack of mass items.
  - methods: `h`
- **class `HorizontalStack`**(Stack) — Represents a horizontal stack of mass items.
  - methods: `h`

## `PyBM.utils.plot_template`


## `PyBM.utils.windows_helpers`

- `isFileLocked(filePath)` — Source: https://stackoverflow.com/questions/13371444/python-check-file-is-locked
