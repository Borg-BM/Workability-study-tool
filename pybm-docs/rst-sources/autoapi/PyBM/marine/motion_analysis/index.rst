PyBM.marine.motion_analysis
===========================

.. py:module:: PyBM.marine.motion_analysis


Submodules
----------

.. toctree::
   :maxdepth: 1

   /autoapi/PyBM/marine/motion_analysis/ForceRAO/index
   /autoapi/PyBM/marine/motion_analysis/MotionRAO/index
   /autoapi/PyBM/marine/motion_analysis/RAO/index
   /autoapi/PyBM/marine/motion_analysis/Response/index
   /autoapi/PyBM/marine/motion_analysis/SpectrumAccessor/index
   /autoapi/PyBM/marine/motion_analysis/TimeDomain/index


Attributes
----------

.. autoapisummary::

   PyBM.marine.motion_analysis.g


Exceptions
----------

.. autoapisummary::

   PyBM.marine.motion_analysis.OutofBoundsError


Classes
-------

.. autoapisummary::

   PyBM.marine.motion_analysis.RAO
   PyBM.marine.motion_analysis.MotionRAO
   PyBM.marine.motion_analysis.SurgeDir
   PyBM.marine.motion_analysis.SwayDir
   PyBM.marine.motion_analysis.HeaveDir
   PyBM.marine.motion_analysis.RollDir
   PyBM.marine.motion_analysis.PitchDir
   PyBM.marine.motion_analysis.YawDir
   PyBM.marine.motion_analysis.WaveOrigin
   PyBM.marine.motion_analysis.RotationUnit
   PyBM.marine.motion_analysis.RAO
   PyBM.marine.motion_analysis.SpectralTools
   PyBM.marine.motion_analysis.EqualEnergySpectrum
   PyBM.marine.motion_analysis.MotionRAO
   PyBM.marine.motion_analysis.TimeDomainTools
   PyBM.marine.motion_analysis.TimeDomain


Functions
---------

.. autoapisummary::

   PyBM.marine.motion_analysis._recursive_group_names
   PyBM.marine.motion_analysis.compute_response
   PyBM.marine.motion_analysis.compute_mpe
   PyBM.marine.motion_analysis.equal_energy_freqs_rao
   PyBM.marine.motion_analysis.apply_directional_spreading
   PyBM.marine.motion_analysis.isFileLocked


Package Contents
----------------

.. py:class:: RAO(data_vars: xarray.core.types.DataVars | None = None, coords: collections.abc.Mapping[Any, Any] | None = None, attrs: collections.abc.Mapping[Any, Any] | None = None)

   Bases: :py:obj:`xarray.Dataset`, :py:obj:`abc.ABC`


   This is the parent class for motion and force RAOs


   .. py:attribute:: __slots__
      :value: ()



   .. py:method:: translate_rao(offset)
      :abstractmethod:



   .. py:method:: default_rao_path(VesselName, revision=0)
      :staticmethod:



   .. py:method:: group_name(Vessel_LC)
      :staticmethod:


      Return the group name for the RAOs in the database

      :param Vessel_LC: Load Case



   .. py:property:: group


   .. py:method:: modify_conventions(surge: SurgeDir = SurgeDir.FWD, sway: SwayDir = SwayDir.PORT, heave: HeaveDir = HeaveDir.UP, roll: RollDir = RollDir.PORT_UP, pitch: PitchDir = PitchDir.BOW_DOWN, yaw: YawDir = YawDir.BOW_PORT, wave_origin: WaveOrigin = WaveOrigin.STERN, rot_unit: RotationUnit = RotationUnit.DEG_PER_M)

      Modify the RAO conventions to match the PyBM default. The inputs are the conventions of the data BEFORE modification.

      :param surge: Surge direction convention BEFORE modification (default: SurgeDir.FWD)
      :type surge: SurgeDir, optional
      :param sway: Sway direction convention BEFORE modification (default: SwayDir.PORT)
      :type sway: SwayDir, optional
      :param heave: Heave direction convention BEFORE modification (default: HeaveDir.UP)
      :type heave: HeaveDir, optional
      :param roll: Roll direction convention BEFORE modification (default: RollDir.PORT_UP)
      :type roll: RollDir, optional
      :param pitch: Pitch direction convention BEFORE modification (default: PitchDir.BOW_DOWN)
      :type pitch: PitchDir, optional
      :param yaw: Yaw direction convention BEFORE modification (default: YawDir.BOW_PORT)
      :type yaw: YawDir, optional
      :param wave_origin: Wave direction convention BEFORE modification (default: WaveOrigin.STERN)
      :type wave_origin: WaveOrigin, optional
      :param rot_unit: Rotation unit convention BEFORE modification (default: RotationUnit.DEG_PER_M)
      :type rot_unit: RotationUnit, optional



   .. py:method:: load_rao(filename, Vessel_LC)
      :classmethod:


      Load RAO from database.



   .. py:method:: from_api(VesselName, Vessel_LC)
      :classmethod:


      Load RAO from API.

      :param VesselName: Name of the vessel
      :param Vessel_LC: Name of the load case
      :return: RAO object
      :raises ValueError: If RAO or load case not found (with available options listed)



   .. py:method:: save_rao(filename=None, revision=None, replace=False)

      Save RAO to NetCDF file

      :param filename: filepath to save the rao
      :param replace: Replace the file if it exists, otherwise append to the data



   .. py:method:: get_roll_period()

      Get the roll period from the RAOs



   .. py:method:: plot(directions=None, amplitude=True, keys=None)

      Plot the RAO for selected directions.

      :param directions: Vector of directions. Default: All directions are used
      :param amplitude: Plot RAO amplitudes if True. Plot phases if False.




