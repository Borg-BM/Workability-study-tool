PyBM.marine.machines.machine_interface
======================================

.. py:module:: PyBM.marine.machines.machine_interface

.. autoapi-nested-parse::

   Generic Interface for BM machine to compute workability



Classes
-------

.. autoapisummary::

   PyBM.marine.machines.machine_interface.Machine_Linear
   PyBM.marine.machines.machine_interface.Machine_Nonlinear


Module Contents
---------------

.. py:class:: Machine_Linear(position, orientation)

   Bases: :py:obj:`abc.ABC`


   Helper class that provides a standard way to create an ABC using
   inheritance.


   .. py:attribute:: pos


   .. py:attribute:: orient


   .. py:attribute:: rotation


   .. py:method:: apply_transform(point: numpy.array) -> numpy.array

      Apply rotation then translation to 3D point

      :param point: 3D vector [x,y,z]
      :type point: np.array
      :return: Transformed position
      :rtype: np.array



   .. py:method:: get_rao_at_poi(rao) -> PyBM.marine.motion_analysis.MotionRAO.MotionRAO

      Get the Motion RAOs at the POI



   .. py:method:: get_POI() -> dict
      :abstractmethod:



   .. py:method:: apply_machine_dofs(rao) -> PyBM.marine.motion_analysis.MotionRAO.MotionRAO


   .. py:method:: get_workability_limit(motion_at_poi, **kwargs)


   .. py:method:: __str__() -> str


.. py:class:: Machine_Nonlinear(position, orientation)

   Bases: :py:obj:`abc.ABC`


   Helper class that provides a standard way to create an ABC using
   inheritance.


   .. py:attribute:: pos


   .. py:attribute:: orient


   .. py:attribute:: rotation


   .. py:method:: apply_transform(point: numpy.array) -> numpy.array

      Apply rotation then translation to 3D point

      :param point: 3D vector [x,y,z]
      :type point: np.array
      :return: Transformed position
      :rtype: np.array



   .. py:method:: get_POI() -> dict
      :abstractmethod:



