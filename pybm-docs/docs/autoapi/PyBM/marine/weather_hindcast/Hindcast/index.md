<!-- Source: https://docs.app.barge-master.com/autoapi/PyBM/marine/weather_hindcast/Hindcast/index.html -->

# PyBM.marine.weather_hindcast.Hindcast

Hindcast analysis framework with pluggable data sources.

Architecture:

- HindcastLoader: Abstract interface for data loaders (see `hindcast_loaders.py`)

- Hindcast (factory): Fetches data once and returns an analysis object

- HindcastScatterTable: Analysis for pre-binned (Hs, Tp) scatter data (`xr.DataArray`)

- HindcastTimeSeries: Analysis for time-series wave data (`pd.DataFrame`)

## Classes

|                                                                                                                                                    |                                                                                 |
|----------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------|
| [`HindcastBase`](#PyBM.marine.weather_hindcast.Hindcast.HindcastBase "PyBM.marine.weather_hindcast.Hindcast.HindcastBase")                         | Abstract internal base with shared attributes and polymorphic abstract methods. |
| [`HindcastScatterTable`](#PyBM.marine.weather_hindcast.Hindcast.HindcastScatterTable "PyBM.marine.weather_hindcast.Hindcast.HindcastScatterTable") | Analysis class for scatter table format hindcast data.                          |
| [`HindcastTimeSeries`](#PyBM.marine.weather_hindcast.Hindcast.HindcastTimeSeries "PyBM.marine.weather_hindcast.Hindcast.HindcastTimeSeries")       | Analysis class for time series format hindcast data.                            |
| [`Hindcast`](#PyBM.marine.weather_hindcast.Hindcast.Hindcast "PyBM.marine.weather_hindcast.Hindcast.Hindcast")                                     | Factory class for creating appropriate hindcast analysis objects.               |

## Module Contents

*class *PyBM.marine.weather_hindcast.Hindcast.HindcastBase(*loader: [PyBM.marine.weather_hindcast.HindcastLoader.HindcastLoader](../HindcastLoader/index.md#PyBM.marine.weather_hindcast.HindcastLoader.HindcastLoader "PyBM.marine.weather_hindcast.HindcastLoader.HindcastLoader")*, *data*)[](../../../../../../source-code/PyBM/marine/weather_hindcast/Hindcast.py)  
Bases: `abc.ABC`

Abstract internal base with shared attributes and polymorphic abstract methods.

The factory fetches data and passes it to the appropriate subclass, so `fetch` is not invoked twice. Subclasses set convenience attributes for easy access.

loader[](../../../../../../source-code/PyBM/marine/weather_hindcast/Hindcast.py)  

time_data*: pandas.DataFrame \| None*[](../../../../../../source-code/PyBM/marine/weather_hindcast/Hindcast.py)  

scatter_data*: xarray.DataArray \| None*[](../../../../../../source-code/PyBM/marine/weather_hindcast/Hindcast.py)  

\_\_getattr\_\_(*name*)[](../../../../../../source-code/PyBM/marine/weather_hindcast/Hindcast.py)  
Delegate missing attributes to the underlying loader.

This allows access like `hindcast.lat` or `hindcast.filepath` without explicitly copying every loader attribute. If the attribute does not exist on the loader, normal AttributeError is raised.

\_\_dir\_\_()[](../../../../../../source-code/PyBM/marine/weather_hindcast/Hindcast.py)  

*abstractmethod *get_Hs_stats(*period: str = 'overall'*, *\*\*kwargs*)[](../../../../../../source-code/PyBM/marine/weather_hindcast/Hindcast.py)  
Return Hs statistics for given period.

Period values:

- ‘overall’ (both types)

- ‘monthly’ (time series only)

*abstractmethod *get_Tp_stats(*period: str = 'overall'*, *\*\*kwargs*)[](../../../../../../source-code/PyBM/marine/weather_hindcast/Hindcast.py)  
Return Tp statistics for given period.

Period values:

- ‘overall’ (both types)

- ‘monthly’ (time series only)

*abstractmethod *plot_Hs_Tp(*ax: matplotlib.pyplot.Axes \| None = None*, *\*\*kwargs*) → matplotlib.pyplot.Axes[](../../../../../../source-code/PyBM/marine/weather_hindcast/Hindcast.py)  
Polymorphic Hs–Tp visualization.

Implementations:

- Time series: hist2d scatter of individual sea states.

- Scatter table: heatmap of binned probabilities.

*abstractmethod *get_workability_percentage(*workability_result*, *period: str = 'overall'*)[](../../../../../../source-code/PyBM/marine/weather_hindcast/Hindcast.py)  
Return workability percentage overall or monthly.

- ScatterTable: only ‘overall’.

- TimeSeries: ‘overall’ returns float %, ‘monthly’ returns pandas Series of % per month.

&nbsp;

*class *PyBM.marine.weather_hindcast.Hindcast.HindcastScatterTable(*loader: [PyBM.marine.weather_hindcast.HindcastLoader.HindcastLoader](../HindcastLoader/index.md#PyBM.marine.weather_hindcast.HindcastLoader.HindcastLoader "PyBM.marine.weather_hindcast.HindcastLoader.HindcastLoader")*, *data: xarray.DataArray*)[](../../../../../../source-code/PyBM/marine/weather_hindcast/Hindcast.py)  
Bases: [`HindcastBase`](#PyBM.marine.weather_hindcast.Hindcast.HindcastBase "PyBM.marine.weather_hindcast.Hindcast.HindcastBase")

Analysis class for scatter table format hindcast data.

Expects data as xr.DataArray with dimensions for Hs and Tp bins.

Provides methods for:

- Hs and Tp statistics

- Overall workability percentage based on workability results

- Joint Hs-Tp wave occurrence plotting

get_Hs_stats(*period: str = 'overall'*, *plot: bool = False*, *ax: matplotlib.pyplot.Axes \| None = None*, *min_span: float = 1.0*, *n_bins: int = 5*)[](../../../../../../source-code/PyBM/marine/weather_hindcast/Hindcast.py)  
Compute wave height statistics from scatter data. Gives the percentage of waves in each Hs bin. The statistic bins are adaptive based on the scatter data bins.

Parameters:  
- **period** (*str*) – Must be ‘overall’.

- **plot** (*bool*) – If True plot bar chart.

- **ax** (*plt.Axes*) – Axis for plot (created if None).

- **min_span** (*float*) – Minimum bin width. For example, default of 1.0 means Hs bins of at least 1 meter width.

- **n_bins** (*int*) – Maximum number of output bins.

Returns:  
Row ‘overall’ with Hs bin fractions. If plot=True returns (DataFrame, Axes).

Return type:  
pd.DataFrame or (pd.DataFrame, plt.Axes)

get_Tp_stats(*period: str = 'overall'*, *plot: bool = False*, *ax: matplotlib.pyplot.Axes \| None = None*, *min_span: float = 2.0*, *n_bins: int = 10*)[](../../../../../../source-code/PyBM/marine/weather_hindcast/Hindcast.py)  
Compute the wave peak period statistics from scatter data. Gives the percentage of waves in each Tp bin. The statistic bins are adaptive based on the scatter data bins.

Parameters:  
- **period** (*str*) – Must be ‘overall’.

- **plot** (*bool*) – If True plot bar chart.

- **ax** (*plt.Axes*) – Axis for plot (created if None).

- **min_span** (*float*) – Minimum bin width. For example, default of 2.0 means Tp bins of at least 2 seconds width.

- **n_bins** (*int*) – Maximum number of output bins.

Returns:  
Row ‘overall’ with adaptive Tp bin fractions (counts). If plot=True returns (DataFrame, Axes).

Return type:  
pd.DataFrame or (pd.DataFrame, plt.Axes)

plot_Hs_Tp(*ax: matplotlib.pyplot.Axes \| None = None*, *workability_result: xarray.DataArray \| None = None*) → matplotlib.pyplot.Axes[](../../../../../../source-code/PyBM/marine/weather_hindcast/Hindcast.py)  
Hs vs Tp occurrence heatmap (scatter table).

Parameters:  
- **ax** (*plt.Axes*) – Axis for plot (created if None).

- **workability_result** (*xr.DataArray*) – (Optional) Array of limiting Hs for each wave peak period (‘Tp’) and possibly direction (‘WaveDirection’). Can be passed to plot the limiting Hs curve vs Tp on top of the heatmap. We assume it is already minimized over machine limit (no lim_type dimension in the array).

Returns:  
Axis with plot.

Return type:  
plt.Axes

get_workability_percentage(*workability_result*, *period: str = 'overall'*) → float[](../../../../../../source-code/PyBM/marine/weather_hindcast/Hindcast.py)  
Calculate overall workability percentage based on the workability results.

For each Tp bin in the scatter table, interpolates the limiting Hs from the workability curve, then computes the cumulative probability up to that Hs limit by interpolating over the Hs bins.

The method properly handles:

- Binned scatter data (where coords represent upper bin edges)

- Interpolation in Hs and Tp dimensions

- Workability curves with different Tp sampling than the scatter table

Parameters:  
- **workability_result** (*xr.DataArray*) – Array of limiting Hs for each wave peak period (‘Tp’) and possibly direction (‘WaveDirection’). We assume it is already minimized over machine limit (no lim_type dimension in the array).

- **period** (*str*) – Must be ‘overall’.

Returns:  
Workability percentage \[0-100\].

Return type:  
float

&nbsp;

*class *PyBM.marine.weather_hindcast.Hindcast.HindcastTimeSeries(*loader: [PyBM.marine.weather_hindcast.HindcastLoader.HindcastLoader](../HindcastLoader/index.md#PyBM.marine.weather_hindcast.HindcastLoader.HindcastLoader "PyBM.marine.weather_hindcast.HindcastLoader.HindcastLoader")*, *data: pandas.DataFrame*)[](../../../../../../source-code/PyBM/marine/weather_hindcast/Hindcast.py)  
Bases: [`HindcastBase`](#PyBM.marine.weather_hindcast.Hindcast.HindcastBase "PyBM.marine.weather_hindcast.Hindcast.HindcastBase")

Analysis class for time series format hindcast data.

Expects data as pd.DataFrame with Date, Hs and Tp columns.

Provides methods for:

- Hs and Tp statistics per month

- Workability percentage based on workability results, organized by month

- Joint Hs-Tp wave occurrence plotting

get_Hs_stats(*period: str = 'monthly'*, *plot: bool \| None = False*, *ax: matplotlib.pyplot.Axes \| None = None*)[](../../../../../../source-code/PyBM/marine/weather_hindcast/Hindcast.py)  
Compute wave height statistics from time series data. For ‘overall’ a single row DataFrame is returned with adaptive Hs bin percentages. For ‘monthly’ rows correspond to calendar months (Jan, Feb, …).

Parameters:  
- **period** (*str*) – ‘overall’ or ‘monthly’.

- **plot** (*bool*) – If True, bar (overall) or stacked bar (monthly).

- **ax** (*plt.Axes*) – Axis for plot.

Returns:  
Percent per Hs bin; if plot=True returns (DataFrame, Axes).

Return type:  
pd.DataFrame or (pd.DataFrame, plt.Axes)

get_Tp_stats(*period: str = 'monthly'*, *plot: bool \| None = False*, *ax: matplotlib.pyplot.Axes \| None = None*)[](../../../../../../source-code/PyBM/marine/weather_hindcast/Hindcast.py)  
Compute the wave peak period statistics from time series data. For ‘overall’ a single row DataFrame is returned with adaptive Tp bin percentages. For ‘monthly’ rows correspond to calendar months (Jan, Feb, …).

Parameters:  
- **period** (*str*) – ‘overall’ or ‘monthly’.

- **plot** (*bool*) – If True, bar (overall) or stacked bar (monthly).

- **ax** (*plt.Axes*) – Axis for plot.

Returns:  
Percent per Tp bin; if plot=True returns (DataFrame, Axes).

Return type:  
pd.DataFrame or (pd.DataFrame, plt.Axes)

plot_Hs_Tp(*n_bins_hs=101*, *n_bins_tp=101*, *ax: matplotlib.pyplot.Axes = None*, *workability_result: xarray.DataArray = None*) → matplotlib.pyplot.Axes[](../../../../../../source-code/PyBM/marine/weather_hindcast/Hindcast.py)  
Hs vs Tp occurrence histogram (time series).

Parameters:  
- **n_bins_hs** (*int*) – Number of Hs bins.

- **n_bins_tp** (*int*) – Number of Tp bins.

- **ax** (*plt.Axes*) – Axis for plot (created if None).

- **workability_result** (*xr.DataArray*) – (Optional) Array of limiting Hs for each wave peak period (‘Tp’) and possibly direction (‘WaveDirection’). Can be passed to plot the limiting Hs curve vs Tp on top of the histogram. We assume it is already minimized over machine limit (no lim_type dimension in the array).

Returns:  
Axis with plot.

Return type:  
plt.Axes

get_workability_percentage(*workability_result*, *period: str = 'monthly'*)[](../../../../../../source-code/PyBM/marine/weather_hindcast/Hindcast.py)  
Calculate workability percentages based on the workability results. Basically for each hindcast time data point, we check if that wave Hs is below the limiting Hs for the given Tp. For ‘overall’ a single float percentage is returned. For ‘monthly’ a pandas Series is returned with percentage per month.

Parameters:  
- **workability_result** – Array of limiting Hs for each wave peak period (‘Tp’) and possibly direction (‘WaveDirection’). We assume it is already minimized over machine limit (no lim_type dimension in the array).

- **period** (*str*) – ‘overall’ returns float, ‘monthly’ returns Series of % per month.

Returns:  
Workability percentage(s).

Return type:  
float \| pandas.Series

&nbsp;

*class *PyBM.marine.weather_hindcast.Hindcast.Hindcast[](../../../../../../source-code/PyBM/marine/weather_hindcast/Hindcast.py)  
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
