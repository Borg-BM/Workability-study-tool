<!-- Source: https://docs.app.barge-master.com/autoapi/PyBM/marine/index.html -->

# PyBM.marine

## Submodules

- [PyBM.marine.barge_hydrostatics](barge_hydrostatics/index.md)
- [PyBM.marine.machines](machines/index.md)
- [PyBM.marine.motion_analysis](motion_analysis/index.md)
- [PyBM.marine.tools](tools/index.md)
- [PyBM.marine.wave_spectrum](wave_spectrum/index.md)
- [PyBM.marine.weather_hindcast](weather_hindcast/index.md)
- [PyBM.marine.workability](workability/index.md)

## Attributes

|                                                      |     |
|------------------------------------------------------|-----|
| [`g`](#PyBM.marine.g "PyBM.marine.g")                |     |
| [`logger`](#PyBM.marine.logger "PyBM.marine.logger") |     |
| [`cmap`](#PyBM.marine.cmap "PyBM.marine.cmap")       |     |

## Exceptions

|                                                                                    |                                                |
|------------------------------------------------------------------------------------|------------------------------------------------|
| [`OutofBoundsError`](#PyBM.marine.OutofBoundsError "PyBM.marine.OutofBoundsError") | Common base class for all non-exit exceptions. |

## Classes

|                                                                                                            |                                                                  |
|------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------|
| [`HeavyFeeder`](#PyBM.marine.HeavyFeeder "PyBM.marine.HeavyFeeder")                                        | Helper class that provides a standard way to create an ABC using |
| [`HeavyFeederSurgeSway`](#PyBM.marine.HeavyFeederSurgeSway "PyBM.marine.HeavyFeederSurgeSway")             | Helper class that provides a standard way to create an ABC using |
| [`Machine_Linear`](#id0 "PyBM.marine.Machine_Linear")                                                      | Helper class that provides a standard way to create an ABC using |
| [`Machine_Nonlinear`](#id10 "PyBM.marine.Machine_Nonlinear")                                               | Helper class that provides a standard way to create an ABC using |
| [`MCG30LHIGHLOAD_Linear`](#PyBM.marine.MCG30LHIGHLOAD_Linear "PyBM.marine.MCG30LHIGHLOAD_Linear")          | Helper class that provides a standard way to create an ABC using |
| [`MCG30LHIGHLOAD_Nonlinear`](#PyBM.marine.MCG30LHIGHLOAD_Nonlinear "PyBM.marine.MCG30LHIGHLOAD_Nonlinear") | Helper class that provides a standard way to create an ABC using |
| [`MCG30LLOWLOAD_Linear`](#PyBM.marine.MCG30LLOWLOAD_Linear "PyBM.marine.MCG30LLOWLOAD_Linear")             | Helper class that provides a standard way to create an ABC using |
| [`MCG30LLOWLOAD_Nonlinear`](#PyBM.marine.MCG30LLOWLOAD_Nonlinear "PyBM.marine.MCG30LLOWLOAD_Nonlinear")    | Helper class that provides a standard way to create an ABC using |
| [`MCG30LTRANSFER_Linear`](#PyBM.marine.MCG30LTRANSFER_Linear "PyBM.marine.MCG30LTRANSFER_Linear")          | Helper class that provides a standard way to create an ABC using |
| [`MCG30LTRANSFER_Nonlinear`](#PyBM.marine.MCG30LTRANSFER_Nonlinear "PyBM.marine.MCG30LTRANSFER_Nonlinear") | Helper class that provides a standard way to create an ABC using |
| [`MCG30MHIGHLOAD_Linear`](#PyBM.marine.MCG30MHIGHLOAD_Linear "PyBM.marine.MCG30MHIGHLOAD_Linear")          | Helper class that provides a standard way to create an ABC using |
| [`MCG30MHIGHLOAD_Nonlinear`](#PyBM.marine.MCG30MHIGHLOAD_Nonlinear "PyBM.marine.MCG30MHIGHLOAD_Nonlinear") | Helper class that provides a standard way to create an ABC using |
| [`MCG30MLOWLOAD_Linear`](#PyBM.marine.MCG30MLOWLOAD_Linear "PyBM.marine.MCG30MLOWLOAD_Linear")             | Helper class that provides a standard way to create an ABC using |
| [`MCG30MLOWLOAD_Nonlinear`](#PyBM.marine.MCG30MLOWLOAD_Nonlinear "PyBM.marine.MCG30MLOWLOAD_Nonlinear")    | Helper class that provides a standard way to create an ABC using |
| [`MCG30MTRANSFER_Linear`](#PyBM.marine.MCG30MTRANSFER_Linear "PyBM.marine.MCG30MTRANSFER_Linear")          | Helper class that provides a standard way to create an ABC using |
| [`MCG30MTRANSFER_Nonlinear`](#PyBM.marine.MCG30MTRANSFER_Nonlinear "PyBM.marine.MCG30MTRANSFER_Nonlinear") | Helper class that provides a standard way to create an ABC using |
| [`T700`](#PyBM.marine.T700 "PyBM.marine.T700")                                                             | Helper class that provides a standard way to create an ABC using |
| [`RAO`](#PyBM.marine.RAO "PyBM.marine.RAO")                                                                | This is the parent class for motion and force RAOs               |
| [`MotionRAO`](#PyBM.marine.MotionRAO "PyBM.marine.MotionRAO")                                              | This is the parent class for motion and force RAOs               |
| [`SurgeDir`](#PyBM.marine.SurgeDir "PyBM.marine.SurgeDir")                                                 | Enum for Surge direction                                         |
| [`SwayDir`](#PyBM.marine.SwayDir "PyBM.marine.SwayDir")                                                    | Enum for Sway direction                                          |
| [`HeaveDir`](#PyBM.marine.HeaveDir "PyBM.marine.HeaveDir")                                                 | Enum for Heave direction                                         |
| [`RollDir`](#PyBM.marine.RollDir "PyBM.marine.RollDir")                                                    | Enum for Roll direction                                          |
| [`PitchDir`](#PyBM.marine.PitchDir "PyBM.marine.PitchDir")                                                 | Enum for Pitch direction                                         |
| [`YawDir`](#PyBM.marine.YawDir "PyBM.marine.YawDir")                                                       | Enum for Yaw direction                                           |
| [`WaveOrigin`](#PyBM.marine.WaveOrigin "PyBM.marine.WaveOrigin")                                           | Enum for Wave direction                                          |
| [`RotationUnit`](#PyBM.marine.RotationUnit "PyBM.marine.RotationUnit")                                     | Enum for Rotation unit                                           |
| [`SpectralTools`](#PyBM.marine.SpectralTools "PyBM.marine.SpectralTools")                                  | Tools to analyse spectra.                                        |
| [`EqualEnergySpectrum`](#PyBM.marine.EqualEnergySpectrum "PyBM.marine.EqualEnergySpectrum")                | Tools to analyse spectra optimized for equal energy frequencies. |
| [`TimeDomainTools`](#PyBM.marine.TimeDomainTools "PyBM.marine.TimeDomainTools")                            | Tools for time domain traces in xarray.DataArray type            |
| [`TimeDomain`](#PyBM.marine.TimeDomain "PyBM.marine.TimeDomain")                                           |                                                                  |
| [`PiersonMoskowitz`](#PyBM.marine.PiersonMoskowitz "PyBM.marine.PiersonMoskowitz")                         | This class defines the Pierson Moskowitz Frequency spectrum.     |
| [`WaveSpectrum`](#PyBM.marine.WaveSpectrum "PyBM.marine.WaveSpectrum")                                     | Helper class that provides a standard way to create an ABC using |
| [`Jonswap`](#PyBM.marine.Jonswap "PyBM.marine.Jonswap")                                                    | This class defines the JONSWAP Frequency spectrum.               |
| [`Torsethaugen`](#PyBM.marine.Torsethaugen "PyBM.marine.Torsethaugen")                                     | This class defines the Torsethaugen Frequency spectrum.          |
| [`Machine_Linear`](#id0 "PyBM.marine.Machine_Linear")                                                      | Helper class that provides a standard way to create an ABC using |
| [`Machine_Nonlinear`](#id10 "PyBM.marine.Machine_Nonlinear")                                               | Helper class that provides a standard way to create an ABC using |
| [`workability_accessor`](#PyBM.marine.workability_accessor "PyBM.marine.workability_accessor")             |                                                                  |

## Functions

|                                                                                                                                                           |                                                                                                                                                              |
|-----------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [`_recursive_group_names`](#PyBM.marine._recursive_group_names "PyBM.marine._recursive_group_names")(groups\[, parent\])                                  | Recursively get the group names from a dictionary of groups                                                                                                  |
| [`compute_response`](#PyBM.marine.compute_response "PyBM.marine.compute_response")(wave, rao\[, poi, Nfreqs, f_bounds\])                                  | Compute the vessel response based on the given wave spectrum and RAO.                                                                                        |
| [`compute_mpe`](#PyBM.marine.compute_mpe "PyBM.marine.compute_mpe")(wave, rao\[, poi, storm_duration, ...\])                                              | Calculate MPE of the given parameter for all points of interest (POI).                                                                                       |
| [`equal_energy_freqs_rao`](#PyBM.marine.equal_energy_freqs_rao "PyBM.marine.equal_energy_freqs_rao")(wave, rao, Nfreqs\[, f_bounds\])                     |                                                                                                                                                              |
| [`apply_directional_spreading`](#PyBM.marine.apply_directional_spreading "PyBM.marine.apply_directional_spreading")(wave, rao)                            |                                                                                                                                                              |
| [`isFileLocked`](#PyBM.marine.isFileLocked "PyBM.marine.isFileLocked")(filePath)                                                                          | Source: [https://stackoverflow.com/questions/13371444/python-check-file-is-locked](https://stackoverflow.com/questions/13371444/python-check-file-is-locked) |
| [`Octopus_to_RAO`](#PyBM.marine.Octopus_to_RAO "PyBM.marine.Octopus_to_RAO")(octopus_file, VesselName, Vessel_LC\[, ...\])                                |                                                                                                                                                              |
| [`get_speeds`](#PyBM.marine.get_speeds "PyBM.marine.get_speeds")(file_iterator)                                                                           |                                                                                                                                                              |
| [`get_wave_directions`](#PyBM.marine.get_wave_directions "PyBM.marine.get_wave_directions")(file_iterator)                                                |                                                                                                                                                              |
| [`get_wave_frequencies`](#PyBM.marine.get_wave_frequencies "PyBM.marine.get_wave_frequencies")(file_iterator, speed)                                      |                                                                                                                                                              |
| [`LIS_to_RAO`](#PyBM.marine.LIS_to_RAO "PyBM.marine.LIS_to_RAO")(filename, VesselName, Vessel_LC)                                                         | Convert LIS data to MotionRAO object.                                                                                                                        |
| [`load_LIS`](#PyBM.marine.load_LIS "PyBM.marine.load_LIS")(filename)                                                                                      |                                                                                                                                                              |
| [`XLS_to_RAO`](#PyBM.marine.XLS_to_RAO "PyBM.marine.XLS_to_RAO")(filename, VesselName, Vessel_LC, origin\[, ...\])                                        | Convert excel file to Xarray RAO object                                                                                                                      |
| [`load_XLS`](#PyBM.marine.load_XLS "PyBM.marine.load_XLS")(filename, mirror)                                                                              |                                                                                                                                                              |
| [`CSV_to_RAO`](#PyBM.marine.CSV_to_RAO "PyBM.marine.CSV_to_RAO")(filename, VesselName, Vessel_LC, origin\[, ...\])                                        | Convert CSV file to Xarray RAO object                                                                                                                        |
| [`load_CSV`](#PyBM.marine.load_CSV "PyBM.marine.load_CSV")(filename, mirror)                                                                              |                                                                                                                                                              |
| [`TXT_to_RAO`](#PyBM.marine.TXT_to_RAO "PyBM.marine.TXT_to_RAO")(filename, VesselName, Vessel_LC, origin\[, ...\])                                        | Convert OrcaFlex .txt file to MotionRAO object.                                                                                                              |
| [`load_TXT`](#PyBM.marine.load_TXT "PyBM.marine.load_TXT")(filename\[, mirror\])                                                                          |                                                                                                                                                              |
| [`__file_len`](#PyBM.marine.__file_len "PyBM.marine.__file_len")(fname)                                                                                   |                                                                                                                                                              |
| [`resample`](#PyBM.marine.resample "PyBM.marine.resample")(data, new_dt, data_dt)                                                                         |                                                                                                                                                              |
| [`__read_file`](#PyBM.marine.__read_file "PyBM.marine.__read_file")(filename\[, read_invalid\])                                                           |                                                                                                                                                              |
| [`read_res`](#PyBM.marine.read_res "PyBM.marine.read_res")(filename\[, dt, read_invalid\])                                                                | Read a text .res file with time traces.                                                                                                                      |
| [`write_pickle`](#PyBM.marine.write_pickle "PyBM.marine.write_pickle")(filename, data_dict)                                                               |                                                                                                                                                              |
| [`write_res`](#PyBM.marine.write_res "PyBM.marine.write_res")(filename, data_dict)                                                                        | Write a data dictionary to a .res text file.                                                                                                                 |
| [`wrap`](#PyBM.marine.wrap "PyBM.marine.wrap")(angle)                                                                                                     |                                                                                                                                                              |
| [`directional_workability`](#PyBM.marine.directional_workability "PyBM.marine.directional_workability")(→ xarray.DataArray)                               | Compute the workability of the machine for the given wave directions.                                                                                        |
| [`directional_workability_timetrace`](#PyBM.marine.directional_workability_timetrace "PyBM.marine.directional_workability_timetrace")(→ xarray.DataArray) | Compute the workability of the machine using the time trace supplied (MCG)                                                                                   |
| [`_polar_plotter`](#PyBM.marine._polar_plotter "PyBM.marine._polar_plotter")(plot_method, workability_result\[, ...\])                                    |                                                                                                                                                              |
| [`multicolored_line`](#PyBM.marine.multicolored_line "PyBM.marine.multicolored_line")(ax, Tp_result)                                                      |                                                                                                                                                              |
| [`multiple_lines`](#PyBM.marine.multiple_lines "PyBM.marine.multiple_lines")(ax, Tp_result)                                                               |                                                                                                                                                              |
| [`set_polar_plot_params`](#PyBM.marine.set_polar_plot_params "PyBM.marine.set_polar_plot_params")(ax, max_y, Tp)                                          |                                                                                                                                                              |
| [`plot_ship`](#PyBM.marine.plot_ship "PyBM.marine.plot_ship")(ax\[, plot_diameter\])                                                                      | Plot a ship contour on the given axis.                                                                                                                       |
| [`_make_legend_proxies`](#PyBM.marine._make_legend_proxies "PyBM.marine._make_legend_proxies")(cmap, \*\*kwargs)                                          |                                                                                                                                                              |

## Package Contents

*class *PyBM.marine.HeavyFeeder(*position*, *orientation*, *comp_point=\[0, 0, 0\]*)[](../../../../source-code/PyBM/marine/machines/HeavyFeeder.py)  
Bases: [`PyBM.marine.machines.machine_interface.Machine_Linear`](machines/machine_interface/index.md#PyBM.marine.machines.machine_interface.Machine_Linear "PyBM.marine.machines.machine_interface.Machine_Linear")

Helper class that provides a standard way to create an ABC using inheritance.

cyl_arm_roll* = 10.409*  

cyl_arm_pitch* = 7.327*  

tds_arm_roll* = 11.43*  

tds_arm_pitch* = 8*  

cb_to_tbic_top* = 6.42*  

vmax* = 0.455*  

bore* = 0.47*  

rod* = 0.23*  

stroke* = 1.1*  

p_hpu* = 31500000.0*  

p_hold_bot* = 35000000.0*  

p_hold_rod* = 42000000.0*  

comp_point_max_horizontal_motion* = 2.0*  

cylinder  

CYLINDER_NAMES* = \['c1', 'c2'\]*  

N_CYLINDERS* = 2*  

POI_NAMES* = \['central_bearing', 'comp_point'\]*  

*property *c1  

*property *c2  

cylinder_coordinates  

comp_point_wrt_cb  

comp_point  

workability_checks  

get_POI()[](../../../../source-code/PyBM/marine/machines/HeavyFeeder.py)  
Return cylinder positions w.r.t. RAO definitions.

apply_machine_dofs(*rao*)[](../../../../source-code/PyBM/marine/machines/HeavyFeeder.py)  

check_stroke_limit(*motion_at_poi*)[](../../../../source-code/PyBM/marine/machines/HeavyFeeder.py)  

check_cylinder_velocity_limit(*motion_at_poi*)[](../../../../source-code/PyBM/marine/machines/HeavyFeeder.py)  

check_horizontal_motion_no_comp(*motion_at_poi*)[](../../../../source-code/PyBM/marine/machines/HeavyFeeder.py)  

check_horizontal_motion(*motion_at_poi*)[](../../../../source-code/PyBM/marine/machines/HeavyFeeder.py)  

plot(*axs: matplotlib.axes.Axes = None*)[](../../../../source-code/PyBM/marine/machines/HeavyFeeder.py)  

&nbsp;

*class *PyBM.marine.HeavyFeederSurgeSway(*position*, *orientation*, *comp_point=\[0, 0, 0\]*)[](../../../../source-code/PyBM/marine/machines/HeavyFeederSurgeSway.py)  
Bases: [`PyBM.marine.machines.HeavyFeeder.HeavyFeeder`](machines/HeavyFeeder/index.md#PyBM.marine.machines.HeavyFeeder.HeavyFeeder "PyBM.marine.machines.HeavyFeeder.HeavyFeeder")

Helper class that provides a standard way to create an ABC using inheritance.

workability_checks  

get_POI()[](../../../../source-code/PyBM/marine/machines/HeavyFeederSurgeSway.py)  
Return cylinder positions w.r.t. RAO definitions.

apply_machine_dofs(*rao*)[](../../../../source-code/PyBM/marine/machines/HeavyFeederSurgeSway.py)  

check_stroke_limit(*motion_at_poi*)[](../../../../source-code/PyBM/marine/machines/HeavyFeederSurgeSway.py)  

&nbsp;

*class *PyBM.marine.Machine_Linear(*position*, *orientation*)[](../../../../source-code/PyBM/marine/machines/machine_interface.py)  
Bases: `abc.ABC`

Helper class that provides a standard way to create an ABC using inheritance.

pos  

orient  

rotation  

apply_transform(*point: numpy.array*) → numpy.array[](../../../../source-code/PyBM/marine/machines/machine_interface.py)  
Apply rotation then translation to 3D point

Parameters:  
**point** (*np.array*) – 3D vector \[x,y,z\]

Returns:  
Transformed position

Return type:  
np.array

get_rao_at_poi(*rao*) → [PyBM.marine.motion_analysis.MotionRAO.MotionRAO](motion_analysis/MotionRAO/index.md#PyBM.marine.motion_analysis.MotionRAO.MotionRAO "PyBM.marine.motion_analysis.MotionRAO.MotionRAO")[](../../../../source-code/PyBM/marine/machines/machine_interface.py)  
Get the Motion RAOs at the POI

*abstractmethod *get_POI() → dict[](../../../../source-code/PyBM/marine/machines/machine_interface.py)  

apply_machine_dofs(*rao*) → [PyBM.marine.motion_analysis.MotionRAO.MotionRAO](motion_analysis/MotionRAO/index.md#PyBM.marine.motion_analysis.MotionRAO.MotionRAO "PyBM.marine.motion_analysis.MotionRAO.MotionRAO")[](../../../../source-code/PyBM/marine/machines/machine_interface.py)  

get_workability_limit(*motion_at_poi*, *\*\*kwargs*)[](../../../../source-code/PyBM/marine/machines/machine_interface.py)  

\_\_str\_\_() → str[](../../../../source-code/PyBM/marine/machines/machine_interface.py)  

&nbsp;

*class *PyBM.marine.Machine_Nonlinear(*position*, *orientation*)[](../../../../source-code/PyBM/marine/machines/machine_interface.py)  
Bases: `abc.ABC`

Helper class that provides a standard way to create an ABC using inheritance.

pos  

orient  

rotation  

apply_transform(*point: numpy.array*) → numpy.array[](../../../../source-code/PyBM/marine/machines/machine_interface.py)  
Apply rotation then translation to 3D point

Parameters:  
**point** (*np.array*) – 3D vector \[x,y,z\]

Returns:  
Transformed position

Return type:  
np.array

*abstractmethod *get_POI() → dict[](../../../../source-code/PyBM/marine/machines/machine_interface.py)  

&nbsp;

*class *PyBM.marine.MCG30LHIGHLOAD_Linear(*position*, *gw_luff_angle_mean*, *gw_slew_angle_mean*, *dp_accuracy=0.1*, *gw_telescope_mean=None*)[](../../../../source-code/PyBM/marine/machines/MCG30.py)  
Bases: `mcg30_helper.MCG30LHIGHLOAD_Params`, `MCG30_Linear.MCG30LIFTING_Linear`

Helper class that provides a standard way to create an ABC using inheritance.

&nbsp;

*class *PyBM.marine.MCG30LHIGHLOAD_Nonlinear(*position*, *gw_luff_angle_mean*, *gw_slew_angle_mean*, *dp_accuracy=0.1*, *gw_telescope_mean=None*)[](../../../../source-code/PyBM/marine/machines/MCG30.py)  
Bases: `mcg30_helper.MCG30LHIGHLOAD_Params`, `MCG30_Nonlinear.MCG30LIFTING_Nonlinear`

Helper class that provides a standard way to create an ABC using inheritance.

&nbsp;

*class *PyBM.marine.MCG30LLOWLOAD_Linear(*position*, *gw_luff_angle_mean*, *gw_slew_angle_mean*, *dp_accuracy=0.1*, *gw_telescope_mean=None*)[](../../../../source-code/PyBM/marine/machines/MCG30.py)  
Bases: `mcg30_helper.MCG30LLOWLOAD_Params`, `MCG30_Linear.MCG30LIFTING_Linear`

Helper class that provides a standard way to create an ABC using inheritance.

&nbsp;

*class *PyBM.marine.MCG30LLOWLOAD_Nonlinear(*position*, *gw_luff_angle_mean*, *gw_slew_angle_mean*, *dp_accuracy=0.1*, *gw_telescope_mean=None*)[](../../../../source-code/PyBM/marine/machines/MCG30.py)  
Bases: `mcg30_helper.MCG30LLOWLOAD_Params`, `MCG30_Nonlinear.MCG30LIFTING_Nonlinear`

Helper class that provides a standard way to create an ABC using inheritance.

&nbsp;

*class *PyBM.marine.MCG30LTRANSFER_Linear(*position*, *gw_luff_angle_mean*, *gw_slew_angle_mean*, *dp_accuracy=0.1*, *gw_telescope_mean=None*)[](../../../../source-code/PyBM/marine/machines/MCG30.py)  
Bases: `mcg30_helper.MCG30LTRANSFER_Params`, `MCG30_Linear.MCG30TRANSFER_Linear`

Helper class that provides a standard way to create an ABC using inheritance.

&nbsp;

*class *PyBM.marine.MCG30LTRANSFER_Nonlinear(*position*, *gw_luff_angle_mean*, *gw_slew_angle_mean*, *dp_accuracy=0.1*, *gw_telescope_mean=None*)[](../../../../source-code/PyBM/marine/machines/MCG30.py)  
Bases: `mcg30_helper.MCG30LTRANSFER_Params`, `MCG30_Nonlinear.MCG30TRANSFER_Nonlinear`

Helper class that provides a standard way to create an ABC using inheritance.

&nbsp;

*class *PyBM.marine.MCG30MHIGHLOAD_Linear(*position*, *gw_luff_angle_mean*, *gw_slew_angle_mean*, *dp_accuracy=0.1*, *gw_telescope_mean=None*)[](../../../../source-code/PyBM/marine/machines/MCG30.py)  
Bases: `mcg30_helper.MCG30MHIGHLOAD_Params`, `MCG30_Linear.MCG30LIFTING_Linear`

Helper class that provides a standard way to create an ABC using inheritance.

&nbsp;

*class *PyBM.marine.MCG30MHIGHLOAD_Nonlinear(*position*, *gw_luff_angle_mean*, *gw_slew_angle_mean*, *dp_accuracy=0.1*, *gw_telescope_mean=None*)[](../../../../source-code/PyBM/marine/machines/MCG30.py)  
Bases: `mcg30_helper.MCG30MHIGHLOAD_Params`, `MCG30_Nonlinear.MCG30LIFTING_Nonlinear`

Helper class that provides a standard way to create an ABC using inheritance.

&nbsp;

*class *PyBM.marine.MCG30MLOWLOAD_Linear(*position*, *gw_luff_angle_mean*, *gw_slew_angle_mean*, *dp_accuracy=0.1*, *gw_telescope_mean=None*)[](../../../../source-code/PyBM/marine/machines/MCG30.py)  
Bases: `mcg30_helper.MCG30MLOWLOAD_Params`, `MCG30_Linear.MCG30LIFTING_Linear`

Helper class that provides a standard way to create an ABC using inheritance.

&nbsp;

*class *PyBM.marine.MCG30MLOWLOAD_Nonlinear(*position*, *gw_luff_angle_mean*, *gw_slew_angle_mean*, *dp_accuracy=0.1*, *gw_telescope_mean=None*)[](../../../../source-code/PyBM/marine/machines/MCG30.py)  
Bases: `mcg30_helper.MCG30MLOWLOAD_Params`, `MCG30_Nonlinear.MCG30LIFTING_Nonlinear`

Helper class that provides a standard way to create an ABC using inheritance.

&nbsp;

*class *PyBM.marine.MCG30MTRANSFER_Linear(*position*, *gw_luff_angle_mean*, *gw_slew_angle_mean*, *dp_accuracy=0.1*, *gw_telescope_mean=None*)[](../../../../source-code/PyBM/marine/machines/MCG30.py)  
Bases: `mcg30_helper.MCG30MTRANSFER_Params`, `MCG30_Linear.MCG30TRANSFER_Linear`

Helper class that provides a standard way to create an ABC using inheritance.

&nbsp;

*class *PyBM.marine.MCG30MTRANSFER_Nonlinear(*position*, *gw_luff_angle_mean*, *gw_slew_angle_mean*, *dp_accuracy=0.1*, *gw_telescope_mean=None*)[](../../../../source-code/PyBM/marine/machines/MCG30.py)  
Bases: `mcg30_helper.MCG30MTRANSFER_Params`, `MCG30_Nonlinear.MCG30TRANSFER_Nonlinear`

Helper class that provides a standard way to create an ABC using inheritance.

&nbsp;

*class *PyBM.marine.T700(*position*, *orientation*, *P_passive=35000000.0*)[](../../../../source-code/PyBM/marine/machines/T700.py)  
Bases: [`PyBM.marine.machines.machine_interface.Machine_Linear`](machines/machine_interface/index.md#PyBM.marine.machines.machine_interface.Machine_Linear "PyBM.marine.machines.machine_interface.Machine_Linear")

Helper class that provides a standard way to create an ABC using inheritance.

cd* = 13.8*  

vmax* = 0.736*  

vmax_center* = 0.44*  

stroke* = 2.2*  

max_flow* = 0.044*  

bore* = 0.42*  

rod* = 0.33*  

rod_center* = 0.26*  

cylinder  

CYLINDER_NAMES* = \['c1', 'c2', 'c3'\]*  

N_CYLINDERS* = 3*  

POI_NAMES* = \['center', 'c1', 'c2', 'c3'\]*  

*property *h  

*property *c1  

*property *c2  

*property *c3  

P_passive* = 35000000.0*  

cylinder_coordinates  

workability_checks  

get_POI()[](../../../../source-code/PyBM/marine/machines/T700.py)  
Return cylinder positions w.r.t. RAO definitions.

check_stroke_limit(*motion_at_poi*)[](../../../../source-code/PyBM/marine/machines/T700.py)  

check_cylinder_velocity_limit(*motion_at_poi*)[](../../../../source-code/PyBM/marine/machines/T700.py)  

check_platform_velocity_limit(*motion_at_poi*)[](../../../../source-code/PyBM/marine/machines/T700.py)  

compute_cylinder_forces(*Fz*, *Mx*, *My*)[](../../../../source-code/PyBM/marine/machines/T700.py)  

plot(*axs: matplotlib.axes.Axes = None*)[](../../../../source-code/PyBM/marine/machines/T700.py)  

&nbsp;

*class *PyBM.marine.RAO(*data_vars: xarray.core.types.DataVars \| None = None*, *coords: collections.abc.Mapping\[Any, Any\] \| None = None*, *attrs: collections.abc.Mapping\[Any, Any\] \| None = None*)[](../../../../source-code/PyBM/marine/motion_analysis/RAO.py)  
Bases: `xarray.Dataset`, `abc.ABC`

This is the parent class for motion and force RAOs

\_\_slots\_\_* = ()*  

*abstractmethod *translate_rao(*offset*)[](../../../../source-code/PyBM/marine/motion_analysis/RAO.py)  

*static *default_rao_path(*VesselName*, *revision=0*)[](../../../../source-code/PyBM/marine/motion_analysis/RAO.py)  

*static *group_name(*Vessel_LC*)[](../../../../source-code/PyBM/marine/motion_analysis/RAO.py)  
Return the group name for the RAOs in the database

Parameters:  
**Vessel_LC** – Load Case

*property *group  

modify_conventions(*surge: [SurgeDir](#PyBM.marine.SurgeDir "PyBM.marine.SurgeDir") = SurgeDir.FWD*, *sway: [SwayDir](#PyBM.marine.SwayDir "PyBM.marine.SwayDir") = SwayDir.PORT*, *heave: [HeaveDir](#PyBM.marine.HeaveDir "PyBM.marine.HeaveDir") = HeaveDir.UP*, *roll: [RollDir](#PyBM.marine.RollDir "PyBM.marine.RollDir") = RollDir.PORT_UP*, *pitch: [PitchDir](#PyBM.marine.PitchDir "PyBM.marine.PitchDir") = PitchDir.BOW_DOWN*, *yaw: [YawDir](#PyBM.marine.YawDir "PyBM.marine.YawDir") = YawDir.BOW_PORT*, *wave_origin: [WaveOrigin](#PyBM.marine.WaveOrigin "PyBM.marine.WaveOrigin") = WaveOrigin.STERN*, *rot_unit: [RotationUnit](#PyBM.marine.RotationUnit "PyBM.marine.RotationUnit") = RotationUnit.DEG_PER_M*)[](../../../../source-code/PyBM/marine/motion_analysis/RAO.py)  
Modify the RAO conventions to match the PyBM default. The inputs are the conventions of the data BEFORE modification.

Parameters:  
- **surge** ([*SurgeDir*](#PyBM.marine.SurgeDir "PyBM.marine.SurgeDir")*,* *optional*) – Surge direction convention BEFORE modification (default: SurgeDir.FWD)

- **sway** ([*SwayDir*](#PyBM.marine.SwayDir "PyBM.marine.SwayDir")*,* *optional*) – Sway direction convention BEFORE modification (default: SwayDir.PORT)

- **heave** ([*HeaveDir*](#PyBM.marine.HeaveDir "PyBM.marine.HeaveDir")*,* *optional*) – Heave direction convention BEFORE modification (default: HeaveDir.UP)

- **roll** ([*RollDir*](#PyBM.marine.RollDir "PyBM.marine.RollDir")*,* *optional*) – Roll direction convention BEFORE modification (default: RollDir.PORT_UP)

- **pitch** ([*PitchDir*](#PyBM.marine.PitchDir "PyBM.marine.PitchDir")*,* *optional*) – Pitch direction convention BEFORE modification (default: PitchDir.BOW_DOWN)

- **yaw** ([*YawDir*](#PyBM.marine.YawDir "PyBM.marine.YawDir")*,* *optional*) – Yaw direction convention BEFORE modification (default: YawDir.BOW_PORT)

- **wave_origin** ([*WaveOrigin*](#PyBM.marine.WaveOrigin "PyBM.marine.WaveOrigin")*,* *optional*) – Wave direction convention BEFORE modification (default: WaveOrigin.STERN)

- **rot_unit** ([*RotationUnit*](#PyBM.marine.RotationUnit "PyBM.marine.RotationUnit")*,* *optional*) – Rotation unit convention BEFORE modification (default: RotationUnit.DEG_PER_M)

*classmethod *load_rao(*filename*, *Vessel_LC*)[](../../../../source-code/PyBM/marine/motion_analysis/RAO.py)  
Load RAO from database.

*classmethod *from_api(*VesselName*, *Vessel_LC*)[](../../../../source-code/PyBM/marine/motion_analysis/RAO.py)  
Load RAO from API.

Parameters:  
- **VesselName** – Name of the vessel

- **Vessel_LC** – Name of the load case

Returns:  
RAO object

Raises:  
**ValueError** – If RAO or load case not found (with available options listed)

save_rao(*filename=None*, *revision=None*, *replace=False*)[](../../../../source-code/PyBM/marine/motion_analysis/RAO.py)  
Save RAO to NetCDF file

Parameters:  
- **filename** – filepath to save the rao

- **replace** – Replace the file if it exists, otherwise append to the data

get_roll_period()[](../../../../source-code/PyBM/marine/motion_analysis/RAO.py)  
Get the roll period from the RAOs

plot(*directions=None*, *amplitude=True*, *keys=None*)[](../../../../source-code/PyBM/marine/motion_analysis/RAO.py)  
Plot the RAO for selected directions.

Parameters:  
- **directions** – Vector of directions. Default: All directions are used

- **amplitude** – Plot RAO amplitudes if True. Plot phases if False.

&nbsp;

*class *PyBM.marine.MotionRAO(*data_vars: xarray.core.types.DataVars \| None = None*, *coords: collections.abc.Mapping\[Any, Any\] \| None = None*, *attrs: collections.abc.Mapping\[Any, Any\] \| None = None*)[](../../../../source-code/PyBM/marine/motion_analysis/MotionRAO.py)  
Bases: [`PyBM.marine.motion_analysis.RAO.RAO`](motion_analysis/RAO/index.md#PyBM.marine.motion_analysis.RAO.RAO "PyBM.marine.motion_analysis.RAO.RAO")

This is the parent class for motion and force RAOs

\_\_slots\_\_* = ()*  

translate_rao(*offset*)[](../../../../source-code/PyBM/marine/motion_analysis/MotionRAO.py)  
Translates the RAO to a point of interest. Ref\[1\] eq (4.27)

Parameters:  
**offset** – \[m\] (x,y,z) offset of the point of interest

Returns:  
Full vessel motion RAOs around POI

&nbsp;

PyBM.marine.g* = 9.81*[](../../../../source-code/PyBM/constants.py)  

&nbsp;

*class *PyBM.marine.SurgeDir(*\*args*, *\*\*kwds*)[](../../../../source-code/PyBM/marine/motion_analysis/RAO.py)  
Bases: `enum.Enum`

Enum for Surge direction

FWD* = 1*  

AFT* = -1*  

&nbsp;

*class *PyBM.marine.SwayDir(*\*args*, *\*\*kwds*)[](../../../../source-code/PyBM/marine/motion_analysis/RAO.py)  
Bases: `enum.Enum`

Enum for Sway direction

PORT* = 1*  

STARBOARD* = -1*  

&nbsp;

*class *PyBM.marine.HeaveDir(*\*args*, *\*\*kwds*)[](../../../../source-code/PyBM/marine/motion_analysis/RAO.py)  
Bases: `enum.Enum`

Enum for Heave direction

UP* = 1*  

DOWN* = -1*  

&nbsp;

*class *PyBM.marine.RollDir(*\*args*, *\*\*kwds*)[](../../../../source-code/PyBM/marine/motion_analysis/RAO.py)  
Bases: `enum.Enum`

Enum for Roll direction

PORT_UP* = 1*  

PORT_DOWN* = -1*  

&nbsp;

*class *PyBM.marine.PitchDir(*\*args*, *\*\*kwds*)[](../../../../source-code/PyBM/marine/motion_analysis/RAO.py)  
Bases: `enum.Enum`

Enum for Pitch direction

BOW_DOWN* = 1*  

BOW_UP* = -1*  

&nbsp;

*class *PyBM.marine.YawDir(*\*args*, *\*\*kwds*)[](../../../../source-code/PyBM/marine/motion_analysis/RAO.py)  
Bases: `enum.Enum`

Enum for Yaw direction

BOW_PORT* = 1*  

BOW_STARBOARD* = -1*  

&nbsp;

*class *PyBM.marine.WaveOrigin(*\*args*, *\*\*kwds*)[](../../../../source-code/PyBM/marine/motion_analysis/RAO.py)  
Bases: `enum.Enum`

Enum for Wave direction

STERN* = 0*  

STARBOARD* = 90*  

BOW* = 180*  

PORT* = 270*  

&nbsp;

*class *PyBM.marine.RotationUnit(*\*args*, *\*\*kwds*)[](../../../../source-code/PyBM/marine/motion_analysis/RAO.py)  
Bases: `enum.Enum`

Enum for Rotation unit

DEG_PER_M* = 1*  

RAD_PER_M  

DEG_PER_FT* = 3.28084*  

DEG_PER_DEG* = 0*  

RAD_PER_RAD  

&nbsp;

PyBM.marine.\_recursive_group_names(*groups: dict*, *parent=None*)[](../../../../source-code/PyBM/marine/motion_analysis/RAO.py)  
Recursively get the group names from a dictionary of groups

&nbsp;

*exception *PyBM.marine.OutofBoundsError[](../../../../source-code/PyBM/exceptions.py)  
Bases: `Exception`

Common base class for all non-exit exceptions.

&nbsp;

PyBM.marine.compute_response(*wave: [PyBM.marine.wave_spectrum.WaveSpectrum](wave_spectrum/index.md#id42 "PyBM.marine.wave_spectrum.WaveSpectrum")*, *rao: [PyBM.marine.motion_analysis.RAO](motion_analysis/index.md#id0 "PyBM.marine.motion_analysis.RAO")*, *poi=None*, *Nfreqs=200*, *f_bounds=None*)[](../../../../source-code/PyBM/marine/motion_analysis/Response.py)  
Compute the vessel response based on the given wave spectrum and RAO.

Parameters:  
- **wave** ([*WaveSpectrum*](#PyBM.marine.WaveSpectrum "PyBM.marine.WaveSpectrum")) – The wave spectrum.

- **rao** ([*RAO*](#PyBM.marine.RAO "PyBM.marine.RAO")) – The response amplitude operator.

- **poi** (*list,* *optional*) – The point of interest \[x,y,z\] in meters, defaults to None.

- **Nfreqs** (*int,* *optional*) – The number of frequencies to consider, defaults to 200.

- **f_bounds** (*tuple,* *optional*) – The frequency bounds, defaults to None.

Returns:  
The computed vessel response.

Return type:  
Response

&nbsp;

PyBM.marine.compute_mpe(*wave: [PyBM.marine.wave_spectrum.WaveSpectrum](wave_spectrum/index.md#id42 "PyBM.marine.wave_spectrum.WaveSpectrum")*, *rao: [PyBM.marine.motion_analysis.RAO](motion_analysis/index.md#id0 "PyBM.marine.motion_analysis.RAO")*, *poi=None*, *storm_duration=10800*, *transfer_function=None*)[](../../../../source-code/PyBM/marine/motion_analysis/Response.py)  
Calculate MPE of the given parameter for all points of interest (POI).

Parameters:  
- **poi** – \[m\] (x,y,z) offset of point of interest

- **storm_duration** – \[s\] duration of the period of interest (usually 3 hours)

- **transfer_function** – (\[\[a\], \[b\]\]) Numerator and Denumerator of continuous transfer function to be applied.

Returns:  
Statistical extreme value

&nbsp;

PyBM.marine.equal_energy_freqs_rao(*wave: [PyBM.marine.wave_spectrum.WaveSpectrum](wave_spectrum/index.md#id42 "PyBM.marine.wave_spectrum.WaveSpectrum")*, *rao: [PyBM.marine.motion_analysis.RAO](motion_analysis/index.md#id0 "PyBM.marine.motion_analysis.RAO")*, *Nfreqs*, *f_bounds=None*)[](../../../../source-code/PyBM/marine/motion_analysis/Response.py)  

&nbsp;

PyBM.marine.apply_directional_spreading(*wave: [PyBM.marine.wave_spectrum.WaveSpectrum](wave_spectrum/index.md#id42 "PyBM.marine.wave_spectrum.WaveSpectrum")*, *rao: [PyBM.marine.motion_analysis.RAO](motion_analysis/index.md#id0 "PyBM.marine.motion_analysis.RAO")*)[](../../../../source-code/PyBM/marine/motion_analysis/Response.py)  

&nbsp;

*class *PyBM.marine.SpectralTools(*xarray_obj*)[](../../../../source-code/PyBM/marine/motion_analysis/SpectrumAccessor.py)  
Tools to analyse spectra.

\_obj  

\_amp* = None*  

\_m0* = None*  

\_m1* = None*  

\_m2* = None*  

*property *m0  

*property *m1  

*property *m2  

*property *amp  

spectral_moment(*order=0*)[](../../../../source-code/PyBM/marine/motion_analysis/SpectrumAccessor.py)  
Compute nth order spectral moment of a spectrum. Ref \[1\]. Eq (6.81)

Parameters:  
**order** (*int,* *optional*) – Order of the moment, defaults to 0

*property *standard_deviation  
Compute the standard deviation from the frequency response. Ref. \[1\] Eq (6.82)

Parameters:  
**m0** – 0th Spectral moment

Returns:  
Standard deviation

*property *zero_crossing_period  
Compute zero-crossing period. Ref. \[1\] Eq (6.84)

Returns:  
\[s\] Average zero crossing period.

MPE(*storm_duration=10800*, *standard_deviations=None*)[](../../../../source-code/PyBM/marine/motion_analysis/SpectrumAccessor.py)  
Compute Most Probable Extreme from Rayleigh Distribution based on storm duration and Zero-crossing period. Ref \[1\], Section 11.1 Eq (11.20)

Parameters:  
**storm_duration** – \[s\] duration of the period of interest (usually 3 hours)

Returns:  
Most probable extreme.

&nbsp;

*class *PyBM.marine.EqualEnergySpectrum(*xarray_obj*)[](../../../../source-code/PyBM/marine/motion_analysis/SpectrumAccessor.py)  
Bases: [`SpectralTools`](#PyBM.marine.SpectralTools "PyBM.marine.SpectralTools")

Tools to analyse spectra optimized for equal energy frequencies.

spectral_moment(*order=0*)[](../../../../source-code/PyBM/marine/motion_analysis/SpectrumAccessor.py)  
Compute nth order spectral moment of an equal energy spectrum. Ref \[1\]. Eq (6.81)

Parameters:  
**order** (*int,* *optional*) – Order of the moment, defaults to 0

&nbsp;

PyBM.marine.isFileLocked(*filePath*)[](../../../../source-code/PyBM/utils/windows_helpers.py)  
Source: [https://stackoverflow.com/questions/13371444/python-check-file-is-locked](https://stackoverflow.com/questions/13371444/python-check-file-is-locked) Checks to see if a file is locked. Performs three checks

> 1.  Checks if the file even exists
>
> 2.  Attempts to open the file for reading. This will determine if the file has a write lock.  
>     Write locks occur when the file is being edited or copied to, e.g. a file copy destination
>
> 3.  Attempts to rename the file. If this fails the file is open by some other process for reading. The  
>     file can be read, but not written to or deleted.

Parameters:  
**filePath** – path of file to check

&nbsp;

*class *PyBM.marine.TimeDomainTools(*xarray_obj*)[](../../../../source-code/PyBM/marine/motion_analysis/TimeDomain.py)  
Tools for time domain traces in xarray.DataArray type

\_obj  

translate_trace(*offset: numpy.array*)[](../../../../source-code/PyBM/marine/motion_analysis/TimeDomain.py)  
Translates the trace in 6 DOF. Does not use small angle approx..

Parameters:  
**offset** (*np.array*) – offset in \[x,y,z\]

translate_trace_smallangle(*offset: numpy.array*)[](../../../../source-code/PyBM/marine/motion_analysis/TimeDomain.py)  
Translates the trace in 6 DOF. Uses small angle approx

Parameters:  
**offset** (*np.array*) – offset in \[x,y,z\]

&nbsp;

*class *PyBM.marine.TimeDomain(*wave: [PyBM.marine.wave_spectrum.WaveSpectrum](wave_spectrum/index.md#id42 "PyBM.marine.wave_spectrum.WaveSpectrum")*, *rao: [PyBM.marine.motion_analysis.MotionRAO.MotionRAO](motion_analysis/MotionRAO/index.md#PyBM.marine.motion_analysis.MotionRAO.MotionRAO "PyBM.marine.motion_analysis.MotionRAO.MotionRAO")*, *vesselCoG*)[](../../../../source-code/PyBM/marine/motion_analysis/TimeDomain.py)  
rao  

vesselCoG  

wave  

*static *time_vector(*dt*, *duration*)[](../../../../source-code/PyBM/marine/motion_analysis/TimeDomain.py)  
Create labelled time vector

Parameters:  
- **dt** – \[s\] Time step

- **duration** – \[s\] Duration of time trace

generate_mat_time_traces(*folder: str*, *dt*, *duration*, *wave*)[](../../../../source-code/PyBM/marine/motion_analysis/TimeDomain.py)  
Generate .mat time traces to be used in the matlab workability tools.

Parameters:  
- **folder** – Folder to save the files

- **dt** – \[s\] Time step

- **duration** – \[s\] Duration of time trace

- **wave** – \[s\] Wave to generate time traces for. Parameters may be vectorized.

- **directions** – \[deg\] Wave directions

generate_time_traces(*folder: str*, *dt*, *duration*, *wave*)[](../../../../source-code/PyBM/marine/motion_analysis/TimeDomain.py)  
Generate .mat time traces to be used in the matlab workability tools.

Parameters:  
- **folder** – Folder to save the files

- **dt** – \[s\] Time step

- **duration** – \[s\] Duration of time trace

- **wave** – \[s\] Wave to generate time traces for. Parameters may be vectorized.

- **directions** – \[deg\] Wave directions

save_mat_file(*folder*, *trace*)[](../../../../source-code/PyBM/marine/motion_analysis/TimeDomain.py)  
Vectorized saving function

save_nc_file(*folder*, *trace*)[](../../../../source-code/PyBM/marine/motion_analysis/TimeDomain.py)  

*static *\_save_nc_file(*folder*, *traces: xarray.DataArray*, *VesselName*, *vesselCoG*)[](../../../../source-code/PyBM/marine/motion_analysis/TimeDomain.py)  
Save traces as a single nc file. will append nc with extra coordinates, if already there. :param folder: folder name :type folder: string :param traces: traces to save. :type traces: xarray.DataArray

*static *default_trace_path(*VesselName*, *revision=0*)[](../../../../source-code/PyBM/marine/motion_analysis/TimeDomain.py)  

load_time_trace(*folder*)[](../../../../source-code/PyBM/marine/motion_analysis/TimeDomain.py)  
Loads time traces. Tries to open nc files first, if non existent, opens mat files. :param folder: folder name :type folder: str

*static *load_all_default_time_traces(*VesselName*, *rev=0*)[](../../../../source-code/PyBM/marine/motion_analysis/TimeDomain.py)  
Load the time traces of the given vessel and revision in the default engineering library folder. :param VesselName: vessel name :type VesselName: str :param rev: revision number :type rev: int

*static *load_all_time_traces(*folder*, *VesselName*)[](../../../../source-code/PyBM/marine/motion_analysis/TimeDomain.py)  
Static version of load_time_trace. Loads all time traces present in given folder. do not need to supply any sort of dimensioning for Tp, Hs or direction. If using default trace path, you can also use the function TimeDomain.load_default_time_trace(). :param folder: folder to load time traces from. :type folder: str :param VesselName: name of the vessel to be loaded. :type VesselName: str

load_mat_time_trace(*folder*)[](../../../../source-code/PyBM/marine/motion_analysis/TimeDomain.py)  
Load a MAT time trace(s) as DataArray. Uses objects’ properties for selecting which traces to load.

Parameters:  
**folder** (*str*) – path of folder

*static *\_load_mat_time_trace(*folder*, *VesselName*, *Tp*, *Hs*, *Direction*)[](../../../../source-code/PyBM/marine/motion_analysis/TimeDomain.py)  
Vectorized static function to load mat time traces according to given parameters.

*static *\_load_single_mat_time_trace(*folder*, *VesselName*, *Tp*, *Hs*, *Direction*)[](../../../../source-code/PyBM/marine/motion_analysis/TimeDomain.py)  

load_nc_time_trace(*folder*)[](../../../../source-code/PyBM/marine/motion_analysis/TimeDomain.py)  
Load NC stored time trace(s) as DataArray

Parameters:  
**folder** – path of folder

*static *\_load_nc_time_trace(*folder*, *VesselName*)[](../../../../source-code/PyBM/marine/motion_analysis/TimeDomain.py)  
Loads nc file with traces.

mat_file_name()[](../../../../source-code/PyBM/marine/motion_analysis/TimeDomain.py)  

*static *\_mat_file_name(*VesselName*, *Tp*, *Hs*, *Direction*)[](../../../../source-code/PyBM/marine/motion_analysis/TimeDomain.py)  
Returns mat file names for trace. Broadcasts arrays in case of multiple values for Tp,Hs,main_direction.

nc_file_name()[](../../../../source-code/PyBM/marine/motion_analysis/TimeDomain.py)  

*static *\_nc_file_name(*VesselName*)[](../../../../source-code/PyBM/marine/motion_analysis/TimeDomain.py)  
Returns nc file name for trace. Since nc files include all directions it is not a vectorized function

*static *\_file_name(*VesselName*, *Tp*, *Hs*, *Direction*)[](../../../../source-code/PyBM/marine/motion_analysis/TimeDomain.py)  

*static *time_trace_from_rao_and_wave(*time: xarray.DataArray*, *wave: [PyBM.marine.wave_spectrum.WaveSpectrum](wave_spectrum/index.md#id42 "PyBM.marine.wave_spectrum.WaveSpectrum")*, *rao: [PyBM.marine.motion_analysis.MotionRAO.MotionRAO](motion_analysis/MotionRAO/index.md#PyBM.marine.motion_analysis.MotionRAO.MotionRAO "PyBM.marine.motion_analysis.MotionRAO.MotionRAO")*, *Nfreqs=100*, *bounds=None*)[](../../../../source-code/PyBM/marine/motion_analysis/TimeDomain.py)  
Generate time trace based on RAO and Wave.

Parameters:  
- **time** (*xr.DataArray*) – \[s\] time vector

- **wave** ([*WaveSpectrum*](#PyBM.marine.WaveSpectrum "PyBM.marine.WaveSpectrum")) – \[m2/(rad/s)\] WaveSpectrum

- **rao** ([*MotionRAO*](#PyBM.marine.MotionRAO "PyBM.marine.MotionRAO")) – \[m/m, deg/m\] 6DOF Motion RAO

multi_directional_time_trace(*wave: [PyBM.marine.wave_spectrum.WaveSpectrum](wave_spectrum/index.md#id42 "PyBM.marine.wave_spectrum.WaveSpectrum")*, *rao: [PyBM.marine.motion_analysis.MotionRAO.MotionRAO](motion_analysis/MotionRAO/index.md#PyBM.marine.motion_analysis.MotionRAO.MotionRAO "PyBM.marine.motion_analysis.MotionRAO.MotionRAO")*, *bounds=None*)[](../../../../source-code/PyBM/marine/motion_analysis/TimeDomain.py)  
Create time trace including wave spreading.

Parameters:  
- **time** (*xr.DataArray*) – \[s\] time vector

- **rao** ([*MotionRAO*](#PyBM.marine.MotionRAO "PyBM.marine.MotionRAO")) – \[m/m, deg/m\] 6DOF Motion RAO

- **wave** ([*WaveSpectrum*](#PyBM.marine.WaveSpectrum "PyBM.marine.WaveSpectrum")) – \[m2/(rad/s)\] WaveSpectrum

single_direction_time_trace(*wave: [PyBM.marine.wave_spectrum.WaveSpectrum](wave_spectrum/index.md#id42 "PyBM.marine.wave_spectrum.WaveSpectrum")*, *rao: [PyBM.marine.motion_analysis.MotionRAO.MotionRAO](motion_analysis/MotionRAO/index.md#PyBM.marine.motion_analysis.MotionRAO.MotionRAO "PyBM.marine.motion_analysis.MotionRAO.MotionRAO")*)[](../../../../source-code/PyBM/marine/motion_analysis/TimeDomain.py)  
Create time trace for a single wave direction

Parameters:  
- **time** (*xr.DataArray*) – \[s\] time vector

- **rao** ([*MotionRAO*](#PyBM.marine.MotionRAO "PyBM.marine.MotionRAO")) – \[m/m, deg/m\] 6DOF Motion RAO. Must have interpolated frequencies according to equal area method

- **wave** ([*WaveSpectrum*](#PyBM.marine.WaveSpectrum "PyBM.marine.WaveSpectrum")) – \[m2/(rad/s)\] WaveSpectrum

*static *compute_deltas(*coordinates*, *dim*)[](../../../../source-code/PyBM/marine/motion_analysis/TimeDomain.py)  
Create bins centered a coordinate points.

Parameters:  
- **coordinates** – Coordinates to create bins around.

- **dim** – Dimension name

*static *zero_crossing_period(*trace*)[](../../../../source-code/PyBM/marine/motion_analysis/TimeDomain.py)  
Compute average zero-crossing period of a time trace.

return: \[s\] average zero-crossing period.

&nbsp;

PyBM.marine.Octopus_to_RAO(*octopus_file*, *VesselName*, *Vessel_LC*, *speed=0*)[](../../../../source-code/PyBM/marine/tools/import_octopus_rao.py)  

&nbsp;

PyBM.marine.get_speeds(*file_iterator*)[](../../../../source-code/PyBM/marine/tools/import_octopus_rao.py)  

&nbsp;

PyBM.marine.get_wave_directions(*file_iterator*)[](../../../../source-code/PyBM/marine/tools/import_octopus_rao.py)  

&nbsp;

PyBM.marine.get_wave_frequencies(*file_iterator*, *speed*)[](../../../../source-code/PyBM/marine/tools/import_octopus_rao.py)  

&nbsp;

PyBM.marine.LIS_to_RAO(*filename*, *VesselName*, *Vessel_LC*)[](../../../../source-code/PyBM/marine/tools/LIS_to_Xarray.py)  
Convert LIS data to MotionRAO object.

Parameters:  
- **filename** – path to LIS file

- **VesselName** – Name of the vessel

- **Vessel_LC** – Vessel Loading condition

&nbsp;

PyBM.marine.load_LIS(*filename*)[](../../../../source-code/PyBM/marine/tools/LIS_to_Xarray.py)  

&nbsp;

PyBM.marine.XLS_to_RAO(*filename*, *VesselName*, *Vessel_LC*, *origin*, *mirror=False*)[](../../../../source-code/PyBM/marine/tools/XLS_to_Xarray.py)  
Convert excel file to Xarray RAO object

Parameters:  
- **filename** – Excel file with RAO data

- **VesselName** – Name of vessel

- **Vessel_LC** – Loading condition of the vessel

- **origin** – \[m\] \[x, y, z\] origin of the RAOs w.r.t to vessel APP/CL/Keel

Returns:  
MotionRAO object

Return type:  
[MotionRAO](#PyBM.marine.MotionRAO "PyBM.marine.MotionRAO")

&nbsp;

PyBM.marine.load_XLS(*filename*, *mirror*)[](../../../../source-code/PyBM/marine/tools/XLS_to_Xarray.py)  

&nbsp;

PyBM.marine.CSV_to_RAO(*filename*, *VesselName*, *Vessel_LC*, *origin*, *mirror=False*)[](../../../../source-code/PyBM/marine/tools/CSV_to_Xarray.py)  
Convert CSV file to Xarray RAO object

Parameters:  
- **filename** – CSV file with RAO data

- **VesselName** – Name of vessel

- **Vessel_LC** – Loading condition of the vessel

- **origin** – \[m\] \[x, y, z\] origin of the RAOs w.r.t to vessel APP/CL/Keel

Returns:  
MotionRAO object

Return type:  
[MotionRAO](#PyBM.marine.MotionRAO "PyBM.marine.MotionRAO")

&nbsp;

PyBM.marine.load_CSV(*filename*, *mirror*)[](../../../../source-code/PyBM/marine/tools/CSV_to_Xarray.py)  

&nbsp;

PyBM.marine.TXT_to_RAO(*filename*, *VesselName*, *Vessel_LC*, *origin*, *mirror=False*)[](../../../../source-code/PyBM/marine/tools/TXT_to_Xarray.py)  
Convert OrcaFlex .txt file to MotionRAO object.

&nbsp;

PyBM.marine.load_TXT(*filename*, *mirror=False*)[](../../../../source-code/PyBM/marine/tools/TXT_to_Xarray.py)  

&nbsp;

PyBM.marine.\_\_file_len(*fname*)[](../../../../source-code/PyBM/marine/tools/read_res.py)  

&nbsp;

PyBM.marine.resample(*data*, *new_dt*, *data_dt*)[](../../../../source-code/PyBM/marine/tools/read_res.py)  

&nbsp;

PyBM.marine.\_\_read_file(*filename*, *read_invalid=True*)[](../../../../source-code/PyBM/marine/tools/read_res.py)  

&nbsp;

PyBM.marine.read_res(*filename*, *dt=0*, *read_invalid=True*)[](../../../../source-code/PyBM/marine/tools/read_res.py)  
Read a text .res file with time traces.

Parameters:  
- **filename** – name of file without extension

- **dt** – \[s\] sample time, if 0 the original sample time is used

- **read_invalid** – \[bool\] If false, invalid files are moved to Invalid folder

Returns:  
Dictionary of time_vectors.

&nbsp;

PyBM.marine.write_pickle(*filename*, *data_dict*)[](../../../../source-code/PyBM/marine/tools/read_res.py)  

&nbsp;

PyBM.marine.write_res(*filename*, *data_dict*)[](../../../../source-code/PyBM/marine/tools/read_res.py)  
Write a data dictionary to a .res text file.

Parameters:  
- **filename** – name of file (without extension)

- **data_dict** – dictionary of key / time_vector pairs

&nbsp;

*class *PyBM.marine.PiersonMoskowitz(*Hs*, *Tp*, *main_direction*, *Ndirs=11*, *spreading=4.0*)[](../../../../source-code/PyBM/marine/wave_spectrum/PiersonMoskowitz.py)  
Bases: [`PyBM.marine.wave_spectrum.WaveSpectrum.WaveSpectrum`](wave_spectrum/WaveSpectrum/index.md#PyBM.marine.wave_spectrum.WaveSpectrum.WaveSpectrum "PyBM.marine.wave_spectrum.WaveSpectrum.WaveSpectrum")

This class defines the Pierson Moskowitz Frequency spectrum.

power_spectrum(*freqs*)[](../../../../source-code/PyBM/marine/wave_spectrum/PiersonMoskowitz.py)  
Compute frequency spectrum for the given frequency points.

Parameters:  
**freqs** – \[Hz\] list of frequency components

Returns:  
\[m2/Hz\] Wave spectral density

*static *\_power_spectrum(*freqs*, *Tp*, *Hs*)[](../../../../source-code/PyBM/marine/wave_spectrum/PiersonMoskowitz.py)  
Ref \[2\] 3.5.5.1

Parameters:  
- **Hs** – \[m\] Significant wave height

- **Tp** – \[s\] Peak period

&nbsp;

*class *PyBM.marine.WaveSpectrum(*Hs*, *Tp*, *main_direction*, *Ndirs=11*, *spreading=4.0*)[](../../../../source-code/PyBM/marine/wave_spectrum/WaveSpectrum.py)  
Bases: `abc.ABC`

Helper class that provides a standard way to create an ABC using inheritance.

*property *Hs  

*property *Tp  

*property *main_direction  
\[deg\] Main direction of wave.

spreading* = 4.0*  

*property *Ndirs  
\[-\] Number of wave directions to use (should be odd).

\_\_str\_\_()[](../../../../source-code/PyBM/marine/wave_spectrum/WaveSpectrum.py)  

*abstractmethod *power_spectrum(*freqs*)[](../../../../source-code/PyBM/marine/wave_spectrum/WaveSpectrum.py)  
Compute frequency spectrum for the given frequency points.

Parameters:  
- **freqs** – \[Hz\] list of frequency components

- **plot** – True to plot spectrum

Returns:  
\[m2/(rad/s)\] Wave spectral density

wave_spectrum(*freqs*)[](../../../../source-code/PyBM/marine/wave_spectrum/WaveSpectrum.py)  
Compute frequency spectrum for the given frequency points.

Parameters:  
- **freqs** – \[Hz\] list of frequency components

- **plot** – True to plot spectrum

Returns:  
\[m2/(rad/s)\] Wave spectral density

equal_energy_frequencies(*bounds*, *df=None*, *Nfreqs=100*)[](../../../../source-code/PyBM/marine/wave_spectrum/WaveSpectrum.py)  
Numeric method to calculate frequencies at equal energies.

Parameters:  
**Nfreqs** (*int,* *optional*) – NUmber of frequency components to generate, defaults to 100

equal_energy_directions(*Ndirs=None*)[](../../../../source-code/PyBM/marine/wave_spectrum/WaveSpectrum.py)  
Compute the directions to use for equal energy directional spreading.

Parameters:  
**Ndirs** – \[-\] number of directions (must be odd)

Returns:  
\[deg\] Vector of directions

*static *equal_energy_method(*func_power_spectrum*, *bounds*, *N*)[](../../../../source-code/PyBM/marine/wave_spectrum/WaveSpectrum.py)  
Numeric equal area method. :param func_power_spectrum: Function that outputs the power spectrum, such as a wave spectrum power spectrum or a spreading function. Must accept array of x coordinates, and output either a xr.DataArray or an array of y. :param bounds: bounds of X, as an array or tuple: (xmin, xmax) :param N: Number of X to divide energy over

directional_wave_spectrum(*freqs*, *Rel_Dirs*)[](../../../../source-code/PyBM/marine/wave_spectrum/WaveSpectrum.py)  
Compute combined directional wave spectrum.

Parameters:  
- **freqs** – \[Hz\] list of frequency components

- **Rel_Dirs** – \[deg\] list of wave directions relative to main direction (between -180 and 180 degrees).

Returns:  
\[m2/Hz\] Wave spectral density

abs_directions(*Rel_Dirs*)[](../../../../source-code/PyBM/marine/wave_spectrum/WaveSpectrum.py)  

equal_energy_directional_wave_spectrum(*freqs*, *Ndirs=None*)[](../../../../source-code/PyBM/marine/wave_spectrum/WaveSpectrum.py)  
Compute directional wave spectrim with spreading using equal energy directions.

Parameters:  
- **freqs** – \[Hz\] Vector of frequency points

- **Ndirs** – \[-\] Number of directions (must be odd)

Returns:  
Directional wave Spectrum

equal_energy_directional_spreading(*Ndirs=None*)[](../../../../source-code/PyBM/marine/wave_spectrum/WaveSpectrum.py)  
Compute directional wave spreading using equal energy directions.

Parameters:  
- **Ndirs** – \[-\] Number of directions (must be odd)

- **plot** – plots the spectrum if True

Returns:  
Directional wave spreading

directional_spreading(*relative_dirs*)[](../../../../source-code/PyBM/marine/wave_spectrum/WaveSpectrum.py)  
Compute directional spreading factors for the given directions.

Function is based on the Cos^n function defined in the Orcaflex documentation.

Parameters:  
- **relative_dirs** – \[deg\] list of wave directions relative to main direction (between -180 and 180 degrees).

- **plot** – True to plot directional spreading

Returns:  
\[-\] spreading factor corresponding to each direction

*static *shift_direction(*wave_data*, *angle_shift*)[](../../../../source-code/PyBM/marine/wave_spectrum/WaveSpectrum.py)  

plot(*freqs*, *Rel_Dirs*, *ax=None*)[](../../../../source-code/PyBM/marine/wave_spectrum/WaveSpectrum.py)  

&nbsp;

PyBM.marine.logger[](../../../../source-code/PyBM/marine/wave_spectrum/PiersonMoskowitz.py)  

&nbsp;

*class *PyBM.marine.Jonswap(*Hs*, *Tp*, *main_direction*, *Ndirs=11*, *spreading=4*, *gamma=None*)[](../../../../source-code/PyBM/marine/wave_spectrum/Jonswap.py)  
Bases: [`PyBM.marine.wave_spectrum.WaveSpectrum.WaveSpectrum`](wave_spectrum/WaveSpectrum/index.md#PyBM.marine.wave_spectrum.WaveSpectrum.WaveSpectrum "PyBM.marine.wave_spectrum.WaveSpectrum.WaveSpectrum")

This class defines the JONSWAP Frequency spectrum.

Parameters:  
- **Hs** – \[m\] Significant wave height

- **Tp** – \[s\] Peak period

- **main_direction** – \[deg\] Wave direction: 0 is from stern 180 from bow, 90 from starboard

- **Ndirs** – \[-\] Number of wave directions

- **spreading** – \[-\] Wave spreading, unidirectional is used if spreading =\< 0

- **gamma** – \[-\] Peakness factor, according to DNV if not specified

\_\_str\_\_()[](../../../../source-code/PyBM/marine/wave_spectrum/Jonswap.py)  

*property *gamma  

*property *Tz  
Zero up-crossing period \[s\]

*static *Tz_to_Tp(*Tz*)[](../../../../source-code/PyBM/marine/wave_spectrum/Jonswap.py)  
Convert zero up-crossing period to peak period \[s\]

Parameters:  
**Tz** – Zero up-crossing period \[s\]

Returns:  
Peak period \[s\]

*static *\_compute_gamma(*Tp*, *Hs*)[](../../../../source-code/PyBM/marine/wave_spectrum/Jonswap.py)  
Compute gamma according to DNV regulations \[2\] 3.5.5.5

Parameters:  
- **Tp** – Peak Period \[s\]

- **Hs** – Significant wave height \[m\]

Returns:  
\[-\] peakedness factor

compute_gamma()[](../../../../source-code/PyBM/marine/wave_spectrum/Jonswap.py)  

power_spectrum(*freqs: xarray.DataArray*)[](../../../../source-code/PyBM/marine/wave_spectrum/Jonswap.py)  
Compute frequency spectrum for the given frequency points.

Parameters:  
**freqs** – \[Hz\] list of frequency components

Returns:  
\[m2/Hz\] Wave spectral density

*static *\_power_spectrum(*freqs*, *gamma*, *Tp*, *Hs*)[](../../../../source-code/PyBM/marine/wave_spectrum/Jonswap.py)  

&nbsp;

*class *PyBM.marine.Torsethaugen(*Hs*, *Tp*, *main_direction*, *Ndirs=11*, *spreading=4*, *offset=0*)[](../../../../source-code/PyBM/marine/wave_spectrum/Torsethaugen.py)  
Bases: [`PyBM.marine.wave_spectrum.WaveSpectrum.WaveSpectrum`](wave_spectrum/WaveSpectrum/index.md#PyBM.marine.wave_spectrum.WaveSpectrum.WaveSpectrum "PyBM.marine.wave_spectrum.WaveSpectrum.WaveSpectrum")

This class defines the Torsethaugen Frequency spectrum.

offset* = 0*  

power_spectrum(*freqs*)[](../../../../source-code/PyBM/marine/wave_spectrum/Torsethaugen.py)  
Compute frequency spectrum for the given frequency points.

Parameters:  
- **freqs** – \[Hz\] list of frequency components

- **Npeak** – \[0, 1 or 2\] 0: use full Torsethaugen spectrum. 1: use first peak only. 2: use second peak only

Returns:  
\[m2/Hz\] Wave spectral density

*static *\_power_spectrum_parameters(*Tp*, *Hs*)[](../../../../source-code/PyBM/marine/wave_spectrum/Torsethaugen.py)  
Compute power spectral parameters for the Torsethaugen double peak spectrum :param Tp: peak wave period :param Hs: significant wave height :return: \[H1, Tp1, H2, Tp2, y, winddominated\]

*static *\_power_spectrum(*freqs*, *Tp*, *Hs*)[](../../../../source-code/PyBM/marine/wave_spectrum/Torsethaugen.py)  
Calculate the double peaked power spectrum of the Torsethaugen paper (simplified) :params freqs: frequencies of the spectral density result :param Tp: peak wave period :param Hs: significant wave height :return: \[H1, Tp1, H2, Tp2, y, winddominated\]

dual_equal_energy_directional_wave_spectrum(*freqs*, *offset=90*, *Ndirs=None*)[](../../../../source-code/PyBM/marine/wave_spectrum/Torsethaugen.py)  
Compute dual peak, combined directional wave spectrum. Uses two JONSWAP spectrums offset by 90 deg or whatever specified.

Parameters:  
- **freqs** – \[Hz\] Vector of frequency points

- **offset** – \[deg\] directionality offset between first peak spectrum and second peak spectrum

- **Ndirs** – \[-\] Number of directions (must be odd)

Returns:  
Directional wave Spectrum

equal_energy_directional_wave_spectrum(*freqs*, *Ndirs=None*)[](../../../../source-code/PyBM/marine/wave_spectrum/Torsethaugen.py)  
Compute directional wave spectrim with spreading using equal energy directions.

Parameters:  
- **freqs** – \[Hz\] Vector of frequency points

- **Ndirs** – \[-\] Number of directions (must be odd)

Returns:  
Directional wave Spectrum

&nbsp;

PyBM.marine.wrap(*angle*)[](../../../../source-code/PyBM/marine/wave_spectrum/WaveSpectrum.py)  

&nbsp;

*class *PyBM.marine.Machine_Linear(*position*, *orientation*)[](../../../../source-code/PyBM/marine/machines/machine_interface.py)  
Bases: `abc.ABC`

Helper class that provides a standard way to create an ABC using inheritance.

pos  

orient  

rotation  

apply_transform(*point: numpy.array*) → numpy.array[](../../../../source-code/PyBM/marine/machines/machine_interface.py)  
Apply rotation then translation to 3D point

Parameters:  
**point** (*np.array*) – 3D vector \[x,y,z\]

Returns:  
Transformed position

Return type:  
np.array

get_rao_at_poi(*rao*) → [PyBM.marine.motion_analysis.MotionRAO.MotionRAO](motion_analysis/MotionRAO/index.md#PyBM.marine.motion_analysis.MotionRAO.MotionRAO "PyBM.marine.motion_analysis.MotionRAO.MotionRAO")[](../../../../source-code/PyBM/marine/machines/machine_interface.py)  
Get the Motion RAOs at the POI

*abstractmethod *get_POI() → dict[](../../../../source-code/PyBM/marine/machines/machine_interface.py)  

apply_machine_dofs(*rao*) → [PyBM.marine.motion_analysis.MotionRAO.MotionRAO](motion_analysis/MotionRAO/index.md#PyBM.marine.motion_analysis.MotionRAO.MotionRAO "PyBM.marine.motion_analysis.MotionRAO.MotionRAO")[](../../../../source-code/PyBM/marine/machines/machine_interface.py)  

get_workability_limit(*motion_at_poi*, *\*\*kwargs*)[](../../../../source-code/PyBM/marine/machines/machine_interface.py)  

\_\_str\_\_() → str[](../../../../source-code/PyBM/marine/machines/machine_interface.py)  

&nbsp;

*class *PyBM.marine.Machine_Nonlinear(*position*, *orientation*)[](../../../../source-code/PyBM/marine/machines/machine_interface.py)  
Bases: `abc.ABC`

Helper class that provides a standard way to create an ABC using inheritance.

pos  

orient  

rotation  

apply_transform(*point: numpy.array*) → numpy.array[](../../../../source-code/PyBM/marine/machines/machine_interface.py)  
Apply rotation then translation to 3D point

Parameters:  
**point** (*np.array*) – 3D vector \[x,y,z\]

Returns:  
Transformed position

Return type:  
np.array

*abstractmethod *get_POI() → dict[](../../../../source-code/PyBM/marine/machines/machine_interface.py)  

&nbsp;

PyBM.marine.cmap[](../../../../source-code/PyBM/marine/workability/workability_limits.py)  

&nbsp;

*class *PyBM.marine.workability_accessor(*obj*)[](../../../../source-code/PyBM/marine/workability/workability_limits.py)  
\_obj  

table(*Hs*, *Hsrange*)[](../../../../source-code/PyBM/marine/workability/workability_limits.py)  

byscatter(*scatter*)[](../../../../source-code/PyBM/marine/workability/workability_limits.py)  

plot_detailed_workability(*max_hs=None*, *fig=None*)[](../../../../source-code/PyBM/marine/workability/workability_limits.py)  
Plot workability for each system limit.

Parameters:  
- **workability_result** (*xr.DataArray*) – \_description\_

- **max_hs** (*\_type\_,* *optional*) – \_description\_, defaults to None

- **fig** (*\_type\_,* *optional*) – \_description\_, defaults to None

plot_combined_workability(*max_hs=None*, *fig=None*)[](../../../../source-code/PyBM/marine/workability/workability_limits.py)  
Plot the result of the workability in polar plots

Parameters:  
- **workability_result** – \[m\] Array of limiting Hs for each wave peak period, direction and machine limit.

- **max_hs** – \[m\] maximum Hs on the polar plot, defaults to None

- **fig** – figure to plot on, defaults to None

&nbsp;

PyBM.marine.directional_workability(*rao: [PyBM.marine.MotionRAO](#PyBM.marine.MotionRAO "PyBM.marine.MotionRAO")*, *wave: [PyBM.marine.WaveSpectrum](#PyBM.marine.WaveSpectrum "PyBM.marine.WaveSpectrum")*, *machine: [PyBM.marine.machines.Machine_Linear](machines/index.md#PyBM.marine.machines.Machine_Linear "PyBM.marine.machines.Machine_Linear")*, *\*\*kwargs*) → xarray.DataArray[](../../../../source-code/PyBM/marine/workability/workability_limits.py)  
Compute the workability of the machine for the given wave directions.

Returns:  
\[m\] Array of limiting Hs for each wave peak period, direction and machine limit.

&nbsp;

PyBM.marine.directional_workability_timetrace(*trace: xarray.DataArray*, *machine: PyBM.marine.machines.MCG30.MCG30_Nonlinear*, *\*\*kwargs*) → xarray.DataArray[](../../../../source-code/PyBM/marine/workability/workability_limits.py)  
Compute the workability of the machine using the time trace supplied (MCG)

Returns:  
\[m\] Array of limiting Hs for each wave peak period, direction and machine limit.

&nbsp;

PyBM.marine.\_polar_plotter(*plot_method*, *workability_result: xarray.DataArray*, *max_hs=None*, *fig: matplotlib.figure.Figure = None*)[](../../../../source-code/PyBM/marine/workability/workability_limits.py)  

&nbsp;

PyBM.marine.multicolored_line(*ax: matplotlib.pyplot.Axes*, *Tp_result*)[](../../../../source-code/PyBM/marine/workability/workability_limits.py)  

&nbsp;

PyBM.marine.multiple_lines(*ax: matplotlib.pyplot.Axes*, *Tp_result*)[](../../../../source-code/PyBM/marine/workability/workability_limits.py)  

&nbsp;

PyBM.marine.set_polar_plot_params(*ax: matplotlib.pyplot.Axes*, *max_y*, *Tp*)[](../../../../source-code/PyBM/marine/workability/workability_limits.py)  

&nbsp;

PyBM.marine.plot_ship(*ax: matplotlib.pyplot.Axes*, *plot_diameter=1.0*)[](../../../../source-code/PyBM/marine/workability/workability_limits.py)  
Plot a ship contour on the given axis.

Parameters:  
- **axs** – Axes to plot on.

- **plot_diameter** – diameter of vessel contour, defaults to 1.0

&nbsp;

PyBM.marine.\_make_legend_proxies(*cmap*, *\*\*kwargs*)[](../../../../source-code/PyBM/marine/workability/workability_limits.py)  
