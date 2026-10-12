PyBM.marine.machines.MCG30.mcg30_helper
=======================================

.. py:module:: PyBM.marine.machines.MCG30.mcg30_helper


Attributes
----------

.. autoapisummary::

   PyBM.marine.machines.MCG30.mcg30_helper._tvt_per_radius
   PyBM.marine.machines.MCG30.mcg30_helper.tvt_per_radius
   PyBM.marine.machines.MCG30.mcg30_helper.MCG30MTIPLADDER_Params
   PyBM.marine.machines.MCG30.mcg30_helper.MCG30LTIPLADDER_Params


Classes
-------

.. autoapisummary::

   PyBM.marine.machines.MCG30.mcg30_helper.MCG30_Params
   PyBM.marine.machines.MCG30.mcg30_helper.MCG30L_Params
   PyBM.marine.machines.MCG30.mcg30_helper.MCG30M_Params
   PyBM.marine.machines.MCG30.mcg30_helper.MCG30TRANSFER_Params
   PyBM.marine.machines.MCG30.mcg30_helper.MCG30HIGHLOAD_Params
   PyBM.marine.machines.MCG30.mcg30_helper.MCG30LOWLOAD_Params
   PyBM.marine.machines.MCG30.mcg30_helper.MCG30MTRANSFER_Params
   PyBM.marine.machines.MCG30.mcg30_helper.MCG30MHIGHLOAD_Params
   PyBM.marine.machines.MCG30.mcg30_helper.MCG30MLOWLOAD_Params
   PyBM.marine.machines.MCG30.mcg30_helper.MCG30LTRANSFER_Params
   PyBM.marine.machines.MCG30.mcg30_helper.MCG30LHIGHLOAD_Params
   PyBM.marine.machines.MCG30.mcg30_helper.MCG30LLOWLOAD_Params


Functions
---------

.. autoapisummary::

   PyBM.marine.machines.MCG30.mcg30_helper.partials_telescope
   PyBM.marine.machines.MCG30.mcg30_helper.partials_luff_world
   PyBM.marine.machines.MCG30.mcg30_helper.partials_luff
   PyBM.marine.machines.MCG30.mcg30_helper.partials_slew_world
   PyBM.marine.machines.MCG30.mcg30_helper.partials_slew
   PyBM.marine.machines.MCG30.mcg30_helper.partials_luff_cyl
   PyBM.marine.machines.MCG30.mcg30_helper.partials_v_tip
   PyBM.marine.machines.MCG30.mcg30_helper.p2ds
   PyBM.marine.machines.MCG30.mcg30_helper.MCG30TIPLADDER_FACTORY


Module Contents
---------------

.. py:function:: partials_telescope(pos_tip, base)

   Calculate the partial derivatives of the telescope position with respect to the response DOFs [ X, Y, Z, Rx, Ry, Rz ].


.. py:function:: partials_luff_world(pos_tip, base)

.. py:function:: partials_luff(pos_tip, base, slew_angle)

.. py:function:: partials_slew_world(pos_tip, base)

.. py:function:: partials_slew(pos_tip, base)

   Calculate the partial derivatives of the slew angle with respect to the response DOFs [ X, Y, Z, Rx, Ry, Rz ].
   :param pos_tip: The position of the tip.
   :type pos_tip: numpy.ndarray
   :param base: The base position.
   :type base: numpy.ndarray
   :return: The partial derivatives of the slew angle.
   :rtype: numpy.ndarray


.. py:function:: partials_luff_cyl(pos_tip, base, slew_angle, luff_angle, lc0, l0, l1)

   Calculate the partial derivatives of the luffing cylinder length with respect to the response DOFs [ X, Y, Z, Rx, Ry, Rz ].
   :param pos_tip: The position of the tip.
   :type pos_tip: float
   :param base: The base value.
   :type base: float
   :param slew_angle: The MCG slew angle.
   :type slew_angle: float
   :param luff_angle: The MCG luff angle.
   :type luff_angle: float
   :param lc0: Location of loffing cylinder bearing on transfer deck in MCGref (XYZ_LUFFCYL_TRANSFER)
   :type lc0: list
   :param l0: Location of Luffing joint in MCGref (XYZ_LUFF)
   :type l0: list
   :param l1: Location of luffing cylinder bearing on telescope 1 in MCGref for luffing angle 0deg (XYZ_LUFFCYL_TELESCOPE_0ANGLE)
   :type l1: list
   :return: The partial derivatives of the luffing cylinder length with respect to the input parameters.
   :rtype: numpy.ndarray


