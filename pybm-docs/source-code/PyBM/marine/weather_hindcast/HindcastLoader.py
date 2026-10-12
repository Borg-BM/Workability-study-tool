"""
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
"""

from abc import ABC, abstractmethod
import datetime
import pandas as pd
import numpy as np
import xarray as xr
from pathlib import Path
from .utils import from_weibull

class HindcastLoader(ABC):
    """Abstract base class for all hindcast data loaders."""
    
    @abstractmethod

    def fetch(self) -> pd.DataFrame | xr.DataArray:
        """
        Fetch raw data from the source. Returns data as a pd.DataFrame (time-series) or xarray.DataArray (scatter table).
        """
        pass

class CopernicusLoader(HindcastLoader):
    """
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
    """
    
    def __init__(self, lat: float, long: float, product_id: int = 0, start_date: str = None, end_date: str = None):
        # Validate if lat and long are floats
        if not isinstance(lat, float):
            raise ValueError("lat must be a float")
        if not isinstance(long, float):
            raise ValueError("long must be a float")

        # Validate date format
        if start_date:
            try:
                datetime.datetime.strptime(start_date, '%Y-%m-%d')
            except ValueError:
                raise ValueError("start_date must be in the format 'YYYY-MM-DD'")
        if end_date:
            try:
                datetime.datetime.strptime(end_date, '%Y-%m-%d')
            except ValueError:
                raise ValueError("end_date must be in the format 'YYYY-MM-DD'")

        product_id_dict = {
            0: 'cmems_mod_glo_wav_my_0.2deg_PT3H-i', # Global Ocean Waves Reanalysis
            1: 'cmems_mod_arc_wav_my_3km_PT1H-i', # Arctic Ocean Wave Hindcast
            2: 'cmems_mod_bal_wav_my_PT1H-i', # Baltic Sea Wave Hindcast
            3: 'cmems_mod_blk_wav_my_2.5km_PT1H-i', # Black Sea Waves Reanalysis
            4: 'cmems_mod_ibi_wav_my_0.027deg_PT1H-i', # Atlantic -Iberian Biscay Irish- Ocean Wave Reanalysis
            5: 'med-hcmr-wav-rean-h', # Mediterranean Sea Waves Reanalysis
            6: 'MetO-NWS-WAV-RAN', # Atlantic- European North West Shelf- Wave Physics Reanalysis
        }

        if product_id not in product_id_dict.keys():
            raise ValueError(f"Invalid product_id. Must be one of {list(product_id_dict.keys())}")
        

        self.lat = lat

        self.long = long

        self.start_date = start_date

        self.end_date = end_date

        self.product_id = product_id_dict[product_id]

    

    def fetch(self) -> pd.DataFrame:
        """Fetch time series data from Copernicus Marine API."""
        import copernicusmarine
        # Login to Copernicus Marine API
        copernicusmarine.login(username="operations@barge-master.com", password="<REDACTED>", force_overwrite=True)
        
        # Fetch data
        df = copernicusmarine.read_dataframe(
            dataset_id=self.product_id,
            variables=["VHM0", "VTPK"],  # VHM0 = significant wave height, VTPK = peak wave period
            minimum_longitude=self.long,
            maximum_longitude=self.long,
            minimum_latitude=self.lat,
            maximum_latitude=self.lat,
            start_datetime=self.start_date,
            end_datetime=self.end_date,
        )
        
        if df is None or df.empty:
            raise ValueError("No data retrieved from the Copernicus API.")
        
        # Clean and standardize columns
        df = df.reset_index()
        df = df.drop(columns=["longitude", "latitude"])
        df.columns = ["Date", "Hs", "Tp"]
        df = df.dropna()
        
        if df.empty:
            raise ValueError("No valid data after removing NaN values.")
        
        return df

