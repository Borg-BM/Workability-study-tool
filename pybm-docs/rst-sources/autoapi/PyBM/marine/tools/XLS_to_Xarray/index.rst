PyBM.marine.tools.XLS_to_Xarray
===============================

.. py:module:: PyBM.marine.tools.XLS_to_Xarray

.. autoapi-nested-parse::

   convert XLS format to useful xarray



Attributes
----------

.. autoapisummary::

   PyBM.marine.tools.XLS_to_Xarray.DOFS


Functions
---------

.. autoapisummary::

   PyBM.marine.tools.XLS_to_Xarray.decode_RAO_XLS
   PyBM.marine.tools.XLS_to_Xarray.load_XLS
   PyBM.marine.tools.XLS_to_Xarray.XLS_to_RAO


Module Contents
---------------

.. py:data:: DOFS
   :value: ['X', 'Y', 'Z', 'Rx', 'Ry', 'Rz']


.. py:function:: decode_RAO_XLS(filename, mirror)

.. py:function:: load_XLS(filename, mirror)

.. py:function:: XLS_to_RAO(filename, VesselName, Vessel_LC, origin, mirror=False)

   Convert excel file to Xarray RAO object

   :param filename: Excel file with RAO data
   :param VesselName: Name of vessel
   :param Vessel_LC: Loading condition of the vessel
   :param origin: [m] [x, y, z] origin of the RAOs w.r.t to vessel APP/CL/Keel
   :return: MotionRAO object
   :rtype: MotionRAO


