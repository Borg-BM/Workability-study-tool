<!-- Source: https://docs.app.barge-master.com/autoapi/PyBM/marine/weather_hindcast/utils/index.html -->

# PyBM.marine.weather_hindcast.utils

Utility functions for hindcast analysis.

## Functions

|                                                                                                                                                               |                                                                           |
|---------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------|
| [`adaptive_bins`](#PyBM.marine.weather_hindcast.utils.adaptive_bins "PyBM.marine.weather_hindcast.utils.adaptive_bins")(coord_values, min_span, n_bins)       | Create adaptive statistics bins based on scatter_data coordinates.        |
| [`from_weibull`](#PyBM.marine.weather_hindcast.utils.from_weibull "PyBM.marine.weather_hindcast.utils.from_weibull")(Hs, Tz, alpha_s, beta_s, a1, a2, b1, b2) | Calculate Hs-Tz scatter according to DNV-RP-C205 2014-04 Formula 3.6.3.4. |

## Module Contents

PyBM.marine.weather_hindcast.utils.adaptive_bins(*coord_values*, *min_span*, *n_bins*)[](../../../../../../source-code/PyBM/marine/weather_hindcast/utils.py)  
Create adaptive statistics bins based on scatter_data coordinates. Essentially this is to be able to get and visualize stats for Hs and Tp that are more useful and not overly granular. The idea is to merge bins until a minimum span is reached, and limit the number of bins to n_bins.

For example, if the scatter table has Hs bins with upper values \[0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0\], and min_span = 1.0, n_bins = 5, the resulting statistic bins would be \[0-1, 1-2, 2-3, 3-4, 4-inf\]. This is much simpler to visualize data instead of 10 fine bins.

Parameters:  
- **coord_values** – Upper bounds of the bins (e.g., self.scatter_data.Hs.values)

- **min_span** – Minimum bin width (e.g., 1.0 for Hs, 2.0 for Tp)

- **n_bins** – Maximum number of output bins (default = 5)

Returns:  
array of upper bin edges including np.inf

&nbsp;

PyBM.marine.weather_hindcast.utils.from_weibull(*Hs*, *Tz*, *alpha_s*, *beta_s*, *a1*, *a2*, *b1*, *b2*, *a0=0.7*, *b0=0.07*, *gamma_s=0*)[](../../../../../../source-code/PyBM/marine/weather_hindcast/utils.py)  
Calculate Hs-Tz scatter according to DNV-RP-C205 2014-04 Formula 3.6.3.4.

Requires Weibull parameters. See DNV-RP-C205 Appendix C Table C-1 for parameters. Only valid for JONSWAP spectrum.

Parameters:  
- **Hs** (*np.array*) – Hs values (bin midpoints)

- **Tz** (*np.array*) – Tz values (bin midpoints)

- **alpha_s** – Weibull scale parameter for significant wave height

- **beta_s** – Weibull shape parameter for significant wave height

- **a1** – Conditional distribution parameter

- **a2** – Conditional distribution parameter

- **b1** – Conditional distribution parameter

- **b2** – Conditional distribution parameter

- **a0** – Conditional distribution parameter (default 0.7)

- **b0** – Conditional distribution parameter (default 0.07)

- **gamma_s** – Weibull location parameter (default 0)

Returns:  
2D scatter diagram with bins with coordinates (Hs, Tz)

Return type:  
xr.DataArray
