"""

Python class to compute barge hydrostatics

Date: 15-05-2023
Author: CBR
Check: JHO
"""

import numpy as np

from ..constants import *
from ..utils import *

class Barge:
    def __init__(self, L, B, Depth, Draft, KG, name=None) -> None:
        """Barge info and Hydrostatics

        :param L: Length [m]
        :param B: Breadth [m]
        :param Depth: Depth [m]
        :param Draft: Draft [m]
        :param KG: Height from keel to center of gravity [m]
        """

        self.name = name

        self.L = L

        self.B = B

        self.Depth = Depth

        self.Draft = Draft

        self.KG = KG

        self.KB = self.Draft / 2

        self._disp = None

        self._Ixx = None

        self._Iyy = None

    @property

    def Awl(self):
        return self.L * self.B  # [m^2] waterline area

    @property

    def disp(self):
        if self._disp:
            return self._disp
        return self.Awl * self.Draft  # [m^3] displacement

    @disp.setter
    def disp(self, value):
        """Displacement [m3]"""
        self._disp = value

    @property

    def mass(self):
        return self.disp * rho  # [kg] mass of barge

    @property

    def Iyy(self):
        """Momement of intertia around y-axis (pitch inertia) based on solid cuboid.

        :return: [kg.m2]
        """
        if self._Iyy:
            return self._Iyy
        return self.mass * (self.L**2 + self.Depth**2) / 12

    @Iyy.setter
    def Iyy(self, value):
        self._Iyy = value

    @property

    def Ixx(self):
        """Momement of intertia around x-axis (roll inertia) based on solid cuboid.

        :return: [kg.m2]
        """
        if self._Ixx:
            return self._Ixx
        return self.mass * (self.B**2 + self.Depth**2) / 12

    @Ixx.setter
    def Ixx(self, value):
        self._Ixx = value

    @property

    def heave_stiffness(self):
        """Compute hydrostatic Heave stiffness of barge.

        :return: Heave stiffness [N/m]
        :rtype: float
        """
        return rho * g * self.Awl

    @property

    def heave_period(self):
        """Natural period of Heave.

        :return: [s]
        """
        return 2 * np.pi * np.sqrt(self.mass / self.heave_stiffness)

    @property

    def pitch_stiffness(self):
        """Compute hydrostatic pitch stiffness of barge (for small angles).

        :return: Pitch stiffness [Nm/rad]
        :rtype: float
        """
        It_pitch = self.B * self.L**3 / 12  # [m^4] second moment of area
        BN = (
            It_pitch / self.disp
        )  # [m] metacentric height from center of buoyancy BN = BM for small angles (approx 0.1% difference for 3deg pitch)
        GN = self.KB + BN - self.KG  # [m] metacentric height from center of gravity
        k_pitch = rho * g * self.disp * GN
        return k_pitch

    @property

    def roll_stiffness(self):
        """Compute hydrostatic roll stiffness of barge (for small angles).

        :return: Roll stiffness [Nm/rad]
        :rtype: float
        """
        It_roll = self.B**3 * self.L / 12  # [m^4] second moment of area
        BN = (
            It_roll / self.disp
        )  # [m] metacentric height from center of buoyancy BN = BM for small angles (approx 0.1% difference for 3deg pitch)
        GN = self.KB + BN - self.KG  # [m] metacentric height from center of gravity
        k_roll = rho * g * self.disp * GN
        return k_roll

    @property

    def pitch_period(self):
        """Natural period of pitch.

        :return: [s]
        """
        return 2 * np.pi * np.sqrt(self.Iyy / self.pitch_stiffness)

    @property

    def roll_period(self):
        """Natural period of Roll.

        :return: [s]
        """
        return 2 * np.pi * np.sqrt(self.Ixx / self.roll_stiffness)

    @property

    def Rxx(self):
        """Radius of gyration in Roll.

        :return: [m]
        """
        return self._radii_of_gyration(self.Ixx)

    @property

    def Ryy(self):
        """Radius of gyration in Pitch.

        :return: [m]
        """
        return self._radii_of_gyration(self.Iyy)

    def _radii_of_gyration(self, Inertia):
        return np.sqrt(Inertia / self.mass)

    def heave_stiffness_at_POI(self, POI: POI) -> float:
        """Get heave stiffness at POI.

        :param POI: position of POI from barge center point.
        :return: [N/m] heave stiffness of POI.
        """
        result = 1 / self.heave_stiffness
        result += POI.x**2 / self.pitch_stiffness
        result += POI.y**2 / self.roll_stiffness
        return 1 / result

    def __str__(self) -> str:
        return (
            f"Barge: {self.name} L={self.L:.1f} m, B={self.B:.1f} m, Depth={self.Depth:.2f} m, Draft={self.Draft:.2f} m"
        )

    def roll_stats(self) -> str:
        return f"Roll: T={self.roll_period:.2f}s, Rxx={self.Rxx:.2f}m"
