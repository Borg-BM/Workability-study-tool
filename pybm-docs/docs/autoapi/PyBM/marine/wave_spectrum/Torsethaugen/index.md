<!-- Source: https://docs.app.barge-master.com/autoapi/PyBM/marine/wave_spectrum/Torsethaugen/index.html -->

# PyBM.marine.wave_spectrum.Torsethaugen

This document defines the Torsethaugen spectrum class.

CBR 21-06-2023

## Classes

|                                                                                                                              |                                                         |
|------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------|
| [`Torsethaugen`](#PyBM.marine.wave_spectrum.Torsethaugen.Torsethaugen "PyBM.marine.wave_spectrum.Torsethaugen.Torsethaugen") | This class defines the Torsethaugen Frequency spectrum. |

## Module Contents

*class *PyBM.marine.wave_spectrum.Torsethaugen.Torsethaugen(*Hs*, *Tp*, *main_direction*, *Ndirs=11*, *spreading=4*, *offset=0*)[](../../../../../../source-code/PyBM/marine/wave_spectrum/Torsethaugen.py)  
Bases: [`PyBM.marine.wave_spectrum.WaveSpectrum.WaveSpectrum`](../WaveSpectrum/index.md#PyBM.marine.wave_spectrum.WaveSpectrum.WaveSpectrum "PyBM.marine.wave_spectrum.WaveSpectrum.WaveSpectrum")

This class defines the Torsethaugen Frequency spectrum.

offset* = 0*[](../../../../../../source-code/PyBM/marine/wave_spectrum/Torsethaugen.py)  

power_spectrum(*freqs*)[](../../../../../../source-code/PyBM/marine/wave_spectrum/Torsethaugen.py)  
Compute frequency spectrum for the given frequency points.

Parameters:  
- **freqs** – \[Hz\] list of frequency components

- **Npeak** – \[0, 1 or 2\] 0: use full Torsethaugen spectrum. 1: use first peak only. 2: use second peak only

Returns:  
\[m2/Hz\] Wave spectral density

*static *\_power_spectrum_parameters(*Tp*, *Hs*)[](../../../../../../source-code/PyBM/marine/wave_spectrum/Torsethaugen.py)  
Compute power spectral parameters for the Torsethaugen double peak spectrum :param Tp: peak wave period :param Hs: significant wave height :return: \[H1, Tp1, H2, Tp2, y, winddominated\]

*static *\_power_spectrum(*freqs*, *Tp*, *Hs*)[](../../../../../../source-code/PyBM/marine/wave_spectrum/Torsethaugen.py)  
Calculate the double peaked power spectrum of the Torsethaugen paper (simplified) :params freqs: frequencies of the spectral density result :param Tp: peak wave period :param Hs: significant wave height :return: \[H1, Tp1, H2, Tp2, y, winddominated\]

dual_equal_energy_directional_wave_spectrum(*freqs*, *offset=90*, *Ndirs=None*)[](../../../../../../source-code/PyBM/marine/wave_spectrum/Torsethaugen.py)  
Compute dual peak, combined directional wave spectrum. Uses two JONSWAP spectrums offset by 90 deg or whatever specified.

Parameters:  
- **freqs** – \[Hz\] Vector of frequency points

- **offset** – \[deg\] directionality offset between first peak spectrum and second peak spectrum

- **Ndirs** – \[-\] Number of directions (must be odd)

Returns:  
Directional wave Spectrum

equal_energy_directional_wave_spectrum(*freqs*, *Ndirs=None*)[](../../../../../../source-code/PyBM/marine/wave_spectrum/Torsethaugen.py)  
Compute directional wave spectrim with spreading using equal energy directions.

Parameters:  
- **freqs** – \[Hz\] Vector of frequency points

- **Ndirs** – \[-\] Number of directions (must be odd)

Returns:  
Directional wave Spectrum
