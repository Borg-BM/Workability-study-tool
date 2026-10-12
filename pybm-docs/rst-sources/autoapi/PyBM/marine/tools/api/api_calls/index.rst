PyBM.marine.tools.api.api_calls
===============================

.. py:module:: PyBM.marine.tools.api.api_calls


Functions
---------

.. autoapisummary::

   PyBM.marine.tools.api.api_calls.get_raos
   PyBM.marine.tools.api.api_calls.get_rao_loadcases
   PyBM.marine.tools.api.api_calls.get_rao_loadcase


Module Contents
---------------

.. py:function:: get_raos(session=None)

   Get RAOs from API (auto-authenticates if needed)


.. py:function:: get_rao_loadcases(VesselName: str, session=None)

   Get loadcases for a specific RAO from API (auto-authenticates if needed)


.. py:function:: get_rao_loadcase(VesselName: str, Vessel_LC: str, session=None)

   Get specific loadcase details for a RAO from API (auto-authenticates if needed)