.. py:function:: partials_v_tip(luff_angle, gw_L, slew_angle)

.. py:function:: p2ds(partials)

   Convert partials to a dataset with POS, VEL and ACC


.. py:data:: _tvt_per_radius

.. py:data:: tvt_per_radius

.. py:class:: MCG30_Params

   Bases: :py:obj:`abc.ABC`


   Helper class that provides a standard way to create an ABC using
   inheritance.


   .. py:attribute:: XYZ_LUFF
      :value: [0, 0, 2.1]



   .. py:attribute:: XYZ_LUFFCYL_TRANSFER
      :value: [0.48, 0, 0.78]



   .. py:attribute:: XYZ_LUFFCYL_TELESCOPE_0ANGLE
      :value: [4.035, 0, 1.7]



   .. py:attribute:: Q_PUMP_MAX
      :value: 0.0062833333333333335



   .. py:attribute:: V_ACC_MAX
      :value: 0.0132



   .. py:attribute:: ROLL_SYSTEM_MAX
      :value: 7.5



   .. py:attribute:: PITCH_SYSTEM_MAX
      :value: 7.5



   .. py:attribute:: A_HORIZONTAL_MAX


   .. py:attribute:: A_HEAVE_MAX
      :value: 1.9620000000000002



   .. py:attribute:: D_LUFFCYLBORE
      :value: 300



   .. py:attribute:: D_LUFFCYLROD
      :value: 210



   .. py:attribute:: A_LUFFCYLBOTTOM


   .. py:attribute:: A_LUFFCYLROD


   .. py:attribute:: VOL_SLEWMOTOR
      :value: 0.00025



   .. py:attribute:: I_SLEWTRANSMISSIONRATIO
      :value: 443.5199999999999



   .. py:attribute:: A_SLEWMOTOR
      :value: 0.00030799999999999995



   .. py:attribute:: D_TELESCOPEDRUM
      :value: 350



   .. py:attribute:: L_DRUM_PERREV


   .. py:attribute:: V_TELESCOPEMOTOR
      :value: 0.002512



   .. py:attribute:: A_TELESCOPEMOTOR


   .. py:method:: plot(axs: matplotlib.axes.Axes = None, vessel: PyBM.utils.data_classes.VesselDimensions = None, rao_origin=None)

      Plots the MCG in 3 dimensions with either a general vessel or a vessel with given dimensions.

      :param axs: Axes to plot onto.
      :type axs: Axes
      :param vessel: vessel dimensions to plot on figure
      :type vessel: VesselDimensions
      :param rao_origin: rao origin position [x,y,z]
      :type rao_origin: np.array



.. py:class:: MCG30L_Params

   Bases: :py:obj:`MCG30_Params`, :py:obj:`abc.ABC`


   Helper class that provides a standard way to create an ABC using
   inheritance.


   .. py:attribute:: gw_L_mean
      :value: 23



   .. py:attribute:: GANGWAY_L_TELESCOPE_MIN
      :value: 17.2



   .. py:attribute:: GANGWAY_L_TELESCOPE_MAX
      :value: 27.94



.. py:class:: MCG30M_Params

   Bases: :py:obj:`MCG30_Params`, :py:obj:`abc.ABC`


   Helper class that provides a standard way to create an ABC using
   inheritance.


   .. py:attribute:: gw_L_mean
      :value: 20.12



   .. py:attribute:: GANGWAY_L_TELESCOPE_MIN
      :value: 14.139999999999999



   .. py:attribute:: GANGWAY_L_TELESCOPE_MAX
      :value: 23.86



.. py:class:: MCG30TRANSFER_Params

   Bases: :py:obj:`MCG30_Params`, :py:obj:`abc.ABC`


   Helper class that provides a standard way to create an ABC using
   inheritance.


   .. py:attribute:: V_TELESCOPE
      :value: 1.6



   .. py:attribute:: AN_LUFF_MIN
      :value: -18



   .. py:attribute:: AN_LUFF_MAX
      :value: 23



   .. py:attribute:: V_LUFFCYL
      :value: 0.156



   .. py:attribute:: V_SLEW
      :value: 5



   .. py:attribute:: AN_LUFF_WORLD
      :value: 10



   .. py:attribute:: AN_SLEW_WORLD
      :value: 10



