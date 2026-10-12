"""
MCG System properties to compute workability. Based on the old MATLAB utilization calculations.

References:
    [1] M:\Engineering\Database\Matlab scripts\Workability\MCG\MCG30_Utilization_Rev5.m
    [2] M:\Engineering\Database\Matlab scripts\Workability\MCG\MCG30_SystemParameters_Rev4.m

"""
from abc import ABC

import numpy as np
import xarray as xr
from matplotlib import pyplot as plt
from matplotlib.axes import Axes

from PyBM.marine.machines.machine_interface import Machine_Nonlinear
from PyBM.utils.data_classes import VesselDimensions

class MCG30_Nonlinear(Machine_Nonlinear, ABC):
    """
    Base class for MCG 3.0 for workability studies.
    All parameters are from [2]
    """

    def __init__(
        self, position, gw_luff_angle_mean, gw_slew_angle_mean, dp_accuracy=0.5, gw_telescope_mean=None
    ) -> None:
        """Create instance of the MCG30.
        :param position: [m] Position of the machine w.r.t. the RAO definitions.
        :param gw_luff_angle_mean: [m] mean luff angle of machine. Use for positioning of MCG and landing position.
        :param gw_slew_angle_mean: [m] mean slew angle of machine. Use for positioning of MCG and landing position.
        :param dp_accuracy: [m] accuracy of DP, assumes a circle with a radius of value given by this param. Default 0.5m
        """
        super().__init__(position, 0)

        self.MCGref = [0, 0, 0]

        self.base = self.XYZ_LUFF  # Luffing joint location w.r.t MCG pos

        self.gw_luff_angle_mean = gw_luff_angle_mean

        self.gw_slew_angle_mean = gw_slew_angle_mean

        self.gw_telescope_mean = gw_telescope_mean if gw_telescope_mean is not None else self.gw_L_mean

        self.dp_accuracy = dp_accuracy

        pos_tip = np.zeros(3)
        pos_tip[0] = (
            self.base[0]
            + np.cos(np.deg2rad(gw_slew_angle_mean)) * np.cos(np.deg2rad(gw_luff_angle_mean)) * self.gw_telescope_mean
        )
        pos_tip[1] = (
            self.base[1]
            + np.sin(np.deg2rad(gw_slew_angle_mean)) * np.cos(np.deg2rad(gw_luff_angle_mean)) * self.gw_telescope_mean
        )
        pos_tip[2] = self.base[2] + np.sin(np.deg2rad(gw_luff_angle_mean)) * self.gw_telescope_mean

        self.pos_tip = pos_tip  # Tip position in vessel

        self.POI_NAMES = ["MCGref", "base", "tip"]

        # self.poi_coordinates are w.r.t RAO CoG

        self.poi_coordinates = [self.apply_transform(c) for c in [self.MCGref, self.base, self.pos_tip]]

        self.workability_checks = {
            "telescope": self.check_telescope_position,
            "v_telescope": self.check_v_telescope,
            "an_luff": self.check_an_luff,
            "sys_pitch": self.check_max_system_pitch,
            "sys_roll": self.check_max_system_roll,
            "xy_acc": self.check_horizontal_acc,
            "heave_acc": self.check_heave_acc,
            "v_luff_cyl": self.check_v_luff_cyl,
            "v_slew": self.check_v_slew
            # "duty": self.check_duty_cycle
        }

    def get_POI(self):
        """Return POI positions w.r.t. RAO definitions."""
        return dict(zip(self.POI_NAMES, self.poi_coordinates))

    def check_telescope_position(self, trace: xr.Dataset, stdevs=3.7):
        # sqrt(X^2, Y^2, Z^2)
        L_telescope = trace["POS"].sel(dict(DOF=["telescope"], POI="base"), drop=True)

        # telescopic length, ignore yaw error dp_accuracy
        # Telescope length that is available for motion compensation. It is the
        # difference between the closest limit (min or max stroke) and the mean
        # telescope stroke, including DP positioning error
        available_tele = np.min(
            [
                L_telescope.mean("Time") - self.GANGWAY_L_TELESCOPE_MIN - np.abs(self.dp_accuracy),
                self.GANGWAY_L_TELESCOPE_MAX - L_telescope.mean("Time") - np.abs(self.dp_accuracy),
            ]
        )

        # Telescope length utilization is the ratio between dynamic use and difference between mean and limit
        return available_tele / (L_telescope.std("Time") * stdevs)

    def check_v_telescope(self, trace: xr.Dataset, stdevs=3.7):
        # sqrt(X^2, Y^2, Z^2)
        V_telescope = trace["VEL"].sel(dict(DOF="telescope", POI="base"), drop=True)

        # Telescope length utilization is the ratio between dynamic use and difference between mean and limit
        return self.V_TELESCOPE / (V_telescope.std("Time") * stdevs)

    def check_an_luff(self, trace: xr.Dataset, stdevs=3.7):
        an_luff = trace["POS"].sel(dict(DOF="an_luff", POI="base"), drop=True)
        an_luff_available4comp = np.min(
            [an_luff.mean("Time") - self.AN_LUFF_MIN, self.AN_LUFF_MAX - an_luff.mean("Time")]
        )
        return an_luff_available4comp / (an_luff.std("Time") * stdevs)

    def check_max_system_pitch(self, trace: xr.Dataset, stdevs=3.7):
        sys_pitch = trace["POS"].sel(dict(DOF="Ry", POI="base"), drop=True)
        return self.PITCH_SYSTEM_MAX / (sys_pitch.std("Time") * stdevs)

    def check_max_system_roll(self, trace: xr.Dataset, stdevs=3.7):
        sys_roll = trace["POS"].sel(dict(DOF="Rx", POI="base"), drop=True)
        return self.ROLL_SYSTEM_MAX / (sys_roll.std("Time") * stdevs)

    def check_horizontal_acc(self, trace: xr.Dataset, stdevs=3.7):
        a_horizontal = np.sqrt(
            np.power(
                trace["ACC"].sel(DOF=["X", "Y"], POI="MCGref", drop=True),
                2,
            ).sum("DOF")
        )
        # a_horizontal = trace["ACC"].sel(dict(DOF="horizontal", POI="CoG"), drop=True)
        a_horizontal_rms = np.sqrt(np.square(a_horizontal).mean("Time"))
        return self.A_HORIZONTAL_MAX / (a_horizontal_rms * stdevs)

    def check_heave_acc(self, trace: xr.Dataset, stdevs=3.7):
        std = trace["ACC"].sel(dict(DOF="Z", POI="base"), drop=True).std("Time")
        return self.A_HEAVE_MAX / (std * stdevs)

    def check_v_luff_cyl(self, trace: xr.Dataset, stdevs=3.7):
        luf_stroke = trace["VEL"].sel(dict(DOF="luf_stroke", POI="base"), drop=True)
        return self.V_LUFFCYL / (luf_stroke.std("Time") * stdevs)

    def check_v_slew(self, trace: xr.Dataset, stdevs=3.7):
        v_slew = trace["VEL"].sel(dict(DOF="an_slew", POI="base"), drop=True)
        return self.V_SLEW / (v_slew.std("Time") * stdevs)

    def check_duty_cycle(self, trace: xr.Dataset, stdevs=3.7):
        def to_accumulator_volume(Qtotal1dim, dt):
            V_acc = xr.zeros_like(Qtotal1dim)
            Q_pump = xr.zeros_like(Qtotal1dim)
            Q_acc = xr.zeros_like(Qtotal1dim)
            for i in enumerate(Qtotal1dim.Time):
                i = i[0]
                if i == 0:
                    continue
                if (Qtotal1dim[i] < self.Q_PUMP_MAX) and (float(V_acc[i - 1]) == 0):
                    Q_pump[i] = float(Qtotal1dim[i])
                    V_acc[i] = 0
                if (Qtotal1dim[i] < self.Q_PUMP_MAX) and (float(V_acc[i - 1]) != 0):
                    Q_pump[i] = self.Q_PUMP_MAX
                    Q_acc[i] = float(Qtotal1dim[i]) - self.Q_PUMP_MAX
                    V_acc[i] = float(V_acc[i - 1]) + (Q_acc[i - 1] + Q_acc[i]) * dt / 2
                    if V_acc[i] < 0:
                        V_acc[i] = 0
                else:
                    Q_pump[i] = self.Q_PUMP_MAX
                    Q_acc[i] = Qtotal1dim[i] - self.Q_PUMP_MAX
                    V_acc[i] = float(V_acc[i - 1]) + (Q_acc[i - 1] + Q_acc[i]) * dt / 2
                    if V_acc[i] > self.V_ACC_MAX:
                        V_acc = self.V_ACC_MAX
            return Q_pump, Q_acc, V_acc

        Q_telescope = np.abs(trace["VEL"].sel(dict(DOF="telescope", POI="base"), drop=True)) * self.A_TELESCOPEMOTOR
        Q_slew = np.abs(trace["VEL"].sel(dict(DOF="an_slew", POI="base"), drop=True)) * self.A_SLEWMOTOR
        Q_luffcyl = np.abs(
            xr.where(
                trace["VEL"].sel(dict(DOF="luf_stroke", POI="base"), drop=True) >= 0,
                trace["VEL"].sel(dict(DOF="luf_stroke", POI="base"), drop=True) * self.A_LUFFCYLBOTTOM,
                trace["VEL"].sel(dict(DOF="luf_stroke", POI="base"), drop=True) * self.A_LUFFCYLROD,
            )
        )
        Q_total = Q_telescope + Q_slew + Q_luffcyl
        dt = Q_total["Time"][1] - Q_total["Time"][0]
        Q_pump, Q_acc, V_acc = to_accumulator_volume(Q_total.squeeze(), dt)
        # Q_net = (Q_total-self.Q_PUMP_MAX)
        # Q_acc = -xr.where(Q_net < 0, -self.Q_PUMP_MAX, Q_net)
        # # xr.where(Q_net < 0, 0, -Q_net*dt).cumsum("Time").plot()
        # V_ac1 = xr.where(Q_net < 0, 0, -Q_net*dt).cumsum("Time")
        # Q_p_back = xr.where(V_ac1 < 0, -Q_net, 0)
        # V_ac2 = xr.where(-dt*Q_p_back.cumsum()<V_ac1, 0, Q_p_back)
        # Q_p_back2 = xr.where(Q_p_back < 0)
        return 100000000 / Q_total.std("Time")

    def translate_telescope(self, trace: xr.DataArray):
        XYZ_telescope = xr.DataArray(self.pos_tip + self.pos, dict(DOF=["X", "Y", "Z"])) - trace.sel(
            DOF=["X", "Y", "Z"], POI="base", drop=True
        )
        L_telescope = np.sqrt(np.power(XYZ_telescope, 2).sum("DOF"))
        return xr.concat([trace, L_telescope.assign_coords(dict(DOF="telescope"))], "DOF")

    def translate_an_luff_world(self, trace: xr.DataArray):
        L_telescope = trace.sel(DOF="telescope", POI="base", drop=True)
        vertical_distance = self.pos_tip[2] + self.pos[2] - trace.sel(DOF="Z", POI="base", drop=True)
        an_luff_world = np.rad2deg(np.arcsin(vertical_distance / L_telescope))
        return xr.concat([trace, an_luff_world.assign_coords(dict(DOF="an_luff_world"))], "DOF")

    def translate_an_luff(self, trace: xr.DataArray):
        an_luff_world = trace.sel(DOF="an_luff_world", POI="base", drop=True)
        an_luff = (
            an_luff_world
            - np.sin(np.deg2rad(self.gw_slew_angle_mean)) * trace.sel(dict(DOF="Rx", POI="base"), drop=True)
            + np.cos(np.deg2rad(self.gw_slew_angle_mean)) * trace.sel(dict(DOF="Ry", POI="base"), drop=True)
        )
        return xr.concat([trace, an_luff.assign_coords(dict(DOF="an_luff"))], "DOF")

    def translate_an_slew_world(self, trace: xr.DataArray):
        an_slew_world = np.rad2deg(
            np.arctan2(
                self.pos_tip[1] + self.pos[1] - trace.sel(dict(DOF="Y", POI="base"), drop=True),
                self.pos_tip[0] + self.pos[0] - trace.sel(dict(DOF="X", POI="base"), drop=True),
            )
        )
        if (self.pos_tip[0] - self.base[0]) < 0:
            an_slew_world = (an_slew_world + 360) % 360
            # negative x means that the slewing angle is between 90 and 270 degrees. due to disconiunity in arctan2, we need to add 180 degrees
        return xr.concat([trace, an_slew_world.assign_coords(dict(DOF="an_slew_world"))], "DOF")

    def translate_an_slew(self, trace: xr.DataArray):
        an_slew_world = trace.sel(DOF="an_slew_world", POI="base", drop=True)
        an_slew = an_slew_world - trace.sel(dict(DOF="Rz", POI="CoG"), drop=True)
        return xr.concat([trace, an_slew.assign_coords(dict(DOF="an_slew"))], "DOF")

    def translate_horizontal(self, trace: xr.DataArray):
        horizontal = np.sqrt(
            np.power(
                trace.sel(DOF=["X", "Y"], POI="MCGref", drop=True),
                2,
            ).sum("DOF")
        )
        return xr.concat([trace, horizontal.assign_coords(dict(DOF="horizontal"))], "DOF")

    def translate_luf_stroke(self, trace: xr.DataArray):
        an_luff = trace.sel(DOF="an_luff", POI="base", drop=True)
        luf_xan_x = (
            np.cos(np.deg2rad(an_luff)) * (self.XYZ_LUFFCYL_TELESCOPE_0ANGLE[0] - self.XYZ_LUFF[0])
            + self.XYZ_LUFF[0]
            - np.sin(np.deg2rad(an_luff)) * (self.XYZ_LUFFCYL_TELESCOPE_0ANGLE[2] - self.XYZ_LUFF[2])
        )
        luf_xan_z = (
            np.sin(np.deg2rad(an_luff)) * (self.XYZ_LUFFCYL_TELESCOPE_0ANGLE[0] - self.XYZ_LUFF[0])
            + self.XYZ_LUFF[2]
            + np.cos(np.deg2rad(an_luff)) * (self.XYZ_LUFFCYL_TELESCOPE_0ANGLE[2] - self.XYZ_LUFF[2])
        )
        luf_stroke = np.sqrt(
            np.square(luf_xan_x - self.XYZ_LUFFCYL_TRANSFER[0]) + np.square(luf_xan_z - self.XYZ_LUFFCYL_TRANSFER[2])
        )
        return xr.concat([trace, luf_stroke.assign_coords(dict(DOF="luf_stroke"))], "DOF")

    def get_workability_limit(self, trace, **kwargs):
        """
        Get workability limits for the machine. Returns an xarray with Hs limits. (assumes linear scalability of time trace)
        :param trace: trace to calculate utilizations for.
        :type trace: xarray.Dataset
        """
        pos_trace = xr.concat(
            [trace.assign_coords(POI="CoG")]
            + [
                trace.timedomain.translate_trace(poi).assign_coords(dict(POI=self.POI_NAMES[i]))
                for i, poi in enumerate(self.poi_coordinates)
            ],
            dim="POI",
        )
        # translate into different DOFs.
        pos_trace = self.translate_telescope(pos_trace)  # telescope
        pos_trace = self.translate_an_luff_world(pos_trace)
        pos_trace = self.translate_an_luff(pos_trace)
        pos_trace = self.translate_an_slew_world(pos_trace)
        pos_trace = self.translate_an_slew(pos_trace)
        pos_trace = self.translate_horizontal(pos_trace)
        pos_trace = self.translate_luf_stroke(pos_trace)

        tt = xr.Dataset()
        tt["POS"] = pos_trace
        tt["VEL"] = tt["POS"].differentiate("Time")
        tt["ACC"] = tt["VEL"].differentiate("Time")
        hs_lim = []
        for lim_type, check in self.workability_checks.items():
            hs_lim.append(check(tt, **kwargs).expand_dims(dim={"lim_type": [lim_type]}))
        return xr.concat(hs_lim, dim="lim_type")

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

