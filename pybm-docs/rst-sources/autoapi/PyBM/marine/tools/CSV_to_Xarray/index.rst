PyBM.marine.tools.CSV_to_Xarray
===============================

.. py:module:: PyBM.marine.tools.CSV_to_Xarray

.. autoapi-nested-parse::

   convert CSV and CSV-like formats to useful xarray

   See an example of the expected format here:
   "O:\Engineering\Database\Vessel Motions\Vessel RAOs and time traces\EWB400\Processed data\RAO Rev0\BasisR.set"



Attributes
----------

.. autoapisummary::

   PyBM.marine.tools.CSV_to_Xarray.DOFS


Functions
---------

.. autoapisummary::

   PyBM.marine.tools.CSV_to_Xarray.parse_csv_sections
   PyBM.marine.tools.CSV_to_Xarray.parse_section
   PyBM.marine.tools.CSV_to_Xarray.extract_dof_name
   PyBM.marine.tools.CSV_to_Xarray.decode_RAO_CSV
   PyBM.marine.tools.CSV_to_Xarray.load_CSV
   PyBM.marine.tools.CSV_to_Xarray.CSV_to_RAO


Module Contents
---------------

.. py:data:: DOFS
   :value: ['X', 'Y', 'Z', 'Rx', 'Ry', 'Rz']


.. py:function:: parse_csv_sections(filename)

   Split the .csv file into sections by '&buildg -csv' / 'END'.


.. py:function:: parse_section(section_text)

   Parse a single amplitude or phase section.


.. py:function:: extract_dof_name(section_text)

   Extract DOF name like 'Surge', 'Sway', etc. from the section header.


.. py:function:: decode_RAO_CSV(filename, mirror)

.. py:function:: load_CSV(filename, mirror)

.. py:function:: CSV_to_RAO(filename, VesselName, Vessel_LC, origin, mirror=False)

   Convert CSV file to Xarray RAO object

   :param filename: CSV file with RAO data
   :param VesselName: Name of vessel
   :param Vessel_LC: Loading condition of the vessel
   :param origin: [m] [x, y, z] origin of the RAOs w.r.t to vessel APP/CL/Keel
   :return: MotionRAO object
   :rtype: MotionRAO


