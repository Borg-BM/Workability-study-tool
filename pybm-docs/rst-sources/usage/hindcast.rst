.. _hindcast:

##########
Hindcast
##########

*********
Overview
*********

The PyBM hindcast module provides a framework for loading, analyzing, and visualizing historical wave data from various sources. The module supports both **time-series** data (e.g., hourly wave measurements) and **scatter tables** (pre-binned Hs-Tp distributions).

.. image:: ../images/hindcast_diagram.png
    :alt: hindcast_diagram
    :align: center
    
|

This user guide covers:

- :ref:`sec-data-sources` - what data sources (loaders) are available and how to use them.
- :ref:`sec-hindcast-functionalities` - what we can do with the loaded hindcast data, including statistical analysis and workability percentage calculations.

You can find extended templates for all the hindcast loaders and functionalities in the :ref:`Templates <templates:Hindcast>` section.

**Key Features**

- Support for multiple data sources (Copernicus, NOAA NDBC, DNV long-term stats, Excel files)
- Statistical analysis (monthly/overall Hs and Tp wave statistics)
- Hs vs Tp wave occurrence visualization
- Workability percentage calculations based on a machine's workability result

**Architecture**

The hindcast framework consists of three main components:

1. **Loaders** - Classes that fetch data from different sources. See all the loaders below in :ref:`sec-data-sources`.
2. **Factory** - The :py:class:`~PyBM.marine.weather_hindcast.Hindcast.Hindcast` factory class that automatically creates the appropriate analysis object based on the loader.
3. **Analysis Objects** - :py:class:`~PyBM.marine.weather_hindcast.Hindcast.HindcastTimeSeries` and :py:class:`~PyBM.marine.weather_hindcast.Hindcast.HindcastScatterTable` for data analysis and visualization.

A typical use of the hindcast module involves:

1. Creating a loader for the desired data source
2. Passing it to the :py:class:`~PyBM.marine.weather_hindcast.Hindcast.Hindcast` factory class
3. Using the returned analysis object for further functionalities

**Data Types**

The module works with two main data types:

- **Time-Series Data**: Continuous wave measurements over time (e.g., hourly Hs and Tp values). Stored as a `pandas.DataFrame` with Date, Hs and Tp columns.
- **Scatter Table Data**: Joint wave distributions of Hs and Tp values. Stored as an `xarray.DataArray` with dimensions for Hs and Tp upper bin values.

This is just informative, the loader classes handle the creation of these data types internally.

.. _sec-data-sources:

***********************
Data Sources (Loaders)
***********************

The available loaders are:

- Excel files

    - Time Series Format
    - Scatter Table Format

- Copernicus Marine Service
- NOAA NDBC Buoy Data
- DNV Weibull Distribution

**How to choose the right loader?**

1. First priority is given to historical data provided by the client. This data is often provided in Excel or CSV files, so the :ref:`Excel loader <sec-excel-loader>` should be used.
2. If no client data is available, two hindcast services can be used by specifying the coordinates of the location of interest:

    - :ref:`Copernicus Marine Service loader <sec-copernicus-loader>`, where the appropriate product ID should be used based on the location.
    - :ref:`NOAA NDBC Buoy Data loader <sec-ndbc-loader>`, suitable for North American coastal regions. For other regions Copernicus is preferred.

3. The last resource should be the :ref:`DNV Weibull Distribution loader <sec-dnv-loader>`, which generates scatter tables based on long-term wave statistics. This method is less accurate and should only be used for very specific cases.

.. _sec-excel-loader:

Excel Files
^^^^^^^^^^^^

Load data from Excel or CSV files. This is the preferred loader as it allows using client-provided historical data.

**Time Series Format** (:py:class:`~PyBM.marine.weather_hindcast.HindcastLoader.ExcelTimeSeriesLoader`)

.. code-block:: python

    from PyBM.marine.weather_hindcast import Hindcast, ExcelTimeSeriesLoader
    
    loader = ExcelTimeSeriesLoader(
        file_path='wave_data.csv',
        date_format='%m/%d/%Y %H:%M'  # Optional, default shown
    )
    
    hindcast = Hindcast(loader)  # Returns HindcastTimeSeries

Expected format: First sheet with header row with columns ``Date``, ``Hs``, ``Tp`` (in that order).
See the template file :download:`HindcastTimeSeries_template.csv <../../../templates/hindcast/HindcastTimeSeries_template.csv>` as reference.

