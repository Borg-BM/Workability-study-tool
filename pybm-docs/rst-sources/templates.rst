Templates
=========

All examples below are available in the `templates` folder of the repository.

Motion Analysis
################

The Motion Analysis tools are largely based on the `Xarray <https://docs.xarray.dev/en/stable/>`_ package, check their docs for details about usage.
Theory behind the Motion Analysis tools can be found in the :ref:`Theory section <theory:Theory>`.

Frequency domain
-----------------

:download:`Download example script file <../../templates/motion_analysis/example__frequency_domain.py>` (right-click and "Save link as...")

.. literalinclude:: ../../templates/motion_analysis/example__frequency_domain.py
    :language: python

Time trace generation
----------------------

:download:`Download example script file <../../templates/motion_analysis/example_time_trace.py>` (right-click and "Save link as...")

.. literalinclude:: ../../templates/motion_analysis/example_time_trace.py
    :language: python

Workability
############

MCG Linear Workability (Commercial)
------------------------------------

MCG for Personnel Transfer
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:download:`Download example script file <../../templates/workability/BM_OPXXXX_VESSEL_NAME_Workability_Transfer_Rev0.py>` (right-click and "Save link as...")

.. literalinclude:: ../../templates/workability/BM_OPXXXX_VESSEL_NAME_Workability_Transfer_Rev0.py
    :language: python

MCG for Lifting Operations
^^^^^^^^^^^^^^^^^^^^^^^^^^

:download:`Download example script file <../../templates/workability/BM_OPXXXX_VESSEL_NAME_Workability_Lifting_Rev0.py>` (right-click and "Save link as...")

.. literalinclude:: ../../templates/workability/BM_OPXXXX_VESSEL_NAME_Workability_Lifting_Rev0.py
    :language: python

MCG Nonlinear Workability
--------------------------

Use this class only if there are time traces of the vessel motions available.

:download:`Download example script file <../../templates/workability/example_MCG_workability.py>` (right-click and "Save link as...")

.. literalinclude:: ../../templates/workability/example_MCG_workability.py
    :language: python

T700 Workability
------------------

:download:`Download example script file <../../templates/workability/example_T700_workability.py>` (right-click and "Save link as...")

.. literalinclude:: ../../templates/workability/example_T700_workability.py
    :language: python

Hindcast
#########

From Excel files (client-provided historical data)
---------------------------------------------------

Time series format
^^^^^^^^^^^^^^^^^^^^

You can use this CSV template file (:download:`HindcastTimeSeries_template.csv <../../templates/hindcast/HindcastTimeSeries_template.csv>`) to provide the time series data. 

:download:`Download example script file <../../templates/hindcast/example_excel_timeseries_loader.py>` (right-click and "Save link as...")

.. literalinclude:: ../../templates/hindcast/example_excel_timeseries_loader.py
    :language: python

Scatter table format
^^^^^^^^^^^^^^^^^^^^^^

You can use this Excel template file (:download:`HindcastScatterTable_template.xlsx <../../templates/hindcast/HindcastScatterTable_template.xlsx>`) to provide the scatter table data. 

:download:`Download example script file <../../templates/hindcast/example_excel_scatter_loader.py>` (right-click and "Save link as...")

.. literalinclude:: ../../templates/hindcast/example_excel_scatter_loader.py
    :language: python

From Copernicus Marine Service
-------------------------------

:download:`Download example script file <../../templates/hindcast/example_copernicus_loader.py>` (right-click and "Save link as...")

.. literalinclude:: ../../templates/hindcast/example_copernicus_loader.py
    :language: python

From NDBC Buoy Data
---------------------

:download:`Download example script file <../../templates/hindcast/example_ndbc_loader.py>` (right-click and "Save link as...")

.. literalinclude:: ../../templates/hindcast/example_ndbc_loader.py
    :language: python

From DNV long-term wave statistics
------------------------------------

:download:`Download example script file <../../templates/hindcast/example_DNV_weibull_workability.py>` (right-click and "Save link as...")

.. literalinclude:: ../../templates/hindcast/example_DNV_weibull_workability.py
    :language: python

IIR filters
##############

The following example shows the usage of the IIR filter design tools:

:download:`Download example script file <../../templates/filtering/example_iir_filter.py>` (right-click and "Save link as...")

.. literalinclude:: ../../templates/filtering/example_iir_filter.py
    :language: python


Heavy Feeder Tower check
##########################

The following example shows the usage of Heavy Feeder Tower check tools:

:download:`Download example script file <../../templates/heavy_feeder/example_tower_check.py>` (right-click and "Save link as...")

.. literalinclude:: ../../templates/heavy_feeder/example_tower_check.py
    :language: python

.. Hydraulic / Mechanical sizing
.. ###############################
