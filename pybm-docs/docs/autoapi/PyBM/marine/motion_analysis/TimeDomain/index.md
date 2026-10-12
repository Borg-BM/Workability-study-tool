<!-- Source: https://docs.app.barge-master.com/autoapi/PyBM/marine/motion_analysis/TimeDomain/index.html -->

# PyBM.marine.motion_analysis.TimeDomain

Time domain tools

References:  
\[1\]: Ship Motion Control, Tristan Perez

## Classes

|                                                                                                                                       |                                                       |
|---------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------|
| [`TimeDomainTools`](#PyBM.marine.motion_analysis.TimeDomain.TimeDomainTools "PyBM.marine.motion_analysis.TimeDomain.TimeDomainTools") | Tools for time domain traces in xarray.DataArray type |
| [`TimeDomain`](#PyBM.marine.motion_analysis.TimeDomain.TimeDomain "PyBM.marine.motion_analysis.TimeDomain.TimeDomain")                |                                                       |

## Module Contents

*class *PyBM.marine.motion_analysis.TimeDomain.TimeDomainTools(*xarray_obj*)[](../../../../../../source-code/PyBM/marine/motion_analysis/TimeDomain.py)  
Tools for time domain traces in xarray.DataArray type

\_obj[](../../../../../../source-code/PyBM/marine/motion_analysis/TimeDomain.py)  

translate_trace(*offset: numpy.array*)[](../../../../../../source-code/PyBM/marine/motion_analysis/TimeDomain.py)  
Translates the trace in 6 DOF. Does not use small angle approx..

Parameters:  
**offset** (*np.array*) – offset in \[x,y,z\]

translate_trace_smallangle(*offset: numpy.array*)[](../../../../../../source-code/PyBM/marine/motion_analysis/TimeDomain.py)  
Translates the trace in 6 DOF. Uses small angle approx

Parameters:  
**offset** (*np.array*) – offset in \[x,y,z\]

&nbsp;

*class *PyBM.marine.motion_analysis.TimeDomain.TimeDomain(*wave: [PyBM.marine.wave_spectrum.WaveSpectrum](../../wave_spectrum/index.md#id42 "PyBM.marine.wave_spectrum.WaveSpectrum")*, *rao: [PyBM.marine.motion_analysis.MotionRAO.MotionRAO](../MotionRAO/index.md#PyBM.marine.motion_analysis.MotionRAO.MotionRAO "PyBM.marine.motion_analysis.MotionRAO.MotionRAO")*, *vesselCoG*)[](../../../../../../source-code/PyBM/marine/motion_analysis/TimeDomain.py)  
rao[](../../../../../../source-code/PyBM/marine/motion_analysis/TimeDomain.py)  

vesselCoG[](../../../../../../source-code/PyBM/marine/motion_analysis/TimeDomain.py)  

wave[](../../../../../../source-code/PyBM/marine/motion_analysis/TimeDomain.py)  

*static *time_vector(*dt*, *duration*)[](../../../../../../source-code/PyBM/marine/motion_analysis/TimeDomain.py)  
Create labelled time vector

Parameters:  
- **dt** – \[s\] Time step

- **duration** – \[s\] Duration of time trace

generate_mat_time_traces(*folder: str*, *dt*, *duration*, *wave*)[](../../../../../../source-code/PyBM/marine/motion_analysis/TimeDomain.py)  
Generate .mat time traces to be used in the matlab workability tools.

Parameters:  
- **folder** – Folder to save the files

- **dt** – \[s\] Time step

- **duration** – \[s\] Duration of time trace

- **wave** – \[s\] Wave to generate time traces for. Parameters may be vectorized.

- **directions** – \[deg\] Wave directions

generate_time_traces(*folder: str*, *dt*, *duration*, *wave*)[](../../../../../../source-code/PyBM/marine/motion_analysis/TimeDomain.py)  
Generate .mat time traces to be used in the matlab workability tools.

Parameters:  
- **folder** – Folder to save the files

- **dt** – \[s\] Time step

- **duration** – \[s\] Duration of time trace

- **wave** – \[s\] Wave to generate time traces for. Parameters may be vectorized.

- **directions** – \[deg\] Wave directions

save_mat_file(*folder*, *trace*)[](../../../../../../source-code/PyBM/marine/motion_analysis/TimeDomain.py)  
Vectorized saving function

save_nc_file(*folder*, *trace*)[](../../../../../../source-code/PyBM/marine/motion_analysis/TimeDomain.py)  

*static *\_save_nc_file(*folder*, *traces: xarray.DataArray*, *VesselName*, *vesselCoG*)[](../../../../../../source-code/PyBM/marine/motion_analysis/TimeDomain.py)  
Save traces as a single nc file. will append nc with extra coordinates, if already there. :param folder: folder name :type folder: string :param traces: traces to save. :type traces: xarray.DataArray

*static *default_trace_path(*VesselName*, *revision=0*)[](../../../../../../source-code/PyBM/marine/motion_analysis/TimeDomain.py)  

load_time_trace(*folder*)[](../../../../../../source-code/PyBM/marine/motion_analysis/TimeDomain.py)  
Loads time traces. Tries to open nc files first, if non existent, opens mat files. :param folder: folder name :type folder: str

*static *load_all_default_time_traces(*VesselName*, *rev=0*)[](../../../../../../source-code/PyBM/marine/motion_analysis/TimeDomain.py)  
Load the time traces of the given vessel and revision in the default engineering library folder. :param VesselName: vessel name :type VesselName: str :param rev: revision number :type rev: int

*static *load_all_time_traces(*folder*, *VesselName*)[](../../../../../../source-code/PyBM/marine/motion_analysis/TimeDomain.py)  
Static version of load_time_trace. Loads all time traces present in given folder. do not need to supply any sort of dimensioning for Tp, Hs or direction. If using default trace path, you can also use the function TimeDomain.load_default_time_trace(). :param folder: folder to load time traces from. :type folder: str :param VesselName: name of the vessel to be loaded. :type VesselName: str

load_mat_time_trace(*folder*)[](../../../../../../source-code/PyBM/marine/motion_analysis/TimeDomain.py)  
Load a MAT time trace(s) as DataArray. Uses objects’ properties for selecting which traces to load.

Parameters:  
**folder** (*str*) – path of folder

*static *\_load_mat_time_trace(*folder*, *VesselName*, *Tp*, *Hs*, *Direction*)[](../../../../../../source-code/PyBM/marine/motion_analysis/TimeDomain.py)  
Vectorized static function to load mat time traces according to given parameters.

*static *\_load_single_mat_time_trace(*folder*, *VesselName*, *Tp*, *Hs*, *Direction*)[](../../../../../../source-code/PyBM/marine/motion_analysis/TimeDomain.py)  

load_nc_time_trace(*folder*)[](../../../../../../source-code/PyBM/marine/motion_analysis/TimeDomain.py)  
Load NC stored time trace(s) as DataArray

Parameters:  
**folder** – path of folder

*static *\_load_nc_time_trace(*folder*, *VesselName*)[](../../../../../../source-code/PyBM/marine/motion_analysis/TimeDomain.py)  
Loads nc file with traces.

mat_file_name()[](../../../../../../source-code/PyBM/marine/motion_analysis/TimeDomain.py)  

*static *\_mat_file_name(*VesselName*, *Tp*, *Hs*, *Direction*)[](../../../../../../source-code/PyBM/marine/motion_analysis/TimeDomain.py)  
Returns mat file names for trace. Broadcasts arrays in case of multiple values for Tp,Hs,main_direction.

nc_file_name()[](../../../../../../source-code/PyBM/marine/motion_analysis/TimeDomain.py)  

*static *\_nc_file_name(*VesselName*)[](../../../../../../source-code/PyBM/marine/motion_analysis/TimeDomain.py)  
Returns nc file name for trace. Since nc files include all directions it is not a vectorized function

*static *\_file_name(*VesselName*, *Tp*, *Hs*, *Direction*)[](../../../../../../source-code/PyBM/marine/motion_analysis/TimeDomain.py)  

*static *time_trace_from_rao_and_wave(*time: xarray.DataArray*, *wave: [PyBM.marine.wave_spectrum.WaveSpectrum](../../wave_spectrum/index.md#id42 "PyBM.marine.wave_spectrum.WaveSpectrum")*, *rao: [PyBM.marine.motion_analysis.MotionRAO.MotionRAO](../MotionRAO/index.md#PyBM.marine.motion_analysis.MotionRAO.MotionRAO "PyBM.marine.motion_analysis.MotionRAO.MotionRAO")*, *Nfreqs=100*, *bounds=None*)[](../../../../../../source-code/PyBM/marine/motion_analysis/TimeDomain.py)  
Generate time trace based on RAO and Wave.

Parameters:  
- **time** (*xr.DataArray*) – \[s\] time vector

- **wave** ([*WaveSpectrum*](../../index.md#PyBM.marine.WaveSpectrum "PyBM.marine.WaveSpectrum")) – \[m2/(rad/s)\] WaveSpectrum

- **rao** ([*MotionRAO*](../../index.md#PyBM.marine.MotionRAO "PyBM.marine.MotionRAO")) – \[m/m, deg/m\] 6DOF Motion RAO

multi_directional_time_trace(*wave: [PyBM.marine.wave_spectrum.WaveSpectrum](../../wave_spectrum/index.md#id42 "PyBM.marine.wave_spectrum.WaveSpectrum")*, *rao: [PyBM.marine.motion_analysis.MotionRAO.MotionRAO](../MotionRAO/index.md#PyBM.marine.motion_analysis.MotionRAO.MotionRAO "PyBM.marine.motion_analysis.MotionRAO.MotionRAO")*, *bounds=None*)[](../../../../../../source-code/PyBM/marine/motion_analysis/TimeDomain.py)  
Create time trace including wave spreading.

Parameters:  
- **time** (*xr.DataArray*) – \[s\] time vector

- **rao** ([*MotionRAO*](../../index.md#PyBM.marine.MotionRAO "PyBM.marine.MotionRAO")) – \[m/m, deg/m\] 6DOF Motion RAO

- **wave** ([*WaveSpectrum*](../../index.md#PyBM.marine.WaveSpectrum "PyBM.marine.WaveSpectrum")) – \[m2/(rad/s)\] WaveSpectrum

single_direction_time_trace(*wave: [PyBM.marine.wave_spectrum.WaveSpectrum](../../wave_spectrum/index.md#id42 "PyBM.marine.wave_spectrum.WaveSpectrum")*, *rao: [PyBM.marine.motion_analysis.MotionRAO.MotionRAO](../MotionRAO/index.md#PyBM.marine.motion_analysis.MotionRAO.MotionRAO "PyBM.marine.motion_analysis.MotionRAO.MotionRAO")*)[](../../../../../../source-code/PyBM/marine/motion_analysis/TimeDomain.py)  
Create time trace for a single wave direction

Parameters:  
- **time** (*xr.DataArray*) – \[s\] time vector

- **rao** ([*MotionRAO*](../../index.md#PyBM.marine.MotionRAO "PyBM.marine.MotionRAO")) – \[m/m, deg/m\] 6DOF Motion RAO. Must have interpolated frequencies according to equal area method

- **wave** ([*WaveSpectrum*](../../index.md#PyBM.marine.WaveSpectrum "PyBM.marine.WaveSpectrum")) – \[m2/(rad/s)\] WaveSpectrum

*static *compute_deltas(*coordinates*, *dim*)[](../../../../../../source-code/PyBM/marine/motion_analysis/TimeDomain.py)  
Create bins centered a coordinate points.

Parameters:  
- **coordinates** – Coordinates to create bins around.

- **dim** – Dimension name

*static *zero_crossing_period(*trace*)[](../../../../../../source-code/PyBM/marine/motion_analysis/TimeDomain.py)  
Compute average zero-crossing period of a time trace.

return: \[s\] average zero-crossing period.
