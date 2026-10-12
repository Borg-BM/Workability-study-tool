PyBM.marine.tools.LIS_to_Xarray
===============================

.. py:module:: PyBM.marine.tools.LIS_to_Xarray

.. autoapi-nested-parse::

   tools to read AQWA RAO files (*.LIS)



Attributes
----------

.. autoapisummary::

   PyBM.marine.tools.LIS_to_Xarray.DOFs
   PyBM.marine.tools.LIS_to_Xarray.RAO_TYPES
   PyBM.marine.tools.LIS_to_Xarray.COG_TYPE
   PyBM.marine.tools.LIS_to_Xarray.N_FREQS_TYPE
   PyBM.marine.tools.LIS_to_Xarray.DRAFT_TYPE


Functions
---------

.. autoapisummary::

   PyBM.marine.tools.LIS_to_Xarray.get_cog
   PyBM.marine.tools.LIS_to_Xarray.get_n_freqs
   PyBM.marine.tools.LIS_to_Xarray.get_draft
   PyBM.marine.tools.LIS_to_Xarray.decode_RAO
   PyBM.marine.tools.LIS_to_Xarray.load_LIS
   PyBM.marine.tools.LIS_to_Xarray.LIS_to_RAO


Module Contents
---------------

.. py:data:: DOFs
   :value: ['X', 'Y', 'Z', 'Rx', 'Ry', 'Rz']


.. py:data:: RAO_TYPES

.. py:data:: COG_TYPE
   :value: '                          CENTRE OF GRAVITY'


.. py:data:: N_FREQS_TYPE
   :value: '    * * * * W A V E   F R E Q U E N C I E S / P E R I O D S   A N D   D I R E C T I O N S * * * *'


.. py:data:: DRAFT_TYPE
   :value: '          DEPTH OF LOWEST POINT ON VESSEL . . . . . . .'


.. py:function:: get_cog(filename)

.. py:function:: get_n_freqs(filename)

.. py:function:: get_draft(filename)

.. py:function:: decode_RAO(filename, rao_type, n_freqs)

.. py:function:: load_LIS(filename)

.. py:function:: LIS_to_RAO(filename, VesselName, Vessel_LC)

   Convert LIS data to MotionRAO object.

   :param filename: path to LIS file
   :param VesselName: Name of the vessel
   :param Vessel_LC: Vessel Loading condition


