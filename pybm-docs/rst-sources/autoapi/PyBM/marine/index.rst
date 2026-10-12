PyBM.marine
===========

.. py:module:: PyBM.marine


Submodules
----------

.. toctree::
   :maxdepth: 1

   /autoapi/PyBM/marine/barge_hydrostatics/index
   /autoapi/PyBM/marine/machines/index
   /autoapi/PyBM/marine/motion_analysis/index
   /autoapi/PyBM/marine/tools/index
   /autoapi/PyBM/marine/wave_spectrum/index
   /autoapi/PyBM/marine/weather_hindcast/index
   /autoapi/PyBM/marine/workability/index


Attributes
----------

.. autoapisummary::

   PyBM.marine.g
   PyBM.marine.logger
   PyBM.marine.cmap


Exceptions
----------

.. autoapisummary::

   PyBM.marine.OutofBoundsError


Classes
-------

.. autoapisummary::

   PyBM.marine.HeavyFeeder
   PyBM.marine.HeavyFeederSurgeSway
   PyBM.marine.Machine_Linear
   PyBM.marine.Machine_Nonlinear
   PyBM.marine.MCG30LHIGHLOAD_Linear
   PyBM.marine.MCG30LHIGHLOAD_Nonlinear
   PyBM.marine.MCG30LLOWLOAD_Linear
   PyBM.marine.MCG30LLOWLOAD_Nonlinear
   PyBM.marine.MCG30LTRANSFER_Linear
   PyBM.marine.MCG30LTRANSFER_Nonlinear
   PyBM.marine.MCG30MHIGHLOAD_Linear
   PyBM.marine.MCG30MHIGHLOAD_Nonlinear
   PyBM.marine.MCG30MLOWLOAD_Linear
   PyBM.marine.MCG30MLOWLOAD_Nonlinear
   PyBM.marine.MCG30MTRANSFER_Linear
   PyBM.marine.MCG30MTRANSFER_Nonlinear
   PyBM.marine.T700
   PyBM.marine.RAO
   PyBM.marine.MotionRAO
   PyBM.marine.SurgeDir
   PyBM.marine.SwayDir
   PyBM.marine.HeaveDir
   PyBM.marine.RollDir
   PyBM.marine.PitchDir
   PyBM.marine.YawDir
   PyBM.marine.WaveOrigin
   PyBM.marine.RotationUnit
   PyBM.marine.SpectralTools
   PyBM.marine.EqualEnergySpectrum
   PyBM.marine.TimeDomainTools
   PyBM.marine.TimeDomain
   PyBM.marine.PiersonMoskowitz
   PyBM.marine.WaveSpectrum
   PyBM.marine.Jonswap
   PyBM.marine.Torsethaugen
   PyBM.marine.Machine_Linear
   PyBM.marine.Machine_Nonlinear
   PyBM.marine.workability_accessor


Functions
---------

.. autoapisummary::

   PyBM.marine._recursive_group_names
   PyBM.marine.compute_response
   PyBM.marine.compute_mpe
   PyBM.marine.equal_energy_freqs_rao
   PyBM.marine.apply_directional_spreading
   PyBM.marine.isFileLocked
   PyBM.marine.Octopus_to_RAO
   PyBM.marine.get_speeds
   PyBM.marine.get_wave_directions
   PyBM.marine.get_wave_frequencies
   PyBM.marine.LIS_to_RAO
   PyBM.marine.load_LIS
   PyBM.marine.XLS_to_RAO
   PyBM.marine.load_XLS
   PyBM.marine.CSV_to_RAO
   PyBM.marine.load_CSV
   PyBM.marine.TXT_to_RAO
   PyBM.marine.load_TXT
   PyBM.marine.__file_len
   PyBM.marine.resample
   PyBM.marine.__read_file
   PyBM.marine.read_res
   PyBM.marine.write_pickle
   PyBM.marine.write_res
   PyBM.marine.wrap
   PyBM.marine.directional_workability
   PyBM.marine.directional_workability_timetrace
   PyBM.marine._polar_plotter
   PyBM.marine.multicolored_line
   PyBM.marine.multiple_lines
   PyBM.marine.set_polar_plot_params
   PyBM.marine.plot_ship
   PyBM.marine._make_legend_proxies


