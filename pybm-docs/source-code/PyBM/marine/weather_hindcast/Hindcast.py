"""Hindcast analysis framework with pluggable data sources.

Architecture:

- HindcastLoader: Abstract interface for data loaders (see ``hindcast_loaders.py``)
- Hindcast (factory): Fetches data once and returns an analysis object
- HindcastScatterTable: Analysis for pre-binned (Hs, Tp) scatter data (``xr.DataArray``)
- HindcastTimeSeries: Analysis for time-series wave data (``pd.DataFrame``)
"""

from typing import Optional
from abc import ABC, abstractmethod
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
from datetime import datetime
import calendar
from .HindcastLoader import HindcastLoader as BaseHindcastLoader
from .utils import adaptive_bins

# ========== Base Hindcast Class ==========

class HindcastBase(ABC):
    """Abstract internal base with shared attributes and polymorphic abstract methods.

    The factory fetches data and passes it to the appropriate subclass, so ``fetch``
    is not invoked twice. Subclasses set convenience attributes for easy access.
    """

    def __init__(self, loader: BaseHindcastLoader, data):

        self.loader = loader

        self.time_data: Optional[pd.DataFrame] = data if isinstance(data, pd.DataFrame) else None

        self.scatter_data: Optional[xr.DataArray] = data if isinstance(data, xr.DataArray) else None

        # Promote simple loader attributes (e.g., lat, lon, start, end, station_id) for convenience
        for attr, value in vars(loader).items():
            # Avoid overwriting existing attributes and skip private/internal ones
            if attr.startswith('_') or hasattr(self, attr):
                continue
            # Only promote simple scalar / str types to keep namespace clean
            if isinstance(value, (int, float, str)):
                setattr(self, attr, value)

    def __getattr__(self, name):
        """Delegate missing attributes to the underlying loader.

        This allows access like ``hindcast.lat`` or ``hindcast.filepath`` without
        explicitly copying every loader attribute. If the attribute does not
        exist on the loader, normal AttributeError is raised.
        """
        if hasattr(self.loader, name):
            return getattr(self.loader, name)
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

    def __dir__(self):
        base_dir = set(super().__dir__())
        loader_dir = set(dir(self.loader))
        return sorted(base_dir | loader_dir)

    # ---- Polymorphic statistics & workability interface ----

    @abstractmethod

    def get_Hs_stats(self, period: str = 'overall', **kwargs):
        """Return Hs statistics for given period.

        Period values:

        - 'overall' (both types)
        - 'monthly' (time series only)
        """
        raise NotImplementedError

    @abstractmethod

    def get_Tp_stats(self, period: str = 'overall', **kwargs):
        """Return Tp statistics for given period.

        Period values:

        - 'overall' (both types)
        - 'monthly' (time series only)
        """
        raise NotImplementedError

    
    @abstractmethod

    def plot_Hs_Tp(self, ax: Optional[plt.Axes] = None, **kwargs) -> plt.Axes:
        """Polymorphic Hs–Tp visualization.

        Implementations:

        - Time series: hist2d scatter of individual sea states.
        - Scatter table: heatmap of binned probabilities.
        """
        raise NotImplementedError

    @abstractmethod

    def get_workability_percentage(self, workability_result, period: str = 'overall'):
        """Return workability percentage overall or monthly.

        - ScatterTable: only 'overall'.
        - TimeSeries: 'overall' returns float %, 'monthly' returns pandas Series of % per month.
        """
        raise NotImplementedError

