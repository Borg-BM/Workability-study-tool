<!-- Source: https://docs.app.barge-master.com/autoapi/PyBM/marine/motion_analysis/RAO/index.html -->

# PyBM.marine.motion_analysis.RAO

Base class for RAOs of Vessels. Inherits xarray.Dataset.

Each dataarray must have coordinates - Frequency \[Hz\] - Direction \[deg\] - Must be from 0 to 360 deg (full circle), including 0 and 360 deg. 0 deg means waves coming from the stern direction, 90 deg starboard, 180 deg bow, 270 deg port - DOF: \[“X”, “Y”, “Z”, “Rx”, “Ry”, “Rz”\] Values of the dataarray are in \[m/m\] or \[deg/m\] (angle)

The following conventions should ALWAYS be used for the RAO:  
- Surge: Forward

- Sway: to Port

- Heave: Up

- Roll: Port up

- Pitch: Bow down

- Yaw: Bow to port

Wave directions:

- 0 deg: Waves coming from the stern

- 90 deg: Waves coming from starboard

CBR 21-06-2023

## Classes

|                                                                                                                |                                                    |
|----------------------------------------------------------------------------------------------------------------|----------------------------------------------------|
| [`SurgeDir`](#PyBM.marine.motion_analysis.RAO.SurgeDir "PyBM.marine.motion_analysis.RAO.SurgeDir")             | Enum for Surge direction                           |
| [`SwayDir`](#PyBM.marine.motion_analysis.RAO.SwayDir "PyBM.marine.motion_analysis.RAO.SwayDir")                | Enum for Sway direction                            |
| [`HeaveDir`](#PyBM.marine.motion_analysis.RAO.HeaveDir "PyBM.marine.motion_analysis.RAO.HeaveDir")             | Enum for Heave direction                           |
| [`RollDir`](#PyBM.marine.motion_analysis.RAO.RollDir "PyBM.marine.motion_analysis.RAO.RollDir")                | Enum for Roll direction                            |
| [`PitchDir`](#PyBM.marine.motion_analysis.RAO.PitchDir "PyBM.marine.motion_analysis.RAO.PitchDir")             | Enum for Pitch direction                           |
| [`YawDir`](#PyBM.marine.motion_analysis.RAO.YawDir "PyBM.marine.motion_analysis.RAO.YawDir")                   | Enum for Yaw direction                             |
| [`WaveOrigin`](#PyBM.marine.motion_analysis.RAO.WaveOrigin "PyBM.marine.motion_analysis.RAO.WaveOrigin")       | Enum for Wave direction                            |
| [`RotationUnit`](#PyBM.marine.motion_analysis.RAO.RotationUnit "PyBM.marine.motion_analysis.RAO.RotationUnit") | Enum for Rotation unit                             |
| [`RAO`](#PyBM.marine.motion_analysis.RAO.RAO "PyBM.marine.motion_analysis.RAO.RAO")                            | This is the parent class for motion and force RAOs |

## Functions

|                                                                                                                                                                  |                                                             |
|------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------|
| [`_recursive_group_names`](#PyBM.marine.motion_analysis.RAO._recursive_group_names "PyBM.marine.motion_analysis.RAO._recursive_group_names")(groups\[, parent\]) | Recursively get the group names from a dictionary of groups |

## Module Contents

*class *PyBM.marine.motion_analysis.RAO.SurgeDir(*\*args*, *\*\*kwds*)[](../../../../../../source-code/PyBM/marine/motion_analysis/RAO.py)  
Bases: `enum.Enum`

Enum for Surge direction

FWD* = 1*[](../../../../../../source-code/PyBM/marine/motion_analysis/RAO.py)  

AFT* = -1*[](../../../../../../source-code/PyBM/marine/motion_analysis/RAO.py)  

&nbsp;

*class *PyBM.marine.motion_analysis.RAO.SwayDir(*\*args*, *\*\*kwds*)[](../../../../../../source-code/PyBM/marine/motion_analysis/RAO.py)  
Bases: `enum.Enum`

Enum for Sway direction

PORT* = 1*[](../../../../../../source-code/PyBM/marine/motion_analysis/RAO.py)  

STARBOARD* = -1*[](../../../../../../source-code/PyBM/marine/motion_analysis/RAO.py)  

&nbsp;

*class *PyBM.marine.motion_analysis.RAO.HeaveDir(*\*args*, *\*\*kwds*)[](../../../../../../source-code/PyBM/marine/motion_analysis/RAO.py)  
Bases: `enum.Enum`

Enum for Heave direction

UP* = 1*[](../../../../../../source-code/PyBM/marine/motion_analysis/RAO.py)  

DOWN* = -1*[](../../../../../../source-code/PyBM/marine/motion_analysis/RAO.py)  

&nbsp;

*class *PyBM.marine.motion_analysis.RAO.RollDir(*\*args*, *\*\*kwds*)[](../../../../../../source-code/PyBM/marine/motion_analysis/RAO.py)  
Bases: `enum.Enum`

Enum for Roll direction

PORT_UP* = 1*[](../../../../../../source-code/PyBM/marine/motion_analysis/RAO.py)  

PORT_DOWN* = -1*[](../../../../../../source-code/PyBM/marine/motion_analysis/RAO.py)  

&nbsp;

*class *PyBM.marine.motion_analysis.RAO.PitchDir(*\*args*, *\*\*kwds*)[](../../../../../../source-code/PyBM/marine/motion_analysis/RAO.py)  
Bases: `enum.Enum`

Enum for Pitch direction

BOW_DOWN* = 1*[](../../../../../../source-code/PyBM/marine/motion_analysis/RAO.py)  

BOW_UP* = -1*[](../../../../../../source-code/PyBM/marine/motion_analysis/RAO.py)  

&nbsp;

*class *PyBM.marine.motion_analysis.RAO.YawDir(*\*args*, *\*\*kwds*)[](../../../../../../source-code/PyBM/marine/motion_analysis/RAO.py)  
Bases: `enum.Enum`

Enum for Yaw direction

BOW_PORT* = 1*[](../../../../../../source-code/PyBM/marine/motion_analysis/RAO.py)  

BOW_STARBOARD* = -1*[](../../../../../../source-code/PyBM/marine/motion_analysis/RAO.py)  

&nbsp;

*class *PyBM.marine.motion_analysis.RAO.WaveOrigin(*\*args*, *\*\*kwds*)[](../../../../../../source-code/PyBM/marine/motion_analysis/RAO.py)  
Bases: `enum.Enum`

Enum for Wave direction

STERN* = 0*[](../../../../../../source-code/PyBM/marine/motion_analysis/RAO.py)  

STARBOARD* = 90*[](../../../../../../source-code/PyBM/marine/motion_analysis/RAO.py)  

BOW* = 180*[](../../../../../../source-code/PyBM/marine/motion_analysis/RAO.py)  

PORT* = 270*[](../../../../../../source-code/PyBM/marine/motion_analysis/RAO.py)  

&nbsp;

*class *PyBM.marine.motion_analysis.RAO.RotationUnit(*\*args*, *\*\*kwds*)[](../../../../../../source-code/PyBM/marine/motion_analysis/RAO.py)  
Bases: `enum.Enum`

Enum for Rotation unit

DEG_PER_M* = 1*[](../../../../../../source-code/PyBM/marine/motion_analysis/RAO.py)  

RAD_PER_M[](../../../../../../source-code/PyBM/marine/motion_analysis/RAO.py)  

DEG_PER_FT* = 3.28084*[](../../../../../../source-code/PyBM/marine/motion_analysis/RAO.py)  

DEG_PER_DEG* = 0*[](../../../../../../source-code/PyBM/marine/motion_analysis/RAO.py)  

RAD_PER_RAD[](../../../../../../source-code/PyBM/marine/motion_analysis/RAO.py)  

&nbsp;

PyBM.marine.motion_analysis.RAO.\_recursive_group_names(*groups: dict*, *parent=None*)[](../../../../../../source-code/PyBM/marine/motion_analysis/RAO.py)  
Recursively get the group names from a dictionary of groups

&nbsp;

*class *PyBM.marine.motion_analysis.RAO.RAO(*data_vars: xarray.core.types.DataVars \| None = None*, *coords: collections.abc.Mapping\[Any, Any\] \| None = None*, *attrs: collections.abc.Mapping\[Any, Any\] \| None = None*)[](../../../../../../source-code/PyBM/marine/motion_analysis/RAO.py)  
Bases: `xarray.Dataset`, `abc.ABC`

This is the parent class for motion and force RAOs

\_\_slots\_\_* = ()*[](../../../../../../source-code/PyBM/marine/motion_analysis/RAO.py)  

*abstractmethod *translate_rao(*offset*)[](../../../../../../source-code/PyBM/marine/motion_analysis/RAO.py)  

*static *default_rao_path(*VesselName*, *revision=0*)[](../../../../../../source-code/PyBM/marine/motion_analysis/RAO.py)  

*static *group_name(*Vessel_LC*)[](../../../../../../source-code/PyBM/marine/motion_analysis/RAO.py)  
Return the group name for the RAOs in the database

Parameters:  
**Vessel_LC** – Load Case

*property *group[](../../../../../../source-code/PyBM/marine/motion_analysis/RAO.py)  

modify_conventions(*surge: [SurgeDir](#PyBM.marine.motion_analysis.RAO.SurgeDir "PyBM.marine.motion_analysis.RAO.SurgeDir") = SurgeDir.FWD*, *sway: [SwayDir](#PyBM.marine.motion_analysis.RAO.SwayDir "PyBM.marine.motion_analysis.RAO.SwayDir") = SwayDir.PORT*, *heave: [HeaveDir](#PyBM.marine.motion_analysis.RAO.HeaveDir "PyBM.marine.motion_analysis.RAO.HeaveDir") = HeaveDir.UP*, *roll: [RollDir](#PyBM.marine.motion_analysis.RAO.RollDir "PyBM.marine.motion_analysis.RAO.RollDir") = RollDir.PORT_UP*, *pitch: [PitchDir](#PyBM.marine.motion_analysis.RAO.PitchDir "PyBM.marine.motion_analysis.RAO.PitchDir") = PitchDir.BOW_DOWN*, *yaw: [YawDir](#PyBM.marine.motion_analysis.RAO.YawDir "PyBM.marine.motion_analysis.RAO.YawDir") = YawDir.BOW_PORT*, *wave_origin: [WaveOrigin](#PyBM.marine.motion_analysis.RAO.WaveOrigin "PyBM.marine.motion_analysis.RAO.WaveOrigin") = WaveOrigin.STERN*, *rot_unit: [RotationUnit](#PyBM.marine.motion_analysis.RAO.RotationUnit "PyBM.marine.motion_analysis.RAO.RotationUnit") = RotationUnit.DEG_PER_M*)[](../../../../../../source-code/PyBM/marine/motion_analysis/RAO.py)  
Modify the RAO conventions to match the PyBM default. The inputs are the conventions of the data BEFORE modification.

Parameters:  
- **surge** ([*SurgeDir*](#PyBM.marine.motion_analysis.RAO.SurgeDir "PyBM.marine.motion_analysis.RAO.SurgeDir")*,* *optional*) – Surge direction convention BEFORE modification (default: SurgeDir.FWD)

- **sway** ([*SwayDir*](#PyBM.marine.motion_analysis.RAO.SwayDir "PyBM.marine.motion_analysis.RAO.SwayDir")*,* *optional*) – Sway direction convention BEFORE modification (default: SwayDir.PORT)

- **heave** ([*HeaveDir*](#PyBM.marine.motion_analysis.RAO.HeaveDir "PyBM.marine.motion_analysis.RAO.HeaveDir")*,* *optional*) – Heave direction convention BEFORE modification (default: HeaveDir.UP)

- **roll** ([*RollDir*](#PyBM.marine.motion_analysis.RAO.RollDir "PyBM.marine.motion_analysis.RAO.RollDir")*,* *optional*) – Roll direction convention BEFORE modification (default: RollDir.PORT_UP)

- **pitch** ([*PitchDir*](#PyBM.marine.motion_analysis.RAO.PitchDir "PyBM.marine.motion_analysis.RAO.PitchDir")*,* *optional*) – Pitch direction convention BEFORE modification (default: PitchDir.BOW_DOWN)

- **yaw** ([*YawDir*](#PyBM.marine.motion_analysis.RAO.YawDir "PyBM.marine.motion_analysis.RAO.YawDir")*,* *optional*) – Yaw direction convention BEFORE modification (default: YawDir.BOW_PORT)

- **wave_origin** ([*WaveOrigin*](#PyBM.marine.motion_analysis.RAO.WaveOrigin "PyBM.marine.motion_analysis.RAO.WaveOrigin")*,* *optional*) – Wave direction convention BEFORE modification (default: WaveOrigin.STERN)

- **rot_unit** ([*RotationUnit*](#PyBM.marine.motion_analysis.RAO.RotationUnit "PyBM.marine.motion_analysis.RAO.RotationUnit")*,* *optional*) – Rotation unit convention BEFORE modification (default: RotationUnit.DEG_PER_M)

*classmethod *load_rao(*filename*, *Vessel_LC*)[](../../../../../../source-code/PyBM/marine/motion_analysis/RAO.py)  
Load RAO from database.

*classmethod *from_api(*VesselName*, *Vessel_LC*)[](../../../../../../source-code/PyBM/marine/motion_analysis/RAO.py)  
Load RAO from API.

Parameters:  
- **VesselName** – Name of the vessel

- **Vessel_LC** – Name of the load case

Returns:  
RAO object

Raises:  
**ValueError** – If RAO or load case not found (with available options listed)

save_rao(*filename=None*, *revision=None*, *replace=False*)[](../../../../../../source-code/PyBM/marine/motion_analysis/RAO.py)  
Save RAO to NetCDF file

Parameters:  
- **filename** – filepath to save the rao

- **replace** – Replace the file if it exists, otherwise append to the data

get_roll_period()[](../../../../../../source-code/PyBM/marine/motion_analysis/RAO.py)  
Get the roll period from the RAOs

plot(*directions=None*, *amplitude=True*, *keys=None*)[](../../../../../../source-code/PyBM/marine/motion_analysis/RAO.py)  
Plot the RAO for selected directions.

Parameters:  
- **directions** – Vector of directions. Default: All directions are used

- **amplitude** – Plot RAO amplitudes if True. Plot phases if False.