Package Contents
----------------

.. py:class:: HeavyFeeder(position, orientation, comp_point=[0, 0, 0])

   Bases: :py:obj:`PyBM.marine.machines.machine_interface.Machine_Linear`


   Helper class that provides a standard way to create an ABC using
   inheritance.


   .. py:attribute:: cyl_arm_roll
      :value: 10.409



   .. py:attribute:: cyl_arm_pitch
      :value: 7.327



   .. py:attribute:: tds_arm_roll
      :value: 11.43



   .. py:attribute:: tds_arm_pitch
      :value: 8



   .. py:attribute:: cb_to_tbic_top
      :value: 6.42



   .. py:attribute:: vmax
      :value: 0.455



   .. py:attribute:: bore
      :value: 0.47



   .. py:attribute:: rod
      :value: 0.23



   .. py:attribute:: stroke
      :value: 1.1



   .. py:attribute:: p_hpu
      :value: 31500000.0



   .. py:attribute:: p_hold_bot
      :value: 35000000.0



   .. py:attribute:: p_hold_rod
      :value: 42000000.0



   .. py:attribute:: comp_point_max_horizontal_motion
      :value: 2.0



   .. py:attribute:: cylinder


   .. py:attribute:: CYLINDER_NAMES
      :value: ['c1', 'c2']



   .. py:attribute:: N_CYLINDERS
      :value: 2



   .. py:attribute:: POI_NAMES
      :value: ['central_bearing', 'comp_point']



   .. py:property:: c1


   .. py:property:: c2


   .. py:attribute:: cylinder_coordinates


   .. py:attribute:: comp_point_wrt_cb


   .. py:attribute:: comp_point


   .. py:attribute:: workability_checks


   .. py:method:: get_POI()

      Return cylinder positions w.r.t. RAO definitions.



   .. py:method:: apply_machine_dofs(rao)


   .. py:method:: check_stroke_limit(motion_at_poi)


   .. py:method:: check_cylinder_velocity_limit(motion_at_poi)


   .. py:method:: check_horizontal_motion_no_comp(motion_at_poi)


   .. py:method:: check_horizontal_motion(motion_at_poi)


   .. py:method:: plot(axs: matplotlib.axes.Axes = None)


.. py:class:: HeavyFeederSurgeSway(position, orientation, comp_point=[0, 0, 0])

   Bases: :py:obj:`PyBM.marine.machines.HeavyFeeder.HeavyFeeder`


   Helper class that provides a standard way to create an ABC using
   inheritance.


   .. py:attribute:: workability_checks


   .. py:method:: get_POI()

      Return cylinder positions w.r.t. RAO definitions.



   .. py:method:: apply_machine_dofs(rao)


   .. py:method:: check_stroke_limit(motion_at_poi)


.. py:class:: Machine_Linear(position, orientation)

   Bases: :py:obj:`abc.ABC`


   Helper class that provides a standard way to create an ABC using
   inheritance.


   .. py:attribute:: pos


   .. py:attribute:: orient


   .. py:attribute:: rotation


   .. py:method:: apply_transform(point: numpy.array) -> numpy.array

      Apply rotation then translation to 3D point

      :param point: 3D vector [x,y,z]
      :type point: np.array
      :return: Transformed position
      :rtype: np.array



   .. py:method:: get_rao_at_poi(rao) -> PyBM.marine.motion_analysis.MotionRAO.MotionRAO

      Get the Motion RAOs at the POI



   .. py:method:: get_POI() -> dict
      :abstractmethod:



   .. py:method:: apply_machine_dofs(rao) -> PyBM.marine.motion_analysis.MotionRAO.MotionRAO


   .. py:method:: get_workability_limit(motion_at_poi, **kwargs)


   .. py:method:: __str__() -> str


