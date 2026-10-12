PyBM.marine.weather_hindcast.HindcastLoader
===========================================

.. py:module:: PyBM.marine.weather_hindcast.HindcastLoader

.. autoapi-nested-parse::

   Hindcast data loaders for various sources.

   Provides loader classes for fetching hindcast data from:

   - Copernicus Marine Service
   - NOAA NDBC buoys
   - DNV Long-term wave stats
   - Excel files (scatter table and time series formats)

   References:
       - [1] NDBC API Documentation: https://pypi.org/project/ndbc-api/
       - [2] NDBC Stations page: https://www.ndbc.noaa.gov/
       - [3] Copernicus Marine Wave Data Store: https://data.marine.copernicus.eu/products?facets=mainVariables%7EWave--tempResolutions%7EHourly
       - [4] Copernicus Marine Toolbox API Help Center: https://help.marine.copernicus.eu/en/collections/9080063-copernicus-marine-toolbox
       - [5] DNV-RP-C205 Environmental Conditions and Environmental Loads



Classes
-------

.. autoapisummary::

   PyBM.marine.weather_hindcast.HindcastLoader.HindcastLoader
   PyBM.marine.weather_hindcast.HindcastLoader.CopernicusLoader
   PyBM.marine.weather_hindcast.HindcastLoader.NDBCLoader
   PyBM.marine.weather_hindcast.HindcastLoader.ExcelTimeSeriesLoader
   PyBM.marine.weather_hindcast.HindcastLoader.ExcelScatterLoader
   PyBM.marine.weather_hindcast.HindcastLoader.DNVLoader


Module Contents
---------------

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



