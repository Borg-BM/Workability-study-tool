from abc import ABC

import numpy as np
import xarray as xr
from matplotlib import pyplot as plt
from matplotlib.axes import Axes

from PyBM.constants import g
from PyBM.utils.data_classes import VesselDimensions

def partials_telescope(pos_tip, base):
    """
    Calculate the partial derivatives of the telescope position with respect to the response DOFs [ X, Y, Z, Rx, Ry, Rz ].
    """
    v = pos_tip - base
    x, y, z = v
    L = np.sqrt(np.sum(np.square(v)))
    pLpx = x / L
    pLpy = y / L
    pLpz = z / L
    return [pLpx, pLpy, pLpz, 0, 0, 0]

def partials_luff_world(pos_tip, base):
    v = pos_tip - base
    x, y, z = v
    L = np.sqrt(np.sum(np.square(v)))
    pLfpx = z * x / (np.square(L) * np.sqrt(np.square(L) - np.square(z)))
    pLfpy = z * y / (np.square(L) * np.sqrt(np.square(L) - np.square(z)))
    pLfpz = -np.sqrt(np.square(L) - np.square(z)) / np.square(L)
    return (180 / np.pi) * np.array([pLfpx, pLfpy, pLfpz, 0, 0, 0])

def partials_luff(pos_tip, base, slew_angle):
    pLfpxyz = partials_luff_world(pos_tip, base)[0:3]
    pLfpRx = -np.sin(np.deg2rad(slew_angle))
    pLfpRy = np.cos(np.deg2rad(slew_angle))
    return np.concatenate([pLfpxyz, [pLfpRx], [pLfpRy], [0]])

def partials_slew_world(pos_tip, base):
    v = pos_tip - base
    x, y, _ = v
    pSlpx = y / (np.square(x) + np.square(y))
    pSlpy = -x / (np.square(x) + np.square(y))
    return (180 / np.pi) * np.array([pSlpx, pSlpy, 0, 0, 0, 0])

def partials_slew(pos_tip, base):
    """
    Calculate the partial derivatives of the slew angle with respect to the response DOFs [ X, Y, Z, Rx, Ry, Rz ].
    :param pos_tip: The position of the tip.
    :type pos_tip: numpy.ndarray
    :param base: The base position.
    :type base: numpy.ndarray
    :return: The partial derivatives of the slew angle.
    :rtype: numpy.ndarray
    """
    pLfpxyz = partials_slew_world(pos_tip, base)[0:3]
    pSlpRz = -1
    return np.concatenate([pLfpxyz, [0, 0, pSlpRz]])

def partials_luff_cyl(pos_tip, base, slew_angle, luff_angle, lc0, l0, l1):
    """
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
    """
    # unpacking parameters
    x_lc0, _, z_lc0, x_l0, _, z_l0, x_l1, _, z_l1 = *lc0, *l0, *l1
    # calculating default luffing cylinder position x_lc, z_lc and luffing cylinder length Lp
    x_lc = (
        x_l0 - x_lc0 + (x_l1 - x_l0) * np.cos(np.deg2rad(luff_angle)) - (z_l1 - z_l0) * np.sin(np.deg2rad(luff_angle))
    )
    z_lc = (
        z_l0 - z_lc0 + (x_l1 - x_l0) * np.sin(np.deg2rad(luff_angle)) + (z_l1 - z_l0) * np.cos(np.deg2rad(luff_angle))
    )
    Lp = np.sqrt(np.sum(np.square(np.array([x_lc, z_lc]))))
    # calculating luffing angle partials
    pSlpxy = (np.pi / 180) * partials_luff(pos_tip, base, slew_angle)
    # pSlpxy = np.concatenate([(np.pi/180)*pSlpxy[0:3], pSlpxy[3:6]])
    # calculating luffing cylinder position partials d(x_lc)/d(q) and d(z_lc)/d(q) where q = [X, Y, Z, Rx, Ry, Rz]
    # these must be multiplied with luffing angle partials.
    pxlcpxyz = np.array(
        [-(x_l1 - x_l0) * np.sin(np.deg2rad(luff_angle)) - (z_l1 - z_l0) * np.cos(np.deg2rad(luff_angle))] * 6
    )
    pzlcpxyz = np.array(
        [(x_l1 - x_l0) * np.cos(np.deg2rad(luff_angle)) - (z_l1 - z_l0) * np.sin(np.deg2rad(luff_angle))] * 6
    )
    # calculating luffing cylinder length partial d(Lp)/d(q) where q = [X, Y, Z, Rx, Ry, Rz]
    pLppx = (pxlcpxyz * x_lc / Lp + pzlcpxyz * z_lc / Lp) * pSlpxy
    return pLppx

