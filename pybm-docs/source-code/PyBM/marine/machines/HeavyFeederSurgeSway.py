""" Heavy Feeder class to compensate Surge and Sway motion of a POI
"""
import xarray as xr

from PyBM.marine.machines.HeavyFeeder import HeavyFeeder

class HeavyFeederSurgeSway(HeavyFeeder):
    def __init__(self, position, orientation, comp_point=[0, 0, 0]) -> None:
        """Create instance of the Heavy Feeder that compensates surge sway.

        :param position: [m] Position of the central Bearing w.r.t. the RAO definitions.
        :param orientation: [deg] Yaw orientation of the machine w.r.t. the RAO definitions, 0 degrees = cylinders on Port side.
        :param comp_point: [x, y, z] [m] Point at which the surge sway motion will be compensated w.r.t. central bearing
        """
        assert comp_point[2] > 0, "The compensation point be above the central bearing to compensate surge sway motion."
        super().__init__(position, orientation, comp_point)

        self.workability_checks = {
            "stroke": self.check_stroke_limit,
            "cylinder_vel": self.check_cylinder_velocity_limit,
            "horizontal_motion_no_comp": self.check_horizontal_motion_no_comp,
        }

    def get_POI(self):
        """Return cylinder positions w.r.t. RAO definitions."""
        poi = dict(zip(self.POI_NAMES, [self.pos, self.comp_point]))
        return poi

    def apply_machine_dofs(self, rao):
        rx = rao.sel(DOF="Y", POI="comp_point", drop=True) / self.comp_point_wrt_cb[2]
        ry = rao.sel(DOF="X", POI="comp_point", drop=True) / self.comp_point_wrt_cb[2]
        for name, coord in zip(self.CYLINDER_NAMES, [self.c1, self.c2]):
            c_rao = (rx * coord[1] + ry * coord[0]).assign_coords(dict(DOF=name))
            rao = xr.concat([rao, c_rao], dim="DOF")
        return rao

    def check_stroke_limit(self, motion_at_poi):
        mpe = motion_at_poi["POS"].sel(DOF=self.CYLINDER_NAMES, POI="central_bearing", drop=True)
        # Alowable stroke assuming mean cilinder arm between roll and pitch
        allowable_stroke = (
            self.stroke
            + self.comp_point_max_horizontal_motion
            * ((self.cyl_arm_pitch + self.cyl_arm_roll) / 2)
            / self.comp_point_wrt_cb[2]
        )
        return allowable_stroke / (2 * mpe.max(dim="DOF"))  # amplitude (+/-) vs max stroke
