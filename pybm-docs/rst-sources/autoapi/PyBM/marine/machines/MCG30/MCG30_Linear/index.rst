PyBM.marine.machines.MCG30.MCG30_Linear
=======================================

.. py:module:: PyBM.marine.machines.MCG30.MCG30_Linear

.. autoapi-nested-parse::

   Linearized MCG. Based on the same limits as MCG30.py but with linearized equations according to first-order taylor expansions.

   References
   [1] M:\Engineering\R&D Projects# PyBM\Engineering\Linearization of the MCG DOFS.pptx 



Classes
-------

.. autoapisummary::

   PyBM.marine.machines.MCG30.MCG30_Linear.MCG30_Linear
   PyBM.marine.machines.MCG30.MCG30_Linear.MCG30TRANSFER_Linear
   PyBM.marine.machines.MCG30.MCG30_Linear.MCG30LIFTING_Linear


Module Contents
---------------

.. py:class:: MCG30_Linear(position, gw_luff_angle_mean, gw_slew_angle_mean, dp_accuracy=0.5, gw_telescope_mean=None)

   Bases: :py:obj:`PyBM.marine.machines.machine_interface.Machine_Linear`, :py:obj:`abc.ABC`


   Base class for MCG 3.0 for workability studies.
   All parameters are from [2]


   .. py:attribute:: MCGref
      :value: [0, 0, 0]



   .. py:attribute:: base


   .. py:attribute:: gw_luff_angle_mean


   .. py:attribute:: gw_slew_angle_mean


   .. py:attribute:: gw_telescope_mean
      :value: None



   .. py:attribute:: dp_accuracy
      :value: 0.5



   .. py:attribute:: pos_tip


   .. py:attribute:: POI_NAMES
      :value: ['MCGref', 'base', 'tip']



   .. py:attribute:: poi_coordinates


   .. py:attribute:: dof_partials


   .. py:attribute:: workability_checks


   .. py:method:: get_POI()

      Return POI positions w.r.t. RAO definitions.



   .. py:method:: translate_linear_dof(rao, name, partials)


   .. py:method:: apply_machine_dofs(rao)


   .. py:method:: check_linearized_limit(limit, DOF, POI, order)


   .. py:method:: check_telescope_position(mpe_at_poi)


   .. py:method:: check_an_luff(mpe_at_poi)


   .. py:method:: check_horizontal_acc(mpe_at_poi)


   .. py:method:: get_workability_limit(motion_at_poi, **kwargs)


.. py:class:: MCG30TRANSFER_Linear(position, gw_luff_angle_mean, gw_slew_angle_mean, dp_accuracy=0.1, gw_telescope_mean=None)

   Bases: :py:obj:`MCG30_Linear`, :py:obj:`abc.ABC`


   Base class for MCG 3.0 for workability studies.
   All parameters are from [2]


   .. py:method:: check_an_luff_world(mpe_at_poi)


.. py:class:: MCG30LIFTING_Linear(position, gw_luff_angle_mean, gw_slew_angle_mean, dp_accuracy=0.1, gw_telescope_mean=None)

   Bases: :py:obj:`MCG30_Linear`, :py:obj:`abc.ABC`


   Base class for MCG 3.0 for workability studies.
   All parameters are from [2]


   .. py:attribute:: lifting_radius


