PyBM.marine.machines.HeavyFeederSurgeSway
=========================================

.. py:module:: PyBM.marine.machines.HeavyFeederSurgeSway

.. autoapi-nested-parse::

   Heavy Feeder class to compensate Surge and Sway motion of a POI



Classes
-------

.. autoapisummary::

   PyBM.marine.machines.HeavyFeederSurgeSway.HeavyFeederSurgeSway


Module Contents
---------------

.. py:class:: HeavyFeederSurgeSway(position, orientation, comp_point=[0, 0, 0])

   Bases: :py:obj:`PyBM.marine.machines.HeavyFeeder.HeavyFeeder`


   Helper class that provides a standard way to create an ABC using
   inheritance.


   .. py:attribute:: workability_checks


   .. py:method:: get_POI()

      Return cylinder positions w.r.t. RAO definitions.



   .. py:method:: apply_machine_dofs(rao)


   .. py:method:: check_stroke_limit(motion_at_poi)


