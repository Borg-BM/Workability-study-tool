PyBM.machines.heavy_feeder.tower_check
======================================

.. py:module:: PyBM.machines.heavy_feeder.tower_check

.. autoapi-nested-parse::

   Date: 20-03-2023
   Date checked: 12-06-2025
   Author: CBR
   Check: AKO

   Refs:
       [1] TWD-NL-2021-512-C-010-REV-6 Heavy feeder re-design LCD
       [2] TBB_280_6KN_Opt_T1T2_acc



Attributes
----------

.. autoapisummary::

   PyBM.machines.heavy_feeder.tower_check.design_loads
   PyBM.machines.heavy_feeder.tower_check.Hs_design


Functions
---------

.. autoapisummary::

   PyBM.machines.heavy_feeder.tower_check.unity_checks_tower


Module Contents
---------------

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


