PyBM.hydraulics.accumulator
===========================

.. py:module:: PyBM.hydraulics.accumulator

.. autoapi-nested-parse::

   Python class to compute Accumulator properties

   Date: 15-05-2023
   Author: CBR
   Check: ---



Attributes
----------

.. autoapisummary::

   PyBM.hydraulics.accumulator.accu_density


Classes
-------

.. autoapisummary::

   PyBM.hydraulics.accumulator.Accumulator


Module Contents
---------------

.. py:data:: accu_density
   :value: 1000.0


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