.. py:class:: Machine_Nonlinear(position, orientation)

   Bases: :py:obj:`abc.ABC`


   Helper class that provides a standard way to create an ABC using
   inheritance.


   .. py:attribute:: pos


   .. py:attribute:: orient


   .. py:attribute:: rotation


   .. py:method:: apply_transform(point: numpy.array) -> numpy.array

      Apply rotation then translation to 3D point

      :param point: 3D vector [x,y,z]
      :type point: np.array
      :return: Transformed position
      :rtype: np.array



   .. py:method:: get_POI() -> dict
      :abstractmethod:



.. py:class:: MCG30LHIGHLOAD_Linear(position, gw_luff_angle_mean, gw_slew_angle_mean, dp_accuracy=0.1, gw_telescope_mean=None)

   Bases: :py:obj:`mcg30_helper.MCG30LHIGHLOAD_Params`, :py:obj:`MCG30_Linear.MCG30LIFTING_Linear`


   Helper class that provides a standard way to create an ABC using
   inheritance.


.. py:class:: MCG30LHIGHLOAD_Nonlinear(position, gw_luff_angle_mean, gw_slew_angle_mean, dp_accuracy=0.1, gw_telescope_mean=None)

   Bases: :py:obj:`mcg30_helper.MCG30LHIGHLOAD_Params`, :py:obj:`MCG30_Nonlinear.MCG30LIFTING_Nonlinear`


   Helper class that provides a standard way to create an ABC using
   inheritance.


.. py:class:: MCG30LLOWLOAD_Linear(position, gw_luff_angle_mean, gw_slew_angle_mean, dp_accuracy=0.1, gw_telescope_mean=None)

   Bases: :py:obj:`mcg30_helper.MCG30LLOWLOAD_Params`, :py:obj:`MCG30_Linear.MCG30LIFTING_Linear`


   Helper class that provides a standard way to create an ABC using
   inheritance.


.. py:class:: MCG30LLOWLOAD_Nonlinear(position, gw_luff_angle_mean, gw_slew_angle_mean, dp_accuracy=0.1, gw_telescope_mean=None)

   Bases: :py:obj:`mcg30_helper.MCG30LLOWLOAD_Params`, :py:obj:`MCG30_Nonlinear.MCG30LIFTING_Nonlinear`


   Helper class that provides a standard way to create an ABC using
   inheritance.


.. py:class:: MCG30LTRANSFER_Linear(position, gw_luff_angle_mean, gw_slew_angle_mean, dp_accuracy=0.1, gw_telescope_mean=None)

   Bases: :py:obj:`mcg30_helper.MCG30LTRANSFER_Params`, :py:obj:`MCG30_Linear.MCG30TRANSFER_Linear`


   Helper class that provides a standard way to create an ABC using
   inheritance.


.. py:class:: MCG30LTRANSFER_Nonlinear(position, gw_luff_angle_mean, gw_slew_angle_mean, dp_accuracy=0.1, gw_telescope_mean=None)

   Bases: :py:obj:`mcg30_helper.MCG30LTRANSFER_Params`, :py:obj:`MCG30_Nonlinear.MCG30TRANSFER_Nonlinear`


   Helper class that provides a standard way to create an ABC using
   inheritance.


.. py:class:: MCG30MHIGHLOAD_Linear(position, gw_luff_angle_mean, gw_slew_angle_mean, dp_accuracy=0.1, gw_telescope_mean=None)

   Bases: :py:obj:`mcg30_helper.MCG30MHIGHLOAD_Params`, :py:obj:`MCG30_Linear.MCG30LIFTING_Linear`


   Helper class that provides a standard way to create an ABC using
   inheritance.