class NDBCLoader(HindcastLoader):
    """
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
    """
    
    def __init__(self, lat: float = None, long: float = None, buoy_id: str = None, start_date: str = None, end_date: str = None):
        # Validation: must provide either (lat, long) or buoy_id
        if lat is not None and long is not None:
            if buoy_id is not None:
                raise ValueError("Please provide either 'lat' and 'long', or 'buoy_id', not both.")
        elif buoy_id is None:
            raise ValueError("Either 'buoy_id' or both 'lat' and 'long' must be provided.")
        
        # Validate date format
        if start_date:
            try:
                datetime.datetime.strptime(start_date, '%Y-%m-%d')
            except ValueError:
                raise ValueError("start_date must be in the format 'YYYY-MM-DD'")
        if end_date:
            try:
                datetime.datetime.strptime(end_date, '%Y-%m-%d')
            except ValueError:
                raise ValueError("end_date must be in the format 'YYYY-MM-DD'")
        

        self.lat = lat

        self.long = long

        self.buoy_id = buoy_id

        self.start_date = start_date

        self.end_date = end_date

    

    def fetch(self) -> pd.DataFrame:
        """Fetch time series data from NDBC."""
        from ndbc_api import NdbcApi
        from geopy.distance import geodesic
        import re
        
        api = NdbcApi()
        
        # Determine buoy_id if not provided
        if self.buoy_id is None:
            print('Please check if lat and long are not mixed up:')
            print(f'- Latitude: {self.lat}')
            print(f'- Longitude: {self.long}')
            self.buoy_id = api.nearest_station(self.lat, self.long)
            
            # Get the location of the buoy in decimal degrees
            buoy_location_str = api.station(station_id=self.buoy_id, as_df=True).loc['Location', 0]
            decimal_deg_exp = re.search(r'([\d.]+)\s*([NS])\s+([\d.]+)\s*([EW])', buoy_location_str)
            buoy_lat = float(decimal_deg_exp.group(1))
            if decimal_deg_exp.group(2) == 'S':
                buoy_lat = -buoy_lat
            buoy_long = float(decimal_deg_exp.group(3))
            if decimal_deg_exp.group(4) == 'W':
                buoy_long = -buoy_long
            
            # Find distance to the nearest buoy
            distance_km = geodesic((self.lat, self.long), (buoy_lat, buoy_long)).kilometers
            print(f'Distance to nearest buoy: {distance_km:.2f} km')
            print('(Inaccuracy expected if distance > 30 km)')
        
        # Get available historical data
        buoy_historical_years = api.available_historical(station_id=self.buoy_id)
        if 'Standard meteorological data' not in list(buoy_historical_years.keys()):
            raise ValueError("No historical data available for the specified buoy. If you were expecting data, check if buoy_id or lat/long are correct.")
        
        # Determine start and end dates if not provided
        if self.start_date is None:
            start_year = min(
                int(datetime.datetime.strptime(year, "%b %Y").year) if not year.isdigit() else int(year)
                for year in buoy_historical_years['Standard meteorological data'].keys()
            )
            self.start_date = f"{start_year}-01-01"
        if self.end_date is None:
            self.end_date = datetime.datetime.today().strftime('%Y-%m-%d')
        
        # Fetch data from API
        df = api.get_data(station_id=self.buoy_id, mode='stdmet', start_time=self.start_date, end_time=self.end_date, as_df=True)
        
        if isinstance(df, dict):
            if df == {}:  # empty dict
                raise ValueError("No data retrieved from the API.")
        else:
            if df is None or df.empty:
                raise ValueError("No data retrieved from the API.")
        
        # Subset columns:
        # WVHT: wave height
        # DPD: dominant wave period (peak period)
        df = df[['WVHT', 'DPD']]
        
        df = df.reset_index().drop(columns="station_id")
        df.columns = ["Date", "Hs", "Tp"]  # rename to standard names
        df = df.dropna(subset=["Hs", "Tp"])  # remove nan entries
        
        if df is None or df.empty:
            raise ValueError("No data exists for the specified time period.")
        
        df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d %H:%M:%S')
        
        return df

    

class ExcelTimeSeriesLoader(HindcastLoader):
    """
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
    """
    
    def __init__(self, file_path: str, date_format: str = '%m/%d/%Y %H:%M'):
        
        # Validate file exists
        if not Path(file_path).is_file():
            raise ValueError(f"File {file_path} does not exist.")
        
        # Validate file type
        if not file_path.endswith((".xls", ".xlsx", ".csv")):
            raise ValueError("Unsupported file type: must be .csv, .xls, or .xlsx")
        

        self.file_path = file_path

        self.date_format = date_format

    

    def fetch(self) -> pd.DataFrame:
        """Load time series data from Excel or CSV file."""
        
        # Read file based on extension
        if self.file_path.endswith((".xls", ".xlsx")):
            df = pd.read_excel(
                self.file_path, 
                sheet_name=0, 
                usecols=[i for i in range(3)],  # read only first 3 columns
                parse_dates=[0], 
                date_format=self.date_format
            )
        elif self.file_path.endswith(".csv"):
            df = pd.read_csv(
                self.file_path, 
                usecols=[i for i in range(3)], 
                parse_dates=[0], 
                date_format=self.date_format
            )
        
        df.columns = ['Date', 'Hs', 'Tp']
        df = df.dropna()
        if df.empty:
            raise ValueError("No valid data after removing NaN values.")
        
        # Sanity check print
        print("\n[Sanity check] Preview of the loaded data:")
        print(df.head(5).to_string(index=False))
        print(f"\nDetected columns: {list(df.columns)}\n")
        
        # Attempt datetime parsing
        try:
            df.iloc[:, 0] = pd.to_datetime(df.iloc[:, 0], errors='raise', format=self.date_format)
        except Exception as e:
            raise ValueError(f"First column could not be parsed as datetime: {e}")
        
        return df

