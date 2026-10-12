PyBM.marine.weather_hindcast.Hindcast
=====================================

.. py:module:: PyBM.marine.weather_hindcast.Hindcast

.. autoapi-nested-parse::

   Hindcast analysis framework with pluggable data sources.

   Architecture:

   - HindcastLoader: Abstract interface for data loaders (see ``hindcast_loaders.py``)
   - Hindcast (factory): Fetches data once and returns an analysis object
   - HindcastScatterTable: Analysis for pre-binned (Hs, Tp) scatter data (``xr.DataArray``)
   - HindcastTimeSeries: Analysis for time-series wave data (``pd.DataFrame``)



Classes
-------

.. autoapisummary::

   PyBM.marine.weather_hindcast.Hindcast.HindcastBase
   PyBM.marine.weather_hindcast.Hindcast.HindcastScatterTable
   PyBM.marine.weather_hindcast.Hindcast.HindcastTimeSeries
   PyBM.marine.weather_hindcast.Hindcast.Hindcast


Module Contents
---------------

.. py:class:: HindcastBase(loader: PyBM.marine.weather_hindcast.HindcastLoader.HindcastLoader, data)

   Bases: :py:obj:`abc.ABC`


   Abstract internal base with shared attributes and polymorphic abstract methods.

   The factory fetches data and passes it to the appropriate subclass, so ``fetch``
   is not invoked twice. Subclasses set convenience attributes for easy access.


   .. py:attribute:: loader


   .. py:attribute:: time_data
      :type:  Optional[pandas.DataFrame]


   .. py:attribute:: scatter_data
      :type:  Optional[xarray.DataArray]


   .. py:method:: __getattr__(name)

      Delegate missing attributes to the underlying loader.

      This allows access like ``hindcast.lat`` or ``hindcast.filepath`` without
      explicitly copying every loader attribute. If the attribute does not
      exist on the loader, normal AttributeError is raised.



   .. py:method:: __dir__()


   .. py:method:: get_Hs_stats(period: str = 'overall', **kwargs)
      :abstractmethod:


      Return Hs statistics for given period.

      Period values:

      - 'overall' (both types)
      - 'monthly' (time series only)



   .. py:method:: get_Tp_stats(period: str = 'overall', **kwargs)
      :abstractmethod:


      Return Tp statistics for given period.

      Period values:

      - 'overall' (both types)
      - 'monthly' (time series only)



   .. py:method:: plot_Hs_Tp(ax: Optional[matplotlib.pyplot.Axes] = None, **kwargs) -> matplotlib.pyplot.Axes
      :abstractmethod:


      Polymorphic Hs–Tp visualization.

      Implementations:

      - Time series: hist2d scatter of individual sea states.
      - Scatter table: heatmap of binned probabilities.



   .. py:method:: get_workability_percentage(workability_result, period: str = 'overall')
      :abstractmethod:


      Return workability percentage overall or monthly.

      - ScatterTable: only 'overall'.
      - TimeSeries: 'overall' returns float %, 'monthly' returns pandas Series of % per month.



.. py:class:: HindcastScatterTable(loader: PyBM.marine.weather_hindcast.HindcastLoader.HindcastLoader, data: xarray.DataArray)

   Bases: :py:obj:`HindcastBase`


   Analysis class for scatter table format hindcast data.

   Expects data as xr.DataArray with dimensions for Hs and Tp bins.

   Provides methods for:

   - Hs and Tp statistics
   - Overall workability percentage based on workability results
   - Joint Hs-Tp wave occurrence plotting


   .. py:method:: get_Hs_stats(period: str = 'overall', plot: bool = False, ax: Optional[matplotlib.pyplot.Axes] = None, min_span: float = 1.0, n_bins: int = 5)

      Compute wave height statistics from scatter data. Gives the percentage of waves in each Hs bin.
      The statistic bins are adaptive based on the scatter data bins.

      :param str period: Must be 'overall'.
      :param bool plot: If True plot bar chart.
      :param plt.Axes ax: Axis for plot (created if None).
      :param float min_span: Minimum bin width. For example, default of 1.0 means Hs bins of at least 1 meter width.
      :param int n_bins: Maximum number of output bins.
      :return: Row 'overall' with Hs bin fractions. If plot=True returns (DataFrame, Axes).
      :rtype: pd.DataFrame or (pd.DataFrame, plt.Axes)



   .. py:method:: get_Tp_stats(period: str = 'overall', plot: bool = False, ax: Optional[matplotlib.pyplot.Axes] = None, min_span: float = 2.0, n_bins: int = 10)

      Compute the wave peak period statistics from scatter data. Gives the percentage of waves in each Tp bin.
      The statistic bins are adaptive based on the scatter data bins.

      :param str period: Must be 'overall'.
      :param bool plot: If True plot bar chart.
      :param plt.Axes ax: Axis for plot (created if None).
      :param float min_span: Minimum bin width. For example, default of 2.0 means Tp bins of at least 2 seconds width.
      :param int n_bins: Maximum number of output bins.
      :return: Row 'overall' with adaptive Tp bin fractions (counts). If plot=True returns (DataFrame, Axes).
      :rtype: pd.DataFrame or (pd.DataFrame, plt.Axes)



   .. py:method:: plot_Hs_Tp(ax: Optional[matplotlib.pyplot.Axes] = None, workability_result: Optional[xarray.DataArray] = None) -> matplotlib.pyplot.Axes

      Hs vs Tp occurrence heatmap (scatter table).

      :param plt.Axes ax: Axis for plot (created if None).
      :param xr.DataArray workability_result: (Optional) Array of limiting Hs for each wave peak period ('Tp') and possibly direction ('WaveDirection'). Can be passed to plot the limiting Hs curve vs Tp on top of the heatmap. We assume it is already minimized over machine limit (no `lim_type` dimension in the array).
      :return: Axis with plot.
      :rtype: plt.Axes



   .. py:method:: get_workability_percentage(workability_result, period: str = 'overall') -> float

      Calculate overall workability percentage based on the workability results.

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



