"""
Python class to compute Cylinder properties

Date: 15-05-2023
Author: CBR
Check: ---

References:
    [1]: NL002692-02-50-2100-ADM-0001-RAI RA98725531
"""

import numpy as np

# HF RP Cylinder properties Ref. [1]

HF_cylinder_bore = 0.47  # [m] bore of cylinder.

HF_cylinder_area = 0.25 * np.pi * HF_cylinder_bore**2  # [m2] cylinder area

HF_cylinder_stroke = 1.47  # [m] cylinder stroke

HF_cylinder_mass = 6959  # [kg] weight including oil, excluding manifold

HF_cylinder_volume = HF_cylinder_area * HF_cylinder_stroke  # [m3] cylinder (oil) volume

HF_manifold_mass = 3508  # [kg] manifold mass

HF_max_vel = 0.455  # [m/s] Maximum velocity

HF_max_flow = HF_max_vel * HF_cylinder_area  # [m3/s]

class Cylinder:
    def __init__(self, piston_area, stroke, max_pressure, minLength=None) -> None:
        """Hydraulic cylinder class.

        :param piston_area: [m2] Area of piston side
        :param stroke: [m] Stroke of cylinder
        :param max_pressure: [Pa] Maximum pressure of the cylinder
        :param minLength: [m] Length of retracted cylinder
        """

        self.A = piston_area

        self.stroke = stroke

        self.minLength = minLength

        self.Pmax = max_pressure

        self.max_vel = np.inf

    @property

    def Dia(self):
        """Diameter of cylinder [m]."""
        return np.sqrt(self.A / np.pi) * 2

    @property

    def Maxforce(self):
        """Maximum force of cylinder [N]."""
        return self.A * self.Pmax

    @property

    def Maxflow(self):
        """Maximum flow of cylinder [m3/s]."""
        return self.A * self.max_vel

    def get_stroke(self, Lcyl):
        """Get cylinder stroke from cylinder length

        :param Lcyl: [m] Total required length of cylinder
        """
        return Lcyl - self.minLength

    def __str__(self) -> str:
        return f"Cylinder: Stroke={self.stroke:.2f}m Dia={self.Dia:.2f}m, Max Pushing Force={self.Maxforce/1e3:.0f}kN, mass={self.mass_estimate()/1e3:.0f}t"

    def mass_estimate(self):
        """Cylinder and manifold mass estimate based  HF cylinder mass.

        :return: [kg] Mass estimate of cylinder and manifold.
        """
        return self.cylinder_mass_estimate() + self.manifold_mass_estimate()

    def cylinder_mass_estimate(self):
        """Give cylinder mass estimate scaled based on HF cylinder area.
        return: [kg] mass estimate.
        """
        return (self.stroke * self.Dia) / (HF_cylinder_bore * HF_cylinder_stroke) * HF_cylinder_mass

    def manifold_mass_estimate(self):
        """Manifold mass scaled based on HF cylinder flow.

        :return: [m3] manifold mass estimate.
        """
        return self.max_vel / HF_max_vel * HF_manifold_mass

class DoubleActingCylinder(Cylinder):
    def __init__(self, piston_area, ring_area, stroke, max_pressure, minLength=None) -> None:
        super().__init__(piston_area, stroke, max_pressure, minLength)

        self.ring_area = ring_area

    def max_pulling_force(self):
        """Maximum pulling force.

        :return: [N] pulling force
        """
        return self.Pmax * self.ring_area

    def __str__(self) -> str:
        return super().__str__() + f", Max Pulling force={self.max_pulling_force()/1e3:.0f}kN"

class TripleChamberCylinder(DoubleActingCylinder):
    def __init__(
        self,
        piston_area,
        ring_area,
        inner_rod_area,
        stroke,
        max_pressure,
        max_passive_pressure=None,
        minLength=None,
    ) -> None:
        super().__init__(inner_rod_area, ring_area, stroke, max_pressure, minLength)

        self.max_passive_pressure = max_passive_pressure or max_pressure

        self.passive_area = piston_area - inner_rod_area

    def max_passive_force(self):
        """Maximum force of the passive chamber.

        :return: [N] passive force
        """
        return self.passive_area * self.max_passive_pressure

    def __str__(self) -> str:
        return super().__str__() + f", Max passive force={self.max_passive_force()/1e3:.0f}kN"