def partials_v_tip(luff_angle, gw_L, slew_angle):
    radius = np.cos(np.deg2rad(luff_angle)) * gw_L
    pvtpRx = np.sin(np.deg2rad(slew_angle)) * radius * np.pi / 180
    pvtpRy = np.cos(np.deg2rad(slew_angle)) * radius * np.pi / 180
    return [0, 0, 1, pvtpRx, pvtpRy, 0]

def p2ds(partials):
    """
    Convert partials to a dataset with POS, VEL and ACC
    """
    da = xr.DataArray(partials, coords={"DOF": ["X", "Y", "Z", "Rx", "Ry", "Rz"]})
    return xr.Dataset({"POS": da, "VEL": da, "ACC": da})

# DEFLECTION TEST VALUES
# _tvt_per_radius = {"radius": [14, 15.5, 17, 19, 21, 23, 25], "tip_velocity": [0.65, 0.66, 0.68, 0.71, 0.74, 0.80, 0.89]}
# DNV APPROVED VALUES

_tvt_per_radius = {"radius": [14, 15.5, 17, 19, 21, 23, 25], "tip_velocity": [0.8, 0.81, 0.82, 0.84, 0.87, 0.92, 0.99]}

tvt_per_radius = xr.DataArray(
    _tvt_per_radius["tip_velocity"], coords={"radius": _tvt_per_radius["radius"]}, dims=["radius"]
)

