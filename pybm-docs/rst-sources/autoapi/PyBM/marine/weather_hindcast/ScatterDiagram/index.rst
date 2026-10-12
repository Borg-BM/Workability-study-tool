PyBM.marine.weather_hindcast.ScatterDiagram
===========================================

.. py:module:: PyBM.marine.weather_hindcast.ScatterDiagram


Functions
---------

.. autoapisummary::

   PyBM.marine.weather_hindcast.ScatterDiagram.from_weibull
   PyBM.marine.weather_hindcast.ScatterDiagram._percentages_from_weibull
   PyBM.marine.weather_hindcast.ScatterDiagram.percentage_from_workability_weibull


Module Contents
---------------

.. py:function:: from_weibull(Hs, Tz, alpha_s, beta_s, a1, a2, b1, b2, a0=0.7, b0=0.07, lambda_s=0)

   calculate Hs-Tz scatter according to
   DNV C205 2014-04 Formula 3.6.3.4
   Requires weibull parameters. see Appendix C Table C-1 for parameters
   Only valid for Jonswap spectrum
   :param Hs: Hs values
   :type Hs: np.array
   :param Tp: Tp values
   :type Tp: np.array
   :param alpha_s: weibull parameter
   :param beta_s: weibull parameter
   :param a1: weibull parameter
   :param a2: weibull parameter
   :param b1: weibull parameter
   :param b2: weibull parameter
   :param a0: weibull parameter
   :param b0: weibull parameter
   :param lambda_s: weibull parameter
   :return: 2D scatter diagram with bins with coordinates (Hs, Tp)


.. py:function:: _percentages_from_weibull(Hs, Tz, alpha_s, beta_s, a1, a2, b1, b2, a0=0.7, b0=0.07, lambda_s=0)

   calculate Hs-Tz cumulative over Hs for each coordinate Hs, Tp.
   Requires weibull parameters. see Appendix C Table C-1 for parameters
   Only valid for Jonswap spectrum
   :param Hs: Hs values
   :type Hs: np.array
   :param Tp: Tp values, must be same length as Hs
   :type Tp: np.array
   :param alpha_s: weibull parameter
   :param beta_s: weibull parameter
   :param a1: weibull parameter
   :param a2: weibull parameter
   :param b1: weibull parameter
   :param b2: weibull parameter
   :param a0: weibull parameter
   :param b0: weibull parameter
   :param lambda_s: weibull parameter
   :return: percentage of scatter below Hs for each coordinate


.. py:function:: percentage_from_workability_weibull(Hs_workability, alpha_s, beta_s, a1, a2, b1, b2, a0=0.7, b0=0.07, lambda_s=0)

   Warning: Weibull distributions are extremely conservative from a sales perspective.
   calculate Hs-Tz cumulative over Hs for each coordinate Hs, Tp.
   DNV C205 2014-04 Formula
   Uses workability hs values, interprets Tp from workability hs values
   Requires weibull parameters. see Appendix C Table C-1 for parameters
   Only valid for Jonswap spectrum
   :param Hs_workability: workability Hs values
   :type Hs_workability: xr.DataArray
   :param alpha_s: weibull parameter
   :param beta_s: weibull parameter
   :param a1: weibull parameter
   :param a2: weibull parameter
   :param b1: weibull parameter
   :param b2: weibull parameter
   :param a0: weibull parameter
   :param b0: weibull parameter
   :param lambda_s: weibull parameter
   :return: percentage of scatter below Hs for each coordinate


