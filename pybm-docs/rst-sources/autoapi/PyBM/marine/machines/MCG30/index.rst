PyBM.marine.machines.MCG30
==========================

.. py:module:: PyBM.marine.machines.MCG30


Submodules
----------

.. toctree::
   :maxdepth: 1

   /autoapi/PyBM/marine/machines/MCG30/MCG30_Linear/index
   /autoapi/PyBM/marine/machines/MCG30/MCG30_Nonlinear/index
   /autoapi/PyBM/marine/machines/MCG30/mcg30_helper/index


Classes
-------

.. autoapisummary::

   PyBM.marine.machines.MCG30.MCG30LHIGHLOAD_Linear
   PyBM.marine.machines.MCG30.MCG30LLOWLOAD_Linear
   PyBM.marine.machines.MCG30.MCG30LTRANSFER_Linear
   PyBM.marine.machines.MCG30.MCG30LTIPLADDER_Linear
   PyBM.marine.machines.MCG30.MCG30MHIGHLOAD_Linear
   PyBM.marine.machines.MCG30.MCG30MLOWLOAD_Linear
   PyBM.marine.machines.MCG30.MCG30MTRANSFER_Linear
   PyBM.marine.machines.MCG30.MCG30MTIPLADDER_Linear
   PyBM.marine.machines.MCG30.MCG30LHIGHLOAD_Nonlinear
   PyBM.marine.machines.MCG30.MCG30LLOWLOAD_Nonlinear
   PyBM.marine.machines.MCG30.MCG30LTRANSFER_Nonlinear
   PyBM.marine.machines.MCG30.MCG30LTIPLADDER_Nonlinear
   PyBM.marine.machines.MCG30.MCG30MHIGHLOAD_Nonlinear
   PyBM.marine.machines.MCG30.MCG30MLOWLOAD_Nonlinear
   PyBM.marine.machines.MCG30.MCG30MTRANSFER_Nonlinear
   PyBM.marine.machines.MCG30.MCG30MTIPLADDER_Nonlinear


Package Contents
----------------

.. py:class:: MCG30LHIGHLOAD_Linear(position, gw_luff_angle_mean, gw_slew_angle_mean, dp_accuracy=0.1, gw_telescope_mean=None)

   Bases: :py:obj:`mcg30_helper.MCG30LHIGHLOAD_Params`, :py:obj:`MCG30_Linear.MCG30LIFTING_Linear`


   Helper class that provides a standard way to create an ABC using
   inheritance.


.. py:class:: MCG30LLOWLOAD_Linear(position, gw_luff_angle_mean, gw_slew_angle_mean, dp_accuracy=0.1, gw_telescope_mean=None)

   Bases: :py:obj:`mcg30_helper.MCG30LLOWLOAD_Params`, :py:obj:`MCG30_Linear.MCG30LIFTING_Linear`


   Helper class that provides a standard way to create an ABC using
   inheritance.


.. py:class:: MCG30LTRANSFER_Linear(position, gw_luff_angle_mean, gw_slew_angle_mean, dp_accuracy=0.1, gw_telescope_mean=None)

   Bases: :py:obj:`mcg30_helper.MCG30LTRANSFER_Params`, :py:obj:`MCG30_Linear.MCG30TRANSFER_Linear`


   Helper class that provides a standard way to create an ABC using
   inheritance.


.. py:class:: MCG30LTIPLADDER_Linear(position, gw_luff_angle_mean, gw_slew_angle_mean, dp_accuracy=0.1, gw_telescope_mean=None)

   Bases: :py:obj:`mcg30_helper.MCG30LTIPLADDER_Params`, :py:obj:`MCG30_Linear.MCG30TRANSFER_Linear`


   For the tip ladder the standard deviation limits are reduced by multiplying them with
       - stroke   70%
       - velocity 35%


.. py:class:: MCG30MHIGHLOAD_Linear(position, gw_luff_angle_mean, gw_slew_angle_mean, dp_accuracy=0.1, gw_telescope_mean=None)

   Bases: :py:obj:`mcg30_helper.MCG30MHIGHLOAD_Params`, :py:obj:`MCG30_Linear.MCG30LIFTING_Linear`


   Helper class that provides a standard way to create an ABC using
   inheritance.


.. py:class:: MCG30MLOWLOAD_Linear(position, gw_luff_angle_mean, gw_slew_angle_mean, dp_accuracy=0.1, gw_telescope_mean=None)

   Bases: :py:obj:`mcg30_helper.MCG30MLOWLOAD_Params`, :py:obj:`MCG30_Linear.MCG30LIFTING_Linear`


   Helper class that provides a standard way to create an ABC using
   inheritance.