**Scatter Table Format** (:py:class:`~PyBM.marine.weather_hindcast.HindcastLoader.ExcelScatterLoader`)

.. code-block:: python

    from PyBM.marine.weather_hindcast import Hindcast, ExcelScatterLoader
    
    loader = ExcelScatterLoader(
        file_path='scatter_table.xlsx',
        sheet_name='Hs-Tp'  # 'Hs-Tp' or 'Tp-Hs'
    )
    
    hindcast = Hindcast(loader)  # Returns HindcastScatterTable

Expected format: Use the template file :download:`HindcastScatterTable_template.xlsx <../../../templates/hindcast/HindcastScatterTable_template.xlsx>` as reference. Instructions for filling the template are included in the file.

.. _sec-copernicus-loader:

Copernicus Marine Service (:py:class:`~PyBM.marine.weather_hindcast.HindcastLoader.CopernicusLoader`)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Load wave hindcast data from Copernicus Marine API.

.. code-block:: python

    from PyBM.marine.weather_hindcast import Hindcast, CopernicusLoader
    
    # Load data for a specific location and time period
    loader = CopernicusLoader(
        lat=52.0,                   # Latitude (decimal degrees)
        long=4.0,                   # Longitude (decimal degrees)
        product_id=0,               # 0 = Global Ocean Waves Reanalysis
        start_date='2020-01-01',    # If no value specified, defaults to earliest available
        end_date='2020-12-31'       # If no value specified, defaults to latest available
    )
    
    hindcast = Hindcast(loader)  # Returns HindcastTimeSeries

**Available Products:**

- 0: `Global Ocean Waves Reanalysis <https://data.marine.copernicus.eu/product/GLOBAL_MULTIYEAR_WAV_001_032/description>`_
- 1: `Arctic Ocean Wave Hindcast <https://data.marine.copernicus.eu/product/ARCTIC_MULTIYEAR_WAV_002_013/description>`_
- 2: `Baltic Sea Wave Hindcast <https://data.marine.copernicus.eu/product/BALTICSEA_MULTIYEAR_WAV_003_015/description>`_
- 3: `Black Sea Waves Reanalysis <https://data.marine.copernicus.eu/product/BLKSEA_MULTIYEAR_WAV_007_006/description>`_
- 4: `Atlantic (Iberian/Biscay/Irish) Ocean Wave Reanalysis <https://data.marine.copernicus.eu/product/IBI_MULTIYEAR_WAV_005_006/description>`_
- 5: `Mediterranean Sea Waves Reanalysis <https://data.marine.copernicus.eu/product/MEDSEA_MULTIYEAR_WAV_006_012/description>`_
- 6: `Atlantic (European North West Shelf) Wave Physics Reanalysis <https://data.marine.copernicus.eu/product/NWSHELF_REANALYSIS_WAV_004_015/description>`_

You can check on the link of each product the coordinates coverage. If no specific product is ideal for the specific location, use product 0 (Global Ocean Waves Reanalysis) as it covers the entire globe.

.. _sec-ndbc-loader:

NOAA NDBC Buoy Data (:py:class:`~PyBM.marine.weather_hindcast.HindcastLoader.NDBCLoader`)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Load historical wave data from NOAA buoy stations (suitable for North American coastal regions). 
You can see all the available buoys `here <https://www.ndbc.noaa.gov/>`_.

.. code-block:: python

    from PyBM.marine.weather_hindcast import Hindcast, NDBCLoader
    
    # Option 1: Specify buoy ID directly
    loader = NDBCLoader(
        buoy_id='46022',
        start_date='2019-01-01', # If no value specified, defaults to earliest available
        end_date='2019-12-31'    # If no value specified, defaults to latest available
    )
    
    # Option 2: Use lat/long to find nearest buoy
    loader = NDBCLoader(
        lat=37.75,
        long=-122.42,
        start_date='2019-01-01', # If no value specified, defaults to earliest available
        end_date='2019-12-31'    # If no value specified, defaults to latest available
    )
    
    hindcast = Hindcast(loader)  # Returns HindcastTimeSeries

.. _sec-dnv-loader:

DNV Weibull Distribution (:py:class:`~PyBM.marine.weather_hindcast.HindcastLoader.DNVLoader`)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Generate scatter tables from DNV long-term wave statistics using Weibull parameters (DNV-RP-C205).
A couple of notes:

