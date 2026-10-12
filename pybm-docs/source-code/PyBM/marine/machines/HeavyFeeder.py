""" Heavy Feeder class to compute workability

References:

    [1] TWD-NL-2021-512-D-010-REV-2, General Arrangement CYLINDER NUMBERING
    [2] NL002692-02-50-2000-HYD-0001-RAF Hydraulic diagram Roll Pitch Cylinder assembly_AB

"""

import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
from matplotlib.axes import Axes

from PyBM.hydraulics import DoubleActingCylinder
from PyBM.marine.machines.machine_interface import Machine_Linear
from PyBM.utils import disc_area

class HeavyFeeder(Machine_Linear):
    # Mechanical properties Ref [1]

    cyl_arm_roll = 10.409  # [m] from cylinder to central bearing in roll

    cyl_arm_pitch = 7.327  # [m] from cylinder to central bearing in pitch

    tds_arm_roll = 11.43  # [m] from TDS to central bearing in roll

    tds_arm_pitch = 8  # [m] from TDS to central bearing in pitch

    cb_to_tbic_top = 5.12 + 1.3  # [m] from central bearing to platform

    # Hydraulic properties Ref [2]

    vmax = 0.455  # [m/s]  maximum cylinder velocity

    bore = 0.47  # [m] bore diameter

    rod = 0.23  # [m] rod diameter

    stroke = 1.1  # [m] Working stroke

    p_hpu = 315e5  # [Pa] Maximum HPU pressure

    p_hold_bot = 350e5  # [Pa] Bottom side holding pressure

    p_hold_rod = 420e5  # [Pa] Rodside holding pressure

    # Operational

    comp_point_max_horizontal_motion = 2.0  # [m] maximum tower top motion (double amplitude)

    cylinder = DoubleActingCylinder(disc_area(bore), disc_area(bore) - disc_area(rod), stroke, p_hpu)

    CYLINDER_NAMES = ["c1", "c2"]

    N_CYLINDERS = len(CYLINDER_NAMES)

    POI_NAMES = ["central_bearing", "comp_point"]

    # Derived properties
    @property

    def c1(self):
        return np.array([self.cyl_arm_pitch, self.cyl_arm_roll, 0])

    @property

    def c2(self):
        return np.array([-self.cyl_arm_pitch, self.cyl_arm_roll, 0])

    def __init__(self, position, orientation, comp_point=[0, 0, 0]) -> None:
        """Create instance of the Heavy Feeder.

        :param position: [m] Position of the central Bearing w.r.t. the RAO definitions.
        :param orientation: [deg] Yaw orientation of the machine w.r.t. the RAO definitions, 0 degrees = cylinders on Port side.
        :param comp_point: [m] Point at which the surge sway motion will be evaluated for the horizontal motion limit w.r.t. central bearing
        """
        super().__init__(position, orientation)

        self.cylinder_coordinates = [self.apply_transform(c) for c in [self.c1, self.c2]]

        self.comp_point_wrt_cb = np.array(comp_point)

        self.comp_point = self.apply_transform(np.array(comp_point))

        self.workability_checks = {
            "stroke": self.check_stroke_limit,
            "cylinder_vel": self.check_cylinder_velocity_limit,
            "tower_horizontal_motion": self.check_horizontal_motion,
            "tower_horizontal_motion_no_comp": self.check_horizontal_motion_no_comp,
        }

    def get_POI(self):
        """Return cylinder positions w.r.t. RAO definitions."""
        poi = dict(zip(self.POI_NAMES, [self.pos, self.comp_point]))
        return poi

    def apply_machine_dofs(self, rao):
        for name, coord in zip(self.CYLINDER_NAMES, [self.c1, self.c2]):
            c_rao = (
                rao.sel(DOF="Rx") / 180 * np.pi * coord[1] + rao.sel(DOF="Ry") / 180 * np.pi * coord[0]
            ).assign_coords(dict(DOF=name))
            rao = xr.concat([rao, c_rao], dim="DOF")
        return rao

    def check_stroke_limit(self, motion_at_poi):
        mpe = motion_at_poi["POS"].sel(DOF=self.CYLINDER_NAMES, POI="central_bearing", drop=True)
        return self.stroke / (2 * mpe.max(dim="DOF"))  # amplitude (+/-) vs max stroke

    def check_cylinder_velocity_limit(self, motion_at_poi):
        cylinder_vel = motion_at_poi["VEL"].sel(DOF=self.CYLINDER_NAMES, POI="central_bearing", drop=True)
        return self.vmax / cylinder_vel.max(dim="DOF")

    def check_horizontal_motion_no_comp(self, motion_at_poi):
        X = motion_at_poi["POS"].sel(DOF="X", POI="comp_point", drop=True)
        Y = motion_at_poi["POS"].sel(DOF="Y", POI="comp_point", drop=True)
        mpe = np.sqrt(np.square(X) + np.square(Y))  # Conservative assumption because phase is not considered
        return self.comp_point_max_horizontal_motion / (2 * mpe)

    def check_horizontal_motion(self, motion_at_poi):
        X = motion_at_poi["POS"].sel(DOF="X", POI="central_bearing", drop=True)
        Y = motion_at_poi["POS"].sel(DOF="Y", POI="central_bearing", drop=True)
        mpe = np.sqrt(np.square(X) + np.square(Y))  # Conservative assumption because phase is not considered
        return self.comp_point_max_horizontal_motion / (2 * mpe)

    def plot(self, axs: Axes = None):
        axs = axs or plt.gca()
        # Plot Cylinder points
        x = [c[0] for c in self.cylinder_coordinates + [self.pos] + [self.cylinder_coordinates[0]]]
        y = [c[1] for c in self.cylinder_coordinates + [self.pos] + [self.cylinder_coordinates[0]]]
        axs.plot(self.pos[0], self.pos[1], "ro")
        axs.plot(x, y, "b")
        for i, c in enumerate(self.cylinder_coordinates):
            axs.annotate(f"c{i+1:d}", c[0:2])
        # plot Circle
        angle = np.linspace(0, 2 * np.pi, 100)
        plt.plot(self.pos[0] + 4 * np.cos(angle), self.pos[1] + 4 * np.sin(angle), "b")
        axs.annotate("Bow", xy=(0.95, 0.5), xycoords="axes fraction")
        axs.annotate("Port", xy=(0.5, 0.95), xycoords="axes fraction")
        axs.annotate("Starboard", xy=(0.5, 0.05), xycoords="axes fraction")
        axs.axis("equal")
        axs.grid(True)
        axs.set_xlabel("x")
        axs.set_ylabel("y")