.. py:class:: MotionRAO(data_vars: xarray.core.types.DataVars | None = None, coords: collections.abc.Mapping[Any, Any] | None = None, attrs: collections.abc.Mapping[Any, Any] | None = None)

   Bases: :py:obj:`PyBM.marine.motion_analysis.RAO.RAO`


   This is the parent class for motion and force RAOs


   .. py:attribute:: __slots__
      :value: ()



   .. py:method:: translate_rao(offset)

      Translates the RAO to a point of interest. Ref[1] eq (4.27)

      :param offset: [m] (x,y,z) offset of the point of interest
      :return: Full vessel motion RAOs around POI



.. py:data:: g
   :value: 9.81


.. py:class:: SurgeDir(*args, **kwds)

   Bases: :py:obj:`enum.Enum`


   Enum for Surge direction


   .. py:attribute:: FWD
      :value: 1



   .. py:attribute:: AFT
      :value: -1



.. py:class:: SwayDir(*args, **kwds)

   Bases: :py:obj:`enum.Enum`


   Enum for Sway direction


   .. py:attribute:: PORT
      :value: 1



   .. py:attribute:: STARBOARD
      :value: -1



.. py:class:: HeaveDir(*args, **kwds)

   Bases: :py:obj:`enum.Enum`


   Enum for Heave direction


   .. py:attribute:: UP
      :value: 1



   .. py:attribute:: DOWN
      :value: -1



.. py:class:: RollDir(*args, **kwds)

   Bases: :py:obj:`enum.Enum`


   Enum for Roll direction


   .. py:attribute:: PORT_UP
      :value: 1



   .. py:attribute:: PORT_DOWN
      :value: -1



.. py:class:: PitchDir(*args, **kwds)

   Bases: :py:obj:`enum.Enum`


   Enum for Pitch direction


   .. py:attribute:: BOW_DOWN
      :value: 1



   .. py:attribute:: BOW_UP
      :value: -1



.. py:class:: YawDir(*args, **kwds)

   Bases: :py:obj:`enum.Enum`


   Enum for Yaw direction


   .. py:attribute:: BOW_PORT
      :value: 1



   .. py:attribute:: BOW_STARBOARD
      :value: -1



.. py:class:: WaveOrigin(*args, **kwds)

   Bases: :py:obj:`enum.Enum`


   Enum for Wave direction


   .. py:attribute:: STERN
      :value: 0



   .. py:attribute:: STARBOARD
      :value: 90



   .. py:attribute:: BOW
      :value: 180



   .. py:attribute:: PORT
      :value: 270



