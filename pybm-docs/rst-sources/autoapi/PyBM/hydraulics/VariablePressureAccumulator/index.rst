PyBM.hydraulics.VariablePressureAccumulator
===========================================

.. py:module:: PyBM.hydraulics.VariablePressureAccumulator


Attributes
----------

.. autoapisummary::

   PyBM.hydraulics.VariablePressureAccumulator.normal_symbols
   PyBM.hydraulics.VariablePressureAccumulator.positive_symbols
   PyBM.hydraulics.VariablePressureAccumulator.syms
   PyBM.hydraulics.VariablePressureAccumulator.d_accu_T700
   PyBM.hydraulics.VariablePressureAccumulator.V_accu_T700
   PyBM.hydraulics.VariablePressureAccumulator.V_nitro_T700


Classes
-------

.. autoapisummary::

   PyBM.hydraulics.VariablePressureAccumulator.VariablePressureAccumulator


Functions
---------

.. autoapisummary::

   PyBM.hydraulics.VariablePressureAccumulator.guesser


Module Contents
---------------

.. py:data:: normal_symbols
   :value: ()


.. py:data:: positive_symbols
   :value: ()


.. py:data:: syms

.. py:data:: d_accu_T700
   :value: 0.36


.. py:data:: V_accu_T700
   :value: 0.25


.. py:data:: V_nitro_T700
   :value: 4.0


.. py:function:: guesser(symbols: list)

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