.. py:class:: MCG30MTRANSFER_Linear(position, gw_luff_angle_mean, gw_slew_angle_mean, dp_accuracy=0.1, gw_telescope_mean=None)

   Bases: :py:obj:`mcg30_helper.MCG30MTRANSFER_Params`, :py:obj:`MCG30_Linear.MCG30TRANSFER_Linear`


   Helper class that provides a standard way to create an ABC using
   inheritance.


.. py:class:: MCG30MTIPLADDER_Linear(position, gw_luff_angle_mean, gw_slew_angle_mean, dp_accuracy=0.1, gw_telescope_mean=None)

   Bases: :py:obj:`mcg30_helper.MCG30MTIPLADDER_Params`, :py:obj:`MCG30_Linear.MCG30TRANSFER_Linear`


   For the tip ladder the standard deviation limits are reduced by multiplying them with
       - stroke   70%
       - velocity 35%


.. py:class:: MCG30LHIGHLOAD_Nonlinear(position, gw_luff_angle_mean, gw_slew_angle_mean, dp_accuracy=0.1, gw_telescope_mean=None)

   Bases: :py:obj:`mcg30_helper.MCG30LHIGHLOAD_Params`, :py:obj:`MCG30_Nonlinear.MCG30LIFTING_Nonlinear`


   Helper class that provides a standard way to create an ABC using
   inheritance.


.. py:class:: MCG30LLOWLOAD_Nonlinear(position, gw_luff_angle_mean, gw_slew_angle_mean, dp_accuracy=0.1, gw_telescope_mean=None)

   Bases: :py:obj:`mcg30_helper.MCG30LLOWLOAD_Params`, :py:obj:`MCG30_Nonlinear.MCG30LIFTING_Nonlinear`


   Helper class that provides a standard way to create an ABC using
   inheritance.


.. py:class:: MCG30LTRANSFER_Nonlinear(position, gw_luff_angle_mean, gw_slew_angle_mean, dp_accuracy=0.1, gw_telescope_mean=None)

   Bases: :py:obj:`mcg30_helper.MCG30LTRANSFER_Params`, :py:obj:`MCG30_Nonlinear.MCG30TRANSFER_Nonlinear`


   Helper class that provides a standard way to create an ABC using
   inheritance.


.. py:class:: MCG30LTIPLADDER_Nonlinear(position, gw_luff_angle_mean, gw_slew_angle_mean, dp_accuracy=0.1, gw_telescope_mean=None)

   Bases: :py:obj:`mcg30_helper.MCG30LTIPLADDER_Params`, :py:obj:`MCG30_Nonlinear.MCG30TRANSFER_Nonlinear`


   For the tip ladder the standard deviation limits are reduced by multiplying them with
       - stroke   70%
       - velocity 35%


.. py:class:: MCG30MHIGHLOAD_Nonlinear(position, gw_luff_angle_mean, gw_slew_angle_mean, dp_accuracy=0.1, gw_telescope_mean=None)

   Bases: :py:obj:`mcg30_helper.MCG30MHIGHLOAD_Params`, :py:obj:`MCG30_Nonlinear.MCG30LIFTING_Nonlinear`


   Helper class that provides a standard way to create an ABC using
   inheritance.


.. py:class:: MCG30MLOWLOAD_Nonlinear(position, gw_luff_angle_mean, gw_slew_angle_mean, dp_accuracy=0.1, gw_telescope_mean=None)

   Bases: :py:obj:`mcg30_helper.MCG30MLOWLOAD_Params`, :py:obj:`MCG30_Nonlinear.MCG30LIFTING_Nonlinear`


   Helper class that provides a standard way to create an ABC using
   inheritance.


.. py:class:: MCG30MTRANSFER_Nonlinear(position, gw_luff_angle_mean, gw_slew_angle_mean, dp_accuracy=0.1, gw_telescope_mean=None)

   Bases: :py:obj:`mcg30_helper.MCG30MTRANSFER_Params`, :py:obj:`MCG30_Nonlinear.MCG30TRANSFER_Nonlinear`


   Helper class that provides a standard way to create an ABC using
   inheritance.


.. py:class:: MCG30MTIPLADDER_Nonlinear(position, gw_luff_angle_mean, gw_slew_angle_mean, dp_accuracy=0.1, gw_telescope_mean=None)

   Bases: :py:obj:`mcg30_helper.MCG30MTIPLADDER_Params`, :py:obj:`MCG30_Nonlinear.MCG30TRANSFER_Nonlinear`


   For the tip ladder the standard deviation limits are reduced by multiplying them with
       - stroke   70%
       - velocity 35%