.. py:class:: MCG30MHIGHLOAD_Nonlinear(position, gw_luff_angle_mean, gw_slew_angle_mean, dp_accuracy=0.1, gw_telescope_mean=None)

   Bases: :py:obj:`mcg30_helper.MCG30MHIGHLOAD_Params`, :py:obj:`MCG30_Nonlinear.MCG30LIFTING_Nonlinear`


   Helper class that provides a standard way to create an ABC using
   inheritance.


.. py:class:: MCG30MLOWLOAD_Linear(position, gw_luff_angle_mean, gw_slew_angle_mean, dp_accuracy=0.1, gw_telescope_mean=None)

   Bases: :py:obj:`mcg30_helper.MCG30MLOWLOAD_Params`, :py:obj:`MCG30_Linear.MCG30LIFTING_Linear`


   Helper class that provides a standard way to create an ABC using
   inheritance.


.. py:class:: MCG30MLOWLOAD_Nonlinear(position, gw_luff_angle_mean, gw_slew_angle_mean, dp_accuracy=0.1, gw_telescope_mean=None)

   Bases: :py:obj:`mcg30_helper.MCG30MLOWLOAD_Params`, :py:obj:`MCG30_Nonlinear.MCG30LIFTING_Nonlinear`


   Helper class that provides a standard way to create an ABC using
   inheritance.


.. py:class:: MCG30MTRANSFER_Linear(position, gw_luff_angle_mean, gw_slew_angle_mean, dp_accuracy=0.1, gw_telescope_mean=None)

   Bases: :py:obj:`mcg30_helper.MCG30MTRANSFER_Params`, :py:obj:`MCG30_Linear.MCG30TRANSFER_Linear`


   Helper class that provides a standard way to create an ABC using
   inheritance.


.. py:class:: MCG30MTRANSFER_Nonlinear(position, gw_luff_angle_mean, gw_slew_angle_mean, dp_accuracy=0.1, gw_telescope_mean=None)

   Bases: :py:obj:`mcg30_helper.MCG30MTRANSFER_Params`, :py:obj:`MCG30_Nonlinear.MCG30TRANSFER_Nonlinear`


   Helper class that provides a standard way to create an ABC using
   inheritance.


.. py:class:: T700(position, orientation, P_passive=35000000.0)

   Bases: :py:obj:`PyBM.marine.machines.machine_interface.Machine_Linear`


   Helper class that provides a standard way to create an ABC using
   inheritance.


   .. py:attribute:: cd
      :value: 13.8



   .. py:attribute:: vmax
      :value: 0.736



   .. py:attribute:: vmax_center
      :value: 0.44



   .. py:attribute:: stroke
      :value: 2.2



   .. py:attribute:: max_flow
      :value: 0.044



   .. py:attribute:: bore
      :value: 0.42



   .. py:attribute:: rod
      :value: 0.33



   .. py:attribute:: rod_center
      :value: 0.26



   .. py:attribute:: cylinder


   .. py:attribute:: CYLINDER_NAMES
      :value: ['c1', 'c2', 'c3']



   .. py:attribute:: N_CYLINDERS
      :value: 3



   .. py:attribute:: POI_NAMES
      :value: ['center', 'c1', 'c2', 'c3']



   .. py:property:: h


   .. py:property:: c1


   .. py:property:: c2


   .. py:property:: c3


   .. py:attribute:: P_passive
      :value: 35000000.0



   .. py:attribute:: cylinder_coordinates


   .. py:attribute:: workability_checks


   .. py:method:: get_POI()

      Return cylinder positions w.r.t. RAO definitions.



   .. py:method:: check_stroke_limit(motion_at_poi)


   .. py:method:: check_cylinder_velocity_limit(motion_at_poi)


   .. py:method:: check_platform_velocity_limit(motion_at_poi)


   .. py:method:: compute_cylinder_forces(Fz, Mx, My)


   .. py:method:: plot(axs: matplotlib.axes.Axes = None)


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


