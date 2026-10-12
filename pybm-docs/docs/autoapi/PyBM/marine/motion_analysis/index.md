<!-- Source: https://docs.app.barge-master.com/autoapi/PyBM/marine/motion_analysis/index.html -->

# PyBM.marine.motion_analysis

## Submodules

- [PyBM.marine.motion_analysis.ForceRAO](ForceRAO/index.md)
- [PyBM.marine.motion_analysis.MotionRAO](MotionRAO/index.md)
- [PyBM.marine.motion_analysis.RAO](RAO/index.md)
- [PyBM.marine.motion_analysis.Response](Response/index.md)
- [PyBM.marine.motion_analysis.SpectrumAccessor](SpectrumAccessor/index.md)
- [PyBM.marine.motion_analysis.TimeDomain](TimeDomain/index.md)

## Attributes

|                                                                       |     |
|-----------------------------------------------------------------------|-----|
| [`g`](#PyBM.marine.motion_analysis.g "PyBM.marine.motion_analysis.g") |     |

## Exceptions

|                                                                                                                    |                                                |
|--------------------------------------------------------------------------------------------------------------------|------------------------------------------------|
| [`OutofBoundsError`](#PyBM.marine.motion_analysis.OutofBoundsError "PyBM.marine.motion_analysis.OutofBoundsError") | Common base class for all non-exit exceptions. |

## Classes

|                                                                                                                             |                                                                  |
|-----------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------|
| [`RAO`](#id0 "PyBM.marine.motion_analysis.RAO")                                                                             | This is the parent class for motion and force RAOs               |
| [`MotionRAO`](#id12 "PyBM.marine.motion_analysis.MotionRAO")                                                                | This is the parent class for motion and force RAOs               |
| [`SurgeDir`](#PyBM.marine.motion_analysis.SurgeDir "PyBM.marine.motion_analysis.SurgeDir")                                  | Enum for Surge direction                                         |
| [`SwayDir`](#PyBM.marine.motion_analysis.SwayDir "PyBM.marine.motion_analysis.SwayDir")                                     | Enum for Sway direction                                          |
| [`HeaveDir`](#PyBM.marine.motion_analysis.HeaveDir "PyBM.marine.motion_analysis.HeaveDir")                                  | Enum for Heave direction                                         |
| [`RollDir`](#PyBM.marine.motion_analysis.RollDir "PyBM.marine.motion_analysis.RollDir")                                     | Enum for Roll direction                                          |
| [`PitchDir`](#PyBM.marine.motion_analysis.PitchDir "PyBM.marine.motion_analysis.PitchDir")                                  | Enum for Pitch direction                                         |
| [`YawDir`](#PyBM.marine.motion_analysis.YawDir "PyBM.marine.motion_analysis.YawDir")                                        | Enum for Yaw direction                                           |
| [`WaveOrigin`](#PyBM.marine.motion_analysis.WaveOrigin "PyBM.marine.motion_analysis.WaveOrigin")                            | Enum for Wave direction                                          |
| [`RotationUnit`](#PyBM.marine.motion_analysis.RotationUnit "PyBM.marine.motion_analysis.RotationUnit")                      | Enum for Rotation unit                                           |
| [`RAO`](#id0 "PyBM.marine.motion_analysis.RAO")                                                                             | This is the parent class for motion and force RAOs               |
| [`SpectralTools`](#PyBM.marine.motion_analysis.SpectralTools "PyBM.marine.motion_analysis.SpectralTools")                   | Tools to analyse spectra.                                        |
| [`EqualEnergySpectrum`](#PyBM.marine.motion_analysis.EqualEnergySpectrum "PyBM.marine.motion_analysis.EqualEnergySpectrum") | Tools to analyse spectra optimized for equal energy frequencies. |
| [`MotionRAO`](#id12 "PyBM.marine.motion_analysis.MotionRAO")                                                                | This is the parent class for motion and force RAOs               |
| [`TimeDomainTools`](#PyBM.marine.motion_analysis.TimeDomainTools "PyBM.marine.motion_analysis.TimeDomainTools")             | Tools for time domain traces in xarray.DataArray type            |
| [`TimeDomain`](#PyBM.marine.motion_analysis.TimeDomain "PyBM.marine.motion_analysis.TimeDomain")                            |                                                                  |

## Functions

|                                                                                                                                                                       |                                                                                                                                                              |
|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [`_recursive_group_names`](#PyBM.marine.motion_analysis._recursive_group_names "PyBM.marine.motion_analysis._recursive_group_names")(groups\[, parent\])              | Recursively get the group names from a dictionary of groups                                                                                                  |
| [`compute_response`](#PyBM.marine.motion_analysis.compute_response "PyBM.marine.motion_analysis.compute_response")(wave, rao\[, poi, Nfreqs, f_bounds\])              | Compute the vessel response based on the given wave spectrum and RAO.                                                                                        |
| [`compute_mpe`](#PyBM.marine.motion_analysis.compute_mpe "PyBM.marine.motion_analysis.compute_mpe")(wave, rao\[, poi, storm_duration, ...\])                          | Calculate MPE of the given parameter for all points of interest (POI).                                                                                       |
| [`equal_energy_freqs_rao`](#PyBM.marine.motion_analysis.equal_energy_freqs_rao "PyBM.marine.motion_analysis.equal_energy_freqs_rao")(wave, rao, Nfreqs\[, f_bounds\]) |                                                                                                                                                              |
| [`apply_directional_spreading`](#PyBM.marine.motion_analysis.apply_directional_spreading "PyBM.marine.motion_analysis.apply_directional_spreading")(wave, rao)        |                                                                                                                                                              |
| [`isFileLocked`](#PyBM.marine.motion_analysis.isFileLocked "PyBM.marine.motion_analysis.isFileLocked")(filePath)                                                      | Source: [https://stackoverflow.com/questions/13371444/python-check-file-is-locked](https://stackoverflow.com/questions/13371444/python-check-file-is-locked) |

## Package Contents

*class *PyBM.marine.motion_analysis.RAO(*data_vars: xarray.core.types.DataVars \| None = None*, *coords: collections.abc.Mapping\[Any, Any\] \| None = None*, *attrs: collections.abc.Mapping\[Any, Any\] \| None = None*)[](../../../../../source-code/PyBM/marine/motion_analysis/RAO.py)  
Bases: `xarray.Dataset`, `abc.ABC`

This is the parent class for motion and force RAOs

\_\_slots\_\_* = ()*  

*abstractmethod *translate_rao(*offset*)[](../../../../../source-code/PyBM/marine/motion_analysis/RAO.py)  

*static *default_rao_path(*VesselName*, *revision=0*)[](../../../../../source-code/PyBM/marine/motion_analysis/RAO.py)  

*static *group_name(*Vessel_LC*)[](../../../../../source-code/PyBM/marine/motion_analysis/RAO.py)  
Return the group name for the RAOs in the database

Parameters:  
**Vessel_LC** – Load Case

*property *group  

modify_conventions(*surge: [SurgeDir](RAO/index.md#PyBM.marine.motion_analysis.RAO.SurgeDir "PyBM.marine.motion_analysis.RAO.SurgeDir") = SurgeDir.FWD*, *sway: [SwayDir](RAO/index.md#PyBM.marine.motion_analysis.RAO.SwayDir "PyBM.marine.motion_analysis.RAO.SwayDir") = SwayDir.PORT*, *heave: [HeaveDir](RAO/index.md#PyBM.marine.motion_analysis.RAO.HeaveDir "PyBM.marine.motion_analysis.RAO.HeaveDir") = HeaveDir.UP*, *roll: [RollDir](RAO/index.md#PyBM.marine.motion_analysis.RAO.RollDir "PyBM.marine.motion_analysis.RAO.RollDir") = RollDir.PORT_UP*, *pitch: [PitchDir](RAO/index.md#PyBM.marine.motion_analysis.RAO.PitchDir "PyBM.marine.motion_analysis.RAO.PitchDir") = PitchDir.BOW_DOWN*, *yaw: [YawDir](RAO/index.md#PyBM.marine.motion_analysis.RAO.YawDir "PyBM.marine.motion_analysis.RAO.YawDir") = YawDir.BOW_PORT*, *wave_origin: [WaveOrigin](RAO/index.md#PyBM.marine.motion_analysis.RAO.WaveOrigin "PyBM.marine.motion_analysis.RAO.WaveOrigin") = WaveOrigin.STERN*, *rot_unit: [RotationUnit](RAO/index.md#PyBM.marine.motion_analysis.RAO.RotationUnit "PyBM.marine.motion_analysis.RAO.RotationUnit") = RotationUnit.DEG_PER_M*)[](../../../../../source-code/PyBM/marine/motion_analysis/RAO.py)  
Modify the RAO conventions to match the PyBM default. The inputs are the conventions of the data BEFORE modification.

Parameters:  
- **surge** ([*SurgeDir*](RAO/index.md#PyBM.marine.motion_analysis.RAO.SurgeDir "PyBM.marine.motion_analysis.RAO.SurgeDir")*,* *optional*) – Surge direction convention BEFORE modification (default: SurgeDir.FWD)

- **sway** ([*SwayDir*](RAO/index.md#PyBM.marine.motion_analysis.RAO.SwayDir "PyBM.marine.motion_analysis.RAO.SwayDir")*,* *optional*) – Sway direction convention BEFORE modification (default: SwayDir.PORT)

- **heave** ([*HeaveDir*](RAO/index.md#PyBM.marine.motion_analysis.RAO.HeaveDir "PyBM.marine.motion_analysis.RAO.HeaveDir")*,* *optional*) – Heave direction convention BEFORE modification (default: HeaveDir.UP)

- **roll** ([*RollDir*](RAO/index.md#PyBM.marine.motion_analysis.RAO.RollDir "PyBM.marine.motion_analysis.RAO.RollDir")*,* *optional*) – Roll direction convention BEFORE modification (default: RollDir.PORT_UP)

- **pitch** ([*PitchDir*](RAO/index.md#PyBM.marine.motion_analysis.RAO.PitchDir "PyBM.marine.motion_analysis.RAO.PitchDir")*,* *optional*) – Pitch direction convention BEFORE modification (default: PitchDir.BOW_DOWN)

- **yaw** ([*YawDir*](RAO/index.md#PyBM.marine.motion_analysis.RAO.YawDir "PyBM.marine.motion_analysis.RAO.YawDir")*,* *optional*) – Yaw direction convention BEFORE modification (default: YawDir.BOW_PORT)

- **wave_origin** ([*WaveOrigin*](RAO/index.md#PyBM.marine.motion_analysis.RAO.WaveOrigin "PyBM.marine.motion_analysis.RAO.WaveOrigin")*,* *optional*) – Wave direction convention BEFORE modification (default: WaveOrigin.STERN)

- **rot_unit** ([*RotationUnit*](RAO/index.md#PyBM.marine.motion_analysis.RAO.RotationUnit "PyBM.marine.motion_analysis.RAO.RotationUnit")*,* *optional*) – Rotation unit convention BEFORE modification (default: RotationUnit.DEG_PER_M)

*classmethod *load_rao(*filename*, *Vessel_LC*)[](../../../../../source-code/PyBM/marine/motion_analysis/RAO.py)  
Load RAO from database.

*classmethod *from_api(*VesselName*, *Vessel_LC*)[](../../../../../source-code/PyBM/marine/motion_analysis/RAO.py)  
Load RAO from API.

Parameters:  
- **VesselName** – Name of the vessel

- **Vessel_LC** – Name of the load case

Returns:  
RAO object

Raises:  
**ValueError** – If RAO or load case not found (with available options listed)

save_rao(*filename=None*, *revision=None*, *replace=False*)[](../../../../../source-code/PyBM/marine/motion_analysis/RAO.py)  
Save RAO to NetCDF file

Parameters:  
- **filename** – filepath to save the rao

- **replace** – Replace the file if it exists, otherwise append to the data

get_roll_period()[](../../../../../source-code/PyBM/marine/motion_analysis/RAO.py)  
Get the roll period from the RAOs

plot(*directions=None*, *amplitude=True*, *keys=None*)[](../../../../../source-code/PyBM/marine/motion_analysis/RAO.py)  
Plot the RAO for selected directions.

Parameters:  
- **directions** – Vector of directions. Default: All directions are used

- **amplitude** – Plot RAO amplitudes if True. Plot phases if False.

&nbsp;

*class *PyBM.marine.motion_analysis.MotionRAO(*data_vars: xarray.core.types.DataVars \| None = None*, *coords: collections.abc.Mapping\[Any, Any\] \| None = None*, *attrs: collections.abc.Mapping\[Any, Any\] \| None = None*)[](../../../../../source-code/PyBM/marine/motion_analysis/MotionRAO.py)  
Bases: [`PyBM.marine.motion_analysis.RAO.RAO`](RAO/index.md#PyBM.marine.motion_analysis.RAO.RAO "PyBM.marine.motion_analysis.RAO.RAO")

This is the parent class for motion and force RAOs

\_\_slots\_\_* = ()*  

translate_rao(*offset*)[](../../../../../source-code/PyBM/marine/motion_analysis/MotionRAO.py)  
Translates the RAO to a point of interest. Ref\[1\] eq (4.27)

Parameters:  
**offset** – \[m\] (x,y,z) offset of the point of interest

Returns:  
Full vessel motion RAOs around POI

&nbsp;

PyBM.marine.motion_analysis.g* = 9.81*[](../../../../../source-code/PyBM/constants.py)  

&nbsp;

*class *PyBM.marine.motion_analysis.SurgeDir(*\*args*, *\*\*kwds*)[](../../../../../source-code/PyBM/marine/motion_analysis/RAO.py)  
Bases: `enum.Enum`

Enum for Surge direction

FWD* = 1*  

AFT* = -1*  

&nbsp;

*class *PyBM.marine.motion_analysis.SwayDir(*\*args*, *\*\*kwds*)[](../../../../../source-code/PyBM/marine/motion_analysis/RAO.py)  
Bases: `enum.Enum`

Enum for Sway direction

PORT* = 1*  

STARBOARD* = -1*  

&nbsp;

*class *PyBM.marine.motion_analysis.HeaveDir(*\*args*, *\*\*kwds*)[](../../../../../source-code/PyBM/marine/motion_analysis/RAO.py)  
Bases: `enum.Enum`

Enum for Heave direction

UP* = 1*  

DOWN* = -1*  

&nbsp;

*class *PyBM.marine.motion_analysis.RollDir(*\*args*, *\*\*kwds*)[](../../../../../source-code/PyBM/marine/motion_analysis/RAO.py)  
Bases: `enum.Enum`

Enum for Roll direction

PORT_UP* = 1*  

PORT_DOWN* = -1*  

&nbsp;

*class *PyBM.marine.motion_analysis.PitchDir(*\*args*, *\*\*kwds*)[](../../../../../source-code/PyBM/marine/motion_analysis/RAO.py)  
Bases: `enum.Enum`

Enum for Pitch direction

BOW_DOWN* = 1*  

BOW_UP* = -1*  

&nbsp;

*class *PyBM.marine.motion_analysis.YawDir(*\*args*, *\*\*kwds*)[](../../../../../source-code/PyBM/marine/motion_analysis/RAO.py)  
Bases: `enum.Enum`

Enum for Yaw direction

BOW_PORT* = 1*  

BOW_STARBOARD* = -1*  

&nbsp;

*class *PyBM.marine.motion_analysis.WaveOrigin(*\*args*, *\*\*kwds*)[](../../../../../source-code/PyBM/marine/motion_analysis/RAO.py)  
Bases: `enum.Enum`

Enum for Wave direction

STERN* = 0*  

STARBOARD* = 90*  

BOW* = 180*  

PORT* = 270*  

&nbsp;

*class *PyBM.marine.motion_analysis.RotationUnit(*\*args*, *\*\*kwds*)[](../../../../../source-code/PyBM/marine/motion_analysis/RAO.py)  
Bases: `enum.Enum`

Enum for Rotation unit

DEG_PER_M* = 1*  

RAD_PER_M  

DEG_PER_FT* = 3.28084*  

DEG_PER_DEG* = 0*  

RAD_PER_RAD  

&nbsp;

PyBM.marine.motion_analysis.\_recursive_group_names(*groups: dict*, *parent=None*)[](../../../../../source-code/PyBM/marine/motion_analysis/RAO.py)  
Recursively get the group names from a dictionary of groups

&nbsp;

*class *PyBM.marine.motion_analysis.RAO(*data_vars: xarray.core.types.DataVars \| None = None*, *coords: collections.abc.Mapping\[Any, Any\] \| None = None*, *attrs: collections.abc.Mapping\[Any, Any\] \| None = None*)[](../../../../../source-code/PyBM/marine/motion_analysis/RAO.py)  
Bases: `xarray.Dataset`, `abc.ABC`

This is the parent class for motion and force RAOs

\_\_slots\_\_* = ()*  

*abstractmethod *translate_rao(*offset*)[](../../../../../source-code/PyBM/marine/motion_analysis/RAO.py)  

*static *default_rao_path(*VesselName*, *revision=0*)[](../../../../../source-code/PyBM/marine/motion_analysis/RAO.py)  

*static *group_name(*Vessel_LC*)[](../../../../../source-code/PyBM/marine/motion_analysis/RAO.py)  
Return the group name for the RAOs in the database

Parameters:  
**Vessel_LC** – Load Case

*property *group  

modify_conventions(*surge: [SurgeDir](RAO/index.md#PyBM.marine.motion_analysis.RAO.SurgeDir "PyBM.marine.motion_analysis.RAO.SurgeDir") = SurgeDir.FWD*, *sway: [SwayDir](RAO/index.md#PyBM.marine.motion_analysis.RAO.SwayDir "PyBM.marine.motion_analysis.RAO.SwayDir") = SwayDir.PORT*, *heave: [HeaveDir](RAO/index.md#PyBM.marine.motion_analysis.RAO.HeaveDir "PyBM.marine.motion_analysis.RAO.HeaveDir") = HeaveDir.UP*, *roll: [RollDir](RAO/index.md#PyBM.marine.motion_analysis.RAO.RollDir "PyBM.marine.motion_analysis.RAO.RollDir") = RollDir.PORT_UP*, *pitch: [PitchDir](RAO/index.md#PyBM.marine.motion_analysis.RAO.PitchDir "PyBM.marine.motion_analysis.RAO.PitchDir") = PitchDir.BOW_DOWN*, *yaw: [YawDir](RAO/index.md#PyBM.marine.motion_analysis.RAO.YawDir "PyBM.marine.motion_analysis.RAO.YawDir") = YawDir.BOW_PORT*, *wave_origin: [WaveOrigin](RAO/index.md#PyBM.marine.motion_analysis.RAO.WaveOrigin "PyBM.marine.motion_analysis.RAO.WaveOrigin") = WaveOrigin.STERN*, *rot_unit: [RotationUnit](RAO/index.md#PyBM.marine.motion_analysis.RAO.RotationUnit "PyBM.marine.motion_analysis.RAO.RotationUnit") = RotationUnit.DEG_PER_M*)[](../../../../../source-code/PyBM/marine/motion_analysis/RAO.py)  
Modify the RAO conventions to match the PyBM default. The inputs are the conventions of the data BEFORE modification.

Parameters:  
- **surge** ([*SurgeDir*](RAO/index.md#PyBM.marine.motion_analysis.RAO.SurgeDir "PyBM.marine.motion_analysis.RAO.SurgeDir")*,* *optional*) – Surge direction convention BEFORE modification (default: SurgeDir.FWD)

- **sway** ([*SwayDir*](RAO/index.md#PyBM.marine.motion_analysis.RAO.SwayDir "PyBM.marine.motion_analysis.RAO.SwayDir")*,* *optional*) – Sway direction convention BEFORE modification (default: SwayDir.PORT)

- **heave** ([*HeaveDir*](RAO/index.md#PyBM.marine.motion_analysis.RAO.HeaveDir "PyBM.marine.motion_analysis.RAO.HeaveDir")*,* *optional*) – Heave direction convention BEFORE modification (default: HeaveDir.UP)

- **roll** ([*RollDir*](RAO/index.md#PyBM.marine.motion_analysis.RAO.RollDir "PyBM.marine.motion_analysis.RAO.RollDir")*,* *optional*) – Roll direction convention BEFORE modification (default: RollDir.PORT_UP)

- **pitch** ([*PitchDir*](RAO/index.md#PyBM.marine.motion_analysis.RAO.PitchDir "PyBM.marine.motion_analysis.RAO.PitchDir")*,* *optional*) – Pitch direction convention BEFORE modification (default: PitchDir.BOW_DOWN)

- **yaw** ([*YawDir*](RAO/index.md#PyBM.marine.motion_analysis.RAO.YawDir "PyBM.marine.motion_analysis.RAO.YawDir")*,* *optional*) – Yaw direction convention BEFORE modification (default: YawDir.BOW_PORT)

- **wave_origin** ([*WaveOrigin*](RAO/index.md#PyBM.marine.motion_analysis.RAO.WaveOrigin "PyBM.marine.motion_analysis.RAO.WaveOrigin")*,* *optional*) – Wave direction convention BEFORE modification (default: WaveOrigin.STERN)

- **rot_unit** ([*RotationUnit*](RAO/index.md#PyBM.marine.motion_analysis.RAO.RotationUnit "PyBM.marine.motion_analysis.RAO.RotationUnit")*,* *optional*) – Rotation unit convention BEFORE modification (default: RotationUnit.DEG_PER_M)

*classmethod *load_rao(*filename*, *Vessel_LC*)[](../../../../../source-code/PyBM/marine/motion_analysis/RAO.py)  
Load RAO from database.

*classmethod *from_api(*VesselName*, *Vessel_LC*)[](../../../../../source-code/PyBM/marine/motion_analysis/RAO.py)  
Load RAO from API.

Parameters:  
- **VesselName** – Name of the vessel

- **Vessel_LC** – Name of the load case

Returns:  
RAO object

Raises:  
**ValueError** – If RAO or load case not found (with available options listed)

save_rao(*filename=None*, *revision=None*, *replace=False*)[](../../../../../source-code/PyBM/marine/motion_analysis/RAO.py)  
Save RAO to NetCDF file

Parameters:  
- **filename** – filepath to save the rao

- **replace** – Replace the file if it exists, otherwise append to the data

get_roll_period()[](../../../../../source-code/PyBM/marine/motion_analysis/RAO.py)  
Get the roll period from the RAOs

plot(*directions=None*, *amplitude=True*, *keys=None*)[](../../../../../source-code/PyBM/marine/motion_analysis/RAO.py)  
Plot the RAO for selected directions.

Parameters:  
- **directions** – Vector of directions. Default: All directions are used

- **amplitude** – Plot RAO amplitudes if True. Plot phases if False.

&nbsp;

*exception *PyBM.marine.motion_analysis.OutofBoundsError[](../../../../../source-code/PyBM/exceptions.py)  
Bases: `Exception`

Common base class for all non-exit exceptions.

&nbsp;

PyBM.marine.motion_analysis.compute_response(*wave: [PyBM.marine.wave_spectrum.WaveSpectrum](../wave_spectrum/index.md#id42 "PyBM.marine.wave_spectrum.WaveSpectrum")*, *rao: [PyBM.marine.motion_analysis.RAO](#id0 "PyBM.marine.motion_analysis.RAO")*, *poi=None*, *Nfreqs=200*, *f_bounds=None*)[](../../../../../source-code/PyBM/marine/motion_analysis/Response.py)  
Compute the vessel response based on the given wave spectrum and RAO.

Parameters:  
- **wave** ([*WaveSpectrum*](../index.md#PyBM.marine.WaveSpectrum "PyBM.marine.WaveSpectrum")) – The wave spectrum.

- **rao** ([*RAO*](#id0 "PyBM.marine.motion_analysis.RAO")) – The response amplitude operator.

- **poi** (*list,* *optional*) – The point of interest \[x,y,z\] in meters, defaults to None.

- **Nfreqs** (*int,* *optional*) – The number of frequencies to consider, defaults to 200.

- **f_bounds** (*tuple,* *optional*) – The frequency bounds, defaults to None.

Returns:  
The computed vessel response.

Return type:  
Response

&nbsp;

PyBM.marine.motion_analysis.compute_mpe(*wave: [PyBM.marine.wave_spectrum.WaveSpectrum](../wave_spectrum/index.md#id42 "PyBM.marine.wave_spectrum.WaveSpectrum")*, *rao: [PyBM.marine.motion_analysis.RAO](#id0 "PyBM.marine.motion_analysis.RAO")*, *poi=None*, *storm_duration=10800*, *transfer_function=None*)[](../../../../../source-code/PyBM/marine/motion_analysis/Response.py)  
Calculate MPE of the given parameter for all points of interest (POI).

Parameters:  
- **poi** – \[m\] (x,y,z) offset of point of interest

- **storm_duration** – \[s\] duration of the period of interest (usually 3 hours)

- **transfer_function** – (\[\[a\], \[b\]\]) Numerator and Denumerator of continuous transfer function to be applied.

Returns:  
Statistical extreme value

&nbsp;

PyBM.marine.motion_analysis.equal_energy_freqs_rao(*wave: [PyBM.marine.wave_spectrum.WaveSpectrum](../wave_spectrum/index.md#id42 "PyBM.marine.wave_spectrum.WaveSpectrum")*, *rao: [PyBM.marine.motion_analysis.RAO](#id0 "PyBM.marine.motion_analysis.RAO")*, *Nfreqs*, *f_bounds=None*)[](../../../../../source-code/PyBM/marine/motion_analysis/Response.py)  

&nbsp;

PyBM.marine.motion_analysis.apply_directional_spreading(*wave: [PyBM.marine.wave_spectrum.WaveSpectrum](../wave_spectrum/index.md#id42 "PyBM.marine.wave_spectrum.WaveSpectrum")*, *rao: [PyBM.marine.motion_analysis.RAO](#id0 "PyBM.marine.motion_analysis.RAO")*)[](../../../../../source-code/PyBM/marine/motion_analysis/Response.py)  

&nbsp;

*class *PyBM.marine.motion_analysis.SpectralTools(*xarray_obj*)[](../../../../../source-code/PyBM/marine/motion_analysis/SpectrumAccessor.py)  
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

spectral_moment(*order=0*)[](../../../../../source-code/PyBM/marine/motion_analysis/SpectrumAccessor.py)  
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

MPE(*storm_duration=10800*, *standard_deviations=None*)[](../../../../../source-code/PyBM/marine/motion_analysis/SpectrumAccessor.py)  
Compute Most Probable Extreme from Rayleigh Distribution based on storm duration and Zero-crossing period. Ref \[1\], Section 11.1 Eq (11.20)

Parameters:  
**storm_duration** – \[s\] duration of the period of interest (usually 3 hours)

Returns:  
Most probable extreme.

&nbsp;

*class *PyBM.marine.motion_analysis.EqualEnergySpectrum(*xarray_obj*)[](../../../../../source-code/PyBM/marine/motion_analysis/SpectrumAccessor.py)  
Bases: [`SpectralTools`](#PyBM.marine.motion_analysis.SpectralTools "PyBM.marine.motion_analysis.SpectralTools")

Tools to analyse spectra optimized for equal energy frequencies.

spectral_moment(*order=0*)[](../../../../../source-code/PyBM/marine/motion_analysis/SpectrumAccessor.py)  
Compute nth order spectral moment of an equal energy spectrum. Ref \[1\]. Eq (6.81)

Parameters:  
**order** (*int,* *optional*) – Order of the moment, defaults to 0

&nbsp;

*class *PyBM.marine.motion_analysis.MotionRAO(*data_vars: xarray.core.types.DataVars \| None = None*, *coords: collections.abc.Mapping\[Any, Any\] \| None = None*, *attrs: collections.abc.Mapping\[Any, Any\] \| None = None*)[](../../../../../source-code/PyBM/marine/motion_analysis/MotionRAO.py)  
Bases: [`PyBM.marine.motion_analysis.RAO.RAO`](RAO/index.md#PyBM.marine.motion_analysis.RAO.RAO "PyBM.marine.motion_analysis.RAO.RAO")

This is the parent class for motion and force RAOs

\_\_slots\_\_* = ()*  

translate_rao(*offset*)[](../../../../../source-code/PyBM/marine/motion_analysis/MotionRAO.py)  
Translates the RAO to a point of interest. Ref\[1\] eq (4.27)

Parameters:  
**offset** – \[m\] (x,y,z) offset of the point of interest

Returns:  
Full vessel motion RAOs around POI

&nbsp;

PyBM.marine.motion_analysis.isFileLocked(*filePath*)[](../../../../../source-code/PyBM/utils/windows_helpers.py)  
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

*class *PyBM.marine.motion_analysis.TimeDomainTools(*xarray_obj*)[](../../../../../source-code/PyBM/marine/motion_analysis/TimeDomain.py)  
Tools for time domain traces in xarray.DataArray type

\_obj  

translate_trace(*offset: numpy.array*)[](../../../../../source-code/PyBM/marine/motion_analysis/TimeDomain.py)  
Translates the trace in 6 DOF. Does not use small angle approx..

Parameters:  
**offset** (*np.array*) – offset in \[x,y,z\]

translate_trace_smallangle(*offset: numpy.array*)[](../../../../../source-code/PyBM/marine/motion_analysis/TimeDomain.py)  
Translates the trace in 6 DOF. Uses small angle approx

Parameters:  
**offset** (*np.array*) – offset in \[x,y,z\]

&nbsp;

*class *PyBM.marine.motion_analysis.TimeDomain(*wave: [PyBM.marine.wave_spectrum.WaveSpectrum](../wave_spectrum/index.md#id42 "PyBM.marine.wave_spectrum.WaveSpectrum")*, *rao: [PyBM.marine.motion_analysis.MotionRAO.MotionRAO](MotionRAO/index.md#PyBM.marine.motion_analysis.MotionRAO.MotionRAO "PyBM.marine.motion_analysis.MotionRAO.MotionRAO")*, *vesselCoG*)[](../../../../../source-code/PyBM/marine/motion_analysis/TimeDomain.py)  
rao  

vesselCoG  

wave  

*static *time_vector(*dt*, *duration*)[](../../../../../source-code/PyBM/marine/motion_analysis/TimeDomain.py)  
Create labelled time vector

Parameters:  
- **dt** – \[s\] Time step

- **duration** – \[s\] Duration of time trace

generate_mat_time_traces(*folder: str*, *dt*, *duration*, *wave*)[](../../../../../source-code/PyBM/marine/motion_analysis/TimeDomain.py)  
Generate .mat time traces to be used in the matlab workability tools.

Parameters:  
- **folder** – Folder to save the files

- **dt** – \[s\] Time step

- **duration** – \[s\] Duration of time trace

- **wave** – \[s\] Wave to generate time traces for. Parameters may be vectorized.

- **directions** – \[deg\] Wave directions

generate_time_traces(*folder: str*, *dt*, *duration*, *wave*)[](../../../../../source-code/PyBM/marine/motion_analysis/TimeDomain.py)  
Generate .mat time traces to be used in the matlab workability tools.

Parameters:  
- **folder** – Folder to save the files

- **dt** – \[s\] Time step

- **duration** – \[s\] Duration of time trace

- **wave** – \[s\] Wave to generate time traces for. Parameters may be vectorized.

- **directions** – \[deg\] Wave directions

save_mat_file(*folder*, *trace*)[](../../../../../source-code/PyBM/marine/motion_analysis/TimeDomain.py)  
Vectorized saving function

save_nc_file(*folder*, *trace*)[](../../../../../source-code/PyBM/marine/motion_analysis/TimeDomain.py)  

*static *\_save_nc_file(*folder*, *traces: xarray.DataArray*, *VesselName*, *vesselCoG*)[](../../../../../source-code/PyBM/marine/motion_analysis/TimeDomain.py)  
Save traces as a single nc file. will append nc with extra coordinates, if already there. :param folder: folder name :type folder: string :param traces: traces to save. :type traces: xarray.DataArray

*static *default_trace_path(*VesselName*, *revision=0*)[](../../../../../source-code/PyBM/marine/motion_analysis/TimeDomain.py)  

load_time_trace(*folder*)[](../../../../../source-code/PyBM/marine/motion_analysis/TimeDomain.py)  
Loads time traces. Tries to open nc files first, if non existent, opens mat files. :param folder: folder name :type folder: str

*static *load_all_default_time_traces(*VesselName*, *rev=0*)[](../../../../../source-code/PyBM/marine/motion_analysis/TimeDomain.py)  
Load the time traces of the given vessel and revision in the default engineering library folder. :param VesselName: vessel name :type VesselName: str :param rev: revision number :type rev: int

*static *load_all_time_traces(*folder*, *VesselName*)[](../../../../../source-code/PyBM/marine/motion_analysis/TimeDomain.py)  
Static version of load_time_trace. Loads all time traces present in given folder. do not need to supply any sort of dimensioning for Tp, Hs or direction. If using default trace path, you can also use the function TimeDomain.load_default_time_trace(). :param folder: folder to load time traces from. :type folder: str :param VesselName: name of the vessel to be loaded. :type VesselName: str

load_mat_time_trace(*folder*)[](../../../../../source-code/PyBM/marine/motion_analysis/TimeDomain.py)  
Load a MAT time trace(s) as DataArray. Uses objects’ properties for selecting which traces to load.

Parameters:  
**folder** (*str*) – path of folder

*static *\_load_mat_time_trace(*folder*, *VesselName*, *Tp*, *Hs*, *Direction*)[](../../../../../source-code/PyBM/marine/motion_analysis/TimeDomain.py)  
Vectorized static function to load mat time traces according to given parameters.

*static *\_load_single_mat_time_trace(*folder*, *VesselName*, *Tp*, *Hs*, *Direction*)[](../../../../../source-code/PyBM/marine/motion_analysis/TimeDomain.py)  

load_nc_time_trace(*folder*)[](../../../../../source-code/PyBM/marine/motion_analysis/TimeDomain.py)  
Load NC stored time trace(s) as DataArray

Parameters:  
**folder** – path of folder

*static *\_load_nc_time_trace(*folder*, *VesselName*)[](../../../../../source-code/PyBM/marine/motion_analysis/TimeDomain.py)  
Loads nc file with traces.

mat_file_name()[](../../../../../source-code/PyBM/marine/motion_analysis/TimeDomain.py)  

*static *\_mat_file_name(*VesselName*, *Tp*, *Hs*, *Direction*)[](../../../../../source-code/PyBM/marine/motion_analysis/TimeDomain.py)  
Returns mat file names for trace. Broadcasts arrays in case of multiple values for Tp,Hs,main_direction.

nc_file_name()[](../../../../../source-code/PyBM/marine/motion_analysis/TimeDomain.py)  

*static *\_nc_file_name(*VesselName*)[](../../../../../source-code/PyBM/marine/motion_analysis/TimeDomain.py)  
Returns nc file name for trace. Since nc files include all directions it is not a vectorized function

*static *\_file_name(*VesselName*, *Tp*, *Hs*, *Direction*)[](../../../../../source-code/PyBM/marine/motion_analysis/TimeDomain.py)  

*static *time_trace_from_rao_and_wave(*time: xarray.DataArray*, *wave: [PyBM.marine.wave_spectrum.WaveSpectrum](../wave_spectrum/index.md#id42 "PyBM.marine.wave_spectrum.WaveSpectrum")*, *rao: [PyBM.marine.motion_analysis.MotionRAO.MotionRAO](MotionRAO/index.md#PyBM.marine.motion_analysis.MotionRAO.MotionRAO "PyBM.marine.motion_analysis.MotionRAO.MotionRAO")*, *Nfreqs=100*, *bounds=None*)[](../../../../../source-code/PyBM/marine/motion_analysis/TimeDomain.py)  
Generate time trace based on RAO and Wave.

Parameters:  
- **time** (*xr.DataArray*) – \[s\] time vector

- **wave** ([*WaveSpectrum*](../index.md#PyBM.marine.WaveSpectrum "PyBM.marine.WaveSpectrum")) – \[m2/(rad/s)\] WaveSpectrum

- **rao** ([*MotionRAO*](#id12 "PyBM.marine.motion_analysis.MotionRAO")) – \[m/m, deg/m\] 6DOF Motion RAO

multi_directional_time_trace(*wave: [PyBM.marine.wave_spectrum.WaveSpectrum](../wave_spectrum/index.md#id42 "PyBM.marine.wave_spectrum.WaveSpectrum")*, *rao: [PyBM.marine.motion_analysis.MotionRAO.MotionRAO](MotionRAO/index.md#PyBM.marine.motion_analysis.MotionRAO.MotionRAO "PyBM.marine.motion_analysis.MotionRAO.MotionRAO")*, *bounds=None*)[](../../../../../source-code/PyBM/marine/motion_analysis/TimeDomain.py)  
Create time trace including wave spreading.

Parameters:  
- **time** (*xr.DataArray*) – \[s\] time vector

- **rao** ([*MotionRAO*](#id12 "PyBM.marine.motion_analysis.MotionRAO")) – \[m/m, deg/m\] 6DOF Motion RAO

- **wave** ([*WaveSpectrum*](../index.md#PyBM.marine.WaveSpectrum "PyBM.marine.WaveSpectrum")) – \[m2/(rad/s)\] WaveSpectrum

single_direction_time_trace(*wave: [PyBM.marine.wave_spectrum.WaveSpectrum](../wave_spectrum/index.md#id42 "PyBM.marine.wave_spectrum.WaveSpectrum")*, *rao: [PyBM.marine.motion_analysis.MotionRAO.MotionRAO](MotionRAO/index.md#PyBM.marine.motion_analysis.MotionRAO.MotionRAO "PyBM.marine.motion_analysis.MotionRAO.MotionRAO")*)[](../../../../../source-code/PyBM/marine/motion_analysis/TimeDomain.py)  
Create time trace for a single wave direction

Parameters:  
- **time** (*xr.DataArray*) – \[s\] time vector

- **rao** ([*MotionRAO*](#id12 "PyBM.marine.motion_analysis.MotionRAO")) – \[m/m, deg/m\] 6DOF Motion RAO. Must have interpolated frequencies according to equal area method

- **wave** ([*WaveSpectrum*](../index.md#PyBM.marine.WaveSpectrum "PyBM.marine.WaveSpectrum")) – \[m2/(rad/s)\] WaveSpectrum

*static *compute_deltas(*coordinates*, *dim*)[](../../../../../source-code/PyBM/marine/motion_analysis/TimeDomain.py)  
Create bins centered a coordinate points.

Parameters:  
- **coordinates** – Coordinates to create bins around.

- **dim** – Dimension name

*static *zero_crossing_period(*trace*)[](../../../../../source-code/PyBM/marine/motion_analysis/TimeDomain.py)  
Compute average zero-crossing period of a time trace.

return: \[s\] average zero-crossing period.
