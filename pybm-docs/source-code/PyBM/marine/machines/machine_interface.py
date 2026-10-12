""" Generic Interface for BM machine to compute workability"""
from abc import ABC, abstractmethod

import numpy as np
import xarray as xr
from scipy.spatial.transform import Rotation

from PyBM.marine.motion_analysis.MotionRAO import MotionRAO

class Machine_Linear(ABC):
    def __init__(self, position, orientation) -> None:
        """Abstract machine class.

        :param position: [m] Position of the machine w.r.t. the RAO definitions.
        :param orientation: [deg] Yaw orientation of the machine w.r.t. the RAO definitions.
        """

        self.pos = position

        self.orient = orientation

        self.rotation = Rotation.from_euler("z", self.orient, degrees=True)

    def apply_transform(self, point: np.array) -> np.array:
        """Apply rotation then translation to 3D point

        :param point: 3D vector [x,y,z]
        :type point: np.array
        :return: Transformed position
        :rtype: np.array
        """
        point = self.rotation.apply(point)
        point += self.pos
        return point

    def get_rao_at_poi(self, rao) -> MotionRAO:
        """Get the Motion RAOs at the POI"""
        rao_at_poi = xr.Dataset()
        for name, poi in self.get_POI().items():
            temp = MotionRAO.translate_rao(rao, poi).expand_dims(dim={"POI": [name]})
            rao_at_poi = rao_at_poi.merge(temp, combine_attrs="drop_conflicts", compat="no_conflicts", join="outer")
        rao_at_poi = self.apply_machine_dofs(rao_at_poi)  # Apply machine DOFs
        return rao_at_poi

    @abstractmethod

    def get_POI(self) -> dict:
        pass

    def apply_machine_dofs(self, rao) -> MotionRAO:
        return rao

    def get_workability_limit(self, motion_at_poi, **kwargs):
        hs_lim = []
        for lim_type, check in self.workability_checks.items():
            hs_lim.append(check(motion_at_poi, **kwargs).expand_dims(dim={"lim_type": [lim_type]}))
        return xr.concat(hs_lim, dim="lim_type")

    def __str__(self) -> str:
        return f"{self.__class__.__name__}: \n\tPosition: {self.pos}m, Orientation: {self.orient}deg"

class Machine_Nonlinear(ABC):
    def __init__(self, position, orientation) -> None:
        """Abstract machine class.

        :param position: [m] Position of the machine w.r.t. the RAO definitions.
        :param orientation: [deg] Yaw orientation of the machine w.r.t. the RAO definitions.
        """

        self.pos = position

        self.orient = orientation

        self.rotation = Rotation.from_euler("z", self.orient, degrees=True)

    def apply_transform(self, point: np.array) -> np.array:
        """Apply rotation then translation to 3D point

        :param point: 3D vector [x,y,z]
        :type point: np.array
        :return: Transformed position
        :rtype: np.array
        """
        point = self.rotation.apply(point)
        point += self.pos
        return point

    # def get_rao_at_poi(self, rao) -> MotionRAO:
    #     """Get the Motion RAOs at the POI"""
    #     rao_at_poi = xr.Dataset()
    #     for name, poi in self.get_POI().items():
    #         temp = MotionRAO.translate_rao(rao, poi).expand_dims(dim={"POI": [name]})
    #         rao_at_poi = rao_at_poi.merge(temp, combine_attrs="drop_conflicts")
    #     rao_at_poi = self.apply_machine_dofs(rao_at_poi)  # Apply machine DOFs
    #     return rao_at_poi

    @abstractmethod

    def get_POI(self) -> dict:
        pass

    # def apply_machine_dofs(self, rao) -> MotionRAO:
    #     return rao

    # def get_workability_limit(self, motion_at_poi, **kwargs):
    #     hs_lim = []
    #     for lim_type, check in self.workability_checks.items():
    #         hs_lim.append(check(motion_at_poi, **kwargs).expand_dims(dim={"lim_type": [lim_type]}))
    #     return xr.concat(hs_lim, dim="lim_type")

    # def __str__(self) -> str:
    #     return f"{self.__class__.__name__}: \n\tPosition: {self.pos}m, Orientation: {self.orient}deg"