.. py:class:: HindcastTimeSeries(loader: PyBM.marine.weather_hindcast.HindcastLoader.HindcastLoader, data: pandas.DataFrame)

   Bases: :py:obj:`HindcastBase`


   Analysis class for time series format hindcast data.

   Expects data as pd.DataFrame with Date, Hs and Tp columns.

   Provides methods for:

   - Hs and Tp statistics per month
   - Workability percentage based on workability results, organized by month
   - Joint Hs-Tp wave occurrence plotting


   .. py:method:: get_Hs_stats(period: str = 'monthly', plot: Optional[bool] = False, ax: Optional[matplotlib.pyplot.Axes] = None)

      Compute wave height statistics from time series data.
      For 'overall' a single row DataFrame is returned with adaptive Hs bin percentages.
      For 'monthly' rows correspond to calendar months (Jan, Feb, ...).

      :param str period: 'overall' or 'monthly'.
      :param bool plot: If True, bar (overall) or stacked bar (monthly).
      :param plt.Axes ax: Axis for plot.
      :return: Percent per Hs bin; if plot=True returns (DataFrame, Axes).
      :rtype: pd.DataFrame or (pd.DataFrame, plt.Axes)



   .. py:method:: get_Tp_stats(period: str = 'monthly', plot: Optional[bool] = False, ax: Optional[matplotlib.pyplot.Axes] = None)

      Compute the wave peak period statistics from time series data.
      For 'overall' a single row DataFrame is returned with adaptive Tp bin percentages.
      For 'monthly' rows correspond to calendar months (Jan, Feb, ...).

      :param str period: 'overall' or 'monthly'.
      :param bool plot: If True, bar (overall) or stacked bar (monthly).
      :param plt.Axes ax: Axis for plot.
      :return: Percent per Tp bin; if plot=True returns (DataFrame, Axes).
      :rtype: pd.DataFrame or (pd.DataFrame, plt.Axes)



   .. py:method:: plot_Hs_Tp(n_bins_hs=101, n_bins_tp=101, ax: matplotlib.pyplot.Axes = None, workability_result: xarray.DataArray = None) -> matplotlib.pyplot.Axes

      Hs vs Tp occurrence histogram (time series).

      :param int n_bins_hs: Number of Hs bins.
      :param int n_bins_tp: Number of Tp bins.
      :param plt.Axes ax: Axis for plot (created if None).
      :param xr.DataArray workability_result: (Optional) Array of limiting Hs for each wave peak period ('Tp') and possibly direction ('WaveDirection'). Can be passed to plot the limiting Hs curve vs Tp on top of the histogram. We assume it is already minimized over machine limit (no `lim_type` dimension in the array).
      :return: Axis with plot.
      :rtype: plt.Axes




   .. py:method:: get_workability_percentage(workability_result, period: str = 'monthly')

      Calculate workability percentages based on the workability results. 
      Basically for each hindcast time data point, we check if that wave Hs is below the limiting Hs for the given Tp.
      For 'overall' a single float percentage is returned.
      For 'monthly' a pandas Series is returned with percentage per month.

      :param workability_result: Array of limiting Hs for each wave peak period ('Tp') and possibly direction ('WaveDirection'). We assume it is already minimized over machine limit (no `lim_type` dimension in the array).
      :param str period: 'overall' returns float, 'monthly' returns Series of % per month.
      :return: Workability percentage(s).
      :rtype: float | pandas.Series




.. py:class:: Hindcast

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


