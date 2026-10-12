PyBM.marine.tools
=================

.. py:module:: PyBM.marine.tools


Submodules
----------

.. toctree::
   :maxdepth: 1

   /autoapi/PyBM/marine/tools/CSV_to_Xarray/index
   /autoapi/PyBM/marine/tools/LIS_to_Xarray/index
   /autoapi/PyBM/marine/tools/TXT_to_Xarray/index
   /autoapi/PyBM/marine/tools/XLS_to_Xarray/index
   /autoapi/PyBM/marine/tools/api/index
   /autoapi/PyBM/marine/tools/import_octopus_rao/index
   /autoapi/PyBM/marine/tools/read_res/index


Functions
---------

.. autoapisummary::

   PyBM.marine.tools.Octopus_to_RAO
   PyBM.marine.tools.get_speeds
   PyBM.marine.tools.get_wave_directions
   PyBM.marine.tools.get_wave_frequencies
   PyBM.marine.tools.LIS_to_RAO
   PyBM.marine.tools.load_LIS
   PyBM.marine.tools.__file_len
   PyBM.marine.tools.resample
   PyBM.marine.tools.__read_file
   PyBM.marine.tools.read_res
   PyBM.marine.tools.write_pickle
   PyBM.marine.tools.write_res
   PyBM.marine.tools.XLS_to_RAO
   PyBM.marine.tools.load_XLS
   PyBM.marine.tools.CSV_to_RAO
   PyBM.marine.tools.load_CSV
   PyBM.marine.tools.TXT_to_RAO
   PyBM.marine.tools.load_TXT


Package Contents
----------------

.. py:function:: Octopus_to_RAO(octopus_file, VesselName, Vessel_LC, speed=0)

.. py:function:: get_speeds(file_iterator)

.. py:function:: get_wave_directions(file_iterator)

.. py:function:: get_wave_frequencies(file_iterator, speed)

.. py:function:: LIS_to_RAO(filename, VesselName, Vessel_LC)

   Convert LIS data to MotionRAO object.

   :param filename: path to LIS file
   :param VesselName: Name of the vessel
   :param Vessel_LC: Vessel Loading condition


.. py:function:: load_LIS(filename)

.. py:function:: __file_len(fname)

.. py:function:: resample(data, new_dt, data_dt)

.. py:function:: __read_file(filename, read_invalid=True)

.. py:function:: read_res(filename, dt=0, read_invalid=True)

   Read a text .res file with time traces.

   :param filename: name of file without extension
   :param dt: [s] sample time, if 0 the original sample time is used
   :param read_invalid: [bool] If false, invalid files are moved to Invalid folder
   :return: Dictionary of time_vectors.


.. py:function:: write_pickle(filename, data_dict)

.. py:function:: write_res(filename, data_dict)

   Write a data dictionary to a .res text file.

   :param filename: name of file (without extension)
   :param data_dict: dictionary of key / time_vector pairs


.. py:function:: XLS_to_RAO(filename, VesselName, Vessel_LC, origin, mirror=False)

   Convert excel file to Xarray RAO object

   :param filename: Excel file with RAO data
   :param VesselName: Name of vessel
   :param Vessel_LC: Loading condition of the vessel
   :param origin: [m] [x, y, z] origin of the RAOs w.r.t to vessel APP/CL/Keel
   :return: MotionRAO object
   :rtype: MotionRAO


.. py:function:: load_XLS(filename, mirror)

.. py:function:: CSV_to_RAO(filename, VesselName, Vessel_LC, origin, mirror=False)

   Convert CSV file to Xarray RAO object

   :param filename: CSV file with RAO data
   :param VesselName: Name of vessel
   :param Vessel_LC: Loading condition of the vessel
   :param origin: [m] [x, y, z] origin of the RAOs w.r.t to vessel APP/CL/Keel
   :return: MotionRAO object
   :rtype: MotionRAO


.. py:function:: load_CSV(filename, mirror)

.. py:function:: TXT_to_RAO(filename, VesselName, Vessel_LC, origin, mirror=False)

   Convert OrcaFlex .txt file to MotionRAO object.


.. py:function:: load_TXT(filename, mirror=False)

