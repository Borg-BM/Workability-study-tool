<!-- Source: https://docs.app.barge-master.com/autoapi/PyBM/marine/tools/read_res/index.html -->

# PyBM.marine.tools.read_res

This file reads .res output files from aNySIM and returns a dictionary with all the data

## Functions

|                                                                                                                               |                                              |
|-------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------|
| [`__file_len`](#PyBM.marine.tools.read_res.__file_len "PyBM.marine.tools.read_res.__file_len")(fname)                         |                                              |
| [`resample`](#PyBM.marine.tools.read_res.resample "PyBM.marine.tools.read_res.resample")(data, new_dt, data_dt)               |                                              |
| [`__read_file`](#PyBM.marine.tools.read_res.__read_file "PyBM.marine.tools.read_res.__read_file")(filename\[, read_invalid\]) |                                              |
| [`read_res`](#PyBM.marine.tools.read_res.read_res "PyBM.marine.tools.read_res.read_res")(filename\[, dt, read_invalid\])      | Read a text .res file with time traces.      |
| [`write_pickle`](#PyBM.marine.tools.read_res.write_pickle "PyBM.marine.tools.read_res.write_pickle")(filename, data_dict)     |                                              |
| [`write_res`](#PyBM.marine.tools.read_res.write_res "PyBM.marine.tools.read_res.write_res")(filename, data_dict)              | Write a data dictionary to a .res text file. |

## Module Contents

PyBM.marine.tools.read_res.\_\_file_len(*fname*)[](../../../../../../source-code/PyBM/marine/tools/read_res.py)  

&nbsp;

PyBM.marine.tools.read_res.resample(*data*, *new_dt*, *data_dt*)[](../../../../../../source-code/PyBM/marine/tools/read_res.py)  

&nbsp;

PyBM.marine.tools.read_res.\_\_read_file(*filename*, *read_invalid=True*)[](../../../../../../source-code/PyBM/marine/tools/read_res.py)  

&nbsp;

PyBM.marine.tools.read_res.read_res(*filename*, *dt=0*, *read_invalid=True*)[](../../../../../../source-code/PyBM/marine/tools/read_res.py)  
Read a text .res file with time traces.

Parameters:  
- **filename** – name of file without extension

- **dt** – \[s\] sample time, if 0 the original sample time is used

- **read_invalid** – \[bool\] If false, invalid files are moved to Invalid folder

Returns:  
Dictionary of time_vectors.

&nbsp;

PyBM.marine.tools.read_res.write_pickle(*filename*, *data_dict*)[](../../../../../../source-code/PyBM/marine/tools/read_res.py)  

&nbsp;

PyBM.marine.tools.read_res.write_res(*filename*, *data_dict*)[](../../../../../../source-code/PyBM/marine/tools/read_res.py)  
Write a data dictionary to a .res text file.

Parameters:  
- **filename** – name of file (without extension)

- **data_dict** – dictionary of key / time_vector pairs
