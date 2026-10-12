import numpy as np
import xarray as xr
from scipy.integrate import quad

def from_weibull(Hs, Tz, alpha_s, beta_s, a1, a2, b1, b2, a0=0.7, b0=0.07, lambda_s=0):
    """
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
    """
    # Note: The 1.287 factor is based on the Jonswap spectrum. This will not be valid for other spectra.
    h = xr.DataArray(Hs, {"Hs": Hs})
    t = xr.DataArray(Tz, {"Tz": Tz})

    def f_Hs(Hs):
        return (
            (beta_s / alpha_s)
            * np.power((Hs - lambda_s) / alpha_s, beta_s - 1)
            * np.exp(-np.power((Hs - lambda_s) / alpha_s, beta_s))
        )

    def f_Tz_Hs(Hs, Tz):
        mu = a0 + a1 * np.power(Hs, a2)
        sigma = b0 + b1 * np.exp(b2 * Hs)
        return 1 / (sigma * Tz * np.sqrt(2 * np.pi)) * np.exp(-np.power(np.log(Tz) - mu, 2) / (2 * sigma**2))

    datot = f_Hs(h) * f_Tz_Hs(h, t)
    return datot

def _percentages_from_weibull(Hs, Tz, alpha_s, beta_s, a1, a2, b1, b2, a0=0.7, b0=0.07, lambda_s=0):
    """
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
    """
    # Tz = np.array(Tp) / 1.287
    f_hs_cum = np.frompyfunc(
        lambda hs, tz: quad(lambda h: from_weibull(h, tz, alpha_s, beta_s, a1, a2, b1, b2, a0, b0, lambda_s), 0, hs)[0],
        2,
        1,
    )
    # f_tp_cum = np.frompyfunc(lambda hs, tp: quad(lambda t: from_weibull(hs, t, alpha_s, beta_s, a1, a2, b1, b2, a0, b0, lambda_s, sum), 0, tp)[0], 2,1)
    return f_hs_cum(Hs, Tz)

def percentage_from_workability_weibull(Hs_workability, alpha_s, beta_s, a1, a2, b1, b2, a0=0.7, b0=0.07, lambda_s=0):
    """
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
    """
    Tps = Hs_workability.Tp
    # assumes Jonswap spectrum
    Hs_workability = Hs_workability.assign_coords(Tz=("Tp", np.array(Tps) / 1.287))
    Tz = Hs_workability.Tz

    max_workability = quad(
        lambda t: _percentages_from_weibull(np.inf, t, alpha_s, beta_s, a1, a2, b1, b2, a0, b0, lambda_s),
        Tz.min(),
        Tz.max(),
    )[0]
    if not max_workability > 0.99:
        raise ValueError(
            f"Workability Tps values only cover {max_workability*100}% of the weibull distribution. Choose a larger Tp range to cover at least 99%."
        )
    return xr.apply_ufunc(
        lambda h, t: _percentages_from_weibull(h, t, alpha_s, beta_s, a1, a2, b1, b2, a0, b0, lambda_s),
        Hs_workability,
        Tz,
    ).integrate("Tz")
