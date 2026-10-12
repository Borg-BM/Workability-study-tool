<!-- Source: https://docs.app.barge-master.com/autoapi/PyBM/marine/machines/MCG30/mcg30_helper/index.html -->

# PyBM.marine.machines.MCG30.mcg30_helper

## Attributes

|                                                                                                                                                              |     |
|--------------------------------------------------------------------------------------------------------------------------------------------------------------|-----|
| [`_tvt_per_radius`](#PyBM.marine.machines.MCG30.mcg30_helper._tvt_per_radius "PyBM.marine.machines.MCG30.mcg30_helper._tvt_per_radius")                      |     |
| [`tvt_per_radius`](#PyBM.marine.machines.MCG30.mcg30_helper.tvt_per_radius "PyBM.marine.machines.MCG30.mcg30_helper.tvt_per_radius")                         |     |
| [`MCG30MTIPLADDER_Params`](#PyBM.marine.machines.MCG30.mcg30_helper.MCG30MTIPLADDER_Params "PyBM.marine.machines.MCG30.mcg30_helper.MCG30MTIPLADDER_Params") |     |
| [`MCG30LTIPLADDER_Params`](#PyBM.marine.machines.MCG30.mcg30_helper.MCG30LTIPLADDER_Params "PyBM.marine.machines.MCG30.mcg30_helper.MCG30LTIPLADDER_Params") |     |

## Classes

|                                                                                                                                                           |                                                                  |
|-----------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------|
| [`MCG30_Params`](#PyBM.marine.machines.MCG30.mcg30_helper.MCG30_Params "PyBM.marine.machines.MCG30.mcg30_helper.MCG30_Params")                            | Helper class that provides a standard way to create an ABC using |
| [`MCG30L_Params`](#PyBM.marine.machines.MCG30.mcg30_helper.MCG30L_Params "PyBM.marine.machines.MCG30.mcg30_helper.MCG30L_Params")                         | Helper class that provides a standard way to create an ABC using |
| [`MCG30M_Params`](#PyBM.marine.machines.MCG30.mcg30_helper.MCG30M_Params "PyBM.marine.machines.MCG30.mcg30_helper.MCG30M_Params")                         | Helper class that provides a standard way to create an ABC using |
| [`MCG30TRANSFER_Params`](#PyBM.marine.machines.MCG30.mcg30_helper.MCG30TRANSFER_Params "PyBM.marine.machines.MCG30.mcg30_helper.MCG30TRANSFER_Params")    | Helper class that provides a standard way to create an ABC using |
| [`MCG30HIGHLOAD_Params`](#PyBM.marine.machines.MCG30.mcg30_helper.MCG30HIGHLOAD_Params "PyBM.marine.machines.MCG30.mcg30_helper.MCG30HIGHLOAD_Params")    | Helper class that provides a standard way to create an ABC using |
| [`MCG30LOWLOAD_Params`](#PyBM.marine.machines.MCG30.mcg30_helper.MCG30LOWLOAD_Params "PyBM.marine.machines.MCG30.mcg30_helper.MCG30LOWLOAD_Params")       | Helper class that provides a standard way to create an ABC using |
| [`MCG30MTRANSFER_Params`](#PyBM.marine.machines.MCG30.mcg30_helper.MCG30MTRANSFER_Params "PyBM.marine.machines.MCG30.mcg30_helper.MCG30MTRANSFER_Params") | Helper class that provides a standard way to create an ABC using |
| [`MCG30MHIGHLOAD_Params`](#PyBM.marine.machines.MCG30.mcg30_helper.MCG30MHIGHLOAD_Params "PyBM.marine.machines.MCG30.mcg30_helper.MCG30MHIGHLOAD_Params") | Helper class that provides a standard way to create an ABC using |
| [`MCG30MLOWLOAD_Params`](#PyBM.marine.machines.MCG30.mcg30_helper.MCG30MLOWLOAD_Params "PyBM.marine.machines.MCG30.mcg30_helper.MCG30MLOWLOAD_Params")    | Helper class that provides a standard way to create an ABC using |
| [`MCG30LTRANSFER_Params`](#PyBM.marine.machines.MCG30.mcg30_helper.MCG30LTRANSFER_Params "PyBM.marine.machines.MCG30.mcg30_helper.MCG30LTRANSFER_Params") | Helper class that provides a standard way to create an ABC using |
| [`MCG30LHIGHLOAD_Params`](#PyBM.marine.machines.MCG30.mcg30_helper.MCG30LHIGHLOAD_Params "PyBM.marine.machines.MCG30.mcg30_helper.MCG30LHIGHLOAD_Params") | Helper class that provides a standard way to create an ABC using |
| [`MCG30LLOWLOAD_Params`](#PyBM.marine.machines.MCG30.mcg30_helper.MCG30LLOWLOAD_Params "PyBM.marine.machines.MCG30.mcg30_helper.MCG30LLOWLOAD_Params")    | Helper class that provides a standard way to create an ABC using |

## Functions

|                                                                                                                                                                                     |                                                                                                                               |
|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------|
| [`partials_telescope`](#PyBM.marine.machines.MCG30.mcg30_helper.partials_telescope "PyBM.marine.machines.MCG30.mcg30_helper.partials_telescope")(pos_tip, base)                     | Calculate the partial derivatives of the telescope position with respect to the response DOFs \[ X, Y, Z, Rx, Ry, Rz \].      |
| [`partials_luff_world`](#PyBM.marine.machines.MCG30.mcg30_helper.partials_luff_world "PyBM.marine.machines.MCG30.mcg30_helper.partials_luff_world")(pos_tip, base)                  |                                                                                                                               |
| [`partials_luff`](#PyBM.marine.machines.MCG30.mcg30_helper.partials_luff "PyBM.marine.machines.MCG30.mcg30_helper.partials_luff")(pos_tip, base, slew_angle)                        |                                                                                                                               |
| [`partials_slew_world`](#PyBM.marine.machines.MCG30.mcg30_helper.partials_slew_world "PyBM.marine.machines.MCG30.mcg30_helper.partials_slew_world")(pos_tip, base)                  |                                                                                                                               |
| [`partials_slew`](#PyBM.marine.machines.MCG30.mcg30_helper.partials_slew "PyBM.marine.machines.MCG30.mcg30_helper.partials_slew")(pos_tip, base)                                    | Calculate the partial derivatives of the slew angle with respect to the response DOFs \[ X, Y, Z, Rx, Ry, Rz \].              |
| [`partials_luff_cyl`](#PyBM.marine.machines.MCG30.mcg30_helper.partials_luff_cyl "PyBM.marine.machines.MCG30.mcg30_helper.partials_luff_cyl")(pos_tip, base, slew_angle, ...)       | Calculate the partial derivatives of the luffing cylinder length with respect to the response DOFs \[ X, Y, Z, Rx, Ry, Rz \]. |
| [`partials_v_tip`](#PyBM.marine.machines.MCG30.mcg30_helper.partials_v_tip "PyBM.marine.machines.MCG30.mcg30_helper.partials_v_tip")(luff_angle, gw_L, slew_angle)                  |                                                                                                                               |
| [`p2ds`](#PyBM.marine.machines.MCG30.mcg30_helper.p2ds "PyBM.marine.machines.MCG30.mcg30_helper.p2ds")(partials)                                                                    | Convert partials to a dataset with POS, VEL and ACC                                                                           |
| [`MCG30TIPLADDER_FACTORY`](#PyBM.marine.machines.MCG30.mcg30_helper.MCG30TIPLADDER_FACTORY "PyBM.marine.machines.MCG30.mcg30_helper.MCG30TIPLADDER_FACTORY")(MCG_Size_Params_Class) |                                                                                                                               |

## Module Contents

PyBM.marine.machines.MCG30.mcg30_helper.partials_telescope(*pos_tip*, *base*)[](../../../../../../../source-code/PyBM/marine/machines/MCG30/mcg30_helper.py)  
Calculate the partial derivatives of the telescope position with respect to the response DOFs \[ X, Y, Z, Rx, Ry, Rz \].

&nbsp;

PyBM.marine.machines.MCG30.mcg30_helper.partials_luff_world(*pos_tip*, *base*)[](../../../../../../../source-code/PyBM/marine/machines/MCG30/mcg30_helper.py)  

&nbsp;

PyBM.marine.machines.MCG30.mcg30_helper.partials_luff(*pos_tip*, *base*, *slew_angle*)[](../../../../../../../source-code/PyBM/marine/machines/MCG30/mcg30_helper.py)  

&nbsp;

PyBM.marine.machines.MCG30.mcg30_helper.partials_slew_world(*pos_tip*, *base*)[](../../../../../../../source-code/PyBM/marine/machines/MCG30/mcg30_helper.py)  

&nbsp;

PyBM.marine.machines.MCG30.mcg30_helper.partials_slew(*pos_tip*, *base*)[](../../../../../../../source-code/PyBM/marine/machines/MCG30/mcg30_helper.py)  
Calculate the partial derivatives of the slew angle with respect to the response DOFs \[ X, Y, Z, Rx, Ry, Rz \]. :param pos_tip: The position of the tip. :type pos_tip: numpy.ndarray :param base: The base position. :type base: numpy.ndarray :return: The partial derivatives of the slew angle. :rtype: numpy.ndarray

&nbsp;

PyBM.marine.machines.MCG30.mcg30_helper.partials_luff_cyl(*pos_tip*, *base*, *slew_angle*, *luff_angle*, *lc0*, *l0*, *l1*)[](../../../../../../../source-code/PyBM/marine/machines/MCG30/mcg30_helper.py)  
Calculate the partial derivatives of the luffing cylinder length with respect to the response DOFs \[ X, Y, Z, Rx, Ry, Rz \]. :param pos_tip: The position of the tip. :type pos_tip: float :param base: The base value. :type base: float :param slew_angle: The MCG slew angle. :type slew_angle: float :param luff_angle: The MCG luff angle. :type luff_angle: float :param lc0: Location of loffing cylinder bearing on transfer deck in MCGref (XYZ_LUFFCYL_TRANSFER) :type lc0: list :param l0: Location of Luffing joint in MCGref (XYZ_LUFF) :type l0: list :param l1: Location of luffing cylinder bearing on telescope 1 in MCGref for luffing angle 0deg (XYZ_LUFFCYL_TELESCOPE_0ANGLE) :type l1: list :return: The partial derivatives of the luffing cylinder length with respect to the input parameters. :rtype: numpy.ndarray

&nbsp;

PyBM.marine.machines.MCG30.mcg30_helper.partials_v_tip(*luff_angle*, *gw_L*, *slew_angle*)[](../../../../../../../source-code/PyBM/marine/machines/MCG30/mcg30_helper.py)  

&nbsp;

PyBM.marine.machines.MCG30.mcg30_helper.p2ds(*partials*)[](../../../../../../../source-code/PyBM/marine/machines/MCG30/mcg30_helper.py)  
Convert partials to a dataset with POS, VEL and ACC

&nbsp;

PyBM.marine.machines.MCG30.mcg30_helper.\_tvt_per_radius[](../../../../../../../source-code/PyBM/marine/machines/MCG30/mcg30_helper.py)  

&nbsp;

PyBM.marine.machines.MCG30.mcg30_helper.tvt_per_radius[](../../../../../../../source-code/PyBM/marine/machines/MCG30/mcg30_helper.py)  

&nbsp;

*class *PyBM.marine.machines.MCG30.mcg30_helper.MCG30_Params[](../../../../../../../source-code/PyBM/marine/machines/MCG30/mcg30_helper.py)  
Bases: `abc.ABC`

Helper class that provides a standard way to create an ABC using inheritance.

XYZ_LUFF* = \[0, 0, 2.1\]*[](../../../../../../../source-code/PyBM/marine/machines/MCG30/mcg30_helper.py)  

XYZ_LUFFCYL_TRANSFER* = \[0.48, 0, 0.78\]*[](../../../../../../../source-code/PyBM/marine/machines/MCG30/mcg30_helper.py)  

XYZ_LUFFCYL_TELESCOPE_0ANGLE* = \[4.035, 0, 1.7\]*[](../../../../../../../source-code/PyBM/marine/machines/MCG30/mcg30_helper.py)  

Q_PUMP_MAX* = 0.0062833333333333335*[](../../../../../../../source-code/PyBM/marine/machines/MCG30/mcg30_helper.py)  

V_ACC_MAX* = 0.0132*[](../../../../../../../source-code/PyBM/marine/machines/MCG30/mcg30_helper.py)  

ROLL_SYSTEM_MAX* = 7.5*[](../../../../../../../source-code/PyBM/marine/machines/MCG30/mcg30_helper.py)  

PITCH_SYSTEM_MAX* = 7.5*[](../../../../../../../source-code/PyBM/marine/machines/MCG30/mcg30_helper.py)  

A_HORIZONTAL_MAX[](../../../../../../../source-code/PyBM/marine/machines/MCG30/mcg30_helper.py)  

A_HEAVE_MAX* = 1.9620000000000002*[](../../../../../../../source-code/PyBM/marine/machines/MCG30/mcg30_helper.py)  

D_LUFFCYLBORE* = 300*[](../../../../../../../source-code/PyBM/marine/machines/MCG30/mcg30_helper.py)  

D_LUFFCYLROD* = 210*[](../../../../../../../source-code/PyBM/marine/machines/MCG30/mcg30_helper.py)  

A_LUFFCYLBOTTOM[](../../../../../../../source-code/PyBM/marine/machines/MCG30/mcg30_helper.py)  

A_LUFFCYLROD[](../../../../../../../source-code/PyBM/marine/machines/MCG30/mcg30_helper.py)  

VOL_SLEWMOTOR* = 0.00025*[](../../../../../../../source-code/PyBM/marine/machines/MCG30/mcg30_helper.py)  

I_SLEWTRANSMISSIONRATIO* = 443.5199999999999*[](../../../../../../../source-code/PyBM/marine/machines/MCG30/mcg30_helper.py)  

A_SLEWMOTOR* = 0.00030799999999999995*[](../../../../../../../source-code/PyBM/marine/machines/MCG30/mcg30_helper.py)  

D_TELESCOPEDRUM* = 350*[](../../../../../../../source-code/PyBM/marine/machines/MCG30/mcg30_helper.py)  

L_DRUM_PERREV[](../../../../../../../source-code/PyBM/marine/machines/MCG30/mcg30_helper.py)  

V_TELESCOPEMOTOR* = 0.002512*[](../../../../../../../source-code/PyBM/marine/machines/MCG30/mcg30_helper.py)  

A_TELESCOPEMOTOR[](../../../../../../../source-code/PyBM/marine/machines/MCG30/mcg30_helper.py)  

plot(*axs: matplotlib.axes.Axes = None*, *vessel: [PyBM.utils.data_classes.VesselDimensions](../../../../utils/data_classes/index.md#PyBM.utils.data_classes.VesselDimensions "PyBM.utils.data_classes.VesselDimensions") = None*, *rao_origin=None*)[](../../../../../../../source-code/PyBM/marine/machines/MCG30/mcg30_helper.py)  
Plots the MCG in 3 dimensions with either a general vessel or a vessel with given dimensions.

Parameters:  
- **axs** (*Axes*) – Axes to plot onto.

- **vessel** ([*VesselDimensions*](../../../../index.md#PyBM.VesselDimensions "PyBM.VesselDimensions")) – vessel dimensions to plot on figure

- **rao_origin** (*np.array*) – rao origin position \[x,y,z\]

&nbsp;

*class *PyBM.marine.machines.MCG30.mcg30_helper.MCG30L_Params[](../../../../../../../source-code/PyBM/marine/machines/MCG30/mcg30_helper.py)  
Bases: [`MCG30_Params`](#PyBM.marine.machines.MCG30.mcg30_helper.MCG30_Params "PyBM.marine.machines.MCG30.mcg30_helper.MCG30_Params"), `abc.ABC`

Helper class that provides a standard way to create an ABC using inheritance.

gw_L_mean* = 23*[](../../../../../../../source-code/PyBM/marine/machines/MCG30/mcg30_helper.py)  

GANGWAY_L_TELESCOPE_MIN* = 17.2*[](../../../../../../../source-code/PyBM/marine/machines/MCG30/mcg30_helper.py)  

GANGWAY_L_TELESCOPE_MAX* = 27.94*[](../../../../../../../source-code/PyBM/marine/machines/MCG30/mcg30_helper.py)  

&nbsp;

*class *PyBM.marine.machines.MCG30.mcg30_helper.MCG30M_Params[](../../../../../../../source-code/PyBM/marine/machines/MCG30/mcg30_helper.py)  
Bases: [`MCG30_Params`](#PyBM.marine.machines.MCG30.mcg30_helper.MCG30_Params "PyBM.marine.machines.MCG30.mcg30_helper.MCG30_Params"), `abc.ABC`

Helper class that provides a standard way to create an ABC using inheritance.

gw_L_mean* = 20.12*[](../../../../../../../source-code/PyBM/marine/machines/MCG30/mcg30_helper.py)  

GANGWAY_L_TELESCOPE_MIN* = 14.139999999999999*[](../../../../../../../source-code/PyBM/marine/machines/MCG30/mcg30_helper.py)  

GANGWAY_L_TELESCOPE_MAX* = 23.86*[](../../../../../../../source-code/PyBM/marine/machines/MCG30/mcg30_helper.py)  

&nbsp;

*class *PyBM.marine.machines.MCG30.mcg30_helper.MCG30TRANSFER_Params[](../../../../../../../source-code/PyBM/marine/machines/MCG30/mcg30_helper.py)  
Bases: [`MCG30_Params`](#PyBM.marine.machines.MCG30.mcg30_helper.MCG30_Params "PyBM.marine.machines.MCG30.mcg30_helper.MCG30_Params"), `abc.ABC`

Helper class that provides a standard way to create an ABC using inheritance.

V_TELESCOPE* = 1.6*[](../../../../../../../source-code/PyBM/marine/machines/MCG30/mcg30_helper.py)  

AN_LUFF_MIN* = -18*[](../../../../../../../source-code/PyBM/marine/machines/MCG30/mcg30_helper.py)  

AN_LUFF_MAX* = 23*[](../../../../../../../source-code/PyBM/marine/machines/MCG30/mcg30_helper.py)  

V_LUFFCYL* = 0.156*[](../../../../../../../source-code/PyBM/marine/machines/MCG30/mcg30_helper.py)  

V_SLEW* = 5*[](../../../../../../../source-code/PyBM/marine/machines/MCG30/mcg30_helper.py)  

AN_LUFF_WORLD* = 10*[](../../../../../../../source-code/PyBM/marine/machines/MCG30/mcg30_helper.py)  

AN_SLEW_WORLD* = 10*[](../../../../../../../source-code/PyBM/marine/machines/MCG30/mcg30_helper.py)  

&nbsp;

*class *PyBM.marine.machines.MCG30.mcg30_helper.MCG30HIGHLOAD_Params[](../../../../../../../source-code/PyBM/marine/machines/MCG30/mcg30_helper.py)  
Bases: [`MCG30_Params`](#PyBM.marine.machines.MCG30.mcg30_helper.MCG30_Params "PyBM.marine.machines.MCG30.mcg30_helper.MCG30_Params"), `abc.ABC`

Helper class that provides a standard way to create an ABC using inheritance.

V_TELESCOPE* = 1.6*[](../../../../../../../source-code/PyBM/marine/machines/MCG30/mcg30_helper.py)  

AN_LUFF_MIN* = -5*[](../../../../../../../source-code/PyBM/marine/machines/MCG30/mcg30_helper.py)  

AN_LUFF_MAX* = 40*[](../../../../../../../source-code/PyBM/marine/machines/MCG30/mcg30_helper.py)  

V_LUFFCYL* = 0.156*[](../../../../../../../source-code/PyBM/marine/machines/MCG30/mcg30_helper.py)  

V_SLEW* = 5*[](../../../../../../../source-code/PyBM/marine/machines/MCG30/mcg30_helper.py)  

V_ROLL_SYSTEM_MAX* = 1.5*[](../../../../../../../source-code/PyBM/marine/machines/MCG30/mcg30_helper.py)  

V_PITCH_SYSTEM_MAX* = 1.5*[](../../../../../../../source-code/PyBM/marine/machines/MCG30/mcg30_helper.py)  

V_HEAVE_MAX* = 0.6*[](../../../../../../../source-code/PyBM/marine/machines/MCG30/mcg30_helper.py)  

*property *tip_v_threshold[](../../../../../../../source-code/PyBM/marine/machines/MCG30/mcg30_helper.py)  

&nbsp;

*class *PyBM.marine.machines.MCG30.mcg30_helper.MCG30LOWLOAD_Params[](../../../../../../../source-code/PyBM/marine/machines/MCG30/mcg30_helper.py)  
Bases: [`MCG30_Params`](#PyBM.marine.machines.MCG30.mcg30_helper.MCG30_Params "PyBM.marine.machines.MCG30.mcg30_helper.MCG30_Params"), `abc.ABC`

Helper class that provides a standard way to create an ABC using inheritance.

V_TELESCOPE* = 1.6*[](../../../../../../../source-code/PyBM/marine/machines/MCG30/mcg30_helper.py)  

AN_LUFF_MIN* = -5*[](../../../../../../../source-code/PyBM/marine/machines/MCG30/mcg30_helper.py)  

AN_LUFF_MAX* = 40*[](../../../../../../../source-code/PyBM/marine/machines/MCG30/mcg30_helper.py)  

V_LUFFCYL* = 0.156*[](../../../../../../../source-code/PyBM/marine/machines/MCG30/mcg30_helper.py)  

V_SLEW* = 5*[](../../../../../../../source-code/PyBM/marine/machines/MCG30/mcg30_helper.py)  

V_ROLL_SYSTEM_MAX* = 3.0*[](../../../../../../../source-code/PyBM/marine/machines/MCG30/mcg30_helper.py)  

V_PITCH_SYSTEM_MAX* = 3.0*[](../../../../../../../source-code/PyBM/marine/machines/MCG30/mcg30_helper.py)  

V_HEAVE_MAX* = 1.2*[](../../../../../../../source-code/PyBM/marine/machines/MCG30/mcg30_helper.py)  

*property *tip_v_threshold[](../../../../../../../source-code/PyBM/marine/machines/MCG30/mcg30_helper.py)  

&nbsp;

PyBM.marine.machines.MCG30.mcg30_helper.MCG30TIPLADDER_FACTORY(*MCG_Size_Params_Class*)[](../../../../../../../source-code/PyBM/marine/machines/MCG30/mcg30_helper.py)  

&nbsp;

*class *PyBM.marine.machines.MCG30.mcg30_helper.MCG30MTRANSFER_Params[](../../../../../../../source-code/PyBM/marine/machines/MCG30/mcg30_helper.py)  
Bases: [`MCG30M_Params`](#PyBM.marine.machines.MCG30.mcg30_helper.MCG30M_Params "PyBM.marine.machines.MCG30.mcg30_helper.MCG30M_Params"), [`MCG30TRANSFER_Params`](#PyBM.marine.machines.MCG30.mcg30_helper.MCG30TRANSFER_Params "PyBM.marine.machines.MCG30.mcg30_helper.MCG30TRANSFER_Params"), `abc.ABC`

Helper class that provides a standard way to create an ABC using inheritance.

GANGWAY_L_TELESCOPE_MIN* = 16.11*[](../../../../../../../source-code/PyBM/marine/machines/MCG30/mcg30_helper.py)  

GANGWAY_L_TELESCOPE_MAX* = 24.13*[](../../../../../../../source-code/PyBM/marine/machines/MCG30/mcg30_helper.py)  

&nbsp;

*class *PyBM.marine.machines.MCG30.mcg30_helper.MCG30MHIGHLOAD_Params[](../../../../../../../source-code/PyBM/marine/machines/MCG30/mcg30_helper.py)  
Bases: [`MCG30M_Params`](#PyBM.marine.machines.MCG30.mcg30_helper.MCG30M_Params "PyBM.marine.machines.MCG30.mcg30_helper.MCG30M_Params"), [`MCG30HIGHLOAD_Params`](#PyBM.marine.machines.MCG30.mcg30_helper.MCG30HIGHLOAD_Params "PyBM.marine.machines.MCG30.mcg30_helper.MCG30HIGHLOAD_Params"), `abc.ABC`

Helper class that provides a standard way to create an ABC using inheritance.

&nbsp;

*class *PyBM.marine.machines.MCG30.mcg30_helper.MCG30MLOWLOAD_Params[](../../../../../../../source-code/PyBM/marine/machines/MCG30/mcg30_helper.py)  
Bases: [`MCG30M_Params`](#PyBM.marine.machines.MCG30.mcg30_helper.MCG30M_Params "PyBM.marine.machines.MCG30.mcg30_helper.MCG30M_Params"), [`MCG30LOWLOAD_Params`](#PyBM.marine.machines.MCG30.mcg30_helper.MCG30LOWLOAD_Params "PyBM.marine.machines.MCG30.mcg30_helper.MCG30LOWLOAD_Params"), `abc.ABC`

Helper class that provides a standard way to create an ABC using inheritance.

&nbsp;

*class *PyBM.marine.machines.MCG30.mcg30_helper.MCG30LTRANSFER_Params[](../../../../../../../source-code/PyBM/marine/machines/MCG30/mcg30_helper.py)  
Bases: [`MCG30L_Params`](#PyBM.marine.machines.MCG30.mcg30_helper.MCG30L_Params "PyBM.marine.machines.MCG30.mcg30_helper.MCG30L_Params"), [`MCG30TRANSFER_Params`](#PyBM.marine.machines.MCG30.mcg30_helper.MCG30TRANSFER_Params "PyBM.marine.machines.MCG30.mcg30_helper.MCG30TRANSFER_Params"), `abc.ABC`

Helper class that provides a standard way to create an ABC using inheritance.

GANGWAY_L_TELESCOPE_MIN* = 19*[](../../../../../../../source-code/PyBM/marine/machines/MCG30/mcg30_helper.py)  

GANGWAY_L_TELESCOPE_MAX* = 27*[](../../../../../../../source-code/PyBM/marine/machines/MCG30/mcg30_helper.py)  

&nbsp;

*class *PyBM.marine.machines.MCG30.mcg30_helper.MCG30LHIGHLOAD_Params[](../../../../../../../source-code/PyBM/marine/machines/MCG30/mcg30_helper.py)  
Bases: [`MCG30L_Params`](#PyBM.marine.machines.MCG30.mcg30_helper.MCG30L_Params "PyBM.marine.machines.MCG30.mcg30_helper.MCG30L_Params"), [`MCG30HIGHLOAD_Params`](#PyBM.marine.machines.MCG30.mcg30_helper.MCG30HIGHLOAD_Params "PyBM.marine.machines.MCG30.mcg30_helper.MCG30HIGHLOAD_Params"), `abc.ABC`

Helper class that provides a standard way to create an ABC using inheritance.

&nbsp;

*class *PyBM.marine.machines.MCG30.mcg30_helper.MCG30LLOWLOAD_Params[](../../../../../../../source-code/PyBM/marine/machines/MCG30/mcg30_helper.py)  
Bases: [`MCG30L_Params`](#PyBM.marine.machines.MCG30.mcg30_helper.MCG30L_Params "PyBM.marine.machines.MCG30.mcg30_helper.MCG30L_Params"), [`MCG30LOWLOAD_Params`](#PyBM.marine.machines.MCG30.mcg30_helper.MCG30LOWLOAD_Params "PyBM.marine.machines.MCG30.mcg30_helper.MCG30LOWLOAD_Params"), `abc.ABC`

Helper class that provides a standard way to create an ABC using inheritance.

&nbsp;

PyBM.marine.machines.MCG30.mcg30_helper.MCG30MTIPLADDER_Params[](../../../../../../../source-code/PyBM/marine/machines/MCG30/mcg30_helper.py)  

&nbsp;

PyBM.marine.machines.MCG30.mcg30_helper.MCG30LTIPLADDER_Params[](../../../../../../../source-code/PyBM/marine/machines/MCG30/mcg30_helper.py)  
