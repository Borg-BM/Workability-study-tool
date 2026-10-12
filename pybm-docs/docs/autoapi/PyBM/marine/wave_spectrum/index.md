<!-- Source: https://docs.app.barge-master.com/autoapi/PyBM/marine/wave_spectrum/index.html -->

# PyBM.marine.wave_spectrum

## Submodules

- [PyBM.marine.wave_spectrum.Jonswap](Jonswap/index.md)
- [PyBM.marine.wave_spectrum.PiersonMoskowitz](PiersonMoskowitz/index.md)
- [PyBM.marine.wave_spectrum.Torsethaugen](Torsethaugen/index.md)
- [PyBM.marine.wave_spectrum.WaveSpectrum](WaveSpectrum/index.md)

## Attributes

|                                                      |     |
|------------------------------------------------------|-----|
| [`logger`](#id19 "PyBM.marine.wave_spectrum.logger") |     |
| [`logger`](#id19 "PyBM.marine.wave_spectrum.logger") |     |

## Classes

|                                                                                                    |                                                                  |
|----------------------------------------------------------------------------------------------------|------------------------------------------------------------------|
| [`PiersonMoskowitz`](#id20 "PyBM.marine.wave_spectrum.PiersonMoskowitz")                           | This class defines the Pierson Moskowitz Frequency spectrum.     |
| [`WaveSpectrum`](#id42 "PyBM.marine.wave_spectrum.WaveSpectrum")                                   | Helper class that provides a standard way to create an ABC using |
| [`Jonswap`](#PyBM.marine.wave_spectrum.Jonswap "PyBM.marine.wave_spectrum.Jonswap")                | This class defines the JONSWAP Frequency spectrum.               |
| [`WaveSpectrum`](#id42 "PyBM.marine.wave_spectrum.WaveSpectrum")                                   | Helper class that provides a standard way to create an ABC using |
| [`PiersonMoskowitz`](#id20 "PyBM.marine.wave_spectrum.PiersonMoskowitz")                           | This class defines the Pierson Moskowitz Frequency spectrum.     |
| [`WaveSpectrum`](#id42 "PyBM.marine.wave_spectrum.WaveSpectrum")                                   | Helper class that provides a standard way to create an ABC using |
| [`Torsethaugen`](#PyBM.marine.wave_spectrum.Torsethaugen "PyBM.marine.wave_spectrum.Torsethaugen") | This class defines the Torsethaugen Frequency spectrum.          |
| [`WaveSpectrum`](#id42 "PyBM.marine.wave_spectrum.WaveSpectrum")                                   | Helper class that provides a standard way to create an ABC using |

## Functions

|                                                                                   |     |
|-----------------------------------------------------------------------------------|-----|
| [`wrap`](#PyBM.marine.wave_spectrum.wrap "PyBM.marine.wave_spectrum.wrap")(angle) |     |

## Package Contents

*class *PyBM.marine.wave_spectrum.PiersonMoskowitz(*Hs*, *Tp*, *main_direction*, *Ndirs=11*, *spreading=4.0*)[](../../../../../source-code/PyBM/marine/wave_spectrum/PiersonMoskowitz.py)  
Bases: [`PyBM.marine.wave_spectrum.WaveSpectrum.WaveSpectrum`](WaveSpectrum/index.md#PyBM.marine.wave_spectrum.WaveSpectrum.WaveSpectrum "PyBM.marine.wave_spectrum.WaveSpectrum.WaveSpectrum")

This class defines the Pierson Moskowitz Frequency spectrum.

power_spectrum(*freqs*)[](../../../../../source-code/PyBM/marine/wave_spectrum/PiersonMoskowitz.py)  
Compute frequency spectrum for the given frequency points.

Parameters:  
**freqs** – \[Hz\] list of frequency components

Returns:  
\[m2/Hz\] Wave spectral density

*static *\_power_spectrum(*freqs*, *Tp*, *Hs*)[](../../../../../source-code/PyBM/marine/wave_spectrum/PiersonMoskowitz.py)  
Ref \[2\] 3.5.5.1

Parameters:  
- **Hs** – \[m\] Significant wave height

- **Tp** – \[s\] Peak period

&nbsp;

*class *PyBM.marine.wave_spectrum.WaveSpectrum(*Hs*, *Tp*, *main_direction*, *Ndirs=11*, *spreading=4.0*)[](../../../../../source-code/PyBM/marine/wave_spectrum/WaveSpectrum.py)  
Bases: `abc.ABC`

Helper class that provides a standard way to create an ABC using inheritance.

*property *Hs  

*property *Tp  

*property *main_direction  
\[deg\] Main direction of wave.

spreading* = 4.0*  

*property *Ndirs  
\[-\] Number of wave directions to use (should be odd).

\_\_str\_\_()[](../../../../../source-code/PyBM/marine/wave_spectrum/WaveSpectrum.py)  

*abstractmethod *power_spectrum(*freqs*)[](../../../../../source-code/PyBM/marine/wave_spectrum/WaveSpectrum.py)  
Compute frequency spectrum for the given frequency points.

Parameters:  
- **freqs** – \[Hz\] list of frequency components

- **plot** – True to plot spectrum

Returns:  
\[m2/(rad/s)\] Wave spectral density

wave_spectrum(*freqs*)[](../../../../../source-code/PyBM/marine/wave_spectrum/WaveSpectrum.py)  
Compute frequency spectrum for the given frequency points.

Parameters:  
- **freqs** – \[Hz\] list of frequency components

- **plot** – True to plot spectrum

Returns:  
\[m2/(rad/s)\] Wave spectral density

equal_energy_frequencies(*bounds*, *df=None*, *Nfreqs=100*)[](../../../../../source-code/PyBM/marine/wave_spectrum/WaveSpectrum.py)  
Numeric method to calculate frequencies at equal energies.

Parameters:  
**Nfreqs** (*int,* *optional*) – NUmber of frequency components to generate, defaults to 100

equal_energy_directions(*Ndirs=None*)[](../../../../../source-code/PyBM/marine/wave_spectrum/WaveSpectrum.py)  
Compute the directions to use for equal energy directional spreading.

Parameters:  
**Ndirs** – \[-\] number of directions (must be odd)

Returns:  
\[deg\] Vector of directions

*static *equal_energy_method(*func_power_spectrum*, *bounds*, *N*)[](../../../../../source-code/PyBM/marine/wave_spectrum/WaveSpectrum.py)  
Numeric equal area method. :param func_power_spectrum: Function that outputs the power spectrum, such as a wave spectrum power spectrum or a spreading function. Must accept array of x coordinates, and output either a xr.DataArray or an array of y. :param bounds: bounds of X, as an array or tuple: (xmin, xmax) :param N: Number of X to divide energy over

directional_wave_spectrum(*freqs*, *Rel_Dirs*)[](../../../../../source-code/PyBM/marine/wave_spectrum/WaveSpectrum.py)  
Compute combined directional wave spectrum.

Parameters:  
- **freqs** – \[Hz\] list of frequency components

- **Rel_Dirs** – \[deg\] list of wave directions relative to main direction (between -180 and 180 degrees).

Returns:  
\[m2/Hz\] Wave spectral density

abs_directions(*Rel_Dirs*)[](../../../../../source-code/PyBM/marine/wave_spectrum/WaveSpectrum.py)  

equal_energy_directional_wave_spectrum(*freqs*, *Ndirs=None*)[](../../../../../source-code/PyBM/marine/wave_spectrum/WaveSpectrum.py)  
Compute directional wave spectrim with spreading using equal energy directions.

Parameters:  
- **freqs** – \[Hz\] Vector of frequency points

- **Ndirs** – \[-\] Number of directions (must be odd)

Returns:  
Directional wave Spectrum

equal_energy_directional_spreading(*Ndirs=None*)[](../../../../../source-code/PyBM/marine/wave_spectrum/WaveSpectrum.py)  
Compute directional wave spreading using equal energy directions.

Parameters:  
- **Ndirs** – \[-\] Number of directions (must be odd)

- **plot** – plots the spectrum if True

Returns:  
Directional wave spreading

directional_spreading(*relative_dirs*)[](../../../../../source-code/PyBM/marine/wave_spectrum/WaveSpectrum.py)  
Compute directional spreading factors for the given directions.

Function is based on the Cos^n function defined in the Orcaflex documentation.

Parameters:  
- **relative_dirs** – \[deg\] list of wave directions relative to main direction (between -180 and 180 degrees).

- **plot** – True to plot directional spreading

Returns:  
\[-\] spreading factor corresponding to each direction

*static *shift_direction(*wave_data*, *angle_shift*)[](../../../../../source-code/PyBM/marine/wave_spectrum/WaveSpectrum.py)  

plot(*freqs*, *Rel_Dirs*, *ax=None*)[](../../../../../source-code/PyBM/marine/wave_spectrum/WaveSpectrum.py)  

&nbsp;

PyBM.marine.wave_spectrum.logger[](../../../../../source-code/PyBM/marine/wave_spectrum/PiersonMoskowitz.py)  

&nbsp;

*class *PyBM.marine.wave_spectrum.Jonswap(*Hs*, *Tp*, *main_direction*, *Ndirs=11*, *spreading=4*, *gamma=None*)[](../../../../../source-code/PyBM/marine/wave_spectrum/Jonswap.py)  
Bases: [`PyBM.marine.wave_spectrum.WaveSpectrum.WaveSpectrum`](WaveSpectrum/index.md#PyBM.marine.wave_spectrum.WaveSpectrum.WaveSpectrum "PyBM.marine.wave_spectrum.WaveSpectrum.WaveSpectrum")

This class defines the JONSWAP Frequency spectrum.

Parameters:  
- **Hs** – \[m\] Significant wave height

- **Tp** – \[s\] Peak period

- **main_direction** – \[deg\] Wave direction: 0 is from stern 180 from bow, 90 from starboard

- **Ndirs** – \[-\] Number of wave directions

- **spreading** – \[-\] Wave spreading, unidirectional is used if spreading =\< 0

- **gamma** – \[-\] Peakness factor, according to DNV if not specified

\_\_str\_\_()[](../../../../../source-code/PyBM/marine/wave_spectrum/Jonswap.py)  

*property *gamma  

*property *Tz  
Zero up-crossing period \[s\]

*static *Tz_to_Tp(*Tz*)[](../../../../../source-code/PyBM/marine/wave_spectrum/Jonswap.py)  
Convert zero up-crossing period to peak period \[s\]

Parameters:  
**Tz** – Zero up-crossing period \[s\]

Returns:  
Peak period \[s\]

*static *\_compute_gamma(*Tp*, *Hs*)[](../../../../../source-code/PyBM/marine/wave_spectrum/Jonswap.py)  
Compute gamma according to DNV regulations \[2\] 3.5.5.5

Parameters:  
- **Tp** – Peak Period \[s\]

- **Hs** – Significant wave height \[m\]

Returns:  
\[-\] peakedness factor

compute_gamma()[](../../../../../source-code/PyBM/marine/wave_spectrum/Jonswap.py)  

power_spectrum(*freqs: xarray.DataArray*)[](../../../../../source-code/PyBM/marine/wave_spectrum/Jonswap.py)  
Compute frequency spectrum for the given frequency points.

Parameters:  
**freqs** – \[Hz\] list of frequency components

Returns:  
\[m2/Hz\] Wave spectral density

*static *\_power_spectrum(*freqs*, *gamma*, *Tp*, *Hs*)[](../../../../../source-code/PyBM/marine/wave_spectrum/Jonswap.py)  

&nbsp;

*class *PyBM.marine.wave_spectrum.WaveSpectrum(*Hs*, *Tp*, *main_direction*, *Ndirs=11*, *spreading=4.0*)[](../../../../../source-code/PyBM/marine/wave_spectrum/WaveSpectrum.py)  
Bases: `abc.ABC`

Helper class that provides a standard way to create an ABC using inheritance.

*property *Hs  

*property *Tp  

*property *main_direction  
\[deg\] Main direction of wave.

spreading* = 4.0*  

*property *Ndirs  
\[-\] Number of wave directions to use (should be odd).

\_\_str\_\_()[](../../../../../source-code/PyBM/marine/wave_spectrum/WaveSpectrum.py)  

*abstractmethod *power_spectrum(*freqs*)[](../../../../../source-code/PyBM/marine/wave_spectrum/WaveSpectrum.py)  
Compute frequency spectrum for the given frequency points.

Parameters:  
- **freqs** – \[Hz\] list of frequency components

- **plot** – True to plot spectrum

Returns:  
\[m2/(rad/s)\] Wave spectral density

wave_spectrum(*freqs*)[](../../../../../source-code/PyBM/marine/wave_spectrum/WaveSpectrum.py)  
Compute frequency spectrum for the given frequency points.

Parameters:  
- **freqs** – \[Hz\] list of frequency components

- **plot** – True to plot spectrum

Returns:  
\[m2/(rad/s)\] Wave spectral density

equal_energy_frequencies(*bounds*, *df=None*, *Nfreqs=100*)[](../../../../../source-code/PyBM/marine/wave_spectrum/WaveSpectrum.py)  
Numeric method to calculate frequencies at equal energies.

Parameters:  
**Nfreqs** (*int,* *optional*) – NUmber of frequency components to generate, defaults to 100

equal_energy_directions(*Ndirs=None*)[](../../../../../source-code/PyBM/marine/wave_spectrum/WaveSpectrum.py)  
Compute the directions to use for equal energy directional spreading.

Parameters:  
**Ndirs** – \[-\] number of directions (must be odd)

Returns:  
\[deg\] Vector of directions

*static *equal_energy_method(*func_power_spectrum*, *bounds*, *N*)[](../../../../../source-code/PyBM/marine/wave_spectrum/WaveSpectrum.py)  
Numeric equal area method. :param func_power_spectrum: Function that outputs the power spectrum, such as a wave spectrum power spectrum or a spreading function. Must accept array of x coordinates, and output either a xr.DataArray or an array of y. :param bounds: bounds of X, as an array or tuple: (xmin, xmax) :param N: Number of X to divide energy over

directional_wave_spectrum(*freqs*, *Rel_Dirs*)[](../../../../../source-code/PyBM/marine/wave_spectrum/WaveSpectrum.py)  
Compute combined directional wave spectrum.

Parameters:  
- **freqs** – \[Hz\] list of frequency components

- **Rel_Dirs** – \[deg\] list of wave directions relative to main direction (between -180 and 180 degrees).

Returns:  
\[m2/Hz\] Wave spectral density

abs_directions(*Rel_Dirs*)[](../../../../../source-code/PyBM/marine/wave_spectrum/WaveSpectrum.py)  

equal_energy_directional_wave_spectrum(*freqs*, *Ndirs=None*)[](../../../../../source-code/PyBM/marine/wave_spectrum/WaveSpectrum.py)  
Compute directional wave spectrim with spreading using equal energy directions.

Parameters:  
- **freqs** – \[Hz\] Vector of frequency points

- **Ndirs** – \[-\] Number of directions (must be odd)

Returns:  
Directional wave Spectrum

equal_energy_directional_spreading(*Ndirs=None*)[](../../../../../source-code/PyBM/marine/wave_spectrum/WaveSpectrum.py)  
Compute directional wave spreading using equal energy directions.

Parameters:  
- **Ndirs** – \[-\] Number of directions (must be odd)

- **plot** – plots the spectrum if True

Returns:  
Directional wave spreading

directional_spreading(*relative_dirs*)[](../../../../../source-code/PyBM/marine/wave_spectrum/WaveSpectrum.py)  
Compute directional spreading factors for the given directions.

Function is based on the Cos^n function defined in the Orcaflex documentation.

Parameters:  
- **relative_dirs** – \[deg\] list of wave directions relative to main direction (between -180 and 180 degrees).

- **plot** – True to plot directional spreading

Returns:  
\[-\] spreading factor corresponding to each direction

*static *shift_direction(*wave_data*, *angle_shift*)[](../../../../../source-code/PyBM/marine/wave_spectrum/WaveSpectrum.py)  

plot(*freqs*, *Rel_Dirs*, *ax=None*)[](../../../../../source-code/PyBM/marine/wave_spectrum/WaveSpectrum.py)  

&nbsp;

PyBM.marine.wave_spectrum.logger[](../../../../../source-code/PyBM/marine/wave_spectrum/PiersonMoskowitz.py)  

&nbsp;

*class *PyBM.marine.wave_spectrum.PiersonMoskowitz(*Hs*, *Tp*, *main_direction*, *Ndirs=11*, *spreading=4.0*)[](../../../../../source-code/PyBM/marine/wave_spectrum/PiersonMoskowitz.py)  
Bases: [`PyBM.marine.wave_spectrum.WaveSpectrum.WaveSpectrum`](WaveSpectrum/index.md#PyBM.marine.wave_spectrum.WaveSpectrum.WaveSpectrum "PyBM.marine.wave_spectrum.WaveSpectrum.WaveSpectrum")

This class defines the Pierson Moskowitz Frequency spectrum.

power_spectrum(*freqs*)[](../../../../../source-code/PyBM/marine/wave_spectrum/PiersonMoskowitz.py)  
Compute frequency spectrum for the given frequency points.

Parameters:  
**freqs** – \[Hz\] list of frequency components

Returns:  
\[m2/Hz\] Wave spectral density

*static *\_power_spectrum(*freqs*, *Tp*, *Hs*)[](../../../../../source-code/PyBM/marine/wave_spectrum/PiersonMoskowitz.py)  
Ref \[2\] 3.5.5.1

Parameters:  
- **Hs** – \[m\] Significant wave height

- **Tp** – \[s\] Peak period

&nbsp;

*class *PyBM.marine.wave_spectrum.WaveSpectrum(*Hs*, *Tp*, *main_direction*, *Ndirs=11*, *spreading=4.0*)[](../../../../../source-code/PyBM/marine/wave_spectrum/WaveSpectrum.py)  
Bases: `abc.ABC`

Helper class that provides a standard way to create an ABC using inheritance.

*property *Hs  

*property *Tp  

*property *main_direction  
\[deg\] Main direction of wave.

spreading* = 4.0*  

*property *Ndirs  
\[-\] Number of wave directions to use (should be odd).

\_\_str\_\_()[](../../../../../source-code/PyBM/marine/wave_spectrum/WaveSpectrum.py)  

*abstractmethod *power_spectrum(*freqs*)[](../../../../../source-code/PyBM/marine/wave_spectrum/WaveSpectrum.py)  
Compute frequency spectrum for the given frequency points.

Parameters:  
- **freqs** – \[Hz\] list of frequency components

- **plot** – True to plot spectrum

Returns:  
\[m2/(rad/s)\] Wave spectral density

wave_spectrum(*freqs*)[](../../../../../source-code/PyBM/marine/wave_spectrum/WaveSpectrum.py)  
Compute frequency spectrum for the given frequency points.

Parameters:  
- **freqs** – \[Hz\] list of frequency components

- **plot** – True to plot spectrum

Returns:  
\[m2/(rad/s)\] Wave spectral density

equal_energy_frequencies(*bounds*, *df=None*, *Nfreqs=100*)[](../../../../../source-code/PyBM/marine/wave_spectrum/WaveSpectrum.py)  
Numeric method to calculate frequencies at equal energies.

Parameters:  
**Nfreqs** (*int,* *optional*) – NUmber of frequency components to generate, defaults to 100

equal_energy_directions(*Ndirs=None*)[](../../../../../source-code/PyBM/marine/wave_spectrum/WaveSpectrum.py)  
Compute the directions to use for equal energy directional spreading.

Parameters:  
**Ndirs** – \[-\] number of directions (must be odd)

Returns:  
\[deg\] Vector of directions

*static *equal_energy_method(*func_power_spectrum*, *bounds*, *N*)[](../../../../../source-code/PyBM/marine/wave_spectrum/WaveSpectrum.py)  
Numeric equal area method. :param func_power_spectrum: Function that outputs the power spectrum, such as a wave spectrum power spectrum or a spreading function. Must accept array of x coordinates, and output either a xr.DataArray or an array of y. :param bounds: bounds of X, as an array or tuple: (xmin, xmax) :param N: Number of X to divide energy over

directional_wave_spectrum(*freqs*, *Rel_Dirs*)[](../../../../../source-code/PyBM/marine/wave_spectrum/WaveSpectrum.py)  
Compute combined directional wave spectrum.

Parameters:  
- **freqs** – \[Hz\] list of frequency components

- **Rel_Dirs** – \[deg\] list of wave directions relative to main direction (between -180 and 180 degrees).

Returns:  
\[m2/Hz\] Wave spectral density

abs_directions(*Rel_Dirs*)[](../../../../../source-code/PyBM/marine/wave_spectrum/WaveSpectrum.py)  

equal_energy_directional_wave_spectrum(*freqs*, *Ndirs=None*)[](../../../../../source-code/PyBM/marine/wave_spectrum/WaveSpectrum.py)  
Compute directional wave spectrim with spreading using equal energy directions.

Parameters:  
- **freqs** – \[Hz\] Vector of frequency points

- **Ndirs** – \[-\] Number of directions (must be odd)

Returns:  
Directional wave Spectrum

equal_energy_directional_spreading(*Ndirs=None*)[](../../../../../source-code/PyBM/marine/wave_spectrum/WaveSpectrum.py)  
Compute directional wave spreading using equal energy directions.

Parameters:  
- **Ndirs** – \[-\] Number of directions (must be odd)

- **plot** – plots the spectrum if True

Returns:  
Directional wave spreading

directional_spreading(*relative_dirs*)[](../../../../../source-code/PyBM/marine/wave_spectrum/WaveSpectrum.py)  
Compute directional spreading factors for the given directions.

Function is based on the Cos^n function defined in the Orcaflex documentation.

Parameters:  
- **relative_dirs** – \[deg\] list of wave directions relative to main direction (between -180 and 180 degrees).

- **plot** – True to plot directional spreading

Returns:  
\[-\] spreading factor corresponding to each direction

*static *shift_direction(*wave_data*, *angle_shift*)[](../../../../../source-code/PyBM/marine/wave_spectrum/WaveSpectrum.py)  

plot(*freqs*, *Rel_Dirs*, *ax=None*)[](../../../../../source-code/PyBM/marine/wave_spectrum/WaveSpectrum.py)  

&nbsp;

*class *PyBM.marine.wave_spectrum.Torsethaugen(*Hs*, *Tp*, *main_direction*, *Ndirs=11*, *spreading=4*, *offset=0*)[](../../../../../source-code/PyBM/marine/wave_spectrum/Torsethaugen.py)  
Bases: [`PyBM.marine.wave_spectrum.WaveSpectrum.WaveSpectrum`](WaveSpectrum/index.md#PyBM.marine.wave_spectrum.WaveSpectrum.WaveSpectrum "PyBM.marine.wave_spectrum.WaveSpectrum.WaveSpectrum")

This class defines the Torsethaugen Frequency spectrum.

offset* = 0*  

power_spectrum(*freqs*)[](../../../../../source-code/PyBM/marine/wave_spectrum/Torsethaugen.py)  
Compute frequency spectrum for the given frequency points.

Parameters:  
- **freqs** – \[Hz\] list of frequency components

- **Npeak** – \[0, 1 or 2\] 0: use full Torsethaugen spectrum. 1: use first peak only. 2: use second peak only

Returns:  
\[m2/Hz\] Wave spectral density

*static *\_power_spectrum_parameters(*Tp*, *Hs*)[](../../../../../source-code/PyBM/marine/wave_spectrum/Torsethaugen.py)  
Compute power spectral parameters for the Torsethaugen double peak spectrum :param Tp: peak wave period :param Hs: significant wave height :return: \[H1, Tp1, H2, Tp2, y, winddominated\]

*static *\_power_spectrum(*freqs*, *Tp*, *Hs*)[](../../../../../source-code/PyBM/marine/wave_spectrum/Torsethaugen.py)  
Calculate the double peaked power spectrum of the Torsethaugen paper (simplified) :params freqs: frequencies of the spectral density result :param Tp: peak wave period :param Hs: significant wave height :return: \[H1, Tp1, H2, Tp2, y, winddominated\]

dual_equal_energy_directional_wave_spectrum(*freqs*, *offset=90*, *Ndirs=None*)[](../../../../../source-code/PyBM/marine/wave_spectrum/Torsethaugen.py)  
Compute dual peak, combined directional wave spectrum. Uses two JONSWAP spectrums offset by 90 deg or whatever specified.

Parameters:  
- **freqs** – \[Hz\] Vector of frequency points

- **offset** – \[deg\] directionality offset between first peak spectrum and second peak spectrum

- **Ndirs** – \[-\] Number of directions (must be odd)

Returns:  
Directional wave Spectrum

equal_energy_directional_wave_spectrum(*freqs*, *Ndirs=None*)[](../../../../../source-code/PyBM/marine/wave_spectrum/Torsethaugen.py)  
Compute directional wave spectrim with spreading using equal energy directions.

Parameters:  
- **freqs** – \[Hz\] Vector of frequency points

- **Ndirs** – \[-\] Number of directions (must be odd)

Returns:  
Directional wave Spectrum

&nbsp;

PyBM.marine.wave_spectrum.wrap(*angle*)[](../../../../../source-code/PyBM/marine/wave_spectrum/WaveSpectrum.py)  

&nbsp;

*class *PyBM.marine.wave_spectrum.WaveSpectrum(*Hs*, *Tp*, *main_direction*, *Ndirs=11*, *spreading=4.0*)[](../../../../../source-code/PyBM/marine/wave_spectrum/WaveSpectrum.py)  
Bases: `abc.ABC`

Helper class that provides a standard way to create an ABC using inheritance.

*property *Hs  

*property *Tp  

*property *main_direction  
\[deg\] Main direction of wave.

spreading* = 4.0*  

*property *Ndirs  
\[-\] Number of wave directions to use (should be odd).

\_\_str\_\_()[](../../../../../source-code/PyBM/marine/wave_spectrum/WaveSpectrum.py)  

*abstractmethod *power_spectrum(*freqs*)[](../../../../../source-code/PyBM/marine/wave_spectrum/WaveSpectrum.py)  
Compute frequency spectrum for the given frequency points.

Parameters:  
- **freqs** – \[Hz\] list of frequency components

- **plot** – True to plot spectrum

Returns:  
\[m2/(rad/s)\] Wave spectral density

wave_spectrum(*freqs*)[](../../../../../source-code/PyBM/marine/wave_spectrum/WaveSpectrum.py)  
Compute frequency spectrum for the given frequency points.

Parameters:  
- **freqs** – \[Hz\] list of frequency components

- **plot** – True to plot spectrum

Returns:  
\[m2/(rad/s)\] Wave spectral density

equal_energy_frequencies(*bounds*, *df=None*, *Nfreqs=100*)[](../../../../../source-code/PyBM/marine/wave_spectrum/WaveSpectrum.py)  
Numeric method to calculate frequencies at equal energies.

Parameters:  
**Nfreqs** (*int,* *optional*) – NUmber of frequency components to generate, defaults to 100

equal_energy_directions(*Ndirs=None*)[](../../../../../source-code/PyBM/marine/wave_spectrum/WaveSpectrum.py)  
Compute the directions to use for equal energy directional spreading.

Parameters:  
**Ndirs** – \[-\] number of directions (must be odd)

Returns:  
\[deg\] Vector of directions

*static *equal_energy_method(*func_power_spectrum*, *bounds*, *N*)[](../../../../../source-code/PyBM/marine/wave_spectrum/WaveSpectrum.py)  
Numeric equal area method. :param func_power_spectrum: Function that outputs the power spectrum, such as a wave spectrum power spectrum or a spreading function. Must accept array of x coordinates, and output either a xr.DataArray or an array of y. :param bounds: bounds of X, as an array or tuple: (xmin, xmax) :param N: Number of X to divide energy over

directional_wave_spectrum(*freqs*, *Rel_Dirs*)[](../../../../../source-code/PyBM/marine/wave_spectrum/WaveSpectrum.py)  
Compute combined directional wave spectrum.

Parameters:  
- **freqs** – \[Hz\] list of frequency components

- **Rel_Dirs** – \[deg\] list of wave directions relative to main direction (between -180 and 180 degrees).

Returns:  
\[m2/Hz\] Wave spectral density

abs_directions(*Rel_Dirs*)[](../../../../../source-code/PyBM/marine/wave_spectrum/WaveSpectrum.py)  

equal_energy_directional_wave_spectrum(*freqs*, *Ndirs=None*)[](../../../../../source-code/PyBM/marine/wave_spectrum/WaveSpectrum.py)  
Compute directional wave spectrim with spreading using equal energy directions.

Parameters:  
- **freqs** – \[Hz\] Vector of frequency points

- **Ndirs** – \[-\] Number of directions (must be odd)

Returns:  
Directional wave Spectrum

equal_energy_directional_spreading(*Ndirs=None*)[](../../../../../source-code/PyBM/marine/wave_spectrum/WaveSpectrum.py)  
Compute directional wave spreading using equal energy directions.

Parameters:  
- **Ndirs** – \[-\] Number of directions (must be odd)

- **plot** – plots the spectrum if True

Returns:  
Directional wave spreading

directional_spreading(*relative_dirs*)[](../../../../../source-code/PyBM/marine/wave_spectrum/WaveSpectrum.py)  
Compute directional spreading factors for the given directions.

Function is based on the Cos^n function defined in the Orcaflex documentation.

Parameters:  
- **relative_dirs** – \[deg\] list of wave directions relative to main direction (between -180 and 180 degrees).

- **plot** – True to plot directional spreading

Returns:  
\[-\] spreading factor corresponding to each direction

*static *shift_direction(*wave_data*, *angle_shift*)[](../../../../../source-code/PyBM/marine/wave_spectrum/WaveSpectrum.py)  

plot(*freqs*, *Rel_Dirs*, *ax=None*)[](../../../../../source-code/PyBM/marine/wave_spectrum/WaveSpectrum.py)  
