PyBM.hydraulics.cylinder
========================

.. py:module:: PyBM.hydraulics.cylinder

.. autoapi-nested-parse::

   Python class to compute Cylinder properties

   Date: 15-05-2023
   Author: CBR
   Check: ---

   References:
       [1]: NL002692-02-50-2100-ADM-0001-RAI RA98725531



Attributes
----------

.. autoapisummary::

   PyBM.hydraulics.cylinder.HF_cylinder_bore
   PyBM.hydraulics.cylinder.HF_cylinder_area
   PyBM.hydraulics.cylinder.HF_cylinder_stroke
   PyBM.hydraulics.cylinder.HF_cylinder_mass
   PyBM.hydraulics.cylinder.HF_cylinder_volume
   PyBM.hydraulics.cylinder.HF_manifold_mass
   PyBM.hydraulics.cylinder.HF_max_vel
   PyBM.hydraulics.cylinder.HF_max_flow


Classes
-------

.. autoapisummary::

   PyBM.hydraulics.cylinder.Cylinder
   PyBM.hydraulics.cylinder.DoubleActingCylinder
   PyBM.hydraulics.cylinder.TripleChamberCylinder


Module Contents
---------------

.. py:data:: HF_cylinder_bore
   :value: 0.47


.. py:data:: HF_cylinder_area

.. py:data:: HF_cylinder_stroke
   :value: 1.47


.. py:data:: HF_cylinder_mass
   :value: 6959


.. py:data:: HF_cylinder_volume

.. py:data:: HF_manifold_mass
   :value: 3508


.. py:data:: HF_max_vel
   :value: 0.455


.. py:data:: HF_max_flow

.. py:class:: Cylinder(piston_area, stroke, max_pressure, minLength=None)

   .. py:attribute:: A


   .. py:attribute:: stroke


   .. py:attribute:: minLength
      :value: None



   .. py:attribute:: Pmax


   .. py:attribute:: max_vel


   .. py:property:: Dia

      Diameter of cylinder [m].



   .. py:property:: Maxforce

      Maximum force of cylinder [N].



   .. py:property:: Maxflow

      Maximum flow of cylinder [m3/s].



   .. py:method:: get_stroke(Lcyl)

      Get cylinder stroke from cylinder length

      :param Lcyl: [m] Total required length of cylinder



   .. py:method:: __str__() -> str


   .. py:method:: mass_estimate()

      Cylinder and manifold mass estimate based  HF cylinder mass.

      :return: [kg] Mass estimate of cylinder and manifold.



   .. py:method:: cylinder_mass_estimate()

      Give cylinder mass estimate scaled based on HF cylinder area.
      return: [kg] mass estimate.



   .. py:method:: manifold_mass_estimate()

      Manifold mass scaled based on HF cylinder flow.

      :return: [m3] manifold mass estimate.



.. py:class:: DoubleActingCylinder(piston_area, ring_area, stroke, max_pressure, minLength=None)

   Bases: :py:obj:`Cylinder`


   .. py:attribute:: ring_area


   .. py:method:: max_pulling_force()

      Maximum pulling force.

      :return: [N] pulling force



   .. py:method:: __str__() -> str


.. py:class:: TripleChamberCylinder(piston_area, ring_area, inner_rod_area, stroke, max_pressure, max_passive_pressure=None, minLength=None)

   Bases: :py:obj:`DoubleActingCylinder`


   .. py:attribute:: max_passive_pressure


   .. py:attribute:: passive_area


   .. py:method:: max_passive_force()

      Maximum force of the passive chamber.

      :return: [N] passive force



   .. py:method:: __str__() -> str