1. This method is only valid for JONSWAP spectrum.
2. Calculating workability percentages using this loader (DNV C205) will produce highly conservative results. Please use this loader as last resource. If this result is to be used in client communication, it may only be used in combination with a comparison to a base case. For example, comparison between workability of motion compensation versus non-motion compensation. 

The scatter table is generated based on the Weibull probability density function according to DNV-RP-C205 2014-04 Formula 3.6.3.4.

The significant wave height is modelled by a 3-parameter Weibull probability density function:

.. math::
    f_{H_s}(h) = \frac{\beta_s}{\alpha_s}\left(\frac{h - \gamma_s}{\alpha_s}\right)^{\beta_s - 1}e^{-\left(\frac{h - \gamma_s}{\alpha_s}\right)^{\beta_s}}

where :math:`\alpha_s`, :math:`\beta_s` and :math:`\gamma_s` are distribution parameters. :math:`\gamma_s` is often set to zero.

The zero-crossing wave period conditional on Hs is modelled by a lognormal distribution:

.. math::
    f_{T_z|H_s}(t|h) = \frac{1}{t \sigma \sqrt{2\pi}}e^{-\frac{(\ln(t) - \mu)^2}{2\sigma^2}}

where :math:`\mu` and :math:`\sigma` are functions of Hs. DNV refers that the following model gives good fit to the data:

.. math::
    \mu = a_0 + a_1 \cdot h^{a_2}

.. math::
    \sigma = b_0 + b_1 \cdot e^{b_2 \cdot h}

where typically :math:`a_0=0.7`, :math:`b_0=0.07`.

The scatter diagram is obtained by combining the two distributions:

.. math::
    f_{H_s,T_z}(h,t) = f_{H_s}(h) \cdot f_{T_z|H_s}(t|h)

All the remaining parameters (:math:`\alpha_s`, :math:`\beta_s`, :math:`a_1`, :math:`a_2`, :math:`b_1`, :math:`b_2`) are location dependent.
A region of the world is selected using Appendix B of DNV-RP-C205, and the corresponding parameters from Appendix C are picked to generate the scatter table.

.. image:: ../images/DNV_C205_AppB.png
    :alt: dnv_c205_appB
    :align: center

.. image:: ../images/DNV_C205_AppC.png
    :alt: dnv_c205_appC
    :align: center

.. code-block:: python

    from PyBM.marine.weather_hindcast import Hindcast, DNVLoader
    import numpy as np
    
    # Weibull parameters from DNV-RP-C205 Appendix C Table C-1
    loader = DNVLoader(
        alpha_s=2.5,        
        beta_s=1.5,         
        a1=0.5,             
        a2=0.5,
        b1=0.2,
        b2=-0.1,
        a0=0.7,             # Default: 0.7
        b0=0.07,            # Default: 0.07
        gamma_s=0.0,        # Default: 0
        Hs_bins=np.arange(0.5, 8.0, 0.5),   # Optional custom bins
        Tp_bins=np.arange(1.0, 20.0, 1.0)   # Optional custom bins
    )
    
    hindcast = Hindcast(loader)  # Returns HindcastScatterTable

.. _sec-hindcast-functionalities:

*************************
Hindcast Functionalities
*************************

Hs and Tp statistics
^^^^^^^^^^^^^^^^^^^^

Computes the Hs and Tp statistics from the hindcast data. Gives the percentage of waves in each Hs and Tp bin.
For **time-series data**, statistics can be computed **monthly** or **overall**. For **scatter table data**, only **overall** statistics are available.
Returns a pandas DataFrame with the statistics and, optionally, a plot.

**Example:**

.. code-block:: python

    from PyBM.marine.weather_hindcast import Hindcast
    
    # Load hindcast data
    loader = SomeLoader(...)  # e.g., CopernicusLoader, NDBCLoader, ExcelTimeSeriesLoader, (...)
    hindcast = Hindcast(loader)
    
    # Get monthly Hs statistics. Monthly stats only available for time-series data, will throw an error for scatter table data.
    hs_df, ax = hindcast.get_Hs_stats(period='monthly', plot=True)
    plt.show()
    
    # Get overall Tp statistics. Monthly stats only available for time-series data, will throw an error for scatter table data.
    tp_df, ax = hindcast.get_Tp_stats(period='monthly', plot=True)
    plt.show()

.. image:: ../images/Hs_stats.png
    :alt: Hs_stats
    :align: center

.. image:: ../images/Tp_stats.png
    :alt: Tp_stats
    :align: center

Hs vs Tp Occurrence Plot
^^^^^^^^^^^^^^^^^^^^^^^^

