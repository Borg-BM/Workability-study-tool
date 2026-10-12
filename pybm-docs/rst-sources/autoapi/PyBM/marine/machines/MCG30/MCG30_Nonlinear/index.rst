PyBM.marine.machines.MCG30.MCG30_Nonlinear
==========================================

.. py:module:: PyBM.marine.machines.MCG30.MCG30_Nonlinear

.. autoapi-nested-parse::

   MCG System properties to compute workability. Based on the old MATLAB utilization calculations.

   References:
       [1] M:\Engineering\Database\Matlab scripts\Workability\MCG\MCG30_Utilization_Rev5.m
       [2] M:\Engineering\Database\Matlab scripts\Workability\MCG\MCG30_SystemParameters_Rev4.m



Classes
-------

.. autoapisummary::

   PyBM.marine.machines.MCG30.MCG30_Nonlinear.MCG30_Nonlinear
   PyBM.marine.machines.MCG30.MCG30_Nonlinear.MCG30TRANSFER_Nonlinear
   PyBM.marine.machines.MCG30.MCG30_Nonlinear.MCG30LIFTING_Nonlinear


Module Contents
---------------

.. py:class:: MCG30_Nonlinear(position, gw_luff_angle_mean, gw_slew_angle_mean, dp_accuracy=0.5, gw_telescope_mean=None)

   Bases: :py:obj:`PyBM.marine.machines.machine_interface.Machine_Nonlinear`, :py:obj:`abc.ABC`


   Base class for MCG 3.0 for workability studies.
   All parameters are from [2]


   .. py:attribute:: MCGref
      :value: [0, 0, 0]



   .. py:attribute:: base


   .. py:attribute:: gw_luff_angle_mean


   .. py:attribute:: gw_slew_angle_mean


   .. py:attribute:: gw_telescope_mean
      :value: None



   .. py:attribute:: dp_accuracy
      :value: 0.5



   .. py:attribute:: pos_tip


   .. py:attribute:: POI_NAMES
      :value: ['MCGref', 'base', 'tip']



   .. py:attribute:: poi_coordinates


   .. py:attribute:: workability_checks


   .. py:method:: get_POI()

      Return POI positions w.r.t. RAO definitions.



   .. py:method:: check_telescope_position(trace: xarray.Dataset, stdevs=3.7)


   .. py:method:: check_v_telescope(trace: xarray.Dataset, stdevs=3.7)


   .. py:method:: check_an_luff(trace: xarray.Dataset, stdevs=3.7)


   .. py:method:: check_max_system_pitch(trace: xarray.Dataset, stdevs=3.7)


   .. py:method:: check_max_system_roll(trace: xarray.Dataset, stdevs=3.7)


   .. py:method:: check_horizontal_acc(trace: xarray.Dataset, stdevs=3.7)


   .. py:method:: check_heave_acc(trace: xarray.Dataset, stdevs=3.7)


   .. py:method:: check_v_luff_cyl(trace: xarray.Dataset, stdevs=3.7)


   .. py:method:: check_v_slew(trace: xarray.Dataset, stdevs=3.7)


   .. py:method:: check_duty_cycle(trace: xarray.Dataset, stdevs=3.7)


   .. py:method:: translate_telescope(trace: xarray.DataArray)


   .. py:method:: translate_an_luff_world(trace: xarray.DataArray)


   .. py:method:: translate_an_luff(trace: xarray.DataArray)


   .. py:method:: translate_an_slew_world(trace: xarray.DataArray)


   .. py:method:: translate_an_slew(trace: xarray.DataArray)


   .. py:method:: translate_horizontal(trace: xarray.DataArray)


   .. py:method:: translate_luf_stroke(trace: xarray.DataArray)


   .. py:method:: get_workability_limit(trace, **kwargs)

      Get workability limits for the machine. Returns an xarray with Hs limits. (assumes linear scalability of time trace)
      :param trace: trace to calculate utilizations for.
      :type trace: xarray.Dataset



   .. py:method:: plot(axs: matplotlib.axes.Axes = None, vessel: PyBM.utils.data_classes.VesselDimensions = None, rao_origin=None)

      Plots the MCG in 3 dimensions with either a general vessel or a vessel with given dimensions.

      :param axs: Axes to plot onto.
      :type axs: Axes
      :param vessel: vessel dimensions to plot on figure
      :type vessel: VesselDimensions
      :param rao_origin: rao origin position [x,y,z]
      :type rao_origin: np.array



.. py:class:: MCG30TRANSFER_Nonlinear(position, gw_luff_angle_mean, gw_slew_angle_mean, dp_accuracy=0.1, gw_telescope_mean=None)

   Bases: :py:obj:`MCG30_Nonlinear`, :py:obj:`abc.ABC`


   Base class for MCG 3.0 for workability studies.
   All parameters are from [2]


   .. py:method:: check_an_slew_world(trace: xarray.Dataset, stdevs=3.7)


   .. py:method:: check_an_luff_world(trace: xarray.Dataset, stdevs=3.7)


.. py:class:: MCG30LIFTING_Nonlinear(position, gw_luff_angle_mean, gw_slew_angle_mean, dp_accuracy=0.1, gw_telescope_mean=None)

   Bases: :py:obj:`MCG30_Nonlinear`, :py:obj:`abc.ABC`


   Base class for MCG 3.0 for workability studies.
   All parameters are from [2]


   .. py:attribute:: lifting_radius


   .. py:method:: check_v_sys_roll(trace: xarray.Dataset, stdevs=3.7)


   .. py:method:: check_v_sys_pitch(trace: xarray.Dataset, stdevs=3.7)


   .. py:method:: check_v_heave(trace: xarray.Dataset, stdevs=3.7)


   .. py:method:: check_v_tip(trace: xarray.Dataset, stdevs=3.7)


