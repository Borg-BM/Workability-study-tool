PyBM.marine.weather_hindcast
============================

.. py:module:: PyBM.marine.weather_hindcast


Submodules
----------

.. toctree::
   :maxdepth: 1

   /autoapi/PyBM/marine/weather_hindcast/Hindcast/index
   /autoapi/PyBM/marine/weather_hindcast/HindcastLoader/index
   /autoapi/PyBM/marine/weather_hindcast/Metocean/index
   /autoapi/PyBM/marine/weather_hindcast/ScatterDiagram/index
   /autoapi/PyBM/marine/weather_hindcast/utils/index


Classes
-------

.. autoapisummary::

   PyBM.marine.weather_hindcast.Hindcast
   PyBM.marine.weather_hindcast.HindcastTimeSeries
   PyBM.marine.weather_hindcast.HindcastScatterTable
   PyBM.marine.weather_hindcast.HindcastBase
   PyBM.marine.weather_hindcast.HindcastLoader
   PyBM.marine.weather_hindcast.CopernicusLoader
   PyBM.marine.weather_hindcast.NDBCLoader
   PyBM.marine.weather_hindcast.ExcelTimeSeriesLoader
   PyBM.marine.weather_hindcast.ExcelScatterLoader
   PyBM.marine.weather_hindcast.DNVLoader


Package Contents
----------------

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



.. py:class:: HindcastLoader

   Bases: :py:obj:`abc.ABC`


   Abstract base class for all hindcast data loaders.


   .. py:method:: fetch() -> pandas.DataFrame | xarray.DataArray
      :abstractmethod:


      Fetch raw data from the source. Returns data as a pd.DataFrame (time-series) or xarray.DataArray (scatter table).