Plots the Hs vs Tp scatter diagram showing the density of occurrences in each combination of Hs-Tp bin.
Optionally, a workability result can be overlaid on the plot.

**Example:**

.. code-block:: python

    from PyBM.marine.weather_hindcast import Hindcast

    # Load hindcast data
    loader = SomeLoader(...)  # e.g., CopernicusLoader, NDBCLoader, ExcelTimeSeriesLoader, (...)
    hindcast = Hindcast(loader)

    # Calculate workability result (example)
    Tp = np.arange(2, 16, 1)
    wave = Jonswap(1, Tp, main_direction=some_wavedir)
    workability_result = directional_workability(some_rao, wave, some_machine)
    # Minimize over limiting type and wave direction
    workability_result = workability_result.min(["lim_type", "WaveDirection"])

    # Plot Hs vs Tp scatter diagram
    ax = hindcast.plot_Hs_Tp(workability_result=workability_result)
    plt.show()

.. image:: ../images/Hs_vs_Tp_Workability_Limits.png
    :alt: Hs_stats
    :align: center

Workability Percentage Calculation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
After calculating a machine's workability limits (the maximum operational Hs for each wave period Tp), 
you can estimate what percentage of sea states would allow the machine to operate. This is done by 
comparing the workability limits against historical wave conditions from the hindcast data.

**For Time-Series Data:**

The method evaluates each individual wave measurement in the hindcast time series:

1. For each data point (with its specific Hs and Tp values), the workability limit is interpolated to find the maximum allowable Hs at that particular Tp
2. If the actual Hs is below this limit, the sea state is considered workable
3. The percentage is calculated as: (number of workable sea states) / (total sea states) × 100%

Two period options are available:

- ``period='overall'``: Returns the overall workability percentage across the entire time series as a single float value
- ``period='monthly'``: Returns a pandas Series with workability percentages for each calendar month (Jan, Feb, Mar, etc.)

**For Scatter Table Data:**

The method works with the probability distribution of wave conditions:

1. The workability limit (maximum Hs) is interpolated for each Tp bin in the scatter table
2. For each Tp bin, the cumulative probability of all Hs values up to the workability limit is calculated
3. These probabilities are summed across all Tp bins to get the total workability percentage

Only ``period='overall'`` is available for scatter table data (no monthly breakdown possible with aggregated data).

.. code-block:: python

    from PyBM.marine.weather_hindcast import Hindcast
    
    # Load hindcast data
    loader = SomeLoader(...)  # e.g., CopernicusLoader, NDBCLoader, ExcelTimeSeriesLoader, (...)
    hindcast = Hindcast(loader)

    # Calculate workability result (example)
    Tp = np.arange(2, 16, 1)
    wave = Jonswap(1, Tp, main_direction=some_wavedir)
    workability_result = directional_workability(some_rao, wave, some_machine)
    workability_result = workability_result.min(["lim_type", "WaveDirection"])

    # Get monthly workability percentages. Only available for time-series data, will throw an error for scatter table data.
    workability_percentage = hindcast.get_workability_percentage(workability_result, period='monthly')
    # Get overall workability percentage
    overall_percentage = hindcast.get_workability_percentage(workability_result, period='overall')

    # Plot monthly workability percentages
    fig, ax = plt.subplots(figsize=(8, 6))
    workability_percentage.plot.bar(legend=False, ax=ax, color=tuple(np.array([0,173,239])/255), alpha=0.7)
    ax.set_xlabel('Month', fontsize=12)
    ax.set_ylabel('Workability Percentage [%]', fontsize=12)
    ax.set_yticks(np.arange(0, 101, 20))
    ax.grid(axis='y', color='lightgray')
    ax.set_title(
        f"Monthly Workability: {overall_percentage:.2f}%",
        fontsize=14, 
        fontweight='bold'
    )
    plt.show()

.. image:: ../images/monthly_workability.png
    :alt: monthly_workability
    :align: center

**********
References
**********

- DNV-RP-C205: Environmental Conditions and Environmental Loads (2014-04)
- `Copernicus Marine Data Store <https://data.marine.copernicus.eu/>`_
- `Copernicus Marine Toolbox API Help Center <https://help.marine.copernicus.eu/en/collections/9080063-copernicus-marine-toolbox>`_
- `NOAA NDBC <https://www.ndbc.noaa.gov/>`_
- `NDBC API Documentation <https://pypi.org/project/ndbc-api/>`_
