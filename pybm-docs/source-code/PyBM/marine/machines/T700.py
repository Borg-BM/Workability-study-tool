"""T700 System properties to compute workability

References:
    [1] RA53967897_AC_1_GEZ_001
    [2] TWD-2015-006-D-100-REV-1, FOUNDATION -GENERAL ARRANGEMENT
    [3] T700_SystemParameters_Rev0

"""
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes

from PyBM.hydraulics import TripleChamberCylinder
from PyBM.marine.machines.machine_interface import Machine_Linear
from PyBM.marine.motion_analysis import compute_response
from PyBM.utils import component_absolute, disc_area

class T700(Machine_Linear):

    cd = 13.8  # [m] distance between cylinders

    vmax = 0.736  # [m/s]  maximum cylinder velocity [3]

    vmax_center = 0.44  # [m/s] maximum platform center velocity [3]

    stroke = 2.2  # [m] Working stroke [1]

    max_flow = 0.044  # [m3/s] maximum flow of the system [1]

    bore = 0.42  # [m] bore diameter [1]

    rod = 0.33  # [m] rod diameter [1]

    rod_center = 0.26  # [m] diameter of passive chamber [1]

    cylinder = TripleChamberCylinder(
        disc_area(bore),
        disc_area(bore) - disc_area(rod),
        disc_area(rod_center),
        stroke,
        35e6,
    )

    CYLINDER_NAMES = ["c1", "c2", "c3"]

    N_CYLINDERS = len(CYLINDER_NAMES)

    POI_NAMES = ["center"] + CYLINDER_NAMES

    # Derived properties
    @property

    def h(self):
        return np.sqrt(3) / 2 * self.cd

    @property

    def c1(self):
        return np.array([-self.h / 3, -self.cd / 2, 0])

    @property

    def c2(self):
        return np.array([-self.h / 3, self.cd / 2, 0])

    @property

    def c3(self):
        return np.array([self.h * 2 / 3, 0, 0])

    def __init__(self, position, orientation, P_passive=35e6) -> None:
        """Create instance of the T700.

        :param position: [m] Position of the machine w.r.t. the RAO definitions.
        :param orientation: [deg] Yaw orientation of the machine w.r.t. the RAO definitions.
        :param P_passive: [Pa] Pressure of passive chamber.
        """
        super().__init__(position, orientation)

        self.P_passive = P_passive

        self.cylinder_coordinates = [self.apply_transform(c) for c in [self.c1, self.c2, self.c3]]

        self.workability_checks = {
            "stroke": self.check_stroke_limit,
            "cylinder_vel": self.check_cylinder_velocity_limit,
            "platform_vel": self.check_platform_velocity_limit,
            # "flow": self.check_flow_limit,
        }

    def get_POI(self):
        """Return cylinder positions w.r.t. RAO definitions."""
        poi = dict(zip(self.POI_NAMES, [self.pos] + self.cylinder_coordinates))
        return poi

    def check_stroke_limit(self, motion_at_poi):
        mpe = motion_at_poi["POS"].sel(DOF="Z", POI=self.CYLINDER_NAMES, drop=True)
        return self.stroke / (2 * mpe.max(dim="POI"))  # amplitude (+/-) vs max stroke

    def check_cylinder_velocity_limit(self, motion_at_poi):
        cylinder_vel = motion_at_poi["VEL"].sel(DOF="Z", POI=self.CYLINDER_NAMES, drop=True)
        return self.vmax / cylinder_vel.max(dim="POI")

    def check_platform_velocity_limit(self, motion_at_poi):
        platform_vel = motion_at_poi["VEL"].sel(DOF="Z", POI="center", drop=True)
        return self.vmax_center / platform_vel

    # def check_flow_limit(self, rao_at_poi, wave, **kwargs):
    #     """Compute frequency domain flow limit. TODO: Check flow signal frequency for MPE calculation."""
    #     flow_rao = component_absolute(
    #         rao_at_poi["VEL"].sel(DOF="Z", POI=self.CYLINDER_NAMES, drop=True)
    #     ).sum(dim="POI")
    #     flow_response = compute_response(wave, flow_rao)
    #     mpe_flow = MPE_from_response(flow_response, **kwargs) * (self.cylinder.A)
    #     return self.max_flow / mpe_flow

    def compute_cylinder_forces(self, Fz, Mx, My):
        # cylinder locations
        d1 = self.cylinder_coordinates[0][0:2]
        d2 = self.cylinder_coordinates[1][0:2]
        d3 = self.cylinder_coordinates[2][0:2]
        a = np.array([[1, 1, 1], [d1[1], d2[1], d3[1]], [d1[0], d2[0], d3[0]]])
        b = np.array([Fz, Mx, My])
        return np.linalg.solve(a, b)

    def plot(self, axs: Axes = None):
        axs = axs or plt.gca()
        x = [c[0] for c in self.cylinder_coordinates + [self.cylinder_coordinates[0]]]
        y = [c[1] for c in self.cylinder_coordinates + [self.cylinder_coordinates[0]]]
        axs.plot(self.pos[0], self.pos[1], "ro")
        axs.plot(x, y)
        for i, c in enumerate(self.cylinder_coordinates):
            axs.annotate(f"{i+1:d}", c[0:2])
        axs.annotate("Bow", (np.max(x), np.mean(y)))
        axs.annotate("Port", (np.mean(x), np.max(y)))
        axs.axis("equal")
        axs.grid(True)
        axs.set_xlabel("x")
        axs.set_ylabel("y")

if __name__ == "__main__":

    pos = [10, 20, 0]

    orientation = 90
    bm003 = T700(pos, orientation, 350e6)
    print(bm003)
    bm003.plot()
    plt.show()
