PyBM.hydraulics.buckling
========================

.. py:module:: PyBM.hydraulics.buckling


Functions
---------

.. autoapisummary::

   PyBM.hydraulics.buckling.calculate_cyl_deadlength
   PyBM.hydraulics.buckling.buckling_check
   PyBM.hydraulics.buckling.get_min_rod_diameter


Module Contents
---------------

.. py:function:: calculate_cyl_deadlength(d_bore)

   Calculate total length of cylinder.
   based on rule of thumb calculation by BHO ('template cylinder sizing.xlsx')

   :param stroke: [m] Stroke of cylinder
   :param diameter: [m] Diameter of cylinder
   :return: [m] Dead length of cylinder


.. py:function:: buckling_check(Fz, d_rod, buckling_length, E=210000000000.0)

   Check for buckling of the cylinder rod. (acc. BHO 'template cylinder sizing.xlsx')

   :param Fz: [N] Axial force
   :param bore: [m] Bore of cylinder
   :param rod: [m] Rod of cylinder
   :param buckling_length: [m] Length of cylinder rod
   :param E: [Pa] Young's modulus of cylinder
   :return: [bool] True if buckling occurs


.. py:function:: get_min_rod_diameter(Fz, buckling_length, E=210000)

   Check for buckling of the cylinder rod. (acc. BHO 'template cylinder sizing.xlsx')

   :param Fz: [N] Axial force
   :param bore: [m] Bore of cylinder
   :param rod: [m] Rod of cylinder
   :param buckling_length: [m] Length of cylinder rod
   :param E: [N/mm^2] Young's modulus of cylinder
   :return: [bool] True if buckling occurs


