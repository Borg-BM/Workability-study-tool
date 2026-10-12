PyBM.mechanics.mechanical_interface
===================================

.. py:module:: PyBM.mechanics.mechanical_interface


Classes
-------

.. autoapisummary::

   PyBM.mechanics.mechanical_interface.MechanicalInterface


Module Contents
---------------

.. py:class:: MechanicalInterface(min_pos, max_pos)

   Bases: :py:obj:`abc.ABC`


   Helper class that provides a standard way to create an ABC using
   inheritance.


   .. py:attribute:: min_pos


   .. py:attribute:: max_pos


   .. py:method:: L_cylinder(effective_disp)
      :abstractmethod:


      Return cylinder length for given compensation length.

      :param effective_disp: [m] Displacement to compensate for.



   .. py:method:: force_ratio(effective_disp)
      :abstractmethod:


      Return ratio of Cylinder Force / External force for a given position.

      :param effective_disp: [m] Displacement to compensate for.