class MCG30TRANSFER_Nonlinear(MCG30_Nonlinear, ABC):
    def __init__(self, position, gw_luff_angle_mean, gw_slew_angle_mean, dp_accuracy=0.1, gw_telescope_mean=None):
        super().__init__(position, gw_luff_angle_mean, gw_slew_angle_mean, dp_accuracy, gw_telescope_mean)
        self.workability_checks["an_slew_world"] = self.check_an_slew_world
        self.workability_checks["an_luff_world"] = self.check_an_luff_world

    def check_an_slew_world(self, trace: xr.Dataset, stdevs=3.7):
        an_slew_world = trace["POS"].sel(dict(DOF="an_slew_world", POI="base"), drop=True)
        return self.AN_SLEW_WORLD / (an_slew_world.std("Time") * stdevs)

    def check_an_luff_world(self, trace: xr.Dataset, stdevs=3.7):
        an_luff_world = trace["POS"].sel(dict(DOF="an_luff_world", POI="base"), drop=True)
        return self.AN_LUFF_WORLD / (an_luff_world.std("Time") * stdevs)

class MCG30LIFTING_Nonlinear(MCG30_Nonlinear, ABC):
    def __init__(self, position, gw_luff_angle_mean, gw_slew_angle_mean, dp_accuracy=0.1, gw_telescope_mean=None):
        super().__init__(position, gw_luff_angle_mean, gw_slew_angle_mean, dp_accuracy, gw_telescope_mean)

        self.lifting_radius = self.gw_telescope_mean / np.cos(np.deg2rad(self.gw_luff_angle_mean))

        self.workability_checks["v_tip"] = self.check_v_tip
        self.workability_checks["v_sys_roll"] = self.check_v_sys_roll
        self.workability_checks["v_sys_pitch"] = self.check_v_sys_pitch
        self.workability_checks["v_heave"] = self.check_v_heave

    def check_v_sys_roll(self, trace: xr.Dataset, stdevs=3.7):
        v_sys_roll = trace["VEL"].sel(dict(DOF="Rx", POI="base"), drop=True)
        return self.V_ROLL_SYSTEM_MAX / (v_sys_roll.std("Time") * stdevs)

    def check_v_sys_pitch(self, trace: xr.Dataset, stdevs=3.7):
        v_sys_pitch = trace["VEL"].sel(dict(DOF="Ry", POI="base"), drop=True)
        return self.V_PITCH_SYSTEM_MAX / (v_sys_pitch.std("Time") * stdevs)

    def check_v_heave(self, trace: xr.Dataset, stdevs=3.7):
        v_heave = trace["VEL"].sel(dict(DOF="Z", POI="base"), drop=True)
        return self.V_HEAVE_MAX / (v_heave.std("Time") * stdevs)

    def check_v_tip(self, trace: xr.Dataset, stdevs=3.7):
        radius = np.cos(np.deg2rad(self.gw_luff_angle_mean)) * self.gw_telescope_mean
        v_tip = (
            trace["VEL"].sel(dict(DOF="Z", POI="tip"), drop=True)
            + np.sin(np.deg2rad(self.gw_slew_angle_mean))
            * radius
            * trace["VEL"].sel(dict(DOF="Rx", POI="base"), drop=True)
            * np.pi
            / 180
            + np.cos(np.deg2rad(self.gw_slew_angle_mean))
            * radius
            * trace["VEL"].sel(dict(DOF="Ry", POI="base"), drop=True)
            * np.pi
            / 180
        )
        return self.tip_v_threshold / (v_tip.std("Time") * stdevs)