.. py:class:: MCG30HIGHLOAD_Params

   Bases: :py:obj:`MCG30_Params`, :py:obj:`abc.ABC`


   Helper class that provides a standard way to create an ABC using
   inheritance.


   .. py:attribute:: V_TELESCOPE
      :value: 1.6



   .. py:attribute:: AN_LUFF_MIN
      :value: -5



   .. py:attribute:: AN_LUFF_MAX
      :value: 40



   .. py:attribute:: V_LUFFCYL
      :value: 0.156



   .. py:attribute:: V_SLEW
      :value: 5



   .. py:attribute:: V_ROLL_SYSTEM_MAX
      :value: 1.5



   .. py:attribute:: V_PITCH_SYSTEM_MAX
      :value: 1.5



   .. py:attribute:: V_HEAVE_MAX
      :value: 0.6



   .. py:property:: tip_v_threshold


.. py:class:: MCG30LOWLOAD_Params

   Bases: :py:obj:`MCG30_Params`, :py:obj:`abc.ABC`


   Helper class that provides a standard way to create an ABC using
   inheritance.


   .. py:attribute:: V_TELESCOPE
      :value: 1.6



   .. py:attribute:: AN_LUFF_MIN
      :value: -5



   .. py:attribute:: AN_LUFF_MAX
      :value: 40



   .. py:attribute:: V_LUFFCYL
      :value: 0.156



   .. py:attribute:: V_SLEW
      :value: 5



   .. py:attribute:: V_ROLL_SYSTEM_MAX
      :value: 3.0



   .. py:attribute:: V_PITCH_SYSTEM_MAX
      :value: 3.0



   .. py:attribute:: V_HEAVE_MAX
      :value: 1.2



   .. py:property:: tip_v_threshold


.. py:function:: MCG30TIPLADDER_FACTORY(MCG_Size_Params_Class)

.. py:class:: MCG30MTRANSFER_Params

   Bases: :py:obj:`MCG30M_Params`, :py:obj:`MCG30TRANSFER_Params`, :py:obj:`abc.ABC`


   Helper class that provides a standard way to create an ABC using
   inheritance.


   .. py:attribute:: GANGWAY_L_TELESCOPE_MIN
      :value: 16.11



   .. py:attribute:: GANGWAY_L_TELESCOPE_MAX
      :value: 24.13



.. py:class:: MCG30MHIGHLOAD_Params

   Bases: :py:obj:`MCG30M_Params`, :py:obj:`MCG30HIGHLOAD_Params`, :py:obj:`abc.ABC`


   Helper class that provides a standard way to create an ABC using
   inheritance.


.. py:class:: MCG30MLOWLOAD_Params

   Bases: :py:obj:`MCG30M_Params`, :py:obj:`MCG30LOWLOAD_Params`, :py:obj:`abc.ABC`


   Helper class that provides a standard way to create an ABC using
   inheritance.


.. py:class:: MCG30LTRANSFER_Params

   Bases: :py:obj:`MCG30L_Params`, :py:obj:`MCG30TRANSFER_Params`, :py:obj:`abc.ABC`


   Helper class that provides a standard way to create an ABC using
   inheritance.


   .. py:attribute:: GANGWAY_L_TELESCOPE_MIN
      :value: 19



   .. py:attribute:: GANGWAY_L_TELESCOPE_MAX
      :value: 27



.. py:class:: MCG30LHIGHLOAD_Params

   Bases: :py:obj:`MCG30L_Params`, :py:obj:`MCG30HIGHLOAD_Params`, :py:obj:`abc.ABC`


   Helper class that provides a standard way to create an ABC using
   inheritance.


.. py:class:: MCG30LLOWLOAD_Params

   Bases: :py:obj:`MCG30L_Params`, :py:obj:`MCG30LOWLOAD_Params`, :py:obj:`abc.ABC`


   Helper class that provides a standard way to create an ABC using
   inheritance.


.. py:data:: MCG30MTIPLADDER_Params

.. py:data:: MCG30LTIPLADDER_Params

