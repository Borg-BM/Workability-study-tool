<!-- Source: https://docs.app.barge-master.com/autoapi/PyBM/marine/motion_analysis/Response/index.html -->

# PyBM.marine.motion_analysis.Response

Module to calculate vessel motions in the frequency domain.

CBR 21-06-2023

References:  
\[1\] Offshore Hydromechanics, J.M.J. Journée and W.W. Massie

## Functions

|                                                                                                                                                                                         |                                                                        |
|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------|
| [`compute_response`](#PyBM.marine.motion_analysis.Response.compute_response "PyBM.marine.motion_analysis.Response.compute_response")(wave, rao\[, poi, Nfreqs, f_bounds\])              | Compute the vessel response based on the given wave spectrum and RAO.  |
| [`compute_mpe`](#PyBM.marine.motion_analysis.Response.compute_mpe "PyBM.marine.motion_analysis.Response.compute_mpe")(wave, rao\[, poi, storm_duration, ...\])                          | Calculate MPE of the given parameter for all points of interest (POI). |
| [`equal_energy_freqs_rao`](#PyBM.marine.motion_analysis.Response.equal_energy_freqs_rao "PyBM.marine.motion_analysis.Response.equal_energy_freqs_rao")(wave, rao, Nfreqs\[, f_bounds\]) |                                                                        |
| [`apply_directional_spreading`](#PyBM.marine.motion_analysis.Response.apply_directional_spreading "PyBM.marine.motion_analysis.Response.apply_directional_spreading")(wave, rao)        |                                                                        |

## Module Contents

PyBM.marine.motion_analysis.Response.compute_response(*wave: [PyBM.marine.wave_spectrum.WaveSpectrum](../../wave_spectrum/index.md#id42 "PyBM.marine.wave_spectrum.WaveSpectrum")*, *rao: [PyBM.marine.motion_analysis.RAO](../index.md#id0 "PyBM.marine.motion_analysis.RAO")*, *poi=None*, *Nfreqs=200*, *f_bounds=None*)[](../../../../../../source-code/PyBM/marine/motion_analysis/Response.py)  
Compute the vessel response based on the given wave spectrum and RAO.

Parameters:  
- **wave** ([*WaveSpectrum*](../../index.md#PyBM.marine.WaveSpectrum "PyBM.marine.WaveSpectrum")) – The wave spectrum.

- **rao** ([*RAO*](../../index.md#PyBM.marine.RAO "PyBM.marine.RAO")) – The response amplitude operator.

- **poi** (*list,* *optional*) – The point of interest \[x,y,z\] in meters, defaults to None.

- **Nfreqs** (*int,* *optional*) – The number of frequencies to consider, defaults to 200.

- **f_bounds** (*tuple,* *optional*) – The frequency bounds, defaults to None.

Returns:  
The computed vessel response.

Return type:  
Response

&nbsp;

PyBM.marine.motion_analysis.Response.compute_mpe(*wave: [PyBM.marine.wave_spectrum.WaveSpectrum](../../wave_spectrum/index.md#id42 "PyBM.marine.wave_spectrum.WaveSpectrum")*, *rao: [PyBM.marine.motion_analysis.RAO](../index.md#id0 "PyBM.marine.motion_analysis.RAO")*, *poi=None*, *storm_duration=10800*, *transfer_function=None*)[](../../../../../../source-code/PyBM/marine/motion_analysis/Response.py)  
Calculate MPE of the given parameter for all points of interest (POI).

Parameters:  
- **poi** – \[m\] (x,y,z) offset of point of interest

- **storm_duration** – \[s\] duration of the period of interest (usually 3 hours)

- **transfer_function** – (\[\[a\], \[b\]\]) Numerator and Denumerator of continuous transfer function to be applied.

Returns:  
Statistical extreme value

&nbsp;

PyBM.marine.motion_analysis.Response.equal_energy_freqs_rao(*wave: [PyBM.marine.wave_spectrum.WaveSpectrum](../../wave_spectrum/index.md#id42 "PyBM.marine.wave_spectrum.WaveSpectrum")*, *rao: [PyBM.marine.motion_analysis.RAO](../index.md#id0 "PyBM.marine.motion_analysis.RAO")*, *Nfreqs*, *f_bounds=None*)[](../../../../../../source-code/PyBM/marine/motion_analysis/Response.py)  

&nbsp;

PyBM.marine.motion_analysis.Response.apply_directional_spreading(*wave: [PyBM.marine.wave_spectrum.WaveSpectrum](../../wave_spectrum/index.md#id42 "PyBM.marine.wave_spectrum.WaveSpectrum")*, *rao: [PyBM.marine.motion_analysis.RAO](../index.md#id0 "PyBM.marine.motion_analysis.RAO")*)[](../../../../../../source-code/PyBM/marine/motion_analysis/Response.py)  