class MCG30_Params(ABC):
    # Location of Luffing joint in MCGref

    XYZ_LUFF = [0, 0, 2.1]  # m

    # Location of loffing cylinder bearing on transfer deck in MCGref

    XYZ_LUFFCYL_TRANSFER = [0.48, 0, 0.78]  # m

    # Location of luffing cylinder bearing on telescope 1 in MCGref for luffing angle 0deg

    XYZ_LUFFCYL_TELESCOPE_0ANGLE = [4.035, 0, 1.7]  # m

    # Transfer actuator limits

    Q_PUMP_MAX = 377 / 60 / 1000  # [m^3/s] 392 max but reserved 15 for leakage

    # Q_Pump_max_landed= 377/60/1000 # [m^3/s] 392 , 15 for lek

    V_ACC_MAX = 13.2 / 1000  # [m3]

    # 	V_Acc_max_double = 2*V_Acc_max # [m3]

    # generic limits

    ROLL_SYSTEM_MAX = 7.5  # [deg] Allowed vessel roll for system. Not be confused with operational vessel roll

    PITCH_SYSTEM_MAX = 7.5  # [deg] Allowed vessel pitch for system. Not be confused with operational vessel pitch

    A_HORIZONTAL_MAX = np.sqrt(0.1**2 + 0.15**2) * g  # [m/s^2] Maximum allowed horizontal acceleration

    A_HEAVE_MAX = 0.2 * g  # [m/s^2] Maximum allowed heave acceleration

    # calculate area luffing cylinder in m3/m

    D_LUFFCYLBORE = 300  # [mm]

    D_LUFFCYLROD = 210  # [mm]

    A_LUFFCYLBOTTOM = 0.25 * np.pi * (D_LUFFCYLBORE / 1000) ** 2  # [m3/m] or [m2]

    A_LUFFCYLROD = (
        0.25 * np.pi * (D_LUFFCYLBORE / 1000) ** 2 - 0.25 * np.pi * (D_LUFFCYLROD / 1000) ** 2
    )  # [m3/m] or [m2]

    # calculate 'area' of slewing motor in m3/deg

    VOL_SLEWMOTOR = 250 / 1e6  # [m^3/rev]

    I_SLEWTRANSMISSIONRATIO = 88 / 15 * 75.6  # [-] Total slewing gear to motor ratio incl pinion and gearbox

    A_SLEWMOTOR = VOL_SLEWMOTOR / 360 * I_SLEWTRANSMISSIONRATIO  # [m^3/deg]

    # calculate 'area' of telescope motor in m3/m

    D_TELESCOPEDRUM = 350  # [mm]

    L_DRUM_PERREV = np.pi * D_TELESCOPEDRUM / 1000  # [m/rev]

    V_TELESCOPEMOTOR = 2.512 / 1000  # [m^3/rev]

    A_TELESCOPEMOTOR = V_TELESCOPEMOTOR / L_DRUM_PERREV  # [m^3/m]

    def plot(self, axs: Axes = None, vessel: VesselDimensions = None, rao_origin=None):
        """
        Plots the MCG in 3 dimensions with either a general vessel or a vessel with given dimensions.

        :param axs: Axes to plot onto.
        :type axs: Axes
        :param vessel: vessel dimensions to plot on figure
        :type vessel: VesselDimensions
        :param rao_origin: rao origin position [x,y,z]
        :type rao_origin: np.array
        """
        vesseltext = ""
        if vessel is None:
            if rao_origin is None:
                rao_origin = np.array([40, 0, 7])
                print(
                    UserWarning(
                        "Vessel and rao_origin are None, plotting a default vessel. Vessel is only for axis references!"
                    )
                )
            vessel = VesselDimensions()
            vesseltext = "VESSEL NOT FOR SCALE, \nONLY FOR AXIS REFERENCE"
        else:
            if rao_origin is None:
                raise ValueError("vessel was defined but rao_origin was not. Please define both or neither!")
        fig = plt.figure()
        axs = fig.add_subplot(projection="3d")
        x = [c[0] + rao_origin[0] for c in self.poi_coordinates]
        y = [c[1] + rao_origin[1] for c in self.poi_coordinates]
        z = [c[2] + rao_origin[2] for c in self.poi_coordinates]
        axs.set_aspect("equal")
        # Plotting vessel
        X1 = 0
        X3 = vessel.Length
        X2 = (X3) * (2 / 3)
        Y1 = -vessel.Breadth / 2
        Y2 = vessel.Breadth + Y1
        Z1 = 0
        Z2 = vessel.Depth
        x_vessel = np.array([[X1] * 5, [X1] * 5, [X2] * 5, [X3] * 5])
        y_vessel = np.array([[0] * 5, [Y1, Y1, Y2, Y2, Y1], [Y1, Y1, Y2, Y2, Y1], [0] * 5])
        z_vessel = np.array([[Z1] * 5, [Z1, Z2, Z2, Z1, Z1], [Z1, Z2, Z2, Z1, Z1], [Z2, Z2, Z2, Z2, Z2]])
        axs.plot_surface(x_vessel, y_vessel, z_vessel, color="0.7", alpha=0.3)
        # Plotting MCG
        axs.plot3D(x, y, z, "-ro")
        # Plotting RAO origin
        axs.plot3D(*rao_origin, "bo")
        axs.text(*rao_origin, f"RAO/trace origin @{rao_origin}")
        for i, c in enumerate(self.poi_coordinates):
            axs.text(*(c + rao_origin), f"{self.POI_NAMES[i]} @{c+rao_origin}")
        axs.text(10, -5, -7, vesseltext)
        axs.set_aspect("equal")
        axs.grid(True)
        axs.set_xlabel("x")
        axs.set_ylabel("y")