class ExcelScatterLoader(HindcastLoader):
    """
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
    """
    
    def __init__(self, file_path: str, sheet_name: str = 'Hs-Tp'):
        
        # Validate if file exists
        if not Path(file_path).is_file():
            raise ValueError(f"File {file_path} does not exist.")
        
        # Validate sheet name
        if sheet_name.lower() not in ['hs-tp', 'tp-hs']:
            raise ValueError(f"sheet_name must be 'Hs-Tp' or 'Tp-Hs', got '{sheet_name}'")
        

        self.file_path = file_path

        self.sheet_name = sheet_name

    

    def fetch(self) -> xr.DataArray:
        """Load scatter table from Excel file and return as xarray.DataArray."""
        
        # Load entire sheet without header
        df_all = pd.read_excel(self.file_path, sheet_name=self.sheet_name, header=None)
        
        # Determine if data is relative or absolute (cell A22 → row 21, col 0)
        try:
            relative_flag = str(df_all.iloc[21, 0]).strip().lower()
            is_relative = "relative" in relative_flag
        except Exception:
            is_relative = False
        
        # Detect table configuration based on sheet type
        if self.sheet_name.lower() == 'hs-tp':
            header_keyword = "Significant Wave Height"
            data_dim_primary = 'Hs'   # y dimension (rows)
            data_dim_secondary = 'Tp'  # x dimension (columns)
        elif self.sheet_name.lower() == 'tp-hs':
            header_keyword = "Peak Wave Period"
            data_dim_primary = 'Tp'   # y dimension (rows)
            data_dim_secondary = 'Hs'  # x dimension (columns)
        else:
            raise ValueError(f"Unknown sheet_name '{self.sheet_name}'. Use 'Hs-Tp' or 'Tp-Hs'.")
        
        # Find header row
        header_row_idx = df_all[
            df_all.astype(str)
            .apply(lambda r: r.str.contains(header_keyword, case=False, na=False))
            .any(axis=1)
        ].index
        
        if len(header_row_idx) == 0:
            raise ValueError(f"Could not find '{header_keyword}' header in the sheet.")
        header_row_idx = header_row_idx[0]
        
        # Detect first non-empty column in header → table start column
        header_row = df_all.iloc[header_row_idx]
        first_nonempty_col = header_row.first_valid_index()
        
        # Detect end of table (first fully empty row after data starts)
        df_after = df_all.iloc[header_row_idx + 2:, first_nonempty_col:]
        empty_rows = df_after[df_after.isna().all(axis=1)].index
        table_end_idx = empty_rows[0] if len(empty_rows) > 0 else len(df_all)
        
        # Extract secondary dimension bin labels from row after header
        bin_row = df_all.iloc[header_row_idx + 1, first_nonempty_col:]
        bin_row_values = bin_row[3:]  # skip first 3 columns ('lower', 'upper', etc.)
        
        # Convert to numeric, find where NaNs start
        numeric_bins = pd.to_numeric(bin_row_values, errors='coerce')
        nan_pos = np.where(np.isnan(numeric_bins.to_numpy()))[0]
        last_bin_pos = nan_pos[0] if len(nan_pos) > 0 else len(numeric_bins)
        
        # Extract bins
        secondary_bins = numeric_bins.iloc[:last_bin_pos]
        
        # Slice data rows
        df_table = df_all.iloc[
            header_row_idx + 2:table_end_idx, 
            first_nonempty_col + 1:first_nonempty_col + 3 + last_bin_pos
        ].dropna(how='all', axis=0)
        
        # Extract primary bins (Hs or Tp upper bounds) and probability matrix
        primary_bins_upper = pd.to_numeric(df_table.iloc[:, 1], errors='coerce')
        prob_matrix = df_table.iloc[:, 2:].apply(pd.to_numeric, errors='coerce').fillna(0)
        
        # Normalize if absolute data
        if not is_relative:
            total = prob_matrix.to_numpy().sum()
            if total == 0:
                raise ValueError("Total count is zero; cannot normalize absolute data.")
            prob_matrix = prob_matrix / total
        
        # Create xarray DataArray
        scatter_data = xr.DataArray(
            prob_matrix.to_numpy(),
            coords={
                data_dim_primary: primary_bins_upper.values,
                data_dim_secondary: secondary_bins.values
            },
            dims=[data_dim_primary, data_dim_secondary]
        )
        
        return scatter_data

    

