<!-- Source: https://docs.app.barge-master.com/autoapi/PyBM/marine/motion_analysis/SpectrumAccessor/index.html -->

# PyBM.marine.motion_analysis.SpectrumAccessor

Accessor of Xarray Dataset to implement spectral analysis tools.

CBR 06-10-2023

References:  
\[1\] Offshore Hydromechanics, J.M.J. Journée and W.W. Massie

## Classes

|                                                                                                                                                               |                                                                  |
|---------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------|
| [`SpectralTools`](#PyBM.marine.motion_analysis.SpectrumAccessor.SpectralTools "PyBM.marine.motion_analysis.SpectrumAccessor.SpectralTools")                   | Tools to analyse spectra.                                        |
| [`EqualEnergySpectrum`](#PyBM.marine.motion_analysis.SpectrumAccessor.EqualEnergySpectrum "PyBM.marine.motion_analysis.SpectrumAccessor.EqualEnergySpectrum") | Tools to analyse spectra optimized for equal energy frequencies. |

## Module Contents

*class *PyBM.marine.motion_analysis.SpectrumAccessor.SpectralTools(*xarray_obj*)[](../../../../../../source-code/PyBM/marine/motion_analysis/SpectrumAccessor.py)  
Tools to analyse spectra.

\_obj[](../../../../../../source-code/PyBM/marine/motion_analysis/SpectrumAccessor.py)  

\_amp* = None*[](../../../../../../source-code/PyBM/marine/motion_analysis/SpectrumAccessor.py)  

\_m0* = None*[](../../../../../../source-code/PyBM/marine/motion_analysis/SpectrumAccessor.py)  

\_m1* = None*[](../../../../../../source-code/PyBM/marine/motion_analysis/SpectrumAccessor.py)  

\_m2* = None*[](../../../../../../source-code/PyBM/marine/motion_analysis/SpectrumAccessor.py)  

*property *m0[](../../../../../../source-code/PyBM/marine/motion_analysis/SpectrumAccessor.py)  

*property *m1[](../../../../../../source-code/PyBM/marine/motion_analysis/SpectrumAccessor.py)  

*property *m2[](../../../../../../source-code/PyBM/marine/motion_analysis/SpectrumAccessor.py)  

*property *amp[](../../../../../../source-code/PyBM/marine/motion_analysis/SpectrumAccessor.py)  

spectral_moment(*order=0*)[](../../../../../../source-code/PyBM/marine/motion_analysis/SpectrumAccessor.py)  
Compute nth order spectral moment of a spectrum. Ref \[1\]. Eq (6.81)

Parameters:  
**order** (*int,* *optional*) – Order of the moment, defaults to 0

*property *standard_deviation[](../../../../../../source-code/PyBM/marine/motion_analysis/SpectrumAccessor.py)  
Compute the standard deviation from the frequency response. Ref. \[1\] Eq (6.82)

Parameters:  
**m0** – 0th Spectral moment

Returns:  
Standard deviation

*property *zero_crossing_period[](../../../../../../source-code/PyBM/marine/motion_analysis/SpectrumAccessor.py)  
Compute zero-crossing period. Ref. \[1\] Eq (6.84)

Returns:  
\[s\] Average zero crossing period.

MPE(*storm_duration=10800*, *standard_deviations=None*)[](../../../../../../source-code/PyBM/marine/motion_analysis/SpectrumAccessor.py)  
Compute Most Probable Extreme from Rayleigh Distribution based on storm duration and Zero-crossing period. Ref \[1\], Section 11.1 Eq (11.20)

Parameters:  
**storm_duration** – \[s\] duration of the period of interest (usually 3 hours)

Returns:  
Most probable extreme.

&nbsp;

*class *PyBM.marine.motion_analysis.SpectrumAccessor.EqualEnergySpectrum(*xarray_obj*)[](../../../../../../source-code/PyBM/marine/motion_analysis/SpectrumAccessor.py)  
Bases: [`SpectralTools`](#PyBM.marine.motion_analysis.SpectrumAccessor.SpectralTools "PyBM.marine.motion_analysis.SpectrumAccessor.SpectralTools")

Tools to analyse spectra optimized for equal energy frequencies.

spectral_moment(*order=0*)[](../../../../../../source-code/PyBM/marine/motion_analysis/SpectrumAccessor.py)  
Compute nth order spectral moment of an equal energy spectrum. Ref \[1\]. Eq (6.81)

Parameters:  
**order** (*int,* *optional*) – Order of the moment, defaults to 0