.. py:class:: RotationUnit(*args, **kwds)

   Bases: :py:obj:`enum.Enum`


   Enum for Rotation unit


   .. py:attribute:: DEG_PER_M
      :value: 1



   .. py:attribute:: RAD_PER_M


   .. py:attribute:: DEG_PER_FT
      :value: 3.28084



   .. py:attribute:: DEG_PER_DEG
      :value: 0



   .. py:attribute:: RAD_PER_RAD


.. py:function:: _recursive_group_names(groups: dict, parent=None)

   Recursively get the group names from a dictionary of groups


.. py:class:: RAO(data_vars: xarray.core.types.DataVars | None = None, coords: collections.abc.Mapping[Any, Any] | None = None, attrs: collections.abc.Mapping[Any, Any] | None = None)

   Bases: :py:obj:`xarray.Dataset`, :py:obj:`abc.ABC`


   This is the parent class for motion and force RAOs


   .. py:attribute:: __slots__
      :value: ()



   .. py:method:: translate_rao(offset)
      :abstractmethod:



   .. py:method:: default_rao_path(VesselName, revision=0)
      :staticmethod:



   .. py:method:: group_name(Vessel_LC)
      :staticmethod:


      Return the group name for the RAOs in the database

      :param Vessel_LC: Load Case



   .. py:property:: group


   .. py:method:: modify_conventions(surge: SurgeDir = SurgeDir.FWD, sway: SwayDir = SwayDir.PORT, heave: HeaveDir = HeaveDir.UP, roll: RollDir = RollDir.PORT_UP, pitch: PitchDir = PitchDir.BOW_DOWN, yaw: YawDir = YawDir.BOW_PORT, wave_origin: WaveOrigin = WaveOrigin.STERN, rot_unit: RotationUnit = RotationUnit.DEG_PER_M)

      Modify the RAO conventions to match the PyBM default. The inputs are the conventions of the data BEFORE modification.

      :param surge: Surge direction convention BEFORE modification (default: SurgeDir.FWD)
      :type surge: SurgeDir, optional
      :param sway: Sway direction convention BEFORE modification (default: SwayDir.PORT)
      :type sway: SwayDir, optional
      :param heave: Heave direction convention BEFORE modification (default: HeaveDir.UP)
      :type heave: HeaveDir, optional
      :param roll: Roll direction convention BEFORE modification (default: RollDir.PORT_UP)
      :type roll: RollDir, optional
      :param pitch: Pitch direction convention BEFORE modification (default: PitchDir.BOW_DOWN)
      :type pitch: PitchDir, optional
      :param yaw: Yaw direction convention BEFORE modification (default: YawDir.BOW_PORT)
      :type yaw: YawDir, optional
      :param wave_origin: Wave direction convention BEFORE modification (default: WaveOrigin.STERN)
      :type wave_origin: WaveOrigin, optional
      :param rot_unit: Rotation unit convention BEFORE modification (default: RotationUnit.DEG_PER_M)
      :type rot_unit: RotationUnit, optional



   .. py:method:: load_rao(filename, Vessel_LC)
      :classmethod:


      Load RAO from database.



   .. py:method:: from_api(VesselName, Vessel_LC)
      :classmethod:


      Load RAO from API.

      :param VesselName: Name of the vessel
      :param Vessel_LC: Name of the load case
      :return: RAO object
      :raises ValueError: If RAO or load case not found (with available options listed)



   .. py:method:: save_rao(filename=None, revision=None, replace=False)

      Save RAO to NetCDF file

      :param filename: filepath to save the rao
      :param replace: Replace the file if it exists, otherwise append to the data



   .. py:method:: get_roll_period()

      Get the roll period from the RAOs



   .. py:method:: plot(directions=None, amplitude=True, keys=None)

      Plot the RAO for selected directions.

      :param directions: Vector of directions. Default: All directions are used
      :param amplitude: Plot RAO amplitudes if True. Plot phases if False.




.. py:exception:: OutofBoundsError

   Bases: :py:obj:`Exception`


   Common base class for all non-exit exceptions.


.. py:function:: compute_response(wave: PyBM.marine.wave_spectrum.WaveSpectrum, rao: PyBM.marine.motion_analysis.RAO, poi=None, Nfreqs=200, f_bounds=None)

   Compute the vessel response based on the given wave spectrum and RAO.

   :param wave: The wave spectrum.
   :type wave: WaveSpectrum
   :param rao: The response amplitude operator.
   :type rao: RAO
   :param poi: The point of interest [x,y,z] in meters, defaults to None.
   :type poi: list, optional
   :param Nfreqs: The number of frequencies to consider, defaults to 200.
   :type Nfreqs: int, optional
   :param f_bounds: The frequency bounds, defaults to None.
   :type f_bounds: tuple, optional
   :return: The computed vessel response.
   :rtype: Response


