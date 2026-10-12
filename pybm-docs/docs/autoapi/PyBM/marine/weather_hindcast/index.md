<!-- Source: https://docs.app.barge-master.com/autoapi/PyBM/marine/weather_hindcast/index.html -->

# PyBM.marine.weather_hindcast

## Submodules

- [PyBM.marine.weather_hindcast.Hindcast](Hindcast/index.md)
- [PyBM.marine.weather_hindcast.HindcastLoader](HindcastLoader/index.md)
- [PyBM.marine.weather_hindcast.Metocean](Metocean/index.md)
- [PyBM.marine.weather_hindcast.ScatterDiagram](ScatterDiagram/index.md)
- [PyBM.marine.weather_hindcast.utils](utils/index.md)

## Classes

|                                                                                                                                     |                                                                                            |
|-------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------|
| [`Hindcast`](#PyBM.marine.weather_hindcast.Hindcast "PyBM.marine.weather_hindcast.Hindcast")                                        | Factory class for creating appropriate hindcast analysis objects.                          |
| [`HindcastTimeSeries`](#PyBM.marine.weather_hindcast.HindcastTimeSeries "PyBM.marine.weather_hindcast.HindcastTimeSeries")          | Analysis class for time series format hindcast data.                                       |
| [`HindcastScatterTable`](#PyBM.marine.weather_hindcast.HindcastScatterTable "PyBM.marine.weather_hindcast.HindcastScatterTable")    | Analysis class for scatter table format hindcast data.                                     |
| [`HindcastBase`](#PyBM.marine.weather_hindcast.HindcastBase "PyBM.marine.weather_hindcast.HindcastBase")                            | Abstract internal base with shared attributes and polymorphic abstract methods.            |
| [`HindcastLoader`](#PyBM.marine.weather_hindcast.HindcastLoader "PyBM.marine.weather_hindcast.HindcastLoader")                      | Abstract base class for all hindcast data loaders.                                         |
| [`CopernicusLoader`](#PyBM.marine.weather_hindcast.CopernicusLoader "PyBM.marine.weather_hindcast.CopernicusLoader")                | Class to load hindcast data from Copernicus Marine API. \[3\], \[4\]                       |
| [`NDBCLoader`](#PyBM.marine.weather_hindcast.NDBCLoader "PyBM.marine.weather_hindcast.NDBCLoader")                                  | Class to load hindcast data from NOAA NDBC buoys. \[1\], \[2\]                             |
| [`ExcelTimeSeriesLoader`](#PyBM.marine.weather_hindcast.ExcelTimeSeriesLoader "PyBM.marine.weather_hindcast.ExcelTimeSeriesLoader") | Load hindcast time series data from Excel or CSV file.                                     |
| [`ExcelScatterLoader`](#PyBM.marine.weather_hindcast.ExcelScatterLoader "PyBM.marine.weather_hindcast.ExcelScatterLoader")          | Load hindcast scatter table from Excel file.                                               |
| [`DNVLoader`](#PyBM.marine.weather_hindcast.DNVLoader "PyBM.marine.weather_hindcast.DNVLoader")                                     | Load hindcast scatter table from DNV long-term wave statistics using Weibull distribution. |

## Package Contents

*class *PyBM.marine.weather_hindcast.Hindcast[](../../../../../source-code/PyBM/marine/weather_hindcast/Hindcast.py)  
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

&nbsp;

*class *PyBM.marine.weather_hindcast.HindcastTimeSeries(*loader: [PyBM.marine.weather_hindcast.HindcastLoader.HindcastLoader](HindcastLoader/index.md#PyBM.marine.weather_hindcast.HindcastLoader.HindcastLoader "PyBM.marine.weather_hindcast.HindcastLoader.HindcastLoader")*, *data: pandas.DataFrame*)[](../../../../../source-code/PyBM/marine/weather_hindcast/Hindcast.py)  
Bases: [`HindcastBase`](#PyBM.marine.weather_hindcast.HindcastBase "PyBM.marine.weather_hindcast.HindcastBase")

Analysis class for time series format hindcast data.

Expects data as pd.DataFrame with Date, Hs and Tp columns.

Provides methods for:

- Hs and Tp statistics per month

- Workability percentage based on workability results, organized by month

- Joint Hs-Tp wave occurrence plotting

get_Hs_stats(*period: str = 'monthly'*, *plot: bool \| None = False*, *ax: matplotlib.pyplot.Axes \| None = None*)[](../../../../../source-code/PyBM/marine/weather_hindcast/Hindcast.py)  
Compute wave height statistics from time series data. For ‘overall’ a single row DataFrame is returned with adaptive Hs bin percentages. For ‘monthly’ rows correspond to calendar months (Jan, Feb, …).

Parameters:  
- **period** (*str*) – ‘overall’ or ‘monthly’.

- **plot** (*bool*) – If True, bar (overall) or stacked bar (monthly).

- **ax** (*plt.Axes*) – Axis for plot.

Returns:  
Percent per Hs bin; if plot=True returns (DataFrame, Axes).

Return type:  
pd.DataFrame or (pd.DataFrame, plt.Axes)

get_Tp_stats(*period: str = 'monthly'*, *plot: bool \| None = False*, *ax: matplotlib.pyplot.Axes \| None = None*)[](../../../../../source-code/PyBM/marine/weather_hindcast/Hindcast.py)  
Compute the wave peak period statistics from time series data. For ‘overall’ a single row DataFrame is returned with adaptive Tp bin percentages. For ‘monthly’ rows correspond to calendar months (Jan, Feb, …).

Parameters:  
- **period** (*str*) – ‘overall’ or ‘monthly’.

- **plot** (*bool*) – If True, bar (overall) or stacked bar (monthly).

- **ax** (*plt.Axes*) – Axis for plot.

Returns:  
Percent per Tp bin; if plot=True returns (DataFrame, Axes).

Return type:  
pd.DataFrame or (pd.DataFrame, plt.Axes)

plot_Hs_Tp(*n_bins_hs=101*, *n_bins_tp=101*, *ax: matplotlib.pyplot.Axes = None*, *workability_result: xarray.DataArray = None*) → matplotlib.pyplot.Axes[](../../../../../source-code/PyBM/marine/weather_hindcast/Hindcast.py)  
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

get_workability_percentage(*workability_result*, *period: str = 'monthly'*)[](../../../../../source-code/PyBM/marine/weather_hindcast/Hindcast.py)  
Calculate workability percentages based on the workability results. Basically for each hindcast time data point, we check if that wave Hs is below the limiting Hs for the given Tp. For ‘overall’ a single float percentage is returned. For ‘monthly’ a pandas Series is returned with percentage per month.

Parameters:  
- **workability_result** – Array of limiting Hs for each wave peak period (‘Tp’) and possibly direction (‘WaveDirection’). We assume it is already minimized over machine limit (no lim_type dimension in the array).

- **period** (*str*) – ‘overall’ returns float, ‘monthly’ returns Series of % per month.

Returns:  
Workability percentage(s).

Return type:  
float \| pandas.Series

&nbsp;

*class *PyBM.marine.weather_hindcast.HindcastScatterTable(*loader: [PyBM.marine.weather_hindcast.HindcastLoader.HindcastLoader](HindcastLoader/index.md#PyBM.marine.weather_hindcast.HindcastLoader.HindcastLoader "PyBM.marine.weather_hindcast.HindcastLoader.HindcastLoader")*, *data: xarray.DataArray*)[](../../../../../source-code/PyBM/marine/weather_hindcast/Hindcast.py)  
Bases: [`HindcastBase`](#PyBM.marine.weather_hindcast.HindcastBase "PyBM.marine.weather_hindcast.HindcastBase")

Analysis class for scatter table format hindcast data.

Expects data as xr.DataArray with dimensions for Hs and Tp bins.

Provides methods for:

- Hs and Tp statistics

- Overall workability percentage based on workability results

- Joint Hs-Tp wave occurrence plotting

get_Hs_stats(*period: str = 'overall'*, *plot: bool = False*, *ax: matplotlib.pyplot.Axes \| None = None*, *min_span: float = 1.0*, *n_bins: int = 5*)[](../../../../../source-code/PyBM/marine/weather_hindcast/Hindcast.py)  
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

get_Tp_stats(*period: str = 'overall'*, *plot: bool = False*, *ax: matplotlib.pyplot.Axes \| None = None*, *min_span: float = 2.0*, *n_bins: int = 10*)[](../../../../../source-code/PyBM/marine/weather_hindcast/Hindcast.py)  
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

plot_Hs_Tp(*ax: matplotlib.pyplot.Axes \| None = None*, *workability_result: xarray.DataArray \| None = None*) → matplotlib.pyplot.Axes[](../../../../../source-code/PyBM/marine/weather_hindcast/Hindcast.py)  
Hs vs Tp occurrence heatmap (scatter table).

Parameters:  
- **ax** (*plt.Axes*) – Axis for plot (created if None).

- **workability_result** (*xr.DataArray*) – (Optional) Array of limiting Hs for each wave peak period (‘Tp’) and possibly direction (‘WaveDirection’). Can be passed to plot the limiting Hs curve vs Tp on top of the heatmap. We assume it is already minimized over machine limit (no lim_type dimension in the array).

Returns:  
Axis with plot.

Return type:  
plt.Axes

get_workability_percentage(*workability_result*, *period: str = 'overall'*) → float[](../../../../../source-code/PyBM/marine/weather_hindcast/Hindcast.py)  
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

*class *PyBM.marine.weather_hindcast.HindcastBase(*loader: [PyBM.marine.weather_hindcast.HindcastLoader.HindcastLoader](HindcastLoader/index.md#PyBM.marine.weather_hindcast.HindcastLoader.HindcastLoader "PyBM.marine.weather_hindcast.HindcastLoader.HindcastLoader")*, *data*)[](../../../../../source-code/PyBM/marine/weather_hindcast/Hindcast.py)  
Bases: `abc.ABC`

Abstract internal base with shared attributes and polymorphic abstract methods.

The factory fetches data and passes it to the appropriate subclass, so `fetch` is not invoked twice. Subclasses set convenience attributes for easy access.

loader  

time_data*: pandas.DataFrame \| None*  

scatter_data*: xarray.DataArray \| None*  

\_\_getattr\_\_(*name*)[](../../../../../source-code/PyBM/marine/weather_hindcast/Hindcast.py)  
Delegate missing attributes to the underlying loader.

This allows access like `hindcast.lat` or `hindcast.filepath` without explicitly copying every loader attribute. If the attribute does not exist on the loader, normal AttributeError is raised.

\_\_dir\_\_()[](../../../../../source-code/PyBM/marine/weather_hindcast/Hindcast.py)  

*abstractmethod *get_Hs_stats(*period: str = 'overall'*, *\*\*kwargs*)[](../../../../../source-code/PyBM/marine/weather_hindcast/Hindcast.py)  
Return Hs statistics for given period.

Period values:

- ‘overall’ (both types)

- ‘monthly’ (time series only)

*abstractmethod *get_Tp_stats(*period: str = 'overall'*, *\*\*kwargs*)[](../../../../../source-code/PyBM/marine/weather_hindcast/Hindcast.py)  
Return Tp statistics for given period.

Period values:

- ‘overall’ (both types)

- ‘monthly’ (time series only)

*abstractmethod *plot_Hs_Tp(*ax: matplotlib.pyplot.Axes \| None = None*, *\*\*kwargs*) → matplotlib.pyplot.Axes[](../../../../../source-code/PyBM/marine/weather_hindcast/Hindcast.py)  
Polymorphic Hs–Tp visualization.

Implementations:

- Time series: hist2d scatter of individual sea states.

- Scatter table: heatmap of binned probabilities.

*abstractmethod *get_workability_percentage(*workability_result*, *period: str = 'overall'*)[](../../../../../source-code/PyBM/marine/weather_hindcast/Hindcast.py)  
Return workability percentage overall or monthly.

- ScatterTable: only ‘overall’.

- TimeSeries: ‘overall’ returns float %, ‘monthly’ returns pandas Series of % per month.

&nbsp;

*class *PyBM.marine.weather_hindcast.HindcastLoader[](../../../../../source-code/PyBM/marine/weather_hindcast/HindcastLoader.py)  
Bases: `abc.ABC`

Abstract base class for all hindcast data loaders.

*abstractmethod *fetch() → pandas.DataFrame \| xarray.DataArray[](../../../../../source-code/PyBM/marine/weather_hindcast/HindcastLoader.py)  
Fetch raw data from the source. Returns data as a pd.DataFrame (time-series) or xarray.DataArray (scatter table).

&nbsp;

*class *PyBM.marine.weather_hindcast.CopernicusLoader(*lat: float*, *long: float*, *product_id: int = 0*, *start_date: str = None*, *end_date: str = None*)[](../../../../../source-code/PyBM/marine/weather_hindcast/HindcastLoader.py)  
Bases: [`HindcastLoader`](#PyBM.marine.weather_hindcast.HindcastLoader "PyBM.marine.weather_hindcast.HindcastLoader")

Class to load hindcast data from Copernicus Marine API. \[3\], \[4\]

### Parameters

latfloat  
Latitude of the location.

longfloat  
Longitude of the location.

product_idint, optional  
Product ID for the Copernicus Marine dataset. If None, defaults to global wave reanalysis. Available options:

> - 0: Global Ocean Waves Reanalysis ([https://data.marine.copernicus.eu/product/GLOBAL_MULTIYEAR_WAV_001_032/description](https://data.marine.copernicus.eu/product/GLOBAL_MULTIYEAR_WAV_001_032/description))
>
> - 1: Arctic Ocean Wave Hindcast ([https://data.marine.copernicus.eu/product/ARCTIC_MULTIYEAR_WAV_002_013/description](https://data.marine.copernicus.eu/product/ARCTIC_MULTIYEAR_WAV_002_013/description))
>
> - 2: Baltic Sea Wave Hindcast ([https://data.marine.copernicus.eu/product/BALTICSEA_MULTIYEAR_WAV_003_015/description](https://data.marine.copernicus.eu/product/BALTICSEA_MULTIYEAR_WAV_003_015/description))
>
> - 3: Black Sea Waves Reanalysis ([https://data.marine.copernicus.eu/product/BLKSEA_MULTIYEAR_WAV_007_006/description](https://data.marine.copernicus.eu/product/BLKSEA_MULTIYEAR_WAV_007_006/description))
>
> - 4: Atlantic (Iberian/Biscay/Irish) Ocean Wave Reanalysis ([https://data.marine.copernicus.eu/product/IBI_MULTIYEAR_WAV_005_006/description](https://data.marine.copernicus.eu/product/IBI_MULTIYEAR_WAV_005_006/description))
>
> - 5: Mediterranean Sea Waves Reanalysis ([https://data.marine.copernicus.eu/product/MEDSEA_MULTIYEAR_WAV_006_012/description](https://data.marine.copernicus.eu/product/MEDSEA_MULTIYEAR_WAV_006_012/description))
>
> - 6: Atlantic (European North West Shelf) Wave Physics Reanalysis ([https://data.marine.copernicus.eu/product/NWSHELF_REANALYSIS_WAV_004_015/description](https://data.marine.copernicus.eu/product/NWSHELF_REANALYSIS_WAV_004_015/description))

start_datestr, optional  
Start date for the data in ‘YYYY-MM-DD’ format. Defaults to earliest available date.

end_datestr, optional  
End date for the data in ‘YYYY-MM-DD’ format. Defaults to latest available date.

&nbsp;

lat  

&nbsp;

long  

&nbsp;

start_date* = None*  

&nbsp;

end_date* = None*  

&nbsp;

product_id* = 'cmems_mod_glo_wav_my_0.2deg_PT3H-i'*  

&nbsp;

fetch() → pandas.DataFrame[](../../../../../source-code/PyBM/marine/weather_hindcast/HindcastLoader.py)  
Fetch time series data from Copernicus Marine API.

&nbsp;

*class *PyBM.marine.weather_hindcast.NDBCLoader(*lat: float = None*, *long: float = None*, *buoy_id: str = None*, *start_date: str = None*, *end_date: str = None*)[](../../../../../source-code/PyBM/marine/weather_hindcast/HindcastLoader.py)  
Bases: [`HindcastLoader`](#PyBM.marine.weather_hindcast.HindcastLoader "PyBM.marine.weather_hindcast.HindcastLoader")

Class to load hindcast data from NOAA NDBC buoys. \[1\], \[2\] Particularly suitable for North American / USA coastal regions.

### Parameters

latfloat, optional  
Latitude of the location. Required if buoy_id is not provided.

longfloat, optional  
Longitude of the location. Required if buoy_id is not provided.

buoy_idstr, optional  
NDBC buoy station ID. If None, the nearest buoy to lat/long will be used.

start_datestr, optional  
Start date in ‘YYYY-MM-DD’ format. Defaults to earliest available.

end_datestr, optional  
End date in ‘YYYY-MM-DD’ format. Defaults to latest available.

&nbsp;

lat* = None*  

&nbsp;

long* = None*  

&nbsp;

buoy_id* = None*  

&nbsp;

start_date* = None*  

&nbsp;

end_date* = None*  

&nbsp;

fetch() → pandas.DataFrame[](../../../../../source-code/PyBM/marine/weather_hindcast/HindcastLoader.py)  
Fetch time series data from NDBC.

&nbsp;

*class *PyBM.marine.weather_hindcast.ExcelTimeSeriesLoader(*file_path: str*, *date_format: str = '%m/%d/%Y %H:%M'*)[](../../../../../source-code/PyBM/marine/weather_hindcast/HindcastLoader.py)  
Bases: [`HindcastLoader`](#PyBM.marine.weather_hindcast.HindcastLoader "PyBM.marine.weather_hindcast.HindcastLoader")

Load hindcast time series data from Excel or CSV file.

Expected format:

- First sheet

- Header row with columns in order: Date, Hs, Tp

- First 3 columns will be read

### Parameters

file_pathstr  
Path to the Excel file (.xls, .xlsx) or CSV file (.csv).

date_formatstr, optional  
Format of the date in the first column. Default is ‘%m/%d/%Y %H:%M’.

&nbsp;

file_path  

&nbsp;

date_format* = '%m/%d/%Y %H:%M'*  

&nbsp;

fetch() → pandas.DataFrame[](../../../../../source-code/PyBM/marine/weather_hindcast/HindcastLoader.py)  
Load time series data from Excel or CSV file.

&nbsp;

*class *PyBM.marine.weather_hindcast.ExcelScatterLoader(*file_path: str*, *sheet_name: str = 'Hs-Tp'*)[](../../../../../source-code/PyBM/marine/weather_hindcast/HindcastLoader.py)  
Bases: [`HindcastLoader`](#PyBM.marine.weather_hindcast.HindcastLoader "PyBM.marine.weather_hindcast.HindcastLoader")

Load hindcast scatter table from Excel file.

Expected format:

- Template file format: HindcastScatterTable_template.xlsx

- Sheet name: ‘Hs-Tp’ (Hs in rows, Tp in columns) or ‘Tp-Hs’ (Tp in rows, Hs in columns)

- Cell A22 indicates ‘relative’ or ‘absolute’ data

- Header row contains “Significant Wave Height” or “Peak Wave Period”

### Parameters

file_pathstr  
Path to the Excel file formatted according to HindcastScatterTable_template.xlsx.

sheet_namestr, optional  
Name of the sheet containing the scatter data. Either ‘Hs-Tp’ or ‘Tp-Hs’. Defaults to ‘Hs-Tp’.

&nbsp;

file_path  

&nbsp;

sheet_name* = 'Hs-Tp'*  

&nbsp;

fetch() → xarray.DataArray[](../../../../../source-code/PyBM/marine/weather_hindcast/HindcastLoader.py)  
Load scatter table from Excel file and return as xarray.DataArray.

&nbsp;

*class *PyBM.marine.weather_hindcast.DNVLoader(*alpha_s: float*, *beta_s: float*, *a1: float*, *a2: float*, *b1: float*, *b2: float*, *a0: float = 0.7*, *b0: float = 0.07*, *gamma_s: float = 0*, *Hs_bins: numpy.ndarray = np.arange(0.5, 11.0, 0.5)*, *Tp_bins: numpy.ndarray = np.arange(1.0, 21.0, 1.0)*)[](../../../../../source-code/PyBM/marine/weather_hindcast/HindcastLoader.py)  
Bases: [`HindcastLoader`](#PyBM.marine.weather_hindcast.HindcastLoader "PyBM.marine.weather_hindcast.HindcastLoader")

Load hindcast scatter table from DNV long-term wave statistics using Weibull distribution.

Generates scatter diagram (Hs-Tp) based on Weibull probability density function according to DNV-RP-C205 2014-04 Formula 3.6.3.4. \[5\]

Note 1: This is only valid for JONSWAP spectrum. Tp values are computed as Tp = 1.287 \* Tz.

Note 2: (Commercial) Calculating workability percentages using this loader (DNV C205) will produce highly conservative results. Please use this loader as last resource. If this result is to be used in client communication, it may only be used in combination with a comparison to a base case. For example, comparison between workability of motion compensation versus non-motion compensation.

### Parameters

alpha_sfloat  
Weibull scale parameter for significant wave height.

beta_sfloat  
Weibull shape parameter for significant wave height.

a1float  
Weibull parameter for conditional distribution of Tz given Hs.

a2float  
Weibull parameter for conditional distribution of Tz given Hs.

b1float  
Weibull parameter for conditional distribution of Tz given Hs.

b2float  
Weibull parameter for conditional distribution of Tz given Hs.

a0float, optional  
Weibull parameter for conditional distribution of Tz given Hs. Default is 0.7.

b0float, optional  
Weibull parameter for conditional distribution of Tz given Hs. Default is 0.07.

gamma_sfloat, optional  
Weibull location parameter. Default is 0.

Hs_binsnp.ndarray, optional  
Array of Hs bin upper edges. Default is 0.5 to 10.5 m in 0.5 m steps.

Tp_binsnp.ndarray, optional  
Array of Tp bin upper edges. Default is 1 to 20 s in 1 s steps.

### References

DNV-RP-C205 Environmental Conditions and Environmental Loads (2014-04), Section 3.6.3.4 Weibull parameters available in Appendix C Table C-1

Hs_bins  

&nbsp;

Tp_bins  

&nbsp;

alpha_s  

&nbsp;

beta_s  

&nbsp;

a1  

&nbsp;

a2  

&nbsp;

b1  

&nbsp;

b2  

&nbsp;

a0* = 0.7*  

&nbsp;

b0* = 0.07*  

&nbsp;

gamma_s* = 0*  

&nbsp;

fetch() → xarray.DataArray[](../../../../../source-code/PyBM/marine/weather_hindcast/HindcastLoader.py)  
Generate scatter table from Weibull distribution and return as xarray.DataArray.

Returns scatter diagram with dims (‘Hs’, ‘Tp’) containing probability values (normalized to sum to 1).