class HindcastScatterTable(HindcastBase):
    """
    Analysis class for scatter table format hindcast data.
    
    Expects data as xr.DataArray with dimensions for Hs and Tp bins.
    
    Provides methods for:

    - Hs and Tp statistics
    - Overall workability percentage based on workability results
    - Joint Hs-Tp wave occurrence plotting
    """
    
    def __init__(self, loader: BaseHindcastLoader, data: xr.DataArray):
        if not isinstance(data, xr.DataArray):
            raise TypeError(f"HindcastScatterTable requires xr.DataArray data, got {type(data)}.")
        if 'Hs' not in data.dims or 'Tp' not in data.dims:
            raise ValueError("Data must have 'Hs' and 'Tp' dimensions.")
        super().__init__(loader, data)

    def get_Hs_stats(self, period: str = 'overall', plot: bool = False, ax: Optional[plt.Axes] = None, min_span: float = 1.0, n_bins: int = 5):
        """Compute wave height statistics from scatter data. Gives the percentage of waves in each Hs bin.
        The statistic bins are adaptive based on the scatter data bins.

        :param str period: Must be 'overall'.
        :param bool plot: If True plot bar chart.
        :param plt.Axes ax: Axis for plot (created if None).
        :param float min_span: Minimum bin width. For example, default of 1.0 means Hs bins of at least 1 meter width.
        :param int n_bins: Maximum number of output bins.
        :return: Row 'overall' with Hs bin fractions. If plot=True returns (DataFrame, Axes).
        :rtype: pd.DataFrame or (pd.DataFrame, plt.Axes)
        """
        if period != 'overall':
            raise NotImplementedError("Scatter table aggregated: period must be 'overall'.")
        if self.scatter_data is None:
            raise ValueError("Scatter data not loaded. Please use a HindcastLoader first.")
        if not isinstance(min_span, (float, int)) or not isinstance(n_bins, int):
            raise ValueError("min_span must be a float or int. n_bins must be an integer.")

        Hs_dist = self.scatter_data.sum(dim='Tp')
        Hs_upper = self.scatter_data.Hs.values
        Hs_lower = np.concatenate(([0.0], Hs_upper[:-1]))
        Hs_bins = adaptive_bins(Hs_upper, min_span, n_bins)
        Hs_bins = np.concatenate(([0.0], Hs_bins))

        Hs_stats = np.zeros(len(Hs_bins) - 1)
        for i in range(len(Hs_bins) - 1):
            bin_lower, bin_upper = Hs_bins[i], Hs_bins[i + 1]
            mask = (Hs_lower < bin_upper) & (Hs_upper > bin_lower)
            Hs_stats[i] = Hs_dist.values[mask].sum()
        Hs_df = pd.DataFrame([Hs_stats], index=['overall'], columns=Hs_bins[1:])
        
        if plot:
            if ax is None:
                fig, ax = plt.subplots(figsize=(6, 4))
            labels = [f"{Hs_bins[i]:.0f}-{Hs_bins[i+1]:.0f}" for i in range(len(Hs_bins)-1)]
            ax.bar(labels, Hs_stats * 100, width=0.6, edgecolor='black', alpha=0.7)
            ax.set_xlabel('Hs [m]')
            ax.set_ylabel('Percentage [%]')
            ax.set_title('Wave Hs Distribution (Overall)')
            return Hs_df, ax
        return Hs_df

    

    def get_Tp_stats(self, period: str = 'overall', plot: bool = False, ax: Optional[plt.Axes] = None, min_span: float = 2.0, n_bins: int = 10):
        """Compute the wave peak period statistics from scatter data. Gives the percentage of waves in each Tp bin.
        The statistic bins are adaptive based on the scatter data bins.

        :param str period: Must be 'overall'.
        :param bool plot: If True plot bar chart.
        :param plt.Axes ax: Axis for plot (created if None).
        :param float min_span: Minimum bin width. For example, default of 2.0 means Tp bins of at least 2 seconds width.
        :param int n_bins: Maximum number of output bins.
        :return: Row 'overall' with adaptive Tp bin fractions (counts). If plot=True returns (DataFrame, Axes).
        :rtype: pd.DataFrame or (pd.DataFrame, plt.Axes)
        """
        if period != 'overall':
            raise NotImplementedError("Scatter table aggregated: period must be 'overall'.")
        if self.scatter_data is None:
            raise ValueError("Scatter data not loaded. Please use a HindcastLoader first.")
        if not isinstance(min_span, (float, int)) or not isinstance(n_bins, int):
            raise ValueError("min_span must be a float or int. n_bins must be an integer.")
        
        Tp_dist = self.scatter_data.sum(dim='Hs')
        Tp_upper = self.scatter_data.Tp.values
        Tp_lower = np.concatenate(([0.0], Tp_upper[:-1]))
        Tp_bins = adaptive_bins(Tp_upper, min_span, n_bins)
        Tp_bins = np.concatenate(([0.0], Tp_bins))

        Tp_stats = np.zeros(len(Tp_bins) - 1)
        for i in range(len(Tp_bins) - 1):
            bin_lower, bin_upper = Tp_bins[i], Tp_bins[i + 1]
            mask = (Tp_lower < bin_upper) & (Tp_upper > bin_lower)
            Tp_stats[i] = Tp_dist.values[mask].sum()
        Tp_df = pd.DataFrame([Tp_stats], index=['overall'], columns=Tp_bins[1:])

        if plot:
            if ax is None:
                fig, ax = plt.subplots(figsize=(6, 4))
            labels = [f"{Tp_bins[i]:.0f}-{Tp_bins[i+1]:.0f}" for i in range(len(Tp_bins)-1)]
            ax.bar(labels, Tp_stats * 100, width=0.6, edgecolor='black', alpha=0.7)
            ax.set_xlabel('Tp [s]')
            ax.set_ylabel('Percentage [%]')
            ax.set_title('Wave Tp Distribution (Overall)')
            return Tp_df, ax
        return Tp_df

    

    def plot_Hs_Tp(self, ax: Optional[plt.Axes] = None, workability_result: Optional[xr.DataArray] = None) -> plt.Axes:
        """Hs vs Tp occurrence heatmap (scatter table).

        :param plt.Axes ax: Axis for plot (created if None).
        :param xr.DataArray workability_result: (Optional) Array of limiting Hs for each wave peak period ('Tp') and possibly direction ('WaveDirection'). Can be passed to plot the limiting Hs curve vs Tp on top of the heatmap. We assume it is already minimized over machine limit (no `lim_type` dimension in the array).
        :return: Axis with plot.
        :rtype: plt.Axes
        """

        if self.scatter_data is None:
            raise ValueError("Scatter data not loaded. Please use a hindcast loader first.")

        if ax is None:
            fig, ax = plt.subplots(figsize=(8, 6))
        
        hs_bins = self.scatter_data.Hs.values
        tp_bins = self.scatter_data.Tp.values
        pcm = ax.pcolormesh(tp_bins, hs_bins, (self.scatter_data.values)*100, cmap='Blues')
        plt.colorbar(pcm, ax=ax, label='Probability Density [%]')
        ax.set_xlabel('Tp [s]')
        ax.set_ylabel('Hs [m]')
        ax.set_title('Hs vs Tp Wave Occurrence [%]')
        ax.grid()

        if workability_result is not None:
            if not set(workability_result.dims).issubset({'Tp', 'WaveDirection'}):
                raise ValueError("Workability result must be only dependent on 'Tp' and 'WaveDirection'. Make sure to minimize over machine limit and" \
                " to only select one condition (e.g. motion compensation or no compensation).")
            if 'WaveDirection' in workability_result.dims: # workability array not minimized over direction yet
                workability_result = workability_result.min(dim="WaveDirection")

            # Fix the axis limits BEFORE plotting the line
            xlim = ax.get_xlim()
            ylim = ax.get_ylim()
            ax.plot(workability_result['Tp'].values, workability_result.values, color='red', label='Workability Limit')
            # Restore the limits so they don’t stretch
            ax.set_xlim(xlim)
            ax.set_ylim(ylim)
            ax.legend()

        return ax

    

    def get_workability_percentage(self, workability_result, period: str = 'overall') -> float:
        """Calculate overall workability percentage based on the workability results.
        
        For each Tp bin in the scatter table, interpolates the limiting Hs from the workability curve,
        then computes the cumulative probability up to that Hs limit by interpolating over the Hs bins.
        
        The method properly handles:

        - Binned scatter data (where coords represent upper bin edges)
        - Interpolation in Hs and Tp dimensions
        - Workability curves with different Tp sampling than the scatter table

        :param xr.DataArray workability_result: Array of limiting Hs for each wave peak period ('Tp') and possibly direction ('WaveDirection'). We assume it is already minimized over machine limit (no `lim_type` dimension in the array).
        :param str period: Must be 'overall'.
        :return: Workability percentage [0-100].
        :rtype: float
        """
        if period != 'overall':
            raise NotImplementedError("Monthly workability requires time series; scatter table only supports 'overall'.")
        if self.scatter_data is None:
            raise ValueError("Scatter data is not loaded. Please ensure data is fetched before analysis.")
        
        if not set(workability_result.dims).issubset({'Tp', 'WaveDirection'}):
            raise ValueError("Workability result must be only dependent on 'Tp' and 'WaveDirection'. Make sure to minimize over machine limit and" \
            " to only select one condition (e.g. motion compensation or no compensation).")
        
        if 'WaveDirection' in list(workability_result.dims): # workability array not minimized over direction yet
            workability_result = workability_result.min(dim="WaveDirection")

        # Interpolate workability limits to scatter table Tp bins (upper bin edges)
        # This handles cases where workability Tp sampling differs from scatter table bins
        # Note: We use upper bin edges for a more conservative estimate since workability
        # typically decreases with increasing Tp
        
        Tp_upper = self.scatter_data.coords['Tp'].values
        # Check if workability_result Tp range covers scatter table Tp range, warn that if not extrapolation will occur
        if Tp_upper.min() < workability_result.Tp.min() or Tp_upper.max() > workability_result.Tp.max():
            print("Warning: Workability result Tp range does not fully cover scatter table Tp range. Extrapolation will be used for out-of-bounds Tp values.")
            print(f"Workability Tp range: {workability_result.Tp.min().values} to {workability_result.Tp.max().values}")
            print(f"Scatter table Tp range: {Tp_upper.min()} to {Tp_upper.max()}")
            print("Consider running the workability for a larger Tp range for more accurate results.")

        workability_at_scatter_Tp = workability_result.interp(
            Tp=Tp_upper,
            kwargs={'fill_value': 'extrapolate'}
        )
        
        # For each Tp bin in scatter table, compute cumulative probability up to limiting Hs
        workability_probability = 0
        cumsum_scatter = self.scatter_data.cumsum(dim='Hs')
        
        for i, tp_upper in enumerate(Tp_upper):
            # Get the limiting Hs at this Tp bin (upper edge - conservative)
            limiting_hs = float(workability_at_scatter_Tp[i])
            # Interpolate the cumulative probability at this Tp bin up to the limiting Hs
            workability_probability += cumsum_scatter.sel(Tp=tp_upper).interp(
                Hs=limiting_hs,
                kwargs={'fill_value': 'extrapolate'}
            )
        
        workability_percentage = float(workability_probability.values) * 100
        print(f"Overall workability percentage: {workability_percentage:.2f}%")
        return workability_percentage

