PyBM.marine.motion_analysis.RAO
===============================

.. py:module:: PyBM.marine.motion_analysis.RAO

.. autoapi-nested-parse::

   Base class for RAOs of Vessels. Inherits xarray.Dataset.

   Each dataarray must have coordinates
   - Frequency [Hz]
   - Direction [deg] - Must be from 0 to 360 deg (full circle), including 0 and 360 deg. 0 deg means waves coming from the stern direction, 90 deg starboard, 180 deg bow, 270 deg port
   - DOF: ["X", "Y", "Z", "Rx", "Ry", "Rz"]
   Values of the dataarray are in [m/m] or [deg/m] (angle)

   The following conventions should ALWAYS be used for the RAO:
    - Surge: Forward
    - Sway: to Port
    - Heave: Up
    - Roll: Port up
    - Pitch: Bow down
    - Yaw: Bow to port

    Wave directions:
   - 0 deg: Waves coming from the stern
   - 90 deg: Waves coming from starboard


   CBR 21-06-2023



Classes
-------

.. autoapisummary::

   PyBM.marine.motion_analysis.RAO.SurgeDir
   PyBM.marine.motion_analysis.RAO.SwayDir
   PyBM.marine.motion_analysis.RAO.HeaveDir
   PyBM.marine.motion_analysis.RAO.RollDir
   PyBM.marine.motion_analysis.RAO.PitchDir
   PyBM.marine.motion_analysis.RAO.YawDir
   PyBM.marine.motion_analysis.RAO.WaveOrigin
   PyBM.marine.motion_analysis.RAO.RotationUnit
   PyBM.marine.motion_analysis.RAO.RAO


Functions
---------

.. autoapisummary::

   PyBM.marine.motion_analysis.RAO._recursive_group_names


Module Contents
---------------

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




