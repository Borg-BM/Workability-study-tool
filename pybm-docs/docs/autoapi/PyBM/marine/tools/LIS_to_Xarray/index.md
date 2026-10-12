<!-- Source: https://docs.app.barge-master.com/autoapi/PyBM/marine/tools/LIS_to_Xarray/index.html -->

# PyBM.marine.tools.LIS_to_Xarray

tools to read AQWA RAO files ([\*](#id1).LIS)

## Attributes

|                                                                                                                |     |
|----------------------------------------------------------------------------------------------------------------|-----|
| [`DOFs`](#PyBM.marine.tools.LIS_to_Xarray.DOFs "PyBM.marine.tools.LIS_to_Xarray.DOFs")                         |     |
| [`RAO_TYPES`](#PyBM.marine.tools.LIS_to_Xarray.RAO_TYPES "PyBM.marine.tools.LIS_to_Xarray.RAO_TYPES")          |     |
| [`COG_TYPE`](#PyBM.marine.tools.LIS_to_Xarray.COG_TYPE "PyBM.marine.tools.LIS_to_Xarray.COG_TYPE")             |     |
| [`N_FREQS_TYPE`](#PyBM.marine.tools.LIS_to_Xarray.N_FREQS_TYPE "PyBM.marine.tools.LIS_to_Xarray.N_FREQS_TYPE") |     |
| [`DRAFT_TYPE`](#PyBM.marine.tools.LIS_to_Xarray.DRAFT_TYPE "PyBM.marine.tools.LIS_to_Xarray.DRAFT_TYPE")       |     |

## Functions

|                                                                                                                                           |                                       |
|-------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------|
| [`get_cog`](#PyBM.marine.tools.LIS_to_Xarray.get_cog "PyBM.marine.tools.LIS_to_Xarray.get_cog")(filename)                                 |                                       |
| [`get_n_freqs`](#PyBM.marine.tools.LIS_to_Xarray.get_n_freqs "PyBM.marine.tools.LIS_to_Xarray.get_n_freqs")(filename)                     |                                       |
| [`get_draft`](#PyBM.marine.tools.LIS_to_Xarray.get_draft "PyBM.marine.tools.LIS_to_Xarray.get_draft")(filename)                           |                                       |
| [`decode_RAO`](#PyBM.marine.tools.LIS_to_Xarray.decode_RAO "PyBM.marine.tools.LIS_to_Xarray.decode_RAO")(filename, rao_type, n_freqs)     |                                       |
| [`load_LIS`](#PyBM.marine.tools.LIS_to_Xarray.load_LIS "PyBM.marine.tools.LIS_to_Xarray.load_LIS")(filename)                              |                                       |
| [`LIS_to_RAO`](#PyBM.marine.tools.LIS_to_Xarray.LIS_to_RAO "PyBM.marine.tools.LIS_to_Xarray.LIS_to_RAO")(filename, VesselName, Vessel_LC) | Convert LIS data to MotionRAO object. |

## Module Contents

PyBM.marine.tools.LIS_to_Xarray.DOFs* = \['X', 'Y', 'Z', 'Rx', 'Ry', 'Rz'\]*[](../../../../../../source-code/PyBM/marine/tools/LIS_to_Xarray.py)  

&nbsp;

PyBM.marine.tools.LIS_to_Xarray.RAO_TYPES[](../../../../../../source-code/PyBM/marine/tools/LIS_to_Xarray.py)  

&nbsp;

PyBM.marine.tools.LIS_to_Xarray.COG_TYPE* = '                          CENTRE OF GRAVITY'*[](../../../../../../source-code/PyBM/marine/tools/LIS_to_Xarray.py)  

&nbsp;

PyBM.marine.tools.LIS_to_Xarray.N_FREQS_TYPE* = '    \* \* \* \* W A V E   F R E Q U E N C I E S / P E R I O D S   A N D   D I R E C T I O N S \* \* \* \*'*[](../../../../../../source-code/PyBM/marine/tools/LIS_to_Xarray.py)  

&nbsp;

PyBM.marine.tools.LIS_to_Xarray.DRAFT_TYPE* = '          DEPTH OF LOWEST POINT ON VESSEL . . . . . . .'*[](../../../../../../source-code/PyBM/marine/tools/LIS_to_Xarray.py)  

&nbsp;

PyBM.marine.tools.LIS_to_Xarray.get_cog(*filename*)[](../../../../../../source-code/PyBM/marine/tools/LIS_to_Xarray.py)  

&nbsp;

PyBM.marine.tools.LIS_to_Xarray.get_n_freqs(*filename*)[](../../../../../../source-code/PyBM/marine/tools/LIS_to_Xarray.py)  

&nbsp;

PyBM.marine.tools.LIS_to_Xarray.get_draft(*filename*)[](../../../../../../source-code/PyBM/marine/tools/LIS_to_Xarray.py)  

&nbsp;

PyBM.marine.tools.LIS_to_Xarray.decode_RAO(*filename*, *rao_type*, *n_freqs*)[](../../../../../../source-code/PyBM/marine/tools/LIS_to_Xarray.py)  

&nbsp;

PyBM.marine.tools.LIS_to_Xarray.load_LIS(*filename*)[](../../../../../../source-code/PyBM/marine/tools/LIS_to_Xarray.py)  

&nbsp;

PyBM.marine.tools.LIS_to_Xarray.LIS_to_RAO(*filename*, *VesselName*, *Vessel_LC*)[](../../../../../../source-code/PyBM/marine/tools/LIS_to_Xarray.py)  
Convert LIS data to MotionRAO object.

Parameters:  
- **filename** – path to LIS file

- **VesselName** – Name of the vessel

- **Vessel_LC** – Vessel Loading condition
