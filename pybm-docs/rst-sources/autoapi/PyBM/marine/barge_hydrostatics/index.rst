PyBM.marine.barge_hydrostatics
==============================

.. py:module:: PyBM.marine.barge_hydrostatics

.. autoapi-nested-parse::

   Python class to compute barge hydrostatics

   Date: 15-05-2023
   Author: CBR
   Check: JHO



Classes
-------

.. autoapisummary::

   PyBM.marine.barge_hydrostatics.Barge


Module Contents
---------------

.. py:class:: Barge(L, B, Depth, Draft, KG, name=None)

   .. py:attribute:: name
      :value: None



   .. py:attribute:: L


   .. py:attribute:: B


   .. py:attribute:: Depth


   .. py:attribute:: Draft


   .. py:attribute:: KG


   .. py:attribute:: KB


   .. py:attribute:: _disp
      :value: None



   .. py:attribute:: _Ixx
      :value: None



   .. py:attribute:: _Iyy
      :value: None



   .. py:property:: Awl


   .. py:property:: disp


   .. py:property:: mass


   .. py:property:: Iyy

      Momement of intertia around y-axis (pitch inertia) based on solid cuboid.

      :return: [kg.m2]



   .. py:property:: Ixx

      Momement of intertia around x-axis (roll inertia) based on solid cuboid.

      :return: [kg.m2]



   .. py:property:: heave_stiffness

      Compute hydrostatic Heave stiffness of barge.

      :return: Heave stiffness [N/m]
      :rtype: float



   .. py:property:: heave_period

      Natural period of Heave.

      :return: [s]



   .. py:property:: pitch_stiffness

      Compute hydrostatic pitch stiffness of barge (for small angles).

      :return: Pitch stiffness [Nm/rad]
      :rtype: float



   .. py:property:: roll_stiffness

      Compute hydrostatic roll stiffness of barge (for small angles).

      :return: Roll stiffness [Nm/rad]
      :rtype: float



   .. py:property:: pitch_period

      Natural period of pitch.

      :return: [s]



   .. py:property:: roll_period

      Natural period of Roll.

      :return: [s]



   .. py:property:: Rxx

      Radius of gyration in Roll.

      :return: [m]



   .. py:property:: Ryy

      Radius of gyration in Pitch.

      :return: [m]



   .. py:method:: _radii_of_gyration(Inertia)


   .. py:method:: heave_stiffness_at_POI(POI: Barge.heave_stiffness_at_POI.POI) -> float

      Get heave stiffness at POI.

      :param POI: position of POI from barge center point.
      :return: [N/m] heave stiffness of POI.



   .. py:method:: __str__() -> str


   .. py:method:: roll_stats() -> str


