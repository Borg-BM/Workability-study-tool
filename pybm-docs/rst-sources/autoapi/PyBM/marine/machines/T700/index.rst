PyBM.marine.machines.T700
=========================

.. py:module:: PyBM.marine.machines.T700

.. autoapi-nested-parse::

   T700 System properties to compute workability

   References:
       [1] RA53967897_AC_1_GEZ_001
       [2] TWD-2015-006-D-100-REV-1, FOUNDATION -GENERAL ARRANGEMENT
       [3] T700_SystemParameters_Rev0



Attributes
----------

.. autoapisummary::

   PyBM.marine.machines.T700.pos


Classes
-------

.. autoapisummary::

   PyBM.marine.machines.T700.T700


Module Contents
---------------

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


.. py:data:: pos
   :value: [10, 20, 0]