class HindcastTimeSeries(HindcastBase):
    """
    Analysis class for time series format hindcast data.
    
    Expects data as pd.DataFrame with Date, Hs and Tp columns.
    
    Provides methods for:

    - Hs and Tp statistics per month
    - Workability percentage based on workability results, organized by month
    - Joint Hs-Tp wave occurrence plotting
    """
    
    def __init__(self, loader: BaseHindcastLoader, data: pd.DataFrame):
        if not isinstance(data, pd.DataFrame):
            raise TypeError(f"HindcastTimeSeries requires pd.DataFrame data, got {type(data)}.")
        # Check if 'Date', 'Hs' and 'Tp' are present
        if not {'Date', 'Hs', 'Tp'}.issubset(data.columns):
            raise ValueError("Data must have 'Date', 'Hs' and 'Tp' columns.")

        super().__init__(loader, data)
        
        # If start_date or end_date were not provided by the loader, extract from the data
        if not hasattr(self, 'start_date') or self.start_date is None:
            self.start_date = data['Date'].min().strftime('%Y-%m-%d')
        if not hasattr(self, 'end_date') or self.end_date is None:
            self.end_date = data['Date'].max().strftime('%Y-%m-%d')
        
        # self._scatter_cache: Optional[xr.DataArray] = None

    def get_Hs_stats(self, period: str = 'monthly', plot: Optional[bool] = False, ax: Optional[plt.Axes] = None):
        """Compute wave height statistics from time series data.
        For 'overall' a single row DataFrame is returned with adaptive Hs bin percentages.
        For 'monthly' rows correspond to calendar months (Jan, Feb, ...).

        :param str period: 'overall' or 'monthly'.
        :param bool plot: If True, bar (overall) or stacked bar (monthly).
        :param plt.Axes ax: Axis for plot.
        :return: Percent per Hs bin; if plot=True returns (DataFrame, Axes).
        :rtype: pd.DataFrame or (pd.DataFrame, plt.Axes)
        """
        if self.time_data is None:
            raise ValueError("Time series data not set. Please use a hindcast loader first.")
        if period not in {'overall','monthly'}:
            raise ValueError(f"Unsupported period '{period}'. Must be 'overall' or 'monthly'.")
        
        Hs_bins = np.append(np.arange(0, 5, 1), np.inf)
        # overall
        if period == 'overall':
            binned, _ = np.histogram(self.time_data['Hs'], bins=Hs_bins)
            perc = binned / binned.sum() * 100.0 if binned.sum() else binned.astype(float)
            hist_df = pd.DataFrame([perc], index=['overall'], columns=Hs_bins[1:])
            if plot:
                if ax is None:
                    fig, ax = plt.subplots(figsize=(6,4))
                labels = [f"{Hs_bins[i]:.0f}-{Hs_bins[i+1]:.0f}" for i in range(len(Hs_bins)-1)]
                ax.bar(labels, perc, edgecolor='black', alpha=0.7)
                ax.set_ylabel('Percentage [%]'); ax.set_xlabel('Hs [m]'); ax.set_title('Hs Distribution (Overall)')
                return hist_df, ax
            return hist_df
        # monthly
        hist = np.zeros((12, len(Hs_bins)-1))
        for month_num, data in self.time_data['Hs'].groupby(self.time_data['Date'].dt.month):
            binned, _ = np.histogram(data, bins=Hs_bins)
            hist[month_num-1, :] = binned / binned.sum() * 100.0 if binned.sum() else 0.0
        hist_df = pd.DataFrame(hist, columns=Hs_bins[1:]).rename(index=lambda x: calendar.month_abbr[x+1])
        hist_df = hist_df.loc[(hist_df != 0).any(axis=1)]
        if plot:
            if ax is None:
                fig, ax = plt.subplots(figsize=(10,6))
            hist_df.plot.bar(stacked=True, ax=ax)
            ax.legend([f"{Hs_bins[i]:.0f}-{Hs_bins[i+1]:.0f}" for i in range(len(Hs_bins)-1)], title='Hs')
            ax.set_title(f'Hs by month ({self.start_date} to {self.end_date})')
            ax.set_ylabel('Percentage [%]')
            return hist_df, ax
        return hist_df

    def get_Tp_stats(self, period: str = 'monthly', plot: Optional[bool] = False, ax: Optional[plt.Axes] = None):
        """Compute the wave peak period statistics from time series data.
        For 'overall' a single row DataFrame is returned with adaptive Tp bin percentages.
        For 'monthly' rows correspond to calendar months (Jan, Feb, ...).

        :param str period: 'overall' or 'monthly'.
        :param bool plot: If True, bar (overall) or stacked bar (monthly).
        :param plt.Axes ax: Axis for plot.
        :return: Percent per Tp bin; if plot=True returns (DataFrame, Axes).
        :rtype: pd.DataFrame or (pd.DataFrame, plt.Axes)
        """
        if self.time_data is None:
            raise ValueError("Time series data not set. Please use a hindcast loader first.")
        if period not in {'overall','monthly'}:
            raise ValueError(f"Unsupported period '{period}'. Must be 'overall' or 'monthly'.")
        
        Tp_bins = np.append(np.arange(0, 20, 2), np.inf)
        # overall
        if period == 'overall':
            binned, _ = np.histogram(self.time_data['Tp'], bins=Tp_bins)
            perc = binned / binned.sum() * 100.0 if binned.sum() else binned.astype(float)
            hist_df = pd.DataFrame([perc], index=['overall'], columns=Tp_bins[1:])
            if plot:
                if ax is None:
                    fig, ax = plt.subplots(figsize=(6,4))
                labels = [f"{Tp_bins[i]:.0f}-{Tp_bins[i+1]:.0f}" for i in range(len(Tp_bins)-1)]
                ax.bar(labels, perc, edgecolor='black', alpha=0.7)
                ax.set_ylabel('Percentage [%]'); ax.set_xlabel('Tp [s]'); ax.set_title('Tp Distribution (Overall)')
                return hist_df, ax
            return hist_df
        # monthly
        hist = np.zeros((12, len(Tp_bins)-1))
        for month_num, data in self.time_data['Tp'].groupby(self.time_data['Date'].dt.month):
            binned, _ = np.histogram(data, bins=Tp_bins)
            hist[month_num-1, :] = binned / binned.sum() * 100.0 if binned.sum() else 0.0
        hist_df = pd.DataFrame(hist, columns=Tp_bins[1:]).rename(index=lambda x: calendar.month_abbr[x+1])
        hist_df = hist_df.loc[(hist_df != 0).any(axis=1)]
        if plot:
            if ax is None:
                fig, ax = plt.subplots(figsize=(10,6))
            hist_df.plot.bar(stacked=True, ax=ax)
            ax.legend([f"{Tp_bins[i]:.0f}-{Tp_bins[i+1]:.0f}" for i in range(len(Tp_bins)-1)], title='Tp [s]')
            ax.set_title(f'Tp by month ({self.start_date} to {self.end_date})')
            ax.set_ylabel('Percentage [%]')
            return hist_df, ax
        return hist_df

    

    def plot_Hs_Tp(self, n_bins_hs=101, n_bins_tp=101, ax: plt.Axes = None, workability_result: xr.DataArray = None) -> plt.Axes:
        """Hs vs Tp occurrence histogram (time series).

        :param int n_bins_hs: Number of Hs bins.
        :param int n_bins_tp: Number of Tp bins.
        :param plt.Axes ax: Axis for plot (created if None).
        :param xr.DataArray workability_result: (Optional) Array of limiting Hs for each wave peak period ('Tp') and possibly direction ('WaveDirection'). Can be passed to plot the limiting Hs curve vs Tp on top of the histogram. We assume it is already minimized over machine limit (no `lim_type` dimension in the array).
        :return: Axis with plot.
        :rtype: plt.Axes
        
        """
        if self.time_data is None:
            raise ValueError("Time series data not set. Please use a hindcast loader first.")
        
        if ax is None:
            fig, ax = plt.subplots(figsize=(8, 6))

        hs_bins = np.linspace(self.time_data['Hs'].min(), self.time_data['Hs'].max(), n_bins_hs)
        tp_bins = np.linspace(self.time_data['Tp'].min(), self.time_data['Tp'].max(), n_bins_tp)

        h = ax.hist2d(self.time_data['Tp'], self.time_data['Hs'], bins=[tp_bins, hs_bins], cmap='viridis')
        plt.colorbar(h[3], ax=ax, label='Samples')
        ax.set_xlabel('Tp [s]')
        ax.set_ylabel('Hs [m]')
        ax.set_title(f'Hs vs Tp Wave Occurrence ({self.start_date} to {self.end_date})')

        if workability_result is not None:
            if not set(workability_result.dims).issubset({'Tp', 'WaveDirection'}):
                raise ValueError("Workability result must be only dependent on 'Tp' and 'WaveDirection'. Make sure to minimize over machine limit and" \
                " to only select one condition (e.g. motion compensation or no compensation).")
            if 'WaveDirection' in workability_result.dims: # workability array not minimized over direction yet
                workability_result = workability_result.min(dim="WaveDirection")
            
            ax.plot(workability_result['Tp'].values, workability_result.values, color='red', label='Workability Limit')
            ax.legend()

        return ax

    def get_workability_percentage(self, workability_result, period: str = 'monthly'):
        """Calculate workability percentages based on the workability results. 
        Basically for each hindcast time data point, we check if that wave Hs is below the limiting Hs for the given Tp.
        For 'overall' a single float percentage is returned.
        For 'monthly' a pandas Series is returned with percentage per month.

        :param workability_result: Array of limiting Hs for each wave peak period ('Tp') and possibly direction ('WaveDirection'). We assume it is already minimized over machine limit (no `lim_type` dimension in the array).
        :param str period: 'overall' returns float, 'monthly' returns Series of % per month.
        :return: Workability percentage(s).
        :rtype: float | pandas.Series
        
        """
        if self.time_data is None:
            raise ValueError("Time series data not set. Please use a hindcast loader first.")
        if period not in {'overall','monthly'}:
            raise ValueError(f"Unsupported period '{period}'. Must be 'overall' or 'monthly'.")
        
        if not set(workability_result.dims).issubset({'Tp', 'WaveDirection'}):
            raise ValueError("Workability result must be only dependent on 'Tp' and 'WaveDirection'. Make sure to minimize over machine limit and" \
            " to only select one condition (e.g. motion compensation or no compensation).")
        
        if 'WaveDirection' in workability_result.dims: # workability array not minimized over direction yet
            workability_result = workability_result.min(dim="WaveDirection")

        # Check if workability_result Tp range covers time series Tp range, warn if extrapolation will occur
        Tp_min, Tp_max = self.time_data['Tp'].min(), self.time_data['Tp'].max()
        if Tp_min < workability_result.Tp.min().values or Tp_max > workability_result.Tp.max().values:
            print("Warning: Workability result Tp range does not fully cover time series Tp range. Extrapolation will be used for out-of-bounds Tp values.")
            print(f"Workability Tp range: {workability_result.Tp.min().values} to {workability_result.Tp.max().values}")
            print(f"Time series Tp range: {Tp_min} to {Tp_max}")
            print("Consider running the workability for a larger Tp range for more accurate results.")

        workable_series = self.time_data['Hs'] < workability_result.interp(
            Tp=self.time_data['Tp'],
            kwargs={'fill_value': 'extrapolate'}
        )
        print('Overall workability percentage: {:.2f}%'.format(workable_series.mean() * 100.0))
        if period == 'overall':
            return float(workable_series.mean() * 100.0)
        monthly = workable_series.groupby(self.time_data['Date'].dt.month).mean() * 100.0
        monthly.index = monthly.index.map(lambda x: calendar.month_abbr[x])
        monthly.name = 'workability_percent'
        return monthly

