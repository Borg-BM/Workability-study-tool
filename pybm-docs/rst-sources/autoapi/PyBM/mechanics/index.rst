PyBM.mechanics
==============

.. py:module:: PyBM.mechanics


Submodules
----------

.. toctree::
   :maxdepth: 1

   /autoapi/PyBM/mechanics/mechanical_hydraulic_combination/index
   /autoapi/PyBM/mechanics/mechanical_interface/index


Classes
-------

.. autoapisummary::

   PyBM.mechanics.MechanicalHydraulicCombination
   PyBM.mechanics.MechanicalInterface


Package Contents
----------------

.. py:class:: MechanicalHydraulicCombination(mechanics: PyBM.mechanics.mechanical_interface.MechanicalInterface, hydraulics: PyBM.hydraulics.accu_cylinder_combination.AccuCylinderCombination)

   .. py:attribute:: mech


   .. py:attribute:: hyd


   .. py:method:: get_force(Se)


   .. py:method:: __plot(fcn, axes: matplotlib.pyplot.Axes = None)


   .. py:method:: plot_force(axes: matplotlib.pyplot.Axes = None)


   .. py:method:: plot_error(design_force, axes: matplotlib.pyplot.Axes = None)


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



