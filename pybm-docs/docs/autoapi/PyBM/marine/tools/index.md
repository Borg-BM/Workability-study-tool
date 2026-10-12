<!-- Source: https://docs.app.barge-master.com/autoapi/PyBM/marine/tools/index.html -->

# PyBM.marine.tools

## Submodules

- [PyBM.marine.tools.CSV_to_Xarray](CSV_to_Xarray/index.md)
- [PyBM.marine.tools.LIS_to_Xarray](LIS_to_Xarray/index.md)
- [PyBM.marine.tools.TXT_to_Xarray](TXT_to_Xarray/index.md)
- [PyBM.marine.tools.XLS_to_Xarray](XLS_to_Xarray/index.md)
- [PyBM.marine.tools.api](api/index.md)
- [PyBM.marine.tools.import_octopus_rao](import_octopus_rao/index.md)
- [PyBM.marine.tools.read_res](read_res/index.md)

## Functions

|                                                                                                                                        |                                                 |
|----------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------|
| [`Octopus_to_RAO`](#PyBM.marine.tools.Octopus_to_RAO "PyBM.marine.tools.Octopus_to_RAO")(octopus_file, VesselName, Vessel_LC\[, ...\]) |                                                 |
| [`get_speeds`](#PyBM.marine.tools.get_speeds "PyBM.marine.tools.get_speeds")(file_iterator)                                            |                                                 |
| [`get_wave_directions`](#PyBM.marine.tools.get_wave_directions "PyBM.marine.tools.get_wave_directions")(file_iterator)                 |                                                 |
| [`get_wave_frequencies`](#PyBM.marine.tools.get_wave_frequencies "PyBM.marine.tools.get_wave_frequencies")(file_iterator, speed)       |                                                 |
| [`LIS_to_RAO`](#PyBM.marine.tools.LIS_to_RAO "PyBM.marine.tools.LIS_to_RAO")(filename, VesselName, Vessel_LC)                          | Convert LIS data to MotionRAO object.           |
| [`load_LIS`](#PyBM.marine.tools.load_LIS "PyBM.marine.tools.load_LIS")(filename)                                                       |                                                 |
| [`__file_len`](#PyBM.marine.tools.__file_len "PyBM.marine.tools.__file_len")(fname)                                                    |                                                 |
| [`resample`](#PyBM.marine.tools.resample "PyBM.marine.tools.resample")(data, new_dt, data_dt)                                          |                                                 |
| [`__read_file`](#PyBM.marine.tools.__read_file "PyBM.marine.tools.__read_file")(filename\[, read_invalid\])                            |                                                 |
| [`read_res`](read_res/index.md#module-PyBM.marine.tools.read_res "PyBM.marine.tools.read_res")(filename\[, dt, read_invalid\])         | Read a text .res file with time traces.         |
| [`write_pickle`](#PyBM.marine.tools.write_pickle "PyBM.marine.tools.write_pickle")(filename, data_dict)                                |                                                 |
| [`write_res`](#PyBM.marine.tools.write_res "PyBM.marine.tools.write_res")(filename, data_dict)                                         | Write a data dictionary to a .res text file.    |
| [`XLS_to_RAO`](#PyBM.marine.tools.XLS_to_RAO "PyBM.marine.tools.XLS_to_RAO")(filename, VesselName, Vessel_LC, origin\[, ...\])         | Convert excel file to Xarray RAO object         |
| [`load_XLS`](#PyBM.marine.tools.load_XLS "PyBM.marine.tools.load_XLS")(filename, mirror)                                               |                                                 |
| [`CSV_to_RAO`](#PyBM.marine.tools.CSV_to_RAO "PyBM.marine.tools.CSV_to_RAO")(filename, VesselName, Vessel_LC, origin\[, ...\])         | Convert CSV file to Xarray RAO object           |
| [`load_CSV`](#PyBM.marine.tools.load_CSV "PyBM.marine.tools.load_CSV")(filename, mirror)                                               |                                                 |
| [`TXT_to_RAO`](#PyBM.marine.tools.TXT_to_RAO "PyBM.marine.tools.TXT_to_RAO")(filename, VesselName, Vessel_LC, origin\[, ...\])         | Convert OrcaFlex .txt file to MotionRAO object. |
| [`load_TXT`](#PyBM.marine.tools.load_TXT "PyBM.marine.tools.load_TXT")(filename\[, mirror\])                                           |                                                 |

## Package Contents

PyBM.marine.tools.Octopus_to_RAO(*octopus_file*, *VesselName*, *Vessel_LC*, *speed=0*)[](../../../../../source-code/PyBM/marine/tools/import_octopus_rao.py)  

&nbsp;

PyBM.marine.tools.get_speeds(*file_iterator*)[](../../../../../source-code/PyBM/marine/tools/import_octopus_rao.py)  

&nbsp;

PyBM.marine.tools.get_wave_directions(*file_iterator*)[](../../../../../source-code/PyBM/marine/tools/import_octopus_rao.py)  

&nbsp;

PyBM.marine.tools.get_wave_frequencies(*file_iterator*, *speed*)[](../../../../../source-code/PyBM/marine/tools/import_octopus_rao.py)  

&nbsp;

PyBM.marine.tools.LIS_to_RAO(*filename*, *VesselName*, *Vessel_LC*)[](../../../../../source-code/PyBM/marine/tools/LIS_to_Xarray.py)  
Convert LIS data to MotionRAO object.

Parameters:  
- **filename** – path to LIS file

- **VesselName** – Name of the vessel

- **Vessel_LC** – Vessel Loading condition

&nbsp;

PyBM.marine.tools.load_LIS(*filename*)[](../../../../../source-code/PyBM/marine/tools/LIS_to_Xarray.py)  

&nbsp;

PyBM.marine.tools.\_\_file_len(*fname*)[](../../../../../source-code/PyBM/marine/tools/read_res.py)  

&nbsp;

PyBM.marine.tools.resample(*data*, *new_dt*, *data_dt*)[](../../../../../source-code/PyBM/marine/tools/read_res.py)  

&nbsp;

PyBM.marine.tools.\_\_read_file(*filename*, *read_invalid=True*)[](../../../../../source-code/PyBM/marine/tools/read_res.py)  

&nbsp;

PyBM.marine.tools.read_res(*filename*, *dt=0*, *read_invalid=True*)[](../../../../../source-code/PyBM/marine/tools/read_res.py)  
Read a text .res file with time traces.

Parameters:  
- **filename** – name of file without extension

- **dt** – \[s\] sample time, if 0 the original sample time is used

- **read_invalid** – \[bool\] If false, invalid files are moved to Invalid folder

Returns:  
Dictionary of time_vectors.

&nbsp;

PyBM.marine.tools.write_pickle(*filename*, *data_dict*)[](../../../../../source-code/PyBM/marine/tools/read_res.py)  

&nbsp;

PyBM.marine.tools.write_res(*filename*, *data_dict*)[](../../../../../source-code/PyBM/marine/tools/read_res.py)  
Write a data dictionary to a .res text file.

Parameters:  
- **filename** – name of file (without extension)

- **data_dict** – dictionary of key / time_vector pairs

&nbsp;

PyBM.marine.tools.XLS_to_RAO(*filename*, *VesselName*, *Vessel_LC*, *origin*, *mirror=False*)[](../../../../../source-code/PyBM/marine/tools/XLS_to_Xarray.py)  
Convert excel file to Xarray RAO object

Parameters:  
- **filename** – Excel file with RAO data

- **VesselName** – Name of vessel

- **Vessel_LC** – Loading condition of the vessel

- **origin** – \[m\] \[x, y, z\] origin of the RAOs w.r.t to vessel APP/CL/Keel

Returns:  
MotionRAO object

Return type:  
[MotionRAO](../index.md#PyBM.marine.MotionRAO "PyBM.marine.MotionRAO")

&nbsp;

PyBM.marine.tools.load_XLS(*filename*, *mirror*)[](../../../../../source-code/PyBM/marine/tools/XLS_to_Xarray.py)  

&nbsp;

PyBM.marine.tools.CSV_to_RAO(*filename*, *VesselName*, *Vessel_LC*, *origin*, *mirror=False*)[](../../../../../source-code/PyBM/marine/tools/CSV_to_Xarray.py)  
Convert CSV file to Xarray RAO object

Parameters:  
- **filename** – CSV file with RAO data

- **VesselName** – Name of vessel

- **Vessel_LC** – Loading condition of the vessel

- **origin** – \[m\] \[x, y, z\] origin of the RAOs w.r.t to vessel APP/CL/Keel

Returns:  
MotionRAO object

Return type:  
[MotionRAO](../index.md#PyBM.marine.MotionRAO "PyBM.marine.MotionRAO")

&nbsp;

PyBM.marine.tools.load_CSV(*filename*, *mirror*)[](../../../../../source-code/PyBM/marine/tools/CSV_to_Xarray.py)  

&nbsp;

PyBM.marine.tools.TXT_to_RAO(*filename*, *VesselName*, *Vessel_LC*, *origin*, *mirror=False*)[](../../../../../source-code/PyBM/marine/tools/TXT_to_Xarray.py)  
Convert OrcaFlex .txt file to MotionRAO object.

&nbsp;

PyBM.marine.tools.load_TXT(*filename*, *mirror=False*)[](../../../../../source-code/PyBM/marine/tools/TXT_to_Xarray.py)  