# ========== Public Hindcast Factory ==========

class Hindcast:
    """
    Factory class for creating appropriate hindcast analysis objects.
    
    Automatically detects data format from HindcastLoader object and returns the appropriate analysis class:

    - Time series data (pd.DataFrame) → HindcastTimeSeries
    - Scatter table data (xr.DataArray) → HindcastScatterTable
    
    Usage:
        >>> copernicus_loader = CopernicusLoader(lat=52.0, lon=4.0, start='2024-01-01', end='2024-12-31')
        >>> hindcast = Hindcast(copernicus_loader)  # Automatically returns HindcastTimeSeries
        >>> monthly_stats = hindcast.get_Hs_stats()
        >>> monthly_workability = hindcast.get_workability_percentage(workability_result, period='monthly')

        >>> excel_loader = ExcelScatterLoader(filepath='data/scatter.xlsx', sheet_name='Hs-Tp')
        >>> hindcast = Hindcast(excel_loader)  # Automatically returns HindcastScatterTable
        >>> hs_stats = hindcast.get_Hs_stats()
    """
    
    def __new__(cls, loader: BaseHindcastLoader):
        """Fetch once and return appropriate analysis object."""
        data = loader.fetch()
        if isinstance(data, pd.DataFrame):
            return HindcastTimeSeries(loader, data)
        if isinstance(data, xr.DataArray):
            return HindcastScatterTable(loader, data)
        raise TypeError(f"Unsupported data type from loader: {type(data)}. Should be either pd.DataFrame for TimeSeries or xr.DataArray for ScatterTable.")