.. py:class:: PiersonMoskowitz(Hs, Tp, main_direction, Ndirs=11, spreading=4.0)

   Bases: :py:obj:`PyBM.marine.wave_spectrum.WaveSpectrum.WaveSpectrum`


   This class defines the Pierson Moskowitz Frequency spectrum.


   .. py:method:: power_spectrum(freqs)

      Compute frequency spectrum for the given frequency points.

      :param freqs: [Hz] list of frequency components
      :return: [m2/Hz] Wave spectral density



   .. py:method:: _power_spectrum(freqs, Tp, Hs)
      :staticmethod:


      Ref [2] 3.5.5.1

      :param Hs: [m] Significant wave height
      :param Tp: [s] Peak period



.. py:class:: WaveSpectrum(Hs, Tp, main_direction, Ndirs=11, spreading=4.0)

   Bases: :py:obj:`abc.ABC`


   Helper class that provides a standard way to create an ABC using
   inheritance.


   .. py:property:: Hs


   .. py:property:: Tp


   .. py:property:: main_direction

      [deg] Main direction of wave.



   .. py:attribute:: spreading
      :value: 4.0



   .. py:property:: Ndirs

      [-] Number of wave directions to use (should be odd).



   .. py:method:: __str__()


   .. py:method:: power_spectrum(freqs)
      :abstractmethod:


      Compute frequency spectrum for the given frequency points.

      :param freqs: [Hz] list of frequency components
      :param plot: True to plot spectrum
      :return: [m2/(rad/s)] Wave spectral density



   .. py:method:: wave_spectrum(freqs)

      Compute frequency spectrum for the given frequency points.

      :param freqs: [Hz] list of frequency components
      :param plot: True to plot spectrum
      :return: [m2/(rad/s)] Wave spectral density



   .. py:method:: equal_energy_frequencies(bounds, df=None, Nfreqs=100)

      Numeric method to calculate frequencies at equal energies.

      :param Nfreqs: NUmber of frequency components to generate, defaults to 100
      :type Nfreqs: int, optional



   .. py:method:: equal_energy_directions(Ndirs=None)

      Compute the directions to use for equal energy directional spreading.

      :param Ndirs: [-] number of directions (must be odd)
      :return: [deg] Vector of directions



   .. py:method:: equal_energy_method(func_power_spectrum, bounds, N)
      :staticmethod:


      Numeric equal area method.
      :param func_power_spectrum: Function that outputs the power spectrum, such as a wave spectrum power spectrum or a spreading function. Must accept array of x coordinates, and output either a xr.DataArray or an array of y.
      :param bounds: bounds of X, as an array or tuple: (xmin, xmax)
      :param N: Number of X to divide energy over



   .. py:method:: directional_wave_spectrum(freqs, Rel_Dirs)

      Compute combined directional wave spectrum.

      :param freqs: [Hz] list of frequency components
      :param Rel_Dirs: [deg] list of wave directions relative to main direction (between -180 and 180 degrees).

      :return: [m2/Hz] Wave spectral density



   .. py:method:: abs_directions(Rel_Dirs)


   .. py:method:: equal_energy_directional_wave_spectrum(freqs, Ndirs=None)

      Compute directional wave spectrim with spreading using equal energy directions.

      :param freqs: [Hz] Vector of frequency points
      :param Ndirs: [-] Number of directions (must be odd)
      :return: Directional wave Spectrum



   .. py:method:: equal_energy_directional_spreading(Ndirs=None)

      Compute directional wave spreading using equal energy directions.

      :param Ndirs: [-] Number of directions (must be odd)
      :param plot: plots the spectrum if True
      :return: Directional wave spreading



   .. py:method:: directional_spreading(relative_dirs)

      Compute directional spreading factors for the given directions.

      Function is based on the Cos^n function defined in the Orcaflex documentation.

      :param relative_dirs: [deg] list of wave directions relative to main direction (between -180 and 180 degrees).
      :param plot: True to plot directional spreading
      :return: [-] spreading factor corresponding to each direction



   .. py:method:: shift_direction(wave_data, angle_shift)
      :staticmethod:



   .. py:method:: plot(freqs, Rel_Dirs, ax=None)


