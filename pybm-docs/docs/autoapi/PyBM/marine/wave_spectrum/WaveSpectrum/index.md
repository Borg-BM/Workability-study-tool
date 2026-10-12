<!-- Source: https://docs.app.barge-master.com/autoapi/PyBM/marine/wave_spectrum/WaveSpectrum/index.html -->

# PyBM.marine.wave_spectrum.WaveSpectrum

## Classes

|                                                                                                                              |                                                                  |
|------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------|
| [`WaveSpectrum`](#PyBM.marine.wave_spectrum.WaveSpectrum.WaveSpectrum "PyBM.marine.wave_spectrum.WaveSpectrum.WaveSpectrum") | Helper class that provides a standard way to create an ABC using |

## Functions

|                                                                                                             |     |
|-------------------------------------------------------------------------------------------------------------|-----|
| [`wrap`](#PyBM.marine.wave_spectrum.WaveSpectrum.wrap "PyBM.marine.wave_spectrum.WaveSpectrum.wrap")(angle) |     |

## Module Contents

PyBM.marine.wave_spectrum.WaveSpectrum.wrap(*angle*)[](../../../../../../source-code/PyBM/marine/wave_spectrum/WaveSpectrum.py)  

&nbsp;

*class *PyBM.marine.wave_spectrum.WaveSpectrum.WaveSpectrum(*Hs*, *Tp*, *main_direction*, *Ndirs=11*, *spreading=4.0*)[](../../../../../../source-code/PyBM/marine/wave_spectrum/WaveSpectrum.py)  
Bases: `abc.ABC`

Helper class that provides a standard way to create an ABC using inheritance.

*property *Hs[](../../../../../../source-code/PyBM/marine/wave_spectrum/WaveSpectrum.py)  

*property *Tp[](../../../../../../source-code/PyBM/marine/wave_spectrum/WaveSpectrum.py)  

*property *main_direction[](../../../../../../source-code/PyBM/marine/wave_spectrum/WaveSpectrum.py)  
\[deg\] Main direction of wave.

spreading* = 4.0*[](../../../../../../source-code/PyBM/marine/wave_spectrum/WaveSpectrum.py)  

*property *Ndirs[](../../../../../../source-code/PyBM/marine/wave_spectrum/WaveSpectrum.py)  
\[-\] Number of wave directions to use (should be odd).

\_\_str\_\_()[](../../../../../../source-code/PyBM/marine/wave_spectrum/WaveSpectrum.py)  

*abstractmethod *power_spectrum(*freqs*)[](../../../../../../source-code/PyBM/marine/wave_spectrum/WaveSpectrum.py)  
Compute frequency spectrum for the given frequency points.

Parameters:  
- **freqs** – \[Hz\] list of frequency components

- **plot** – True to plot spectrum

Returns:  
\[m2/(rad/s)\] Wave spectral density

wave_spectrum(*freqs*)[](../../../../../../source-code/PyBM/marine/wave_spectrum/WaveSpectrum.py)  
Compute frequency spectrum for the given frequency points.

Parameters:  
- **freqs** – \[Hz\] list of frequency components

- **plot** – True to plot spectrum

Returns:  
\[m2/(rad/s)\] Wave spectral density

equal_energy_frequencies(*bounds*, *df=None*, *Nfreqs=100*)[](../../../../../../source-code/PyBM/marine/wave_spectrum/WaveSpectrum.py)  
Numeric method to calculate frequencies at equal energies.

Parameters:  
**Nfreqs** (*int,* *optional*) – NUmber of frequency components to generate, defaults to 100

equal_energy_directions(*Ndirs=None*)[](../../../../../../source-code/PyBM/marine/wave_spectrum/WaveSpectrum.py)  
Compute the directions to use for equal energy directional spreading.

Parameters:  
**Ndirs** – \[-\] number of directions (must be odd)

Returns:  
\[deg\] Vector of directions

*static *equal_energy_method(*func_power_spectrum*, *bounds*, *N*)[](../../../../../../source-code/PyBM/marine/wave_spectrum/WaveSpectrum.py)  
Numeric equal area method. :param func_power_spectrum: Function that outputs the power spectrum, such as a wave spectrum power spectrum or a spreading function. Must accept array of x coordinates, and output either a xr.DataArray or an array of y. :param bounds: bounds of X, as an array or tuple: (xmin, xmax) :param N: Number of X to divide energy over

directional_wave_spectrum(*freqs*, *Rel_Dirs*)[](../../../../../../source-code/PyBM/marine/wave_spectrum/WaveSpectrum.py)  
Compute combined directional wave spectrum.

Parameters:  
- **freqs** – \[Hz\] list of frequency components

- **Rel_Dirs** – \[deg\] list of wave directions relative to main direction (between -180 and 180 degrees).

Returns:  
\[m2/Hz\] Wave spectral density

abs_directions(*Rel_Dirs*)[](../../../../../../source-code/PyBM/marine/wave_spectrum/WaveSpectrum.py)  

equal_energy_directional_wave_spectrum(*freqs*, *Ndirs=None*)[](../../../../../../source-code/PyBM/marine/wave_spectrum/WaveSpectrum.py)  
Compute directional wave spectrim with spreading using equal energy directions.

Parameters:  
- **freqs** – \[Hz\] Vector of frequency points

- **Ndirs** – \[-\] Number of directions (must be odd)

Returns:  
Directional wave Spectrum

equal_energy_directional_spreading(*Ndirs=None*)[](../../../../../../source-code/PyBM/marine/wave_spectrum/WaveSpectrum.py)  
Compute directional wave spreading using equal energy directions.

Parameters:  
- **Ndirs** – \[-\] Number of directions (must be odd)

- **plot** – plots the spectrum if True

Returns:  
Directional wave spreading

directional_spreading(*relative_dirs*)[](../../../../../../source-code/PyBM/marine/wave_spectrum/WaveSpectrum.py)  
Compute directional spreading factors for the given directions.

Function is based on the Cos^n function defined in the Orcaflex documentation.

Parameters:  
- **relative_dirs** – \[deg\] list of wave directions relative to main direction (between -180 and 180 degrees).

- **plot** – True to plot directional spreading

Returns:  
\[-\] spreading factor corresponding to each direction

*static *shift_direction(*wave_data*, *angle_shift*)[](../../../../../../source-code/PyBM/marine/wave_spectrum/WaveSpectrum.py)  

plot(*freqs*, *Rel_Dirs*, *ax=None*)[](../../../../../../source-code/PyBM/marine/wave_spectrum/WaveSpectrum.py)  