class MCG30L_Params(MCG30_Params, ABC):

    gw_L_mean = 23  # [m] Gangway mean length during landing without DP positioning error

    GANGWAY_L_TELESCOPE_MIN = (
        17.0 + 0.2
    )  # [m] Large gangway minimum operational telescope stroke for dynamic compensation, with 0.2m buffer

    GANGWAY_L_TELESCOPE_MAX = (
        28.14 - 0.2
    )  # [m] Large gangway maximum operational telescope stroke for dynamic compensation, with 0.2m buffer

class MCG30M_Params(MCG30_Params, ABC):

    gw_L_mean = 20.12  # [m] Gangway mean length during landing without DP positioning error

    GANGWAY_L_TELESCOPE_MIN = (
        13.94 + 0.2
    )  # [m] Medium gangway minimum operational telescope stroke for dynamic compensation, with 0.2m buffer

    GANGWAY_L_TELESCOPE_MAX = (
        24.06 - 0.2
    )  # [m] Medium gangway maximum operational telescope stroke for dynamic compensation, with 0.2m buffer

class MCG30TRANSFER_Params(MCG30_Params, ABC):

    V_TELESCOPE = 1.6  # [m/s] Telescope velocity

    AN_LUFF_MIN = -18  # [deg] Available luffing angle, single amplitude

    AN_LUFF_MAX = 23  # [deg] Available luffing angle, single amplitude

    V_LUFFCYL = 0.156  # [m/s] Available luffing cylinder speed

    V_SLEW = 5  # [deg/s] Available slewing angular speed

    AN_LUFF_WORLD = 10  # [deg] Allowed dynamic luffing angle relative to the world (single amplitude), limited by tip rotational DoF

    AN_SLEW_WORLD = 10  # [deg] Allowed dynamic slewing angle relative to the world (single amplitude), limited by tip rotational DoF

class MCG30HIGHLOAD_Params(MCG30_Params, ABC):

    V_TELESCOPE = 1.6  # [m/s] Telescope velocity

    AN_LUFF_MIN = -5  # [deg] Available luffing angle, single amplitude

    AN_LUFF_MAX = 40  # [deg] Available luffing angle, single amplitude

    V_LUFFCYL = 0.156  # [m/s] Available luffing cylinder speed

    V_SLEW = 5  # [deg/s] Available slewing angular speed (ref: BM-PR206-EN-MO-R-0144-Rev0)

    V_ROLL_SYSTEM_MAX = 1.5  # [deg/s] Allowed vessel roll velocity for lifting. Not be confused with operational vessel roll (ref: BM-PR206-EN-MO-R-0144-Rev0)

    V_PITCH_SYSTEM_MAX = 1.5  # [deg/s] Allowed vessel pitch velocity for lifting. Not be confused with operational vessel pitch (ref: BM-PR206-EN-MO-R-0144-Rev0)

    V_HEAVE_MAX = 0.6  # [m/s] Maximum allowed heave velocity for lifting. (ref: BM-PR206-EN-DC-C-0100-Rev1)

    @property

    def tip_v_threshold(self):
        return tvt_per_radius.interp(radius=self.lifting_radius).item()

class MCG30LOWLOAD_Params(MCG30_Params, ABC):

    V_TELESCOPE = 1.6  # [m/s] Telescope velocity

    AN_LUFF_MIN = -5  # [deg] Available luffing angle, single amplitude

    AN_LUFF_MAX = 40  # [deg] Available luffing angle, single amplitude

    V_LUFFCYL = 0.156  # [m/s] Available luffing cylinder speed

    V_SLEW = 5  # [deg/s] Available slewing angular speed

    V_ROLL_SYSTEM_MAX = 3.0  # [deg/s] Allowed vessel roll velocity for lifting. Not be confused with operational vessel roll (ref: BM-PR206-EN-MO-R-0144-Rev0)

    V_PITCH_SYSTEM_MAX = 3.0  # [deg/s] Allowed vessel pitch velocity for lifting. Not be confused with operational vessel pitch (ref: BM-PR206-EN-MO-R-0144-Rev0)

    V_HEAVE_MAX = 1.2  # [m/s] Maximum allowed heave velocity for lifting. (ref: BM-PR206-EN-DC-C-0100-Rev1)

    @property

    def tip_v_threshold(self):
        V_TIP = 1.89  # [m/s] Maximum tip velocity for low load operations (ref: BM-PR206-EN-MO-R-0144-Rev0)
        return V_TIP

