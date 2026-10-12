PyBM.hydraulics.accu_cylinder_combination
=========================================

.. py:module:: PyBM.hydraulics.accu_cylinder_combination

.. autoapi-nested-parse::

   Python class to compute Accumulator properties

   Date: 15-05-2023
   Author: CBR
   Check: ---



Classes
-------

.. autoapisummary::

   PyBM.hydraulics.accu_cylinder_combination.AccuCylinderCombination


Module Contents
---------------

.. py:class:: AccuCylinderCombination(Vaccu, Pmax, Acyl, stroke)

   .. py:attribute:: accu


   .. py:attribute:: cyl


   .. py:method:: get_V1(Pcyl)

      Volume of Accu at point Pcyl

      :param Pcyl: [m] Cylinder position (0 is retracted).
      :return: [m3] Volume at point Pcyl



   .. py:method:: get_p1(Pcyl)

      Get Pressure at at point Pcyl.

      :param Pcyl: [m] Cylinder position (0 is retracted).
      :return: [Pa] pressure for Pcyl.



   .. py:method:: get_cyl_force(Pcyl)

      Cylinder force at point Pcyl

      :param Pcyl: [m] Cylinder position (0 is retracted).
      :return: [N] Force for Pcyl.



   .. py:method:: get_pressure_ratio(Pcyl)

      Ratio of Max Pressure to pressure at point Pcyl

      :param Pcyl: [m] Cylinder position (0 is retracted).
      :return: [Pa] pressure for Pcyl.



   .. py:method:: mass_estimate()

      Total mass estimate.

      :return: [kg] mass



   .. py:method:: __str__() -> str


   .. py:method:: from_pressure_ratio_and_1_point(pressure_ratio, L1, Acyl, P2, stroke, Max_Vaccu=np.inf)
      :classmethod:



   .. py:method:: from_pressure_ratio_and_2_points(pressure_ratio, L2, L1, Acyl, P2, stroke, Max_Vaccu=np.inf)
      :classmethod:


      Create class based on pressure ratio at 2 desired points.

      :param pressure_ratio: [-] P1/P2 ratio off desired pressures
      :param L2: [m] Length of cylinder at position 2 (corresponding to P2)
      :param L1: [m] Length of cylinder at position 1 (corresponding to P1)
      :param A: [m2] Cylinder Area
      :param P2: [Pa] Pressure at Point 2 of Accumulator



   .. py:method:: from_pressure_ratio_and_V2(pressure_ratio, L1, V2, Fcyl, stroke, Max_P2=np.inf)
      :classmethod:


      Create class based on pressure ratio and V2

      :param pressure_ratio: [-] P1/P2 ratio off desired pressures
      :param L1: [m] Length of cylinder at position 1 (corresponding to P1)
      :param V2: [m3] Volume of accumulator
      :param Fcyl: [N] maximum force of Cylinder



   .. py:method:: plot_force(axs=None)

      Plot properties of the combination.

      :param axs: Axes to plot on, defaults to None



