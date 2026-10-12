<!-- Source: https://docs.app.barge-master.com/autoapi/PyBM/marine/tools/TXT_to_Xarray/index.html -->

# PyBM.marine.tools.TXT_to_Xarray

convert TXT Orcaflex formats to useful xarray

See an example of the expected format here: “O:EngineeringDatabaseVessel MotionsVessel RAOs and time tracesEWB400Processed dataRAO Rev0OFMRAO.EWB400.MAXDRAFT.set” More info here: https://www.orcina.com/webhelp/OrcaFlex/Content/html/Importinghydrodynamicdata,Generictextfiles.htm#GenericRAOImport

## Attributes

|                                                                                        |     |
|----------------------------------------------------------------------------------------|-----|
| [`DOFS`](#PyBM.marine.tools.TXT_to_Xarray.DOFS "PyBM.marine.tools.TXT_to_Xarray.DOFS") |     |

## Functions

|                                                                                                                                                            |                                                                |
|------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------|
| [`parse_TXT`](#PyBM.marine.tools.TXT_to_Xarray.parse_TXT "PyBM.marine.tools.TXT_to_Xarray.parse_TXT")(filename)                                            | Parse OrcaFlex .txt file into structured blocks per direction. |
| [`decode_RAO_TXT`](#PyBM.marine.tools.TXT_to_Xarray.decode_RAO_TXT "PyBM.marine.tools.TXT_to_Xarray.decode_RAO_TXT")(filename\[, mirror\])                 | Decode OrcaFlex .txt file to xarray DataArray.                 |
| [`load_TXT`](#PyBM.marine.tools.TXT_to_Xarray.load_TXT "PyBM.marine.tools.TXT_to_Xarray.load_TXT")(filename\[, mirror\])                                   |                                                                |
| [`TXT_to_RAO`](#PyBM.marine.tools.TXT_to_Xarray.TXT_to_RAO "PyBM.marine.tools.TXT_to_Xarray.TXT_to_RAO")(filename, VesselName, Vessel_LC, origin\[, ...\]) | Convert OrcaFlex .txt file to MotionRAO object.                |

## Module Contents

PyBM.marine.tools.TXT_to_Xarray.DOFS* = \['X', 'Y', 'Z', 'Rx', 'Ry', 'Rz'\]*[](../../../../../../source-code/PyBM/marine/tools/TXT_to_Xarray.py)  

&nbsp;

PyBM.marine.tools.TXT_to_Xarray.parse_TXT(*filename*)[](../../../../../../source-code/PyBM/marine/tools/TXT_to_Xarray.py)  
Parse OrcaFlex .txt file into structured blocks per direction.

&nbsp;

PyBM.marine.tools.TXT_to_Xarray.decode_RAO_TXT(*filename*, *mirror=False*)[](../../../../../../source-code/PyBM/marine/tools/TXT_to_Xarray.py)  
Decode OrcaFlex .txt file to xarray DataArray.

&nbsp;

PyBM.marine.tools.TXT_to_Xarray.load_TXT(*filename*, *mirror=False*)[](../../../../../../source-code/PyBM/marine/tools/TXT_to_Xarray.py)  

&nbsp;

PyBM.marine.tools.TXT_to_Xarray.TXT_to_RAO(*filename*, *VesselName*, *Vessel_LC*, *origin*, *mirror=False*)[](../../../../../../source-code/PyBM/marine/tools/TXT_to_Xarray.py)  
Convert OrcaFlex .txt file to MotionRAO object.
