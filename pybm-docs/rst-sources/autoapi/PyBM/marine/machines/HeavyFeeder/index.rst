PyBM.marine.machines.HeavyFeeder
================================

.. py:module:: PyBM.marine.machines.HeavyFeeder

.. autoapi-nested-parse::

   Heavy Feeder class to compute workability

   References:


       [1] TWD-NL-2021-512-D-010-REV-2, General Arrangement CYLINDER NUMBERING
       [2] NL002692-02-50-2000-HYD-0001-RAF Hydraulic diagram Roll Pitch Cylinder assembly_AB



Classes
-------

.. autoapisummary::

   PyBM.marine.machines.HeavyFeeder.HeavyFeeder


Module Contents
---------------

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