def MCG30TIPLADDER_FACTORY(MCG_Size_Params_Class):
    class MCG30TIPLADDER_FACTORY(MCG_Size_Params_Class, ABC):
        """
        For the tip ladder the standard deviation limits are reduced by multiplying them with
            - stroke   70%
            - velocity 35%
        """

        TELESCOPE_STROKE_FACTOR = 0.7
        TELESCOPE_VELOCITY_FACTOR = 0.35

        @property
        def GANGWAY_L_TELESCOPE_MIN(self):
            L_abs = (MCG_Size_Params_Class.GANGWAY_L_TELESCOPE_MAX - MCG_Size_Params_Class.GANGWAY_L_TELESCOPE_MIN) / 2

            GANGWAY_L_TELESCOPE_MIN = MCG_Size_Params_Class.GANGWAY_L_TELESCOPE_MIN + L_abs * (
                1 - self.TELESCOPE_STROKE_FACTOR
            )  # [m] Medium gangway minimum operational telescope stroke for dynamic compensation
            return GANGWAY_L_TELESCOPE_MIN

        @property
        def GANGWAY_L_TELESCOPE_MAX(self):
            L_abs = (MCG_Size_Params_Class.GANGWAY_L_TELESCOPE_MAX - MCG_Size_Params_Class.GANGWAY_L_TELESCOPE_MIN) / 2

            GANGWAY_L_TELESCOPE_MAX = MCG_Size_Params_Class.GANGWAY_L_TELESCOPE_MIN + L_abs * (
                1 + self.TELESCOPE_STROKE_FACTOR
            )  # [m] Medium gangway minimum operational telescope stroke for dynamic compensation
            return GANGWAY_L_TELESCOPE_MAX

        @property
        def V_TELESCOPE(self):
            V_TELESCOPE = self.TELESCOPE_VELOCITY_FACTOR * MCG_Size_Params_Class.V_TELESCOPE  # [m/s] Telescope velocity
            return V_TELESCOPE

    return MCG30TIPLADDER_FACTORY

class MCG30MTRANSFER_Params(MCG30M_Params, MCG30TRANSFER_Params, ABC):

    GANGWAY_L_TELESCOPE_MIN = 16.11  # [m] Medium gangway minimum operational telescope stroke for dynamic compensation

    GANGWAY_L_TELESCOPE_MAX = 24.13  # [m] Medium gangway maximum operational telescope stroke for dynamic compensation

class MCG30MHIGHLOAD_Params(MCG30M_Params, MCG30HIGHLOAD_Params, ABC):
    pass

class MCG30MLOWLOAD_Params(MCG30M_Params, MCG30LOWLOAD_Params, ABC):
    pass

class MCG30LTRANSFER_Params(MCG30L_Params, MCG30TRANSFER_Params, ABC):

    GANGWAY_L_TELESCOPE_MIN = 19  # [m] Large gangway minimum operational telescope stroke for dynamic compensation

    GANGWAY_L_TELESCOPE_MAX = 27  # [m] Large gangway maximum operational telescope stroke for dynamic compensation

class MCG30LHIGHLOAD_Params(MCG30L_Params, MCG30HIGHLOAD_Params, ABC):
    pass

class MCG30LLOWLOAD_Params(MCG30L_Params, MCG30LOWLOAD_Params, ABC):
    pass

MCG30MTIPLADDER_Params = MCG30TIPLADDER_FACTORY(MCG30MTRANSFER_Params)

MCG30LTIPLADDER_Params = MCG30TIPLADDER_FACTORY(MCG30LTRANSFER_Params)
