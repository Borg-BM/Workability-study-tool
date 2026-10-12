PyBM.marine.tools.TXT_to_Xarray
===============================

.. py:module:: PyBM.marine.tools.TXT_to_Xarray

.. autoapi-nested-parse::

   convert TXT Orcaflex formats to useful xarray

   See an example of the expected format here:
   "O:\Engineering\Database\Vessel Motions\Vessel RAOs and time traces\EWB400\Processed data\RAO Rev0\OFMRAO.EWB400.MAXDRAFT.set"
   More info here: https://www.orcina.com/webhelp/OrcaFlex/Content/html/Importinghydrodynamicdata,Generictextfiles.htm#GenericRAOImport



Attributes
----------

.. autoapisummary::

   PyBM.marine.tools.TXT_to_Xarray.DOFS


Functions
---------

.. autoapisummary::

   PyBM.marine.tools.TXT_to_Xarray.parse_TXT
   PyBM.marine.tools.TXT_to_Xarray.decode_RAO_TXT
   PyBM.marine.tools.TXT_to_Xarray.load_TXT
   PyBM.marine.tools.TXT_to_Xarray.TXT_to_RAO


Module Contents
---------------

.. py:data:: DOFS
   :value: ['X', 'Y', 'Z', 'Rx', 'Ry', 'Rz']


.. py:function:: parse_TXT(filename)

   Parse OrcaFlex .txt file into structured blocks per direction.


.. py:function:: decode_RAO_TXT(filename, mirror=False)

   Decode OrcaFlex .txt file to xarray DataArray.


.. py:function:: load_TXT(filename, mirror=False)

.. py:function:: TXT_to_RAO(filename, VesselName, Vessel_LC, origin, mirror=False)

   Convert OrcaFlex .txt file to MotionRAO object.


