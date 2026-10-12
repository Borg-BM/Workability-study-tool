PyBM.marine.motion_analysis.TimeDomain
======================================

.. py:module:: PyBM.marine.motion_analysis.TimeDomain

.. autoapi-nested-parse::

   Time domain tools

   References:
       [1]: Ship Motion Control, Tristan Perez



Classes
-------

.. autoapisummary::

   PyBM.marine.motion_analysis.TimeDomain.TimeDomainTools
   PyBM.marine.motion_analysis.TimeDomain.TimeDomain


Module Contents
---------------

.. py:class:: TimeDomainTools(xarray_obj)

   Tools for time domain traces in xarray.DataArray type


   .. py:attribute:: _obj


   .. py:method:: translate_trace(offset: numpy.array)

      Translates the trace in 6 DOF. Does not use small angle approx..

      :param offset: offset in [x,y,z]
      :type offset: np.array



   .. py:method:: translate_trace_smallangle(offset: numpy.array)

      Translates the trace in 6 DOF. Uses small angle approx

      :param offset: offset in [x,y,z]
      :type offset: np.array



.. py:class:: TimeDomain(wave: PyBM.marine.wave_spectrum.WaveSpectrum, rao: PyBM.marine.motion_analysis.MotionRAO.MotionRAO, vesselCoG)

   .. py:attribute:: rao


   .. py:attribute:: vesselCoG


   .. py:attribute:: wave


   .. py:method:: time_vector(dt, duration)
      :staticmethod:


      Create labelled time vector

      :param dt: [s] Time step
      :param duration: [s] Duration of time trace



   .. py:method:: generate_mat_time_traces(folder: str, dt, duration, wave)

      Generate .mat time traces to be used in the matlab workability tools.

      :param folder: Folder to save the files
      :param dt: [s] Time step
      :param duration: [s] Duration of time trace
      :param wave: [s] Wave to generate time traces for. Parameters may be vectorized.
      :param directions: [deg] Wave directions



   .. py:method:: generate_time_traces(folder: str, dt, duration, wave)

      Generate .mat time traces to be used in the matlab workability tools.

      :param folder: Folder to save the files
      :param dt: [s] Time step
      :param duration: [s] Duration of time trace
      :param wave: [s] Wave to generate time traces for. Parameters may be vectorized.
      :param directions: [deg] Wave directions



   .. py:method:: save_mat_file(folder, trace)

      Vectorized saving function



   .. py:method:: save_nc_file(folder, trace)


   .. py:method:: _save_nc_file(folder, traces: xarray.DataArray, VesselName, vesselCoG)
      :staticmethod:


      Save traces as a single nc file. will append nc with extra coordinates, if already there.
      :param folder: folder name
      :type folder: string
      :param traces: traces to save.
      :type traces: xarray.DataArray



   .. py:method:: default_trace_path(VesselName, revision=0)
      :staticmethod:



   .. py:method:: load_time_trace(folder)

      Loads time traces. Tries to open nc files first, if non existent, opens mat files.
      :param folder: folder name
      :type folder: str



   .. py:method:: load_all_default_time_traces(VesselName, rev=0)
      :staticmethod:


      Load the time traces of the given vessel and revision in the default engineering library folder.
      :param VesselName: vessel name
      :type VesselName: str
      :param rev: revision number
      :type rev: int



   .. py:method:: load_all_time_traces(folder, VesselName)
      :staticmethod:


      Static version of load_time_trace. Loads all time traces present in given folder. do not need to supply any sort of dimensioning for Tp, Hs or direction.
      If using default trace path, you can also use the function TimeDomain.load_default_time_trace().
      :param folder: folder to load time traces from.
      :type folder: str
      :param VesselName: name of the vessel to be loaded.
      :type VesselName: str



   .. py:method:: load_mat_time_trace(folder)

      Load a MAT time trace(s) as DataArray. Uses objects' properties for selecting which traces to load.

      :param folder: path of folder
      :type folder: str



   .. py:method:: _load_mat_time_trace(folder, VesselName, Tp, Hs, Direction)
      :staticmethod:


      Vectorized static function to load mat time traces according to given parameters.



   .. py:method:: _load_single_mat_time_trace(folder, VesselName, Tp, Hs, Direction)
      :staticmethod:



   .. py:method:: load_nc_time_trace(folder)

      Load NC stored time trace(s) as DataArray

      :param folder: path of folder



   .. py:method:: _load_nc_time_trace(folder, VesselName)
      :staticmethod:


      Loads nc file with traces.



   .. py:method:: mat_file_name()


   .. py:method:: _mat_file_name(VesselName, Tp, Hs, Direction)
      :staticmethod:


      Returns mat file names for trace. Broadcasts arrays in case of multiple values for Tp,Hs,main_direction.



   .. py:method:: nc_file_name()


   .. py:method:: _nc_file_name(VesselName)
      :staticmethod:


      Returns nc file name for trace. Since nc files include all directions it is not a vectorized function



   .. py:method:: _file_name(VesselName, Tp, Hs, Direction)
      :staticmethod:



   .. py:method:: time_trace_from_rao_and_wave(time: xarray.DataArray, wave: PyBM.marine.wave_spectrum.WaveSpectrum, rao: PyBM.marine.motion_analysis.MotionRAO.MotionRAO, Nfreqs=100, bounds=None)
      :staticmethod:


      Generate time trace based on RAO and Wave.

      :param time: [s] time vector
      :type time: xr.DataArray
      :param wave: [m2/(rad/s)] WaveSpectrum
      :type wave: WaveSpectrum
      :param rao: [m/m, deg/m] 6DOF Motion RAO
      :type rao: MotionRAO



   .. py:method:: multi_directional_time_trace(wave: PyBM.marine.wave_spectrum.WaveSpectrum, rao: PyBM.marine.motion_analysis.MotionRAO.MotionRAO, bounds=None)

      Create time trace including wave spreading.

      :param time: [s] time vector
      :type time: xr.DataArray
      :param rao: [m/m, deg/m] 6DOF Motion RAO
      :type rao: MotionRAO
      :param wave: [m2/(rad/s)] WaveSpectrum
      :type wave: WaveSpectrum



   .. py:method:: single_direction_time_trace(wave: PyBM.marine.wave_spectrum.WaveSpectrum, rao: PyBM.marine.motion_analysis.MotionRAO.MotionRAO)

      Create time trace for a single wave direction

      :param time: [s] time vector
      :type time: xr.DataArray
      :param rao: [m/m, deg/m] 6DOF Motion RAO. Must have interpolated frequencies according to equal area method
      :type rao: MotionRAO
      :param wave: [m2/(rad/s)] WaveSpectrum
      :type wave: WaveSpectrum



   .. py:method:: compute_deltas(coordinates, dim)
      :staticmethod:


      Create bins centered a coordinate points.

      :param coordinates: Coordinates to create bins around.
      :param dim: Dimension name



   .. py:method:: zero_crossing_period(trace)
      :staticmethod:


      Compute average zero-crossing period of a time trace.

      return: [s] average zero-crossing period.



