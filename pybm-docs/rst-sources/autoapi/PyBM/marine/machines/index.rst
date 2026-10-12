PyBM.marine.machines
====================

.. py:module:: PyBM.marine.machines


Submodules
----------

.. toctree::
   :maxdepth: 1

   /autoapi/PyBM/marine/machines/HeavyFeeder/index
   /autoapi/PyBM/marine/machines/HeavyFeederSurgeSway/index
   /autoapi/PyBM/marine/machines/MCG30/index
   /autoapi/PyBM/marine/machines/T700/index
   /autoapi/PyBM/marine/machines/machine_interface/index


Classes
-------

.. autoapisummary::

   PyBM.marine.machines.HeavyFeeder
   PyBM.marine.machines.HeavyFeederSurgeSway
   PyBM.marine.machines.Machine_Linear
   PyBM.marine.machines.Machine_Nonlinear
   PyBM.marine.machines.MCG30LHIGHLOAD_Linear
   PyBM.marine.machines.MCG30LHIGHLOAD_Nonlinear
   PyBM.marine.machines.MCG30LLOWLOAD_Linear
   PyBM.marine.machines.MCG30LLOWLOAD_Nonlinear
   PyBM.marine.machines.MCG30LTRANSFER_Linear
   PyBM.marine.machines.MCG30LTRANSFER_Nonlinear
   PyBM.marine.machines.MCG30MHIGHLOAD_Linear
   PyBM.marine.machines.MCG30MHIGHLOAD_Nonlinear
   PyBM.marine.machines.MCG30MLOWLOAD_Linear
   PyBM.marine.machines.MCG30MLOWLOAD_Nonlinear
   PyBM.marine.machines.MCG30MTRANSFER_Linear
   PyBM.marine.machines.MCG30MTRANSFER_Nonlinear
   PyBM.marine.machines.T700


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


