"""
Linearized MCG. Based on the same limits as MCG30.py but with linearized equations according to first-order taylor expansions.

References
[1] M:\Engineering\R&D Projects\043 PyBM\Engineering\Linearization of the MCG DOFS.pptx 
"""
from abc import ABC

import numpy as np
import xarray as xr
from matplotlib import pyplot as plt
from matplotlib.axes import Axes

from PyBM.marine.machines.machine_interface import Machine_Linear
from PyBM.marine.machines.MCG30.mcg30_helper import (
    p2ds,
    partials_luff,
    partials_luff_cyl,
    partials_luff_world,
    partials_slew,
    partials_slew_world,
    partials_telescope,
    partials_v_tip,
)
from PyBM.utils.data_classes import VesselDimensions

class MCG30_Linear(Machine_Linear, ABC):
    """
    Base class for MCG 3.0 for workability studies.
    All parameters are from [2]
    """

    def __init__(
        self, position, gw_luff_angle_mean, gw_slew_angle_mean, dp_accuracy=0.5, gw_telescope_mean=None
    ) -> None:
        """Create instance of the MCG30.
        :param position: [m] Position of the machine w.r.t. the RAO definitions.
        :param gw_luff_angle_mean: [deg] mean luff angle of machine. Use for positioning of MCG and landing position.
        :param gw_slew_angle_mean: [deg] mean slew angle of machine. Use for positioning of MCG and landing position.
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

        self.dof_partials = {
            "telescope": partials_telescope(self.pos_tip, self.base),
            "an_luff": partials_luff(self.pos_tip, self.base, self.gw_slew_angle_mean),
            "an_slew": partials_slew(self.pos_tip, self.base),
            "luf_stroke": partials_luff_cyl(
                self.pos_tip,
                self.base,
                self.gw_slew_angle_mean,
                self.gw_luff_angle_mean,
                self.XYZ_LUFFCYL_TRANSFER,
                self.XYZ_LUFF,
                self.XYZ_LUFFCYL_TELESCOPE_0ANGLE,
            ),
        }

        self.workability_checks = {
            "telescope": self.check_telescope_position,
            "v_telescope": self.check_linearized_limit(self.V_TELESCOPE, "telescope", "base", "VEL"),
            "an_luff": self.check_an_luff,
            "sys_pitch": self.check_linearized_limit(self.PITCH_SYSTEM_MAX, "Ry", "base", "POS"),
            "sys_roll": self.check_linearized_limit(self.ROLL_SYSTEM_MAX, "Rx", "base", "POS"),
            "xy_acc": self.check_horizontal_acc,
            "heave_acc": self.check_linearized_limit(self.A_HEAVE_MAX, "Z", "base", "ACC"),
            "v_luff_cyl": self.check_linearized_limit(self.V_LUFFCYL, "luf_stroke", "base", "VEL"),
            "v_slew": self.check_linearized_limit(self.V_SLEW, "an_slew", "base", "VEL")
            # "duty": self.check_duty_cycle
        }

    def get_POI(self):
        """Return POI positions w.r.t. RAO definitions."""
        return dict(zip(self.POI_NAMES, self.poi_coordinates))

    def translate_linear_dof(self, rao, name, partials):
        t_rao = ((rao * p2ds(partials)).sum("DOF")).assign_coords(DOF=name)
        return xr.concat([rao, t_rao], dim="DOF")

    def apply_machine_dofs(self, rao):
        for name, partials in self.dof_partials.items():
            rao = self.translate_linear_dof(rao, name, partials)
        return rao

    def check_linearized_limit(self, limit, DOF, POI, order):
        return lambda mpe_at_poi: limit / mpe_at_poi[order].sel({"DOF": DOF, "POI": POI}, drop=True)

    def check_telescope_position(self, mpe_at_poi):
        L_telescope = mpe_at_poi["POS"].sel(dict(DOF=["telescope"], POI="base"), drop=True).squeeze()

        # Telescope length that is available for motion compensation. It is the
        # difference between the closest limit (min or max stroke) and the mean
        # telescope stroke, including DP positioning error. Ignore yaw dp error
        available_tele = np.min(
            [
                self.gw_telescope_mean - self.GANGWAY_L_TELESCOPE_MIN - np.abs(self.dp_accuracy),
                self.GANGWAY_L_TELESCOPE_MAX - self.gw_telescope_mean - np.abs(self.dp_accuracy),
            ]
        )
        return available_tele / L_telescope

    def check_an_luff(self, mpe_at_poi):
        an_luff = mpe_at_poi["POS"].sel(dict(DOF="an_luff", POI="base"), drop=True)
        an_luff_available4comp = np.min(
            [self.gw_luff_angle_mean - self.AN_LUFF_MIN, self.AN_LUFF_MAX - self.gw_luff_angle_mean]
        )
        return an_luff_available4comp / an_luff

    def check_horizontal_acc(self, mpe_at_poi):
        a_horizontal = np.sqrt(np.square(mpe_at_poi["ACC"].sel(DOF=["X", "Y"], POI="MCGref", drop=True)).sum("DOF"))
        return self.A_HORIZONTAL_MAX / a_horizontal

    def get_workability_limit(self, motion_at_poi, **kwargs):
        hs_lim = []
        for lim_type, check in self.workability_checks.items():
            hs_lim.append(check(motion_at_poi, **kwargs).expand_dims(dim={"lim_type": [lim_type]}))
        return xr.concat(hs_lim, dim="lim_type")

class MCG30TRANSFER_Linear(MCG30_Linear, ABC):
    def __init__(self, position, gw_luff_angle_mean, gw_slew_angle_mean, dp_accuracy=0.1, gw_telescope_mean=None):
        """
        Add linearized vertical tip velocity
        """
        super().__init__(position, gw_luff_angle_mean, gw_slew_angle_mean, dp_accuracy, gw_telescope_mean)
        self.workability_checks["an_slew_world"] = self.check_linearized_limit(
            self.AN_SLEW_WORLD, "an_slew_world", "base", "POS"
        )
        self.workability_checks["an_luff_world"] = self.check_an_luff_world
        self.dof_partials["an_slew_world"] = partials_slew_world(self.pos_tip, self.base)
        self.dof_partials["an_luff_world"] = partials_luff_world(self.pos_tip, self.base)

    def check_an_luff_world(self, mpe_at_poi):
        an_luff_world = mpe_at_poi["POS"].sel(dict(DOF="an_luff_world", POI="base"), drop=True).squeeze()
        return self.AN_LUFF_WORLD / an_luff_world

class MCG30LIFTING_Linear(MCG30_Linear, ABC):
    def __init__(self, position, gw_luff_angle_mean, gw_slew_angle_mean, dp_accuracy=0.1, gw_telescope_mean=None):
        """
        Add linearized vertical tip velocity
        """
        super().__init__(position, gw_luff_angle_mean, gw_slew_angle_mean, dp_accuracy, gw_telescope_mean)

        self.lifting_radius = self.gw_telescope_mean / np.cos(np.deg2rad(self.gw_luff_angle_mean))

        self.workability_checks["v_tip"] = self.check_linearized_limit(self.tip_v_threshold, "v_tip", "tip", "VEL")
        self.workability_checks["v_sys_roll"] = self.check_linearized_limit(self.V_ROLL_SYSTEM_MAX, "Rx", "base", "VEL")
        self.workability_checks["v_sys_pitch"] = self.check_linearized_limit(
            self.V_PITCH_SYSTEM_MAX, "Ry", "base", "VEL"
        )
        self.workability_checks["v_heave"] = self.check_linearized_limit(self.V_HEAVE_MAX, "Z", "base", "VEL")
        self.dof_partials["v_tip"] = partials_v_tip(
            self.gw_luff_angle_mean, self.gw_telescope_mean, self.gw_slew_angle_mean
        )