.. py:function:: compute_mpe(wave: PyBM.marine.wave_spectrum.WaveSpectrum, rao: PyBM.marine.motion_analysis.RAO, poi=None, storm_duration=10800, transfer_function=None)

   Calculate MPE of the given parameter for all points of interest (POI).

   :param poi: [m] (x,y,z) offset of point of interest
   :param storm_duration: [s] duration of the period of interest (usually 3 hours)
   :param transfer_function: ([[a], [b]]) Numerator and Denumerator of continuous transfer function to be applied.
   :return: Statistical extreme value



.. py:function:: equal_energy_freqs_rao(wave: PyBM.marine.wave_spectrum.WaveSpectrum, rao: PyBM.marine.motion_analysis.RAO, Nfreqs, f_bounds=None)

.. py:function:: apply_directional_spreading(wave: PyBM.marine.wave_spectrum.WaveSpectrum, rao: PyBM.marine.motion_analysis.RAO)

.. py:class:: SpectralTools(xarray_obj)

   Tools to analyse spectra.


   .. py:attribute:: _obj


   .. py:attribute:: _amp
      :value: None



   .. py:attribute:: _m0
      :value: None



   .. py:attribute:: _m1
      :value: None



   .. py:attribute:: _m2
      :value: None



   .. py:property:: m0


   .. py:property:: m1


   .. py:property:: m2


   .. py:property:: amp


   .. py:method:: spectral_moment(order=0)

      Compute nth order spectral moment of a spectrum.
      Ref [1]. Eq (6.81)

      :param order: Order of the moment, defaults to 0
      :type order: int, optional



   .. py:property:: standard_deviation

      Compute the standard deviation from the frequency response.
      Ref. [1] Eq (6.82)

      :param m0: 0th Spectral moment
      :return: Standard deviation



   .. py:property:: zero_crossing_period

      Compute zero-crossing period.
      Ref. [1] Eq (6.84)

      :return: [s] Average zero crossing period.



   .. py:method:: MPE(storm_duration=10800, standard_deviations=None)

      Compute Most Probable Extreme from Rayleigh Distribution based on storm duration and Zero-crossing period.
      Ref [1], Section 11.1 Eq (11.20)

      :param storm_duration: [s] duration of the period of interest (usually 3 hours)
      :return: Most probable extreme.




.. py:class:: EqualEnergySpectrum(xarray_obj)

   Bases: :py:obj:`SpectralTools`


   Tools to analyse spectra optimized for equal energy frequencies.


   .. py:method:: spectral_moment(order=0)

      Compute nth order spectral moment of an equal energy spectrum.
      Ref [1]. Eq (6.81)

      :param order: Order of the moment, defaults to 0
      :type order: int, optional



.. py:class:: MotionRAO(data_vars: xarray.core.types.DataVars | None = None, coords: collections.abc.Mapping[Any, Any] | None = None, attrs: collections.abc.Mapping[Any, Any] | None = None)

   Bases: :py:obj:`PyBM.marine.motion_analysis.RAO.RAO`


   This is the parent class for motion and force RAOs


   .. py:attribute:: __slots__
      :value: ()



   .. py:method:: translate_rao(offset)

      Translates the RAO to a point of interest. Ref[1] eq (4.27)

      :param offset: [m] (x,y,z) offset of the point of interest
      :return: Full vessel motion RAOs around POI



.. py:function:: isFileLocked(filePath)

   Source: https://stackoverflow.com/questions/13371444/python-check-file-is-locked
   Checks to see if a file is locked. Performs three checks
       1. Checks if the file even exists
       2. Attempts to open the file for reading. This will determine if the file has a write lock.
           Write locks occur when the file is being edited or copied to, e.g. a file copy destination
       3. Attempts to rename the file. If this fails the file is open by some other process for reading. The
           file can be read, but not written to or deleted.
   :param filePath: path of file to check


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



