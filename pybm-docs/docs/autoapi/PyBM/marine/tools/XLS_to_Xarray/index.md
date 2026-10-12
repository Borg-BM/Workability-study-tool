<!-- Source: https://docs.app.barge-master.com/autoapi/PyBM/marine/tools/XLS_to_Xarray/index.html -->

# PyBM.marine.tools.XLS_to_Xarray

convert XLS format to useful xarray

## Attributes

|                                                                                        |     |
|----------------------------------------------------------------------------------------|-----|
| [`DOFS`](#PyBM.marine.tools.XLS_to_Xarray.DOFS "PyBM.marine.tools.XLS_to_Xarray.DOFS") |     |

## Functions

|                                                                                                                                                            |                                         |
|------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------|
| [`decode_RAO_XLS`](#PyBM.marine.tools.XLS_to_Xarray.decode_RAO_XLS "PyBM.marine.tools.XLS_to_Xarray.decode_RAO_XLS")(filename, mirror)                     |                                         |
| [`load_XLS`](#PyBM.marine.tools.XLS_to_Xarray.load_XLS "PyBM.marine.tools.XLS_to_Xarray.load_XLS")(filename, mirror)                                       |                                         |
| [`XLS_to_RAO`](#PyBM.marine.tools.XLS_to_Xarray.XLS_to_RAO "PyBM.marine.tools.XLS_to_Xarray.XLS_to_RAO")(filename, VesselName, Vessel_LC, origin\[, ...\]) | Convert excel file to Xarray RAO object |

## Module Contents

PyBM.marine.tools.XLS_to_Xarray.DOFS* = \['X', 'Y', 'Z', 'Rx', 'Ry', 'Rz'\]*[](../../../../../../source-code/PyBM/marine/tools/XLS_to_Xarray.py)  

&nbsp;

PyBM.marine.tools.XLS_to_Xarray.decode_RAO_XLS(*filename*, *mirror*)[](../../../../../../source-code/PyBM/marine/tools/XLS_to_Xarray.py)  

&nbsp;

PyBM.marine.tools.XLS_to_Xarray.load_XLS(*filename*, *mirror*)[](../../../../../../source-code/PyBM/marine/tools/XLS_to_Xarray.py)  

&nbsp;

PyBM.marine.tools.XLS_to_Xarray.XLS_to_RAO(*filename*, *VesselName*, *Vessel_LC*, *origin*, *mirror=False*)[](../../../../../../source-code/PyBM/marine/tools/XLS_to_Xarray.py)  
Convert excel file to Xarray RAO object

Parameters:  
- **filename** – Excel file with RAO data

- **VesselName** – Name of vessel

- **Vessel_LC** – Loading condition of the vessel

- **origin** – \[m\] \[x, y, z\] origin of the RAOs w.r.t to vessel APP/CL/Keel

Returns:  
MotionRAO object

Return type:  
[MotionRAO](../../index.md#PyBM.marine.MotionRAO "PyBM.marine.MotionRAO")
