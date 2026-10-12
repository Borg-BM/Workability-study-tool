"""
"""

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
from matplotlib.collections import LineCollection
from matplotlib.colors import BoundaryNorm
from matplotlib.figure import Figure
from matplotlib.lines import Line2D

import PyBM.marine.motion_analysis.SpectrumAccessor
from PyBM.marine.machines import Machine_Linear, Machine_Nonlinear
from PyBM.marine.machines.MCG30 import MCG30_Linear, MCG30_Nonlinear
from PyBM.marine import MotionRAO, WaveSpectrum, compute_response

cmap = mpl.colormaps["tab10"]

@xr.register_dataarray_accessor("workability")

class workability_accessor:
    def __init__(self, obj):

        self._obj = obj

    def table(self, Hs, Hsrange):
        result = self._obj
        tabledata = xr.DataArray(
            np.tile(Hsrange, (len(result.coords["Tp"].values), 1)) / Hs,
            coords={"Tp": result.coords["Tp"].values, "Hs": Hsrange},
        )
        return 100 * tabledata / result

    def byscatter(self, scatter):
        # get maximum limit between all types
        result = self._obj.min(dim="lim_type")
        # sort scatter and make cumulative sum along Hs
        sc = scatter.sortby(["Hs", "Tp"]).interp_like(result)
        # include all wave directions in scatter plot (copies data)
        sc = 100 * sc / sc.sum()
        sc = sc.cumsum(dim="Hs")
        # resultexp = result.sel(Tp=sc.coords["Tp"],method="nearest").assign_coords(dict(Tp=sc.coords["Tp"]))
        # interpolate Hs; fill nan (out of range values) with the last value of the cumsum function.
        return sc.interp(Hs=result).fillna(sc.sel(dict(Hs=sc.coords["Hs"][-1]))).sum("Tp")

    def plot_detailed_workability(self, max_hs=None, fig=None):
        """Plot workability for each system limit.

        :param workability_result: _description_
        :type workability_result: xr.DataArray
        :param max_hs: _description_, defaults to None
        :type max_hs: _type_, optional
        :param fig: _description_, defaults to None
        :type fig: _type_, optional
        """
        _polar_plotter(multiple_lines, self._obj, max_hs, fig)

    def plot_combined_workability(self, max_hs=None, fig=None):
        """Plot the result of the workability in polar plots

        :param workability_result: [m] Array of limiting Hs for each wave peak period, direction and machine limit.
        :param max_hs: [m] maximum Hs on the polar plot, defaults to None
        :param fig: figure to plot on, defaults to None
        """
        _polar_plotter(multicolored_line, self._obj, max_hs, fig)

def directional_workability(rao: MotionRAO, wave: WaveSpectrum, machine: Machine_Linear, **kwargs) -> xr.DataArray:
    """Compute the workability of the machine for the given wave directions.

    :return: [m] Array of limiting Hs for each wave peak period, direction and machine limit.
    """
    if not isinstance(machine, Machine_Linear):
        raise TypeError(
            "For a directional workability the machine must be linearized. Use directional_workability_timetrace() for workability with non-linearized machines."
        )
    rao_at_poi = machine.get_rao_at_poi(rao)
    resp_at_poi = compute_response(wave, rao_at_poi)
    mpe_at_poi = resp_at_poi.spectral_equal_energy.MPE(**kwargs)
    data = machine.get_workability_limit(mpe_at_poi) * wave.Hs
    return data.squeeze()

def directional_workability_timetrace(trace: xr.DataArray, machine: MCG30_Nonlinear, **kwargs) -> xr.DataArray:
    """Compute the workability of the machine using the time trace supplied (MCG)

    :return: [m] Array of limiting Hs for each wave peak period, direction and machine limit.
    """
    if not isinstance(machine, Machine_Nonlinear):
        raise TypeError(
            "For a directional workability the machine must be non-linear. Use directional_workability_timetrace() for workability with non-linearized machines."
        )
    trace = trace.chunk({"Tp": 1, "WaveDirection": 1})
    data = machine.get_workability_limit(trace, **kwargs) * trace.Hs
    return data.compute()

def _polar_plotter(plot_method, workability_result: xr.DataArray, max_hs=None, fig: Figure = None):
    ncols = 2
    workability_result = workability_result.assign_coords(WaveDirection=workability_result.WaveDirection * np.pi / 180)
    workability_result = xr.concat(
        [workability_result, workability_result.loc[dict(WaveDirection=0)].assign_coords(WaveDirection=2 * np.pi)],
        "WaveDirection",
    )
    nrows = np.ceil(workability_result.Tp.size / 2).astype("int")
    max_y = max_hs or workability_result.min(dim="lim_type").max().values
    workability_result = np.minimum(workability_result, max_y - 0.1)
    fig = fig or plt.gcf()
    for i, Tp in enumerate(workability_result.Tp):
        Tp_result = workability_result.isel(Tp=i)
        ax = fig.add_subplot(nrows, ncols, i + 1, projection="polar")
        plot_method(ax, Tp_result.squeeze())
        set_polar_plot_params(ax, max_y, Tp)
    proxies = _make_legend_proxies(cmap)
    plt.gcf().legend(proxies, workability_result.lim_type.values, loc="lower right")
    plt.subplots_adjust(hspace=0.5)

def multicolored_line(ax: plt.Axes, Tp_result):
    norm = BoundaryNorm(range(len(Tp_result.lim_type) + 1), len(Tp_result.lim_type))
    points = np.array([Tp_result.WaveDirection, Tp_result.min(dim="lim_type")]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    lc = LineCollection(segments, cmap=cmap, norm=norm, linewidths=2)
    lc.set_array(Tp_result.argmin(dim="lim_type"))
    ax.add_collection(lc)

def multiple_lines(ax: plt.Axes, Tp_result):
    Tp_result.plot.line(ax=ax, x="WaveDirection", add_legend=False)

def set_polar_plot_params(ax: plt.Axes, max_y, Tp):
    ax.set_theta_zero_location("S")
    ax.set_ylim(0, max_y)
    ax.set_yticks(np.arange(0, max_y, 1))
    ax.grid(True, "major")
    ax.set_title(f"Tp={Tp:.0f}s")
    plot_ship(ax, max_y / 3)

def plot_ship(ax: plt.Axes, plot_diameter=1.0):
    """Plot a ship contour on the given axis.

    :param axs: Axes to plot on.
    :param plot_diameter: diameter of vessel contour, defaults to 1.0
    """
    x = -plot_diameter * np.array([-0.5, 0.25, 0.4, 0.47, 0.4, 0.25, -0.5, -0.5]) * 2
    y = plot_diameter * np.array([0.25, 0.25, 0.17, 0, -0.17, -0.25, -0.25, 0.25]) * 1.5
    r = np.sqrt(np.square(x) + np.square(y))
    theta = np.arctan2(y, x)
    ax.plot(theta, r, "k")

def _make_legend_proxies(cmap, **kwargs):
    proxies = []
    for i in range(cmap.N):
        proxies.append(Line2D([0, 1], [0, 1], color=cmap.colors[i], **kwargs))
    return proxies
