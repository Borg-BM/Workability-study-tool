<!-- Source: https://docs.app.barge-master.com/autoapi/PyBM/marine/tools/api/index.html -->

# PyBM.marine.tools.api

## Submodules

- [PyBM.marine.tools.api.api_calls](api_calls/index.md)
- [PyBM.marine.tools.api.oauth_session](oauth_session/index.md)

## Attributes

|                                                                                            |     |
|--------------------------------------------------------------------------------------------|-----|
| [`API_BASE_URL`](#PyBM.marine.tools.api.API_BASE_URL "PyBM.marine.tools.api.API_BASE_URL") |     |

## Classes

|                                                                                            |                                                    |
|--------------------------------------------------------------------------------------------|----------------------------------------------------|
| [`MotionRAO`](#PyBM.marine.tools.api.MotionRAO "PyBM.marine.tools.api.MotionRAO")          | This is the parent class for motion and force RAOs |
| [`SurgeDir`](#PyBM.marine.tools.api.SurgeDir "PyBM.marine.tools.api.SurgeDir")             | Enum for Surge direction                           |
| [`SwayDir`](#PyBM.marine.tools.api.SwayDir "PyBM.marine.tools.api.SwayDir")                | Enum for Sway direction                            |
| [`HeaveDir`](#PyBM.marine.tools.api.HeaveDir "PyBM.marine.tools.api.HeaveDir")             | Enum for Heave direction                           |
| [`RollDir`](#PyBM.marine.tools.api.RollDir "PyBM.marine.tools.api.RollDir")                | Enum for Roll direction                            |
| [`PitchDir`](#PyBM.marine.tools.api.PitchDir "PyBM.marine.tools.api.PitchDir")             | Enum for Pitch direction                           |
| [`YawDir`](#PyBM.marine.tools.api.YawDir "PyBM.marine.tools.api.YawDir")                   | Enum for Yaw direction                             |
| [`WaveOrigin`](#PyBM.marine.tools.api.WaveOrigin "PyBM.marine.tools.api.WaveOrigin")       | Enum for Wave direction                            |
| [`RotationUnit`](#PyBM.marine.tools.api.RotationUnit "PyBM.marine.tools.api.RotationUnit") | Enum for Rotation unit                             |

## Functions

|                                                                                                                                            |                                                                                 |
|--------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------|
| [`get_authenticated_session`](#PyBM.marine.tools.api.get_authenticated_session "PyBM.marine.tools.api.get_authenticated_session")()        | Get authenticated session using OAuth2 (browser-based, tokens cached locally)   |
| [`get_raos`](#PyBM.marine.tools.api.get_raos "PyBM.marine.tools.api.get_raos")(\[session\])                                                | Get RAOs from API (auto-authenticates if needed)                                |
| [`get_rao_loadcases`](#PyBM.marine.tools.api.get_rao_loadcases "PyBM.marine.tools.api.get_rao_loadcases")(VesselName\[, session\])         | Get loadcases for a specific RAO from API (auto-authenticates if needed)        |
| [`get_rao_loadcase`](#PyBM.marine.tools.api.get_rao_loadcase "PyBM.marine.tools.api.get_rao_loadcase")(VesselName, Vessel_LC\[, session\]) | Get specific loadcase details for a RAO from API (auto-authenticates if needed) |

## Package Contents

*class *PyBM.marine.tools.api.MotionRAO(*data_vars: xarray.core.types.DataVars \| None = None*, *coords: collections.abc.Mapping\[Any, Any\] \| None = None*, *attrs: collections.abc.Mapping\[Any, Any\] \| None = None*)[](../../../../../../source-code/PyBM/marine/motion_analysis/MotionRAO.py)  
Bases: [`PyBM.marine.motion_analysis.RAO.RAO`](../../motion_analysis/RAO/index.md#PyBM.marine.motion_analysis.RAO.RAO "PyBM.marine.motion_analysis.RAO.RAO")

This is the parent class for motion and force RAOs

\_\_slots\_\_* = ()*  

translate_rao(*offset*)[](../../../../../../source-code/PyBM/marine/motion_analysis/MotionRAO.py)  
Translates the RAO to a point of interest. Ref\[1\] eq (4.27)

Parameters:  
**offset** – \[m\] (x,y,z) offset of the point of interest

Returns:  
Full vessel motion RAOs around POI

&nbsp;

*class *PyBM.marine.tools.api.SurgeDir(*\*args*, *\*\*kwds*)[](../../../../../../source-code/PyBM/marine/motion_analysis/RAO.py)  
Bases: `enum.Enum`

Enum for Surge direction

FWD* = 1*  

AFT* = -1*  

&nbsp;

*class *PyBM.marine.tools.api.SwayDir(*\*args*, *\*\*kwds*)[](../../../../../../source-code/PyBM/marine/motion_analysis/RAO.py)  
Bases: `enum.Enum`

Enum for Sway direction

PORT* = 1*  

STARBOARD* = -1*  

&nbsp;

*class *PyBM.marine.tools.api.HeaveDir(*\*args*, *\*\*kwds*)[](../../../../../../source-code/PyBM/marine/motion_analysis/RAO.py)  
Bases: `enum.Enum`

Enum for Heave direction

UP* = 1*  

DOWN* = -1*  

&nbsp;

*class *PyBM.marine.tools.api.RollDir(*\*args*, *\*\*kwds*)[](../../../../../../source-code/PyBM/marine/motion_analysis/RAO.py)  
Bases: `enum.Enum`

Enum for Roll direction

PORT_UP* = 1*  

PORT_DOWN* = -1*  

&nbsp;

*class *PyBM.marine.tools.api.PitchDir(*\*args*, *\*\*kwds*)[](../../../../../../source-code/PyBM/marine/motion_analysis/RAO.py)  
Bases: `enum.Enum`

Enum for Pitch direction

BOW_DOWN* = 1*  

BOW_UP* = -1*  

&nbsp;

*class *PyBM.marine.tools.api.YawDir(*\*args*, *\*\*kwds*)[](../../../../../../source-code/PyBM/marine/motion_analysis/RAO.py)  
Bases: `enum.Enum`

Enum for Yaw direction

BOW_PORT* = 1*  

BOW_STARBOARD* = -1*  

&nbsp;

*class *PyBM.marine.tools.api.WaveOrigin(*\*args*, *\*\*kwds*)[](../../../../../../source-code/PyBM/marine/motion_analysis/RAO.py)  
Bases: `enum.Enum`

Enum for Wave direction

STERN* = 0*  

STARBOARD* = 90*  

BOW* = 180*  

PORT* = 270*  

&nbsp;

*class *PyBM.marine.tools.api.RotationUnit(*\*args*, *\*\*kwds*)[](../../../../../../source-code/PyBM/marine/motion_analysis/RAO.py)  
Bases: `enum.Enum`

Enum for Rotation unit

DEG_PER_M* = 1*  

RAD_PER_M  

DEG_PER_FT* = 3.28084*  

DEG_PER_DEG* = 0*  

RAD_PER_RAD  

&nbsp;

PyBM.marine.tools.api.get_authenticated_session()[](../../../../../../source-code/PyBM/marine/tools/api/oauth_session.py)  
Get authenticated session using OAuth2 (browser-based, tokens cached locally)

&nbsp;

PyBM.marine.tools.api.API_BASE_URL* = 'https://api.app.barge-master.com'*[](../../../../../../source-code/PyBM/marine/tools/api/oauth_session.py)  

&nbsp;

PyBM.marine.tools.api.get_raos(*session=None*)[](../../../../../../source-code/PyBM/marine/tools/api/api_calls.py)  
Get RAOs from API (auto-authenticates if needed)

&nbsp;

PyBM.marine.tools.api.get_rao_loadcases(*VesselName: str*, *session=None*)[](../../../../../../source-code/PyBM/marine/tools/api/api_calls.py)  
Get loadcases for a specific RAO from API (auto-authenticates if needed)

&nbsp;

PyBM.marine.tools.api.get_rao_loadcase(*VesselName: str*, *Vessel_LC: str*, *session=None*)[](../../../../../../source-code/PyBM/marine/tools/api/api_calls.py)  
Get specific loadcase details for a RAO from API (auto-authenticates if needed)
