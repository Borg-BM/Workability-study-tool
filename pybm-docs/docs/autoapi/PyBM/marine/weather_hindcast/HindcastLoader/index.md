<!-- Source: https://docs.app.barge-master.com/autoapi/PyBM/marine/weather_hindcast/HindcastLoader/index.html -->

# PyBM.marine.weather_hindcast.HindcastLoader

Hindcast data loaders for various sources.

Provides loader classes for fetching hindcast data from:

- Copernicus Marine Service

- NOAA NDBC buoys

- DNV Long-term wave stats

- Excel files (scatter table and time series formats)

References:  
- \[1\] NDBC API Documentation: [https://pypi.org/project/ndbc-api/](https://pypi.org/project/ndbc-api/)

- \[2\] NDBC Stations page: [https://www.ndbc.noaa.gov/](https://www.ndbc.noaa.gov/)

- \[3\] Copernicus Marine Wave Data Store: [https://data.marine.copernicus.eu/products?facets=mainVariables%7EWave–tempResolutions%7EHourly](https://data.marine.copernicus.eu/products?facets=mainVariables%7EWave--tempResolutions%7EHourly)

- \[4\] Copernicus Marine Toolbox API Help Center: [https://help.marine.copernicus.eu/en/collections/9080063-copernicus-marine-toolbox](https://help.marine.copernicus.eu/en/collections/9080063-copernicus-marine-toolbox)

- \[5\] DNV-RP-C205 Environmental Conditions and Environmental Loads

## Classes

|                                                                                                                                                                   |                                                                                            |
|-------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------|
| [`HindcastLoader`](#PyBM.marine.weather_hindcast.HindcastLoader.HindcastLoader "PyBM.marine.weather_hindcast.HindcastLoader.HindcastLoader")                      | Abstract base class for all hindcast data loaders.                                         |
| [`CopernicusLoader`](#PyBM.marine.weather_hindcast.HindcastLoader.CopernicusLoader "PyBM.marine.weather_hindcast.HindcastLoader.CopernicusLoader")                | Class to load hindcast data from Copernicus Marine API. \[3\], \[4\]                       |
| [`NDBCLoader`](#PyBM.marine.weather_hindcast.HindcastLoader.NDBCLoader "PyBM.marine.weather_hindcast.HindcastLoader.NDBCLoader")                                  | Class to load hindcast data from NOAA NDBC buoys. \[1\], \[2\]                             |
| [`ExcelTimeSeriesLoader`](#PyBM.marine.weather_hindcast.HindcastLoader.ExcelTimeSeriesLoader "PyBM.marine.weather_hindcast.HindcastLoader.ExcelTimeSeriesLoader") | Load hindcast time series data from Excel or CSV file.                                     |
| [`ExcelScatterLoader`](#PyBM.marine.weather_hindcast.HindcastLoader.ExcelScatterLoader "PyBM.marine.weather_hindcast.HindcastLoader.ExcelScatterLoader")          | Load hindcast scatter table from Excel file.                                               |
| [`DNVLoader`](#PyBM.marine.weather_hindcast.HindcastLoader.DNVLoader "PyBM.marine.weather_hindcast.HindcastLoader.DNVLoader")                                     | Load hindcast scatter table from DNV long-term wave statistics using Weibull distribution. |

## Module Contents

*class *PyBM.marine.weather_hindcast.HindcastLoader.HindcastLoader[](../../../../../../source-code/PyBM/marine/weather_hindcast/HindcastLoader.py)  
Bases: `abc.ABC`

Abstract base class for all hindcast data loaders.

*abstractmethod *fetch() → pandas.DataFrame \| xarray.DataArray[](../../../../../../source-code/PyBM/marine/weather_hindcast/HindcastLoader.py)  
Fetch raw data from the source. Returns data as a pd.DataFrame (time-series) or xarray.DataArray (scatter table).

&nbsp;

*class *PyBM.marine.weather_hindcast.HindcastLoader.CopernicusLoader(*lat: float*, *long: float*, *product_id: int = 0*, *start_date: str = None*, *end_date: str = None*)[](../../../../../../source-code/PyBM/marine/weather_hindcast/HindcastLoader.py)  
Bases: [`HindcastLoader`](#PyBM.marine.weather_hindcast.HindcastLoader.HindcastLoader "PyBM.marine.weather_hindcast.HindcastLoader.HindcastLoader")

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

lat[](../../../../../../source-code/PyBM/marine/weather_hindcast/HindcastLoader.py)  

&nbsp;

long[](../../../../../../source-code/PyBM/marine/weather_hindcast/HindcastLoader.py)  

&nbsp;

start_date* = None*[](../../../../../../source-code/PyBM/marine/weather_hindcast/HindcastLoader.py)  

&nbsp;

end_date* = None*[](../../../../../../source-code/PyBM/marine/weather_hindcast/HindcastLoader.py)  

&nbsp;

product_id* = 'cmems_mod_glo_wav_my_0.2deg_PT3H-i'*[](../../../../../../source-code/PyBM/marine/weather_hindcast/HindcastLoader.py)  

&nbsp;

fetch() → pandas.DataFrame[](../../../../../../source-code/PyBM/marine/weather_hindcast/HindcastLoader.py)  
Fetch time series data from Copernicus Marine API.

&nbsp;

*class *PyBM.marine.weather_hindcast.HindcastLoader.NDBCLoader(*lat: float = None*, *long: float = None*, *buoy_id: str = None*, *start_date: str = None*, *end_date: str = None*)[](../../../../../../source-code/PyBM/marine/weather_hindcast/HindcastLoader.py)  
Bases: [`HindcastLoader`](#PyBM.marine.weather_hindcast.HindcastLoader.HindcastLoader "PyBM.marine.weather_hindcast.HindcastLoader.HindcastLoader")

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

lat* = None*[](../../../../../../source-code/PyBM/marine/weather_hindcast/HindcastLoader.py)  

&nbsp;

long* = None*[](../../../../../../source-code/PyBM/marine/weather_hindcast/HindcastLoader.py)  

&nbsp;

buoy_id* = None*[](../../../../../../source-code/PyBM/marine/weather_hindcast/HindcastLoader.py)  

&nbsp;

start_date* = None*[](../../../../../../source-code/PyBM/marine/weather_hindcast/HindcastLoader.py)  

&nbsp;

end_date* = None*[](../../../../../../source-code/PyBM/marine/weather_hindcast/HindcastLoader.py)  

&nbsp;

fetch() → pandas.DataFrame[](../../../../../../source-code/PyBM/marine/weather_hindcast/HindcastLoader.py)  
Fetch time series data from NDBC.

&nbsp;

*class *PyBM.marine.weather_hindcast.HindcastLoader.ExcelTimeSeriesLoader(*file_path: str*, *date_format: str = '%m/%d/%Y %H:%M'*)[](../../../../../../source-code/PyBM/marine/weather_hindcast/HindcastLoader.py)  
Bases: [`HindcastLoader`](#PyBM.marine.weather_hindcast.HindcastLoader.HindcastLoader "PyBM.marine.weather_hindcast.HindcastLoader.HindcastLoader")

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

file_path[](../../../../../../source-code/PyBM/marine/weather_hindcast/HindcastLoader.py)  

&nbsp;

date_format* = '%m/%d/%Y %H:%M'*[](../../../../../../source-code/PyBM/marine/weather_hindcast/HindcastLoader.py)  

&nbsp;

fetch() → pandas.DataFrame[](../../../../../../source-code/PyBM/marine/weather_hindcast/HindcastLoader.py)  
Load time series data from Excel or CSV file.

&nbsp;

*class *PyBM.marine.weather_hindcast.HindcastLoader.ExcelScatterLoader(*file_path: str*, *sheet_name: str = 'Hs-Tp'*)[](../../../../../../source-code/PyBM/marine/weather_hindcast/HindcastLoader.py)  
Bases: [`HindcastLoader`](#PyBM.marine.weather_hindcast.HindcastLoader.HindcastLoader "PyBM.marine.weather_hindcast.HindcastLoader.HindcastLoader")

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

file_path[](../../../../../../source-code/PyBM/marine/weather_hindcast/HindcastLoader.py)  

&nbsp;

sheet_name* = 'Hs-Tp'*[](../../../../../../source-code/PyBM/marine/weather_hindcast/HindcastLoader.py)  

&nbsp;

fetch() → xarray.DataArray[](../../../../../../source-code/PyBM/marine/weather_hindcast/HindcastLoader.py)  
Load scatter table from Excel file and return as xarray.DataArray.

&nbsp;

*class *PyBM.marine.weather_hindcast.HindcastLoader.DNVLoader(*alpha_s: float*, *beta_s: float*, *a1: float*, *a2: float*, *b1: float*, *b2: float*, *a0: float = 0.7*, *b0: float = 0.07*, *gamma_s: float = 0*, *Hs_bins: numpy.ndarray = np.arange(0.5, 11.0, 0.5)*, *Tp_bins: numpy.ndarray = np.arange(1.0, 21.0, 1.0)*)[](../../../../../../source-code/PyBM/marine/weather_hindcast/HindcastLoader.py)  
Bases: [`HindcastLoader`](#PyBM.marine.weather_hindcast.HindcastLoader.HindcastLoader "PyBM.marine.weather_hindcast.HindcastLoader.HindcastLoader")

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

Hs_bins[](../../../../../../source-code/PyBM/marine/weather_hindcast/HindcastLoader.py)  

&nbsp;

Tp_bins[](../../../../../../source-code/PyBM/marine/weather_hindcast/HindcastLoader.py)  

&nbsp;

alpha_s[](../../../../../../source-code/PyBM/marine/weather_hindcast/HindcastLoader.py)  

&nbsp;

beta_s[](../../../../../../source-code/PyBM/marine/weather_hindcast/HindcastLoader.py)  

&nbsp;

a1[](../../../../../../source-code/PyBM/marine/weather_hindcast/HindcastLoader.py)  

&nbsp;

a2[](../../../../../../source-code/PyBM/marine/weather_hindcast/HindcastLoader.py)  

&nbsp;

b1[](../../../../../../source-code/PyBM/marine/weather_hindcast/HindcastLoader.py)  

&nbsp;

b2[](../../../../../../source-code/PyBM/marine/weather_hindcast/HindcastLoader.py)  

&nbsp;

a0* = 0.7*[](../../../../../../source-code/PyBM/marine/weather_hindcast/HindcastLoader.py)  

&nbsp;

b0* = 0.07*[](../../../../../../source-code/PyBM/marine/weather_hindcast/HindcastLoader.py)  

&nbsp;

gamma_s* = 0*[](../../../../../../source-code/PyBM/marine/weather_hindcast/HindcastLoader.py)  

&nbsp;

fetch() → xarray.DataArray[](../../../../../../source-code/PyBM/marine/weather_hindcast/HindcastLoader.py)  
Generate scatter table from Weibull distribution and return as xarray.DataArray.

Returns scatter diagram with dims (‘Hs’, ‘Tp’) containing probability values (normalized to sum to 1).
