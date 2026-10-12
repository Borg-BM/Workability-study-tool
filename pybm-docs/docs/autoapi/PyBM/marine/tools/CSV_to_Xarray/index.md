<!-- Source: https://docs.app.barge-master.com/autoapi/PyBM/marine/tools/CSV_to_Xarray/index.html -->

# PyBM.marine.tools.CSV_to_Xarray

convert CSV and CSV-like formats to useful xarray

See an example of the expected format here: “O:EngineeringDatabaseVessel MotionsVessel RAOs and time tracesEWB400Processed dataRAO Rev0BasisR.set”

## Attributes

|                                                                                        |     |
|----------------------------------------------------------------------------------------|-----|
| [`DOFS`](#PyBM.marine.tools.CSV_to_Xarray.DOFS "PyBM.marine.tools.CSV_to_Xarray.DOFS") |     |

## Functions

|                                                                                                                                                            |                                                                      |
|------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------|
| [`parse_csv_sections`](#PyBM.marine.tools.CSV_to_Xarray.parse_csv_sections "PyBM.marine.tools.CSV_to_Xarray.parse_csv_sections")(filename)                 | Split the .csv file into sections by '&buildg -csv' / 'END'.         |
| [`parse_section`](#PyBM.marine.tools.CSV_to_Xarray.parse_section "PyBM.marine.tools.CSV_to_Xarray.parse_section")(section_text)                            | Parse a single amplitude or phase section.                           |
| [`extract_dof_name`](#PyBM.marine.tools.CSV_to_Xarray.extract_dof_name "PyBM.marine.tools.CSV_to_Xarray.extract_dof_name")(section_text)                   | Extract DOF name like 'Surge', 'Sway', etc. from the section header. |
| [`decode_RAO_CSV`](#PyBM.marine.tools.CSV_to_Xarray.decode_RAO_CSV "PyBM.marine.tools.CSV_to_Xarray.decode_RAO_CSV")(filename, mirror)                     |                                                                      |
| [`load_CSV`](#PyBM.marine.tools.CSV_to_Xarray.load_CSV "PyBM.marine.tools.CSV_to_Xarray.load_CSV")(filename, mirror)                                       |                                                                      |
| [`CSV_to_RAO`](#PyBM.marine.tools.CSV_to_Xarray.CSV_to_RAO "PyBM.marine.tools.CSV_to_Xarray.CSV_to_RAO")(filename, VesselName, Vessel_LC, origin\[, ...\]) | Convert CSV file to Xarray RAO object                                |

## Module Contents

PyBM.marine.tools.CSV_to_Xarray.DOFS* = \['X', 'Y', 'Z', 'Rx', 'Ry', 'Rz'\]*[](../../../../../../source-code/PyBM/marine/tools/CSV_to_Xarray.py)  

&nbsp;

PyBM.marine.tools.CSV_to_Xarray.parse_csv_sections(*filename*)[](../../../../../../source-code/PyBM/marine/tools/CSV_to_Xarray.py)  
Split the .csv file into sections by ‘&buildg -csv’ / ‘END’.

&nbsp;

PyBM.marine.tools.CSV_to_Xarray.parse_section(*section_text*)[](../../../../../../source-code/PyBM/marine/tools/CSV_to_Xarray.py)  
Parse a single amplitude or phase section.

&nbsp;

PyBM.marine.tools.CSV_to_Xarray.extract_dof_name(*section_text*)[](../../../../../../source-code/PyBM/marine/tools/CSV_to_Xarray.py)  
Extract DOF name like ‘Surge’, ‘Sway’, etc. from the section header.

&nbsp;

PyBM.marine.tools.CSV_to_Xarray.decode_RAO_CSV(*filename*, *mirror*)[](../../../../../../source-code/PyBM/marine/tools/CSV_to_Xarray.py)  

&nbsp;

PyBM.marine.tools.CSV_to_Xarray.load_CSV(*filename*, *mirror*)[](../../../../../../source-code/PyBM/marine/tools/CSV_to_Xarray.py)  

&nbsp;

PyBM.marine.tools.CSV_to_Xarray.CSV_to_RAO(*filename*, *VesselName*, *Vessel_LC*, *origin*, *mirror=False*)[](../../../../../../source-code/PyBM/marine/tools/CSV_to_Xarray.py)  
Convert CSV file to Xarray RAO object

Parameters:  
- **filename** – CSV file with RAO data

- **VesselName** – Name of vessel

- **Vessel_LC** – Loading condition of the vessel

- **origin** – \[m\] \[x, y, z\] origin of the RAOs w.r.t to vessel APP/CL/Keel

Returns:  
MotionRAO object

Return type:  
[MotionRAO](../../index.md#PyBM.marine.MotionRAO "PyBM.marine.MotionRAO")
