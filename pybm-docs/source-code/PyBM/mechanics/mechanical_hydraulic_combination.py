import matplotlib.pyplot as plt
import numpy as np

from ..hydraulics.accu_cylinder_combination import AccuCylinderCombination
from .mechanical_interface import MechanicalInterface

class MechanicalHydraulicCombination:
    def __init__(self, mechanics: MechanicalInterface, hydraulics: AccuCylinderCombination) -> None:

        self.mech = mechanics

        self.hyd = hydraulics

    def get_force(self, Se):
        Fcyl_over_Fe = self.mech.force_ratio(Se)
        Lcyl = self.mech.L_cylinder(Se)
        stroke = self.hyd.cyl.get_stroke(Lcyl)
        return self.hyd.get_cyl_force(stroke) / Fcyl_over_Fe

    def __plot(
        self,
        fcn,
        axes: plt.Axes = None,
    ):
        axes = axes or plt.gca()
        Se = np.linspace(self.mech.min_pos, self.mech.max_pos)
        axes.plot(Se, fcn(Se))
        axes.set_xlabel("[m] Effective Stroke")
        axes.grid(True)
        return axes

    def plot_force(self, axes: plt.Axes = None):
        fcn = lambda x: self.get_force(x) / 1e3
        axes = self.__plot(fcn, axes)
        axes.set_ylabel("[kN] Effective Force")

    def plot_error(self, design_force, axes: plt.Axes = None):
        fcn = lambda x: (self.get_force(x) - design_force) / design_force * 100
        axes = self.__plot(fcn, axes)
        axes.set_ylabel("[%] Error")