class DNVLoader(HindcastLoader):
    """
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
    """
    
    def __init__(
        self, 
        alpha_s: float, 
        beta_s: float, 
        a1: float, 
        a2: float, 
        b1: float, 
        b2: float, 
        a0: float = 0.7, 
        b0: float = 0.07, 
        gamma_s: float = 0,
        Hs_bins: np.ndarray = np.arange(0.5, 11.0, 0.5), 
        Tp_bins: np.ndarray = np.arange(1.0, 21.0, 1.0)
    ):
        
        # check if weibull params are floats
        for param_name, param_value in {
            'alpha_s': alpha_s,
            'beta_s': beta_s,
            'a1': a1,
            'a2': a2,
            'b1': b1,
            'b2': b2,
            'a0': a0,
            'b0': b0,
            'gamma_s': gamma_s
        }.items():
            if not isinstance(param_value, (float, int)):
                raise ValueError(f"{param_name} must be a float/integer.")
            
        # check if bins are upper edges (must not start at 0)
        if not (isinstance(Hs_bins, np.ndarray) and isinstance(Tp_bins, np.ndarray)):
            raise ValueError("Hs_bins and Tp_bins must be numpy arrays.")
        if Hs_bins[0] == 0 or Tp_bins[0] == 0:
            raise ValueError("Hs_bins and Tp_bins must be upper edges, so they must not start at 0.")

        # Store Weibull parameters and bins

        self.Hs_bins = Hs_bins

        self.Tp_bins = Tp_bins

        self.alpha_s = alpha_s

        self.beta_s = beta_s

        self.a1 = a1

        self.a2 = a2

        self.b1 = b1

        self.b2 = b2

        self.a0 = a0

        self.b0 = b0

        self.gamma_s = gamma_s

    

    def fetch(self) -> xr.DataArray:
        """
        Generate scatter table from Weibull distribution and return as xarray.DataArray.
        
        Returns scatter diagram with dims ('Hs', 'Tp') containing probability values (normalized to sum to 1).
        """
        # Convert upper bin edges to midpoints for from_weibull calculation
        # from_weibull expects bin midpoints, but we store upper edges for consistency
        Hs_lower = np.concatenate(([0.0], self.Hs_bins[:-1]))
        Hs_midpoints = (self.Hs_bins + Hs_lower) / 2.0
        
        Tp_lower = np.concatenate(([0.0], self.Tp_bins[:-1]))
        Tp_midpoints = (self.Tp_bins + Tp_lower) / 2.0
        
        # Convert Tp midpoints to Tz midpoints (from Jonswap: Tp = 1.287 * Tz)
        Tz_midpoints = Tp_midpoints / 1.287
        
        # Generate scatter using from_weibull function with midpoints
        scatter_Hs_Tz = from_weibull(
            Hs_midpoints,
            Tz_midpoints,
            self.alpha_s,
            self.beta_s,
            self.a1,
            self.a2,
            self.b1,
            self.b2,
            self.a0,
            self.b0,
            self.gamma_s
        )
        
        # Create new DataArray with upper bin edges as coordinates (consistent with other loaders)
        scatter_data = xr.DataArray(
            scatter_Hs_Tz.values,
            coords={
                'Hs': self.Hs_bins,
                'Tp': self.Tp_bins
            },
            dims=['Hs', 'Tp']
        )
        
        # Normalize to ensure probabilities sum to 1
        total = scatter_data.sum().values
        if total > 0:
            scatter_data = scatter_data / total
        
        return scatter_data
