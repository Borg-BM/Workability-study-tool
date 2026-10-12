PyBM.machines.standard_feeder.tower_check
=========================================

.. py:module:: PyBM.machines.standard_feeder.tower_check

.. autoapi-nested-parse::

   Date: 06-05-2024
   Author: CVE
   Check: XXX

   Refs:
       [1] TWD-NL-2021-501-C-010-REV-2 - LCD
       [2] TWD-NL-2021-501-R-00-REV-1 - BoD
       [3] TBB_280_6KN_Opt_T1T2_acc
       [4] BM-PR305-EN-2002 LCO Operational BM Standard feeder
       [5] TWD-NL-2021-397-C-110, Standard feeder cylinder limits
       [6] M:\Engineering\R&D Projects# PyBM\Engineering\SF Tower Check Operational Accelerations\MM400_Op_Accelerations_Rev0.py



Attributes
----------

.. autoapisummary::

   PyBM.machines.standard_feeder.tower_check.design_loads
   PyBM.machines.standard_feeder.tower_check.Hs_design_transit
   PyBM.machines.standard_feeder.tower_check.Hs_design_operational
   PyBM.machines.standard_feeder.tower_check.t700
   PyBM.machines.standard_feeder.tower_check.t700_cyl_push_max
   PyBM.machines.standard_feeder.tower_check.t700_cyl_pull_max
   PyBM.machines.standard_feeder.tower_check.t700_cyl_pass_max
   PyBM.machines.standard_feeder.tower_check.t700_cyl_pull_max_act
   PyBM.machines.standard_feeder.tower_check.t700_cyl_push_max_act


Functions
---------

.. autoapisummary::

   PyBM.machines.standard_feeder.tower_check.unity_checks_tower


Module Contents
---------------

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

