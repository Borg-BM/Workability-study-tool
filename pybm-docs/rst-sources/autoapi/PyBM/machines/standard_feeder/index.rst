PyBM.machines.standard_feeder
=============================

.. py:module:: PyBM.machines.standard_feeder


Submodules
----------

.. toctree::
   :maxdepth: 1

   /autoapi/PyBM/machines/standard_feeder/tower_check/index


Attributes
----------

.. autoapisummary::

   PyBM.machines.standard_feeder.design_loads
   PyBM.machines.standard_feeder.Hs_design_transit
   PyBM.machines.standard_feeder.Hs_design_operational
   PyBM.machines.standard_feeder.t700
   PyBM.machines.standard_feeder.t700_cyl_push_max
   PyBM.machines.standard_feeder.t700_cyl_pull_max
   PyBM.machines.standard_feeder.t700_cyl_pass_max
   PyBM.machines.standard_feeder.t700_cyl_pull_max_act
   PyBM.machines.standard_feeder.t700_cyl_push_max_act
   PyBM.machines.standard_feeder.g
   PyBM.machines.standard_feeder.rho


Classes
-------

.. autoapisummary::

   PyBM.machines.standard_feeder.T700
   PyBM.machines.standard_feeder.Tower
   PyBM.machines.standard_feeder.VerticalStack
   PyBM.machines.standard_feeder.massItem


Functions
---------

.. autoapisummary::

   PyBM.machines.standard_feeder.unity_checks_tower


Package Contents
----------------

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


.. py:class:: Tower

   Bases: :py:obj:`massItem`


   Represents a tower mass item.


   .. py:attribute:: D
      :type:  float
      :value: 0


      [m] Diameter of Tower



   .. py:property:: I

      Get the inertia around the center of gravity of the tower.



.. py:class:: VerticalStack(items, cog_factor=1.0)

   Bases: :py:obj:`Stack`


   Represents a vertical stack of mass items.


   .. py:property:: h

      [m] Get the height of the vertical stack.



.. py:class:: massItem

   Represents a mass item with height, mass, and center of gravity properties.


   .. py:attribute:: h
      :type:  float

      [m] height



   .. py:attribute:: m
      :type:  float

      [kg] mass



   .. py:attribute:: h_cog
      :type:  float
      :value: 0


      [m] Height of CoG



   .. py:attribute:: x_cog
      :type:  float
      :value: 0


      [m] Longitudinal offset of CoG



   .. py:attribute:: y_cog
      :type:  float
      :value: 0


      [m] transverse offset of CoG



   .. py:attribute:: I
      :type:  float
      :value: 0


      Inertia around CoG [kg.m2]



   .. py:method:: get_I() -> float

      [kg.m2] Get the inertia around the center of gravity.



   .. py:method:: set_I(value: float)

      [kg.m2] Set the inertia around the center of gravity.



   .. py:method:: I_shifted(offset)

      Get the inertia around an offset point.

      :param offset: [m] distance from stack CoG
      :return: Inertia around offset point [kg.m2]



.. py:data:: design_loads

.. py:data:: Hs_design_transit
   :value: 2.5


.. py:data:: Hs_design_operational
   :value: 2.0


.. py:data:: t700

.. py:data:: t700_cyl_push_max

.. py:data:: t700_cyl_pull_max

.. py:data:: t700_cyl_pass_max

.. py:data:: t700_cyl_pull_max_act
   :value: 1431000.0


.. py:data:: t700_cyl_push_max_act
   :value: 1431000.0


.. py:function:: unity_checks_tower(tower: PyBM.utils.mass_items.massItem, tbic: PyBM.utils.mass_items.massItem = None, lifting_tool: PyBM.utils.mass_items.massItem = None, Hs_transit: float = None, Hs_operational: float = None, debug=False) -> numpy.array

.. py:data:: g
   :value: 9.81


.. py:data:: rho
   :value: 1025


