"""
Python class to compute Accumulator properties

Date: 15-05-2023
Author: CBR
Check: ---
"""

import matplotlib.pylab as plt
import numpy as np

from .accumulator import Accumulator
from .cylinder import Cylinder

class AccuCylinderCombination:
    def __init__(self, Vaccu, Pmax, Acyl, stroke) -> None:
        """Create passive Accu / Cylinder combination

        :param Vaccu: [m3] Gas volume of accu only.
        :param Pmax: [Pa] Maximum pressure of Accu.
        :param Acyl: [m2] Area of cylinder piston side.
        :param stroke: [m] Stroke of cylinder
        """

        self.accu = Accumulator(Vaccu, Pmax)

        self.cyl = Cylinder(Acyl, stroke, Pmax)

    def get_V1(self, Pcyl):
        """Volume of Accu at point Pcyl

        :param Pcyl: [m] Cylinder position (0 is retracted).
        :return: [m3] Volume at point Pcyl
        """
        return self.accu.V + Pcyl * self.cyl.A

    def get_p1(self, Pcyl):
        """Get Pressure at at point Pcyl.

        :param Pcyl: [m] Cylinder position (0 is retracted).
        :return: [Pa] pressure for Pcyl.
        """
        return self.accu.get_p1(self.get_V1(Pcyl))

    def get_cyl_force(self, Pcyl):
        """Cylinder force at point Pcyl

        :param Pcyl: [m] Cylinder position (0 is retracted).
        :return: [N] Force for Pcyl.
        """
        return self.get_p1(Pcyl) * self.cyl.A

    def get_pressure_ratio(self, Pcyl):
        """Ratio of Max Pressure to pressure at point Pcyl

        :param Pcyl: [m] Cylinder position (0 is retracted).
        :return: [Pa] pressure for Pcyl.
        """
        V1 = self.get_V1(Pcyl)
        return self.accu.get_pressure_ratio(V1)

    def mass_estimate(self):
        """Total mass estimate.

        :return: [kg] mass"""
        return self.cyl.mass_estimate() + self.accu.mass_estimate()

    def __str__(self) -> str:
        return self.accu.__str__() + "\n" + self.cyl.__str__()

    @classmethod

    def from_pressure_ratio_and_1_point(cls, pressure_ratio, L1, Acyl, P2, stroke, Max_Vaccu=np.inf):
        return cls.from_pressure_ratio_and_2_points(pressure_ratio, 0.0, L1, Acyl, P2, stroke, Max_Vaccu)

    @classmethod

    def from_pressure_ratio_and_2_points(cls, pressure_ratio, L2, L1, Acyl, P2, stroke, Max_Vaccu=np.inf):
        """Create class based on pressure ratio at 2 desired points.

        :param pressure_ratio: [-] P1/P2 ratio off desired pressures
        :param L2: [m] Length of cylinder at position 2 (corresponding to P2)
        :param L1: [m] Length of cylinder at position 1 (corresponding to P1)
        :param A: [m2] Cylinder Area
        :param P2: [Pa] Pressure at Point 2 of Accumulator
        """
        Delta_p = (pressure_ratio) ** (1 / Accumulator.k)
        Delta_L = L1 - L2
        V2 = Delta_p / (1 - Delta_p) * Delta_L * Acyl
        Vaccu = V2 - Acyl * L2
        Pmax = P2 * (V2 / Vaccu) ** Accumulator.k
        if Vaccu > Max_Vaccu:
            Vaccu = Max_Vaccu
            temp = (1 - Delta_p) / (Delta_p * Delta_L)
            Acyl = temp / (1 - temp * L2) * Vaccu
        return cls(Vaccu, Pmax, Acyl, stroke)

    @classmethod

    def from_pressure_ratio_and_V2(cls, pressure_ratio, L1, V2, Fcyl, stroke, Max_P2=np.inf):
        """Create class based on pressure ratio and V2

        :param pressure_ratio: [-] P1/P2 ratio off desired pressures
        :param L1: [m] Length of cylinder at position 1 (corresponding to P1)
        :param V2: [m3] Volume of accumulator
        :param Fcyl: [N] maximum force of Cylinder
        """
        Delta = (pressure_ratio) ** (1 / Accumulator.k)
        Acyl = V2 * (1 - Delta) / L1
        P2 = Fcyl / Acyl
        if P2 > Max_P2:
            P2 = Max_P2
            Acyl = Fcyl / P2
        return cls(V2, P2, Acyl, stroke)

    def plot_force(self, axs=None):
        """Plot properties of the combination.

        :param axs: Axes to plot on, defaults to None
        """
        axs = axs or plt.gca()
        Pcyl = np.linspace(0, self.cyl.stroke)
        Fcyl = self.get_cyl_force(Pcyl)
        axs.plot(Pcyl, Fcyl / 1e3)
        axs.set_xlabel("[m] Cylinder stroke")
        axs.set_ylabel("[kN] Cylinder Force")
        axs.grid(True)