# ========== Example Usage ==========

# if __name__ == "__main__":
#     # # Example 1: Time series from Copernicus - simple two-step pattern
#     # from .HindcastLoader import CopernicusLoader
#     # loader = CopernicusLoader(lat=52.0, lon=4.0, start='2024-01-01', end='2024-12-31')
#     # hindcast = Hindcast(loader)  # Automatically returns HindcastTimeSeries
#     # monthly = hindcast.get_Hs_stats_monthly()
#     # workability = hindcast.get_workability_by_month(hs_limit=2.5)
#     # scatter = hindcast.to_scatter_table()
#     # scatter.plot_Hs_Tp()
    
#     # # Example 2: Scatter table from Excel - simple two-step pattern
#     # from .HindcastLoader import ExcelScatterLoader
#     # loader = ExcelScatterLoader(filepath='data/scatter.xlsx', sheet_name='Hs-Tp')
#     # hindcast = Hindcast(loader)  # Automatically returns HindcastScatterTable
#     # hs_stats = hindcast.get_Hs_stats()
#     # hindcast.plot_Hs_Tp()

#     # Example 3: DNV Weibull-based scatter table
#     from HindcastLoader import DNVLoader
#     weibull_params = {
#         'alpha_s': 3.47,
#         'beta_s': 1.57,
#         'a1': 1.272,
#         'a2': 0.114,
#         'b1': 0.0728,
#         'b2': -0.0015,
#         'a0': 0.7,
#         'b0': 0.07,
#         'gamma_s': 0.0
#     }
#     loader = DNVLoader(**weibull_params)
#     hindcast = Hindcast(loader)  # Automatically returns HindcastScatterTable
#     hindcast.plot_Hs_Tp()
#     plt.title('DNV Weibull Scatter Diagram Example')
#     plt.show()
