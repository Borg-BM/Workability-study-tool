<!-- Source: https://docs.app.barge-master.com/autoapi/PyBM/marine/wave_spectrum/PiersonMoskowitz/index.html -->

# PyBM.marine.wave_spectrum.PiersonMoskowitz

This document defines the Pierson Moskowitz spectrum class.

CBR 21-06-2023

References:  
- \[1\] Offshore Hydromechanics, J.M.J. Journée and W.W. Massie

- \[2\] DNV-RP-C205 Environmental Conditions and Environmental Loads, APRIL 2014

## Attributes

|                                                                                                                    |     |
|--------------------------------------------------------------------------------------------------------------------|-----|
| [`logger`](#PyBM.marine.wave_spectrum.PiersonMoskowitz.logger "PyBM.marine.wave_spectrum.PiersonMoskowitz.logger") |     |

## Classes

|                                                                                                                                                  |                                                              |
|--------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------|
| [`PiersonMoskowitz`](#PyBM.marine.wave_spectrum.PiersonMoskowitz.PiersonMoskowitz "PyBM.marine.wave_spectrum.PiersonMoskowitz.PiersonMoskowitz") | This class defines the Pierson Moskowitz Frequency spectrum. |

## Module Contents

PyBM.marine.wave_spectrum.PiersonMoskowitz.logger[](../../../../../../source-code/PyBM/marine/wave_spectrum/PiersonMoskowitz.py)  

&nbsp;

*class *PyBM.marine.wave_spectrum.PiersonMoskowitz.PiersonMoskowitz(*Hs*, *Tp*, *main_direction*, *Ndirs=11*, *spreading=4.0*)[](../../../../../../source-code/PyBM/marine/wave_spectrum/PiersonMoskowitz.py)  
Bases: [`PyBM.marine.wave_spectrum.WaveSpectrum.WaveSpectrum`](../WaveSpectrum/index.md#PyBM.marine.wave_spectrum.WaveSpectrum.WaveSpectrum "PyBM.marine.wave_spectrum.WaveSpectrum.WaveSpectrum")

This class defines the Pierson Moskowitz Frequency spectrum.

power_spectrum(*freqs*)[](../../../../../../source-code/PyBM/marine/wave_spectrum/PiersonMoskowitz.py)  
Compute frequency spectrum for the given frequency points.

Parameters:  
**freqs** – \[Hz\] list of frequency components

Returns:  
\[m2/Hz\] Wave spectral density

*static *\_power_spectrum(*freqs*, *Tp*, *Hs*)[](../../../../../../source-code/PyBM/marine/wave_spectrum/PiersonMoskowitz.py)  
Ref \[2\] 3.5.5.1

Parameters:  
- **Hs** – \[m\] Significant wave height

- **Tp** – \[s\] Peak period
