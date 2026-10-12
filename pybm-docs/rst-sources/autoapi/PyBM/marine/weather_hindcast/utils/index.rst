PyBM.marine.weather_hindcast.utils
==================================

.. py:module:: PyBM.marine.weather_hindcast.utils

.. autoapi-nested-parse::

   Utility functions for hindcast analysis.



Functions
---------

.. autoapisummary::

   PyBM.marine.weather_hindcast.utils.adaptive_bins
   PyBM.marine.weather_hindcast.utils.from_weibull


Module Contents
---------------

.. py:function:: adaptive_bins(coord_values, min_span, n_bins)

   Create adaptive statistics bins based on scatter_data coordinates.
   Essentially this is to be able to get and visualize stats for Hs and Tp that are more useful and not overly granular.
   The idea is to merge bins until a minimum span is reached, and limit the number of bins to n_bins.

   For example, if the scatter table has Hs bins with upper values [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0],
   and min_span = 1.0, n_bins = 5, the resulting statistic bins would be [0-1, 1-2, 2-3, 3-4, 4-inf]. This is much simpler to visualize data instead of 10 fine bins.

   :param coord_values: Upper bounds of the bins (e.g., self.scatter_data.Hs.values)
   :param min_span: Minimum bin width (e.g., 1.0 for Hs, 2.0 for Tp)
   :param n_bins: Maximum number of output bins (default = 5)
   :return: array of upper bin edges including np.inf


.. py:function:: from_weibull(Hs, Tz, alpha_s, beta_s, a1, a2, b1, b2, a0=0.7, b0=0.07, gamma_s=0)

   Calculate Hs-Tz scatter according to DNV-RP-C205 2014-04 Formula 3.6.3.4.

   Requires Weibull parameters. See DNV-RP-C205 Appendix C Table C-1 for parameters.
   Only valid for JONSWAP spectrum.

   :param Hs: Hs values (bin midpoints)
   :type Hs: np.array
   :param Tz: Tz values (bin midpoints)
   :type Tz: np.array
   :param alpha_s: Weibull scale parameter for significant wave height
   :param beta_s: Weibull shape parameter for significant wave height
   :param a1: Conditional distribution parameter
   :param a2: Conditional distribution parameter
   :param b1: Conditional distribution parameter
   :param b2: Conditional distribution parameter
   :param a0: Conditional distribution parameter (default 0.7)
   :param b0: Conditional distribution parameter (default 0.07)
   :param gamma_s: Weibull location parameter (default 0)
   :return: 2D scatter diagram with bins with coordinates (Hs, Tz)
   :rtype: xr.DataArray


