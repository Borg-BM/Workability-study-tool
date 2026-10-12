PyBM.marine.tools.import_octopus_rao
====================================

.. py:module:: PyBM.marine.tools.import_octopus_rao


Attributes
----------

.. autoapisummary::

   PyBM.marine.tools.import_octopus_rao.DOFs


Functions
---------

.. autoapisummary::

   PyBM.marine.tools.import_octopus_rao.Octopus_to_RAO
   PyBM.marine.tools.import_octopus_rao.get_rao_parameter
   PyBM.marine.tools.import_octopus_rao.read_data_line
   PyBM.marine.tools.import_octopus_rao.get_origin
   PyBM.marine.tools.import_octopus_rao.get_wave_directions
   PyBM.marine.tools.import_octopus_rao.get_speeds
   PyBM.marine.tools.import_octopus_rao.get_wave_frequencies
   PyBM.marine.tools.import_octopus_rao.get_rao


Module Contents
---------------

.. py:data:: DOFs
   :value: ['X', 'Y', 'Z', 'Rx', 'Ry', 'Rz']


.. py:function:: Octopus_to_RAO(octopus_file, VesselName, Vessel_LC, speed=0)

.. py:function:: get_rao_parameter(file_iterator, param_string)

.. py:function:: read_data_line(line)

.. py:function:: get_origin(file_iterator)

.. py:function:: get_wave_directions(file_iterator)

.. py:function:: get_speeds(file_iterator)

.. py:function:: get_wave_frequencies(file_iterator, speed)

.. py:function:: get_rao(file_iterator, desired_speed)

