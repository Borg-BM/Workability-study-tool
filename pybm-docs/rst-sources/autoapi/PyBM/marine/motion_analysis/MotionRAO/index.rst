PyBM.marine.motion_analysis.MotionRAO
=====================================

.. py:module:: PyBM.marine.motion_analysis.MotionRAO

.. autoapi-nested-parse::

   Motion RAO class. Inherits RAO class and xarray.Dataset
   Init as Dataset with Three dataarrays:
   POS (positional RAO values)
   VEL (velocity RAO values)
   ACC (acceleration RAO values)

   CBR 21-06-2023

   References:
    [1] Ship Motion Control, Tristan Perez



Classes
-------

.. autoapisummary::

   PyBM.marine.motion_analysis.MotionRAO.MotionRAO


Module Contents
---------------

.. py:class:: MotionRAO(data_vars: xarray.core.types.DataVars | None = None, coords: collections.abc.Mapping[Any, Any] | None = None, attrs: collections.abc.Mapping[Any, Any] | None = None)

   Bases: :py:obj:`PyBM.marine.motion_analysis.RAO.RAO`


   This is the parent class for motion and force RAOs


   .. py:attribute:: __slots__
      :value: ()



   .. py:method:: translate_rao(offset)

      Translates the RAO to a point of interest. Ref[1] eq (4.27)

      :param offset: [m] (x,y,z) offset of the point of interest
      :return: Full vessel motion RAOs around POI