.. py:data:: logger

.. py:class:: Jonswap(Hs, Tp, main_direction, Ndirs=11, spreading=4, gamma=None)

   Bases: :py:obj:`PyBM.marine.wave_spectrum.WaveSpectrum.WaveSpectrum`


   This class defines the JONSWAP Frequency spectrum.

   :param Hs: [m] Significant wave height
   :param Tp: [s] Peak period
   :param main_direction: [deg] Wave direction: 0 is from stern 180 from bow, 90 from starboard
   :param Ndirs: [-] Number of wave directions
   :param spreading: [-] Wave spreading, unidirectional is used if spreading =< 0
   :param gamma: [-] Peakness factor, according to DNV if not specified


   .. py:method:: __str__()


   .. py:property:: gamma


   .. py:property:: Tz

      Zero up-crossing period [s]



   .. py:method:: Tz_to_Tp(Tz)
      :staticmethod:


      Convert zero up-crossing period to peak period [s]

      :param Tz: Zero up-crossing period [s]
      :return: Peak period [s]



   .. py:method:: _compute_gamma(Tp, Hs)
      :staticmethod:


      Compute gamma according to DNV regulations [2] 3.5.5.5

      :param Tp: Peak Period [s]
      :param Hs: Significant wave height [m]
      :return: [-] peakedness factor



   .. py:method:: compute_gamma()


   .. py:method:: power_spectrum(freqs: xarray.DataArray)

      Compute frequency spectrum for the given frequency points.

      :param freqs: [Hz] list of frequency components
      :return: [m2/Hz] Wave spectral density



   .. py:method:: _power_spectrum(freqs, gamma, Tp, Hs)
      :staticmethod:



.. py:class:: Torsethaugen(Hs, Tp, main_direction, Ndirs=11, spreading=4, offset=0)

   Bases: :py:obj:`PyBM.marine.wave_spectrum.WaveSpectrum.WaveSpectrum`


   This class defines the Torsethaugen Frequency spectrum.


   .. py:attribute:: offset
      :value: 0



   .. py:method:: power_spectrum(freqs)

      Compute frequency spectrum for the given frequency points.

      :param freqs: [Hz] list of frequency components
      :param Npeak: [0, 1 or 2] 0: use full Torsethaugen spectrum. 1: use first peak only. 2: use second peak only
      :return: [m2/Hz] Wave spectral density



   .. py:method:: _power_spectrum_parameters(Tp, Hs)
      :staticmethod:


      Compute power spectral parameters for the Torsethaugen double peak spectrum
      :param Tp: peak wave period
      :param Hs: significant wave height
      :return: [H1, Tp1, H2, Tp2, y, winddominated]



   .. py:method:: _power_spectrum(freqs, Tp, Hs)
      :staticmethod:


      Calculate the double peaked power spectrum of the Torsethaugen paper (simplified)
      :params freqs: frequencies of the spectral density result
      :param Tp: peak wave period
      :param Hs: significant wave height
      :return: [H1, Tp1, H2, Tp2, y, winddominated]



   .. py:method:: dual_equal_energy_directional_wave_spectrum(freqs, offset=90, Ndirs=None)

      Compute dual peak, combined directional wave spectrum. Uses two JONSWAP spectrums offset by 90 deg or whatever specified.

      :param freqs: [Hz] Vector of frequency points
      :param offset: [deg] directionality offset between first peak spectrum and second peak spectrum
      :param Ndirs: [-] Number of directions (must be odd)
      :return: Directional wave Spectrum



   .. py:method:: equal_energy_directional_wave_spectrum(freqs, Ndirs=None)

      Compute directional wave spectrim with spreading using equal energy directions.

      :param freqs: [Hz] Vector of frequency points
      :param Ndirs: [-] Number of directions (must be odd)
      :return: Directional wave Spectrum



.. py:function:: wrap(angle)