.. py:class:: CopernicusLoader(lat: float, long: float, product_id: int = 0, start_date: str = None, end_date: str = None)

   Bases: :py:obj:`HindcastLoader`


   Class to load hindcast data from Copernicus Marine API. [3], [4]

   Parameters
   ----------
   lat : float
       Latitude of the location.
   long : float
       Longitude of the location.
   product_id : int, optional
       Product ID for the Copernicus Marine dataset. If None, defaults to global wave reanalysis.
       Available options:
           - 0: Global Ocean Waves Reanalysis (https://data.marine.copernicus.eu/product/GLOBAL_MULTIYEAR_WAV_001_032/description)
           - 1: Arctic Ocean Wave Hindcast (https://data.marine.copernicus.eu/product/ARCTIC_MULTIYEAR_WAV_002_013/description)
           - 2: Baltic Sea Wave Hindcast (https://data.marine.copernicus.eu/product/BALTICSEA_MULTIYEAR_WAV_003_015/description)
           - 3: Black Sea Waves Reanalysis (https://data.marine.copernicus.eu/product/BLKSEA_MULTIYEAR_WAV_007_006/description)
           - 4: Atlantic (Iberian/Biscay/Irish) Ocean Wave Reanalysis (https://data.marine.copernicus.eu/product/IBI_MULTIYEAR_WAV_005_006/description)
           - 5: Mediterranean Sea Waves Reanalysis (https://data.marine.copernicus.eu/product/MEDSEA_MULTIYEAR_WAV_006_012/description)
           - 6: Atlantic (European North West Shelf) Wave Physics Reanalysis (https://data.marine.copernicus.eu/product/NWSHELF_REANALYSIS_WAV_004_015/description)
   start_date : str, optional
       Start date for the data in 'YYYY-MM-DD' format. Defaults to earliest available date.
   end_date : str, optional
       End date for the data in 'YYYY-MM-DD' format. Defaults to latest available date.


   .. py:attribute:: lat


   .. py:attribute:: long


   .. py:attribute:: start_date
      :value: None



   .. py:attribute:: end_date
      :value: None



   .. py:attribute:: product_id
      :value: 'cmems_mod_glo_wav_my_0.2deg_PT3H-i'



   .. py:method:: fetch() -> pandas.DataFrame

      Fetch time series data from Copernicus Marine API.



.. py:class:: NDBCLoader(lat: float = None, long: float = None, buoy_id: str = None, start_date: str = None, end_date: str = None)

   Bases: :py:obj:`HindcastLoader`


   Class to load hindcast data from NOAA NDBC buoys. [1], [2]
   Particularly suitable for North American / USA coastal regions.

   Parameters
   ----------
   lat : float, optional
       Latitude of the location. Required if buoy_id is not provided.
   long : float, optional
       Longitude of the location. Required if buoy_id is not provided.
   buoy_id : str, optional
       NDBC buoy station ID. If None, the nearest buoy to lat/long will be used.
   start_date : str, optional
       Start date in 'YYYY-MM-DD' format. Defaults to earliest available.
   end_date : str, optional
       End date in 'YYYY-MM-DD' format. Defaults to latest available.


   .. py:attribute:: lat
      :value: None



   .. py:attribute:: long
      :value: None



   .. py:attribute:: buoy_id
      :value: None



   .. py:attribute:: start_date
      :value: None



   .. py:attribute:: end_date
      :value: None



   .. py:method:: fetch() -> pandas.DataFrame

      Fetch time series data from NDBC.



.. py:class:: ExcelTimeSeriesLoader(file_path: str, date_format: str = '%m/%d/%Y %H:%M')

   Bases: :py:obj:`HindcastLoader`


   Load hindcast time series data from Excel or CSV file.

   Expected format:

   - First sheet
   - Header row with columns in order: Date, Hs, Tp
   - First 3 columns will be read

   Parameters
   ----------
   file_path : str
       Path to the Excel file (.xls, .xlsx) or CSV file (.csv).
   date_format : str, optional
       Format of the date in the first column. Default is '%m/%d/%Y %H:%M'.


   .. py:attribute:: file_path


   .. py:attribute:: date_format
      :value: '%m/%d/%Y %H:%M'



   .. py:method:: fetch() -> pandas.DataFrame

      Load time series data from Excel or CSV file.



.. py:class:: ExcelScatterLoader(file_path: str, sheet_name: str = 'Hs-Tp')

   Bases: :py:obj:`HindcastLoader`


   Load hindcast scatter table from Excel file.

   Expected format:

   - Template file format: HindcastScatterTable_template.xlsx
   - Sheet name: 'Hs-Tp' (Hs in rows, Tp in columns) or 'Tp-Hs' (Tp in rows, Hs in columns)
   - Cell A22 indicates 'relative' or 'absolute' data
   - Header row contains "Significant Wave Height" or "Peak Wave Period"

   Parameters
   ----------
   file_path : str
       Path to the Excel file formatted according to HindcastScatterTable_template.xlsx.
   sheet_name : str, optional
       Name of the sheet containing the scatter data. Either 'Hs-Tp' or 'Tp-Hs'. Defaults to 'Hs-Tp'.


   .. py:attribute:: file_path


   .. py:attribute:: sheet_name
      :value: 'Hs-Tp'



   .. py:method:: fetch() -> xarray.DataArray

      Load scatter table from Excel file and return as xarray.DataArray.



.. py:class:: DNVLoader(alpha_s: float, beta_s: float, a1: float, a2: float, b1: float, b2: float, a0: float = 0.7, b0: float = 0.07, gamma_s: float = 0, Hs_bins: numpy.ndarray = np.arange(0.5, 11.0, 0.5), Tp_bins: numpy.ndarray = np.arange(1.0, 21.0, 1.0))

   Bases: :py:obj:`HindcastLoader`


   Load hindcast scatter table from DNV long-term wave statistics using Weibull distribution.

   Generates scatter diagram (Hs-Tp) based on Weibull probability density function 
   according to DNV-RP-C205 2014-04 Formula 3.6.3.4. [5]

   Note 1: This is only valid for JONSWAP spectrum. Tp values are computed as Tp = 1.287 * Tz.

   Note 2: (Commercial) Calculating workability percentages using this loader (DNV C205) will produce 
   highly conservative results. Please use this loader as last resource.
   If this result is to be used in client communication, it may 
   only be used in combination with a comparison to a base case. For example, comparison between workability of 
   motion compensation versus non-motion compensation. 

   Parameters
   ----------
   alpha_s : float
       Weibull scale parameter for significant wave height.
   beta_s : float
       Weibull shape parameter for significant wave height.
   a1 : float
       Weibull parameter for conditional distribution of Tz given Hs.
   a2 : float
       Weibull parameter for conditional distribution of Tz given Hs.
   b1 : float
       Weibull parameter for conditional distribution of Tz given Hs.
   b2 : float
       Weibull parameter for conditional distribution of Tz given Hs.
   a0 : float, optional
       Weibull parameter for conditional distribution of Tz given Hs. Default is 0.7.
   b0 : float, optional
       Weibull parameter for conditional distribution of Tz given Hs. Default is 0.07.
   gamma_s : float, optional
       Weibull location parameter. Default is 0.
   Hs_bins : np.ndarray, optional
       Array of Hs bin upper edges. Default is 0.5 to 10.5 m in 0.5 m steps.
   Tp_bins : np.ndarray, optional
       Array of Tp bin upper edges. Default is 1 to 20 s in 1 s steps.

   References
   ----------
   DNV-RP-C205 Environmental Conditions and Environmental Loads (2014-04), Section 3.6.3.4
   Weibull parameters available in Appendix C Table C-1


   .. py:attribute:: Hs_bins


   .. py:attribute:: Tp_bins


   .. py:attribute:: alpha_s


   .. py:attribute:: beta_s


   .. py:attribute:: a1


   .. py:attribute:: a2


   .. py:attribute:: b1


   .. py:attribute:: b2


   .. py:attribute:: a0
      :value: 0.7



   .. py:attribute:: b0
      :value: 0.07



   .. py:attribute:: gamma_s
      :value: 0



   .. py:method:: fetch() -> xarray.DataArray

      Generate scatter table from Weibull distribution and return as xarray.DataArray.

      Returns scatter diagram with dims ('Hs', 'Tp') containing probability values (normalized to sum to 1).



