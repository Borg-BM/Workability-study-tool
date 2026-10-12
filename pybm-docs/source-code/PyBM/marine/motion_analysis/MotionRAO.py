"""
Motion RAO class. Inherits RAO class and xarray.Dataset
Init as Dataset with Three dataarrays:
POS (positional RAO values)
VEL (velocity RAO values)
ACC (acceleration RAO values)

CBR 21-06-2023

References:
 [1] Ship Motion Control, Tristan Perez
"""
import numpy as np

from PyBM.marine.motion_analysis.RAO import RAO

class MotionRAO(RAO):

    __slots__ = ()

    def translate_rao(self, offset):
        """
        Translates the RAO to a point of interest. Ref[1] eq (4.27)

        :param offset: [m] (x,y,z) offset of the point of interest
        :return: Full vessel motion RAOs around POI
        """
        if len(offset) != 3:
            raise ValueError("Offset should be vector of length 3: [x,y,z]")
        Resp = self.copy(deep=True)

        roll = (np.pi / 180) * (Resp.loc[dict(DOF="Rx")])
        pitch = (np.pi / 180) * (Resp.loc[dict(DOF="Ry")])
        yaw = (np.pi / 180) * (Resp.loc[dict(DOF="Rz")])

        Resp.loc[dict(DOF="X")] += -offset[1] * yaw + offset[2] * pitch
        Resp.loc[dict(DOF="Y")] += offset[0] * yaw - offset[2] * roll
        Resp.loc[dict(DOF="Z")] += -offset[0] * pitch + offset[1] * roll

        return Resp
