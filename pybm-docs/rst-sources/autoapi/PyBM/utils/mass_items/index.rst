PyBM.utils.mass_items
=====================

.. py:module:: PyBM.utils.mass_items


Classes
-------

.. autoapisummary::

   PyBM.utils.mass_items.massItem
   PyBM.utils.mass_items.Tower
   PyBM.utils.mass_items.Stack
   PyBM.utils.mass_items.VerticalStack
   PyBM.utils.mass_items.HorizontalStack


Module Contents
---------------

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



.. py:class:: Tower

   Bases: :py:obj:`massItem`


   Represents a tower mass item.


   .. py:attribute:: D
      :type:  float
      :value: 0


      [m] Diameter of Tower



   .. py:property:: I

      Get the inertia around the center of gravity of the tower.



.. py:class:: Stack(items)

   Bases: :py:obj:`abc.ABC`


   Abstract base class for a stack of mass items.


   .. py:attribute:: items


   .. py:property:: m

      Get the total mass of the stack.

      :return: The total mass of the stack in units of meters [kg].
      :rtype: float



   .. py:method:: h()
      :abstractmethod:


      [m] Abstract method to get the height of the stack.



   .. py:property:: h_cog

      [m] Get the height of the center of gravity of the stack.



   .. py:property:: x_cog

      [m] Get the longitudinal offset of the center of gravity of the stack.



   .. py:property:: y_cog

      [m] Get the transverse offset of the center of gravity of the stack.



   .. py:property:: I

      Get the inertia around the center of gravity of the stack.

      :return: Inertia around the center of gravity [kg.m2]



   .. py:method:: I_shifted(offset)

      Get the inertia around an offset point.

      :param offset: [m] distance from stack CoG
      :return: Inertia around offset point [kg.m2]



   .. py:method:: __str__() -> str

      Get a string representation of the stack.



.. py:class:: VerticalStack(items, cog_factor=1.0)

   Bases: :py:obj:`Stack`


   Represents a vertical stack of mass items.


   .. py:property:: h

      [m] Get the height of the vertical stack.



.. py:class:: HorizontalStack(items, spacing, cog_factor=1.0)

   Bases: :py:obj:`Stack`


   Represents a horizontal stack of mass items.


   .. py:property:: h

      [m] Get the height of the horizontal stack.



   .. py:method:: __str__() -> str

      Get a string representation of the horizontal stack.



