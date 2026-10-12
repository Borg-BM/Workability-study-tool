"""
Python class to compute Accumulator properties

Date: 15-05-2023
Author: CBR
Check: ---
"""

accu_density = 50 / (
    50 / 1000
)  # [kg/m3] based on 70kg for a 50L cylinder Ref [https://specialty.airliquide.co.uk/product/nitrogen-5-0-50/?industry=life-sciences]

class Accumulator:

    k = 1.4

    n2_density = 1.2506  # [kg/m3] @ 0Dergrees celcius 1 Atmosphere

    Patm = 1.013e5  # [Pa] Atmospheric pressure

    def __init__(self, Vaccu, Pmax) -> None:

        self.V = Vaccu

        self.Pmax = Pmax

    def get_p1(self, V1):
        """Get Pressure for given Volume V1.

        :param V1: Volume [m3]
        :return: [Pa] pressure for V1.
        """
        return self.Pmax * self.get_pressure_ratio(V1)

    def get_pressure_ratio(self, V1):
        """Ratio of Max Pressure to pressure at point V1

        :param V1: Volume [m3]
        :return: [Pa] pressure for V1.
        """
        return self.V**self.k / (V1) ** self.k

    def mass_estimate(self):
        """Container Mass estimate based on accu volume

        :return: [kg] mass
        """
        return self.V * accu_density

    def gas_mass(self):
        """Get mass of Nitrogen gas.

        :return: [kg] mass"""
        Vatm = self.V * (self.Pmax + self.Patm) / self.Patm  # Ideal gas law
        return Vatm * self.n2_density

    def __str__(self) -> str:
        return f"Accumulator: Vaccu={self.V*1e3:.0f}L, Pmax={self.Pmax/1e5:.0f}Bar, Mass estimate={self.mass_estimate()/1e3:.0f}t"
