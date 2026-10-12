PyBM.machines.heavy_feeder
==========================

.. py:module:: PyBM.machines.heavy_feeder


Submodules
----------

.. toctree::
   :maxdepth: 1

   /autoapi/PyBM/machines/heavy_feeder/tower_check/index


Attributes
----------

.. autoapisummary::

   PyBM.machines.heavy_feeder.design_loads
   PyBM.machines.heavy_feeder.Hs_design
   PyBM.machines.heavy_feeder.g
   PyBM.machines.heavy_feeder.rho


Classes
-------

.. autoapisummary::

   PyBM.machines.heavy_feeder.Tower
   PyBM.machines.heavy_feeder.VerticalStack
   PyBM.machines.heavy_feeder.massItem


Functions
---------

.. autoapisummary::

   PyBM.machines.heavy_feeder.unity_checks_tower


Package Contents
----------------

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

.. py:data:: Hs_design
   :value: 2.5


.. py:function:: unity_checks_tower(tower: PyBM.utils.mass_items.massItem, tbic: PyBM.utils.mass_items.massItem = None, lifting_tool: PyBM.utils.mass_items.massItem = None, Hs: float = None) -> numpy.array

   Calculate unity checks of a different tower w.r.t. the heavy feeder design conditions.

   :param tower: Tower properties
   :type tower: massItem
   :param tbic: TBIC properties, by default the vinyard TBIC will be used.
   :type tbic: massItem
   :param lifting_tool: Lifting tool properties, by default the vinyard tool will be used.
   :type lifting_tool: massItem
   :param Hs: [m] Significant Waave height used for acceleration scaling, defaults to 2.5m
   :type Hs: float
   :return: list of unity checks [Fz, Mx, My]
   :rtype: np.array


.. py:data:: g
   :value: 9.81


.. py:data:: rho
   :value: 1025