.. py:class:: Machine_Linear(position, orientation)

   Bases: :py:obj:`abc.ABC`


   Helper class that provides a standard way to create an ABC using
   inheritance.


   .. py:attribute:: pos


   .. py:attribute:: orient


   .. py:attribute:: rotation


   .. py:method:: apply_transform(point: numpy.array) -> numpy.array

      Apply rotation then translation to 3D point

      :param point: 3D vector [x,y,z]
      :type point: np.array
      :return: Transformed position
      :rtype: np.array



   .. py:method:: get_rao_at_poi(rao) -> PyBM.marine.motion_analysis.MotionRAO.MotionRAO

      Get the Motion RAOs at the POI



   .. py:method:: get_POI() -> dict
      :abstractmethod:



   .. py:method:: apply_machine_dofs(rao) -> PyBM.marine.motion_analysis.MotionRAO.MotionRAO


   .. py:method:: get_workability_limit(motion_at_poi, **kwargs)


   .. py:method:: __str__() -> str


.. py:class:: Machine_Nonlinear(position, orientation)

   Bases: :py:obj:`abc.ABC`


   Helper class that provides a standard way to create an ABC using
   inheritance.


   .. py:attribute:: pos


   .. py:attribute:: orient


   .. py:attribute:: rotation


   .. py:method:: apply_transform(point: numpy.array) -> numpy.array

      Apply rotation then translation to 3D point

      :param point: 3D vector [x,y,z]
      :type point: np.array
      :return: Transformed position
      :rtype: np.array



   .. py:method:: get_POI() -> dict
      :abstractmethod:



.. py:data:: cmap

.. py:class:: workability_accessor(obj)

   .. py:attribute:: _obj


   .. py:method:: table(Hs, Hsrange)


   .. py:method:: byscatter(scatter)


   .. py:method:: plot_detailed_workability(max_hs=None, fig=None)

      Plot workability for each system limit.

      :param workability_result: _description_
      :type workability_result: xr.DataArray
      :param max_hs: _description_, defaults to None
      :type max_hs: _type_, optional
      :param fig: _description_, defaults to None
      :type fig: _type_, optional



   .. py:method:: plot_combined_workability(max_hs=None, fig=None)

      Plot the result of the workability in polar plots

      :param workability_result: [m] Array of limiting Hs for each wave peak period, direction and machine limit.
      :param max_hs: [m] maximum Hs on the polar plot, defaults to None
      :param fig: figure to plot on, defaults to None



.. py:function:: directional_workability(rao: PyBM.marine.MotionRAO, wave: PyBM.marine.WaveSpectrum, machine: PyBM.marine.machines.Machine_Linear, **kwargs) -> xarray.DataArray

   Compute the workability of the machine for the given wave directions.

   :return: [m] Array of limiting Hs for each wave peak period, direction and machine limit.


.. py:function:: directional_workability_timetrace(trace: xarray.DataArray, machine: PyBM.marine.machines.MCG30.MCG30_Nonlinear, **kwargs) -> xarray.DataArray

   Compute the workability of the machine using the time trace supplied (MCG)

   :return: [m] Array of limiting Hs for each wave peak period, direction and machine limit.


.. py:function:: _polar_plotter(plot_method, workability_result: xarray.DataArray, max_hs=None, fig: matplotlib.figure.Figure = None)

.. py:function:: multicolored_line(ax: matplotlib.pyplot.Axes, Tp_result)

.. py:function:: multiple_lines(ax: matplotlib.pyplot.Axes, Tp_result)

.. py:function:: set_polar_plot_params(ax: matplotlib.pyplot.Axes, max_y, Tp)

.. py:function:: plot_ship(ax: matplotlib.pyplot.Axes, plot_diameter=1.0)

   Plot a ship contour on the given axis.

   :param axs: Axes to plot on.
   :param plot_diameter: diameter of vessel contour, defaults to 1.0


.. py:function:: _make_legend_proxies(cmap, **kwargs)

