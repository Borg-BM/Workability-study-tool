PyBM.hydraulics
===============

.. py:module:: PyBM.hydraulics


Submodules
----------

.. toctree::
   :maxdepth: 1

   /autoapi/PyBM/hydraulics/VariablePressureAccumulator/index
   /autoapi/PyBM/hydraulics/accu_cylinder_combination/index
   /autoapi/PyBM/hydraulics/accumulator/index
   /autoapi/PyBM/hydraulics/buckling/index
   /autoapi/PyBM/hydraulics/cylinder/index


Classes
-------

.. autoapisummary::

   PyBM.hydraulics.AccuCylinderCombination
   PyBM.hydraulics.Accumulator
   PyBM.hydraulics.Cylinder
   PyBM.hydraulics.DoubleActingCylinder
   PyBM.hydraulics.TripleChamberCylinder
   PyBM.hydraulics.VariablePressureAccumulator


Functions
---------

.. autoapisummary::

   PyBM.hydraulics.buckling_check
   PyBM.hydraulics.calculate_cyl_deadlength
   PyBM.hydraulics.get_min_rod_diameter


Package Contents
----------------

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



.. py:class:: Accumulator(Vaccu, Pmax)

   .. py:attribute:: k
      :value: 1.4



   .. py:attribute:: n2_density
      :value: 1.2506



   .. py:attribute:: Patm
      :value: 101300.0



   .. py:attribute:: V


   .. py:attribute:: Pmax


   .. py:method:: get_p1(V1)

      Get Pressure for given Volume V1.

      :param V1: Volume [m3]
      :return: [Pa] pressure for V1.



   .. py:method:: get_pressure_ratio(V1)

      Ratio of Max Pressure to pressure at point V1

      :param V1: Volume [m3]
      :return: [Pa] pressure for V1.



   .. py:method:: mass_estimate()

      Container Mass estimate based on accu volume

      :return: [kg] mass



   .. py:method:: gas_mass()

      Get mass of Nitrogen gas.

      :return: [kg] mass



   .. py:method:: __str__() -> str


.. py:function:: buckling_check(Fz, d_rod, buckling_length, E=210000000000.0)

   Check for buckling of the cylinder rod. (acc. BHO 'template cylinder sizing.xlsx')

   :param Fz: [N] Axial force
   :param bore: [m] Bore of cylinder
   :param rod: [m] Rod of cylinder
   :param buckling_length: [m] Length of cylinder rod
   :param E: [Pa] Young's modulus of cylinder
   :return: [bool] True if buckling occurs


.. py:function:: calculate_cyl_deadlength(d_bore)

   Calculate total length of cylinder.
   based on rule of thumb calculation by BHO ('template cylinder sizing.xlsx')

   :param stroke: [m] Stroke of cylinder
   :param diameter: [m] Diameter of cylinder
   :return: [m] Dead length of cylinder


.. py:function:: get_min_rod_diameter(Fz, buckling_length, E=210000)

   Check for buckling of the cylinder rod. (acc. BHO 'template cylinder sizing.xlsx')

   :param Fz: [N] Axial force
   :param bore: [m] Bore of cylinder
   :param rod: [m] Rod of cylinder
   :param buckling_length: [m] Length of cylinder rod
   :param E: [N/mm^2] Young's modulus of cylinder
   :return: [bool] True if buckling occurs


.. py:class:: Cylinder(piston_area, stroke, max_pressure, minLength=None)

   .. py:attribute:: A


   .. py:attribute:: stroke


   .. py:attribute:: minLength
      :value: None



   .. py:attribute:: Pmax


   .. py:attribute:: max_vel


   .. py:property:: Dia

      Diameter of cylinder [m].



   .. py:property:: Maxforce

      Maximum force of cylinder [N].



   .. py:property:: Maxflow

      Maximum flow of cylinder [m3/s].



   .. py:method:: get_stroke(Lcyl)

      Get cylinder stroke from cylinder length

      :param Lcyl: [m] Total required length of cylinder



   .. py:method:: __str__() -> str


   .. py:method:: mass_estimate()

      Cylinder and manifold mass estimate based  HF cylinder mass.

      :return: [kg] Mass estimate of cylinder and manifold.



   .. py:method:: cylinder_mass_estimate()

      Give cylinder mass estimate scaled based on HF cylinder area.
      return: [kg] mass estimate.



   .. py:method:: manifold_mass_estimate()

      Manifold mass scaled based on HF cylinder flow.

      :return: [m3] manifold mass estimate.



.. py:class:: DoubleActingCylinder(piston_area, ring_area, stroke, max_pressure, minLength=None)

   Bases: :py:obj:`Cylinder`


   .. py:attribute:: ring_area


   .. py:method:: max_pulling_force()

      Maximum pulling force.

      :return: [N] pulling force



   .. py:method:: __str__() -> str


.. py:class:: TripleChamberCylinder(piston_area, ring_area, inner_rod_area, stroke, max_pressure, max_passive_pressure=None, minLength=None)

   Bases: :py:obj:`DoubleActingCylinder`


   .. py:attribute:: max_passive_pressure


   .. py:attribute:: passive_area


   .. py:method:: max_passive_force()

      Maximum force of the passive chamber.

      :return: [N] passive force



   .. py:method:: __str__() -> str


.. py:class:: VariablePressureAccumulator(*extra_eq1, Ploss_iso=200000.0, Ploss_accu=200000.0, Ploss_valve=300000.0, Ploss_tank=500000.0, Floss_ex=0, num_solve=False, guesses=False, **kwargs)

   All symbols:
   Pnitro - Nitrogen pressure in the accumulator at midpoint
   Fact - Max active cylinder force
   c_f - Contingency factor of required active force, meant for control delay, or pumping pressure loss/gain in the VPA. Usually 1.2
   Fdyn - Dynamic forces on cylinder, as required active force.
   Floss - Extra active force required to overcome losses in the VPA
   r_acc - Nitrogen pressure loss/gain (ratio) over full stroke of accu (+/-)
   Fmax - Maximum force of the active + passive cylinder
   Fmin - Minimum force of the active + passive cylinder
   Apass - Area of the passive cylinder/chamber
   P1_loss - Pressure loss in V1 of the VPA
   P2_loss - Pressure loss in V2 of the VPA
   P3_loss - Pressure loss in V3 of the VPA
   P4_loss - Pressure loss in V4 of the VPA
   Ppas_max - Maximum passive pressure
   A1 - Area of the tandem cylinder in V1 and V4 in the VPA
   A2 - Area of the tandem cylinder in V2 and V3 in the VPA


   .. py:attribute:: _syms


   .. py:attribute:: all_eqs


   .. py:attribute:: properties


   .. py:method:: syms(k)
      :staticmethod:



   .. py:method:: prop_dict()


   .. py:method:: calc_accu_volume(A1, A2, stroke_vpa, n_pumps=3)
      :staticmethod:



   .. py:method:: calc_nitro_loss(A1, A2, stroke_vpa, V_nitro=V_nitro_T700, n_pumps=3)
      :staticmethod:



   .. py:method:: calc_accu_stroke(A1, A2, stroke_vpa, d_accu=d_accu_T700, n_pumps=3, temp_range=[273.15, 293.15], r_accu_fill_inaccuracy=0.04)
      :staticmethod:



   .. py:method:: get_passive_force_steps()


