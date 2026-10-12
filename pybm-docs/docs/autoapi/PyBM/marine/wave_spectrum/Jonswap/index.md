<!-- Source: https://docs.app.barge-master.com/autoapi/PyBM/marine/wave_spectrum/Jonswap/index.html -->

# PyBM.marine.wave_spectrum.Jonswap

This document defines the JONSWAP spectrum class.

CBR 21-06-2023

References:  
- \[1\] Offshore Hydromechanics, J.M.J. Journée and W.W. Massie

- \[2\] DNV-RP-C205 Environmental Conditions and Environmental Loads, APRIL 2014

## Attributes

|                                                                                                  |     |
|--------------------------------------------------------------------------------------------------|-----|
| [`logger`](#PyBM.marine.wave_spectrum.Jonswap.logger "PyBM.marine.wave_spectrum.Jonswap.logger") |     |

## Classes

|                                                                                                     |                                                    |
|-----------------------------------------------------------------------------------------------------|----------------------------------------------------|
| [`Jonswap`](#PyBM.marine.wave_spectrum.Jonswap.Jonswap "PyBM.marine.wave_spectrum.Jonswap.Jonswap") | This class defines the JONSWAP Frequency spectrum. |

## Module Contents

PyBM.marine.wave_spectrum.Jonswap.logger[](../../../../../../source-code/PyBM/marine/wave_spectrum/Jonswap.py)  

&nbsp;

*class *PyBM.marine.wave_spectrum.Jonswap.Jonswap(*Hs*, *Tp*, *main_direction*, *Ndirs=11*, *spreading=4*, *gamma=None*)[](../../../../../../source-code/PyBM/marine/wave_spectrum/Jonswap.py)  
Bases: [`PyBM.marine.wave_spectrum.WaveSpectrum.WaveSpectrum`](../WaveSpectrum/index.md#PyBM.marine.wave_spectrum.WaveSpectrum.WaveSpectrum "PyBM.marine.wave_spectrum.WaveSpectrum.WaveSpectrum")

This class defines the JONSWAP Frequency spectrum.

Parameters:  
- **Hs** – \[m\] Significant wave height

- **Tp** – \[s\] Peak period

- **main_direction** – \[deg\] Wave direction: 0 is from stern 180 from bow, 90 from starboard

- **Ndirs** – \[-\] Number of wave directions

- **spreading** – \[-\] Wave spreading, unidirectional is used if spreading =\< 0

- **gamma** – \[-\] Peakness factor, according to DNV if not specified

\_\_str\_\_()[](../../../../../../source-code/PyBM/marine/wave_spectrum/Jonswap.py)  

*property *gamma[](../../../../../../source-code/PyBM/marine/wave_spectrum/Jonswap.py)  

*property *Tz[](../../../../../../source-code/PyBM/marine/wave_spectrum/Jonswap.py)  
Zero up-crossing period \[s\]

*static *Tz_to_Tp(*Tz*)[](../../../../../../source-code/PyBM/marine/wave_spectrum/Jonswap.py)  
Convert zero up-crossing period to peak period \[s\]

Parameters:  
**Tz** – Zero up-crossing period \[s\]

Returns:  
Peak period \[s\]

*static *\_compute_gamma(*Tp*, *Hs*)[](../../../../../../source-code/PyBM/marine/wave_spectrum/Jonswap.py)  
Compute gamma according to DNV regulations \[2\] 3.5.5.5

Parameters:  
- **Tp** – Peak Period \[s\]

- **Hs** – Significant wave height \[m\]

Returns:  
\[-\] peakedness factor

compute_gamma()[](../../../../../../source-code/PyBM/marine/wave_spectrum/Jonswap.py)  

power_spectrum(*freqs: xarray.DataArray*)[](../../../../../../source-code/PyBM/marine/wave_spectrum/Jonswap.py)  
Compute frequency spectrum for the given frequency points.

Parameters:  
**freqs** – \[Hz\] list of frequency components

Returns:  
\[m2/Hz\] Wave spectral density

*static *\_power_spectrum(*freqs*, *gamma*, *Tp*, *Hs*)[](../../../../../../source-code/PyBM/marine/wave_spectrum/Jonswap.py)  
