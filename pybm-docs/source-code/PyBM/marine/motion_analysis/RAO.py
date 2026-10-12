"""
Base class for RAOs of Vessels. Inherits xarray.Dataset.

Each dataarray must have coordinates
- Frequency [Hz]
- Direction [deg] - Must be from 0 to 360 deg (full circle), including 0 and 360 deg. 0 deg means waves coming from the stern direction, 90 deg starboard, 180 deg bow, 270 deg port
- DOF: ["X", "Y", "Z", "Rx", "Ry", "Rz"]
Values of the dataarray are in [m/m] or [deg/m] (angle)

The following conventions should ALWAYS be used for the RAO:
 - Surge: Forward
 - Sway: to Port
 - Heave: Up
 - Roll: Port up
 - Pitch: Bow down
 - Yaw: Bow to port

 Wave directions:
- 0 deg: Waves coming from the stern
- 90 deg: Waves coming from starboard

CBR 21-06-2023
"""

from abc import ABC, abstractmethod
from enum import Enum
from pathlib import Path

import matplotlib.pyplot as plt
import netCDF4
import numpy as np
import xarray as xr

from PyBM.constants import g

class SurgeDir(Enum):
    """Enum for Surge direction"""

    FWD = 1

    AFT = -1

class SwayDir(Enum):
    """Enum for Sway direction"""

    PORT = 1

    STARBOARD = -1

class HeaveDir(Enum):
    """Enum for Heave direction"""

    UP = 1

    DOWN = -1

class RollDir(Enum):
    """Enum for Roll direction"""

    PORT_UP = 1

    PORT_DOWN = -1

class PitchDir(Enum):
    """Enum for Pitch direction"""

    BOW_DOWN = 1

    BOW_UP = -1

class YawDir(Enum):
    """Enum for Yaw direction"""

    BOW_PORT = 1

    BOW_STARBOARD = -1

class WaveOrigin(Enum):
    """Enum for Wave direction"""

    STERN = 0

    STARBOARD = 90

    BOW = 180

    PORT = 270

class RotationUnit(Enum):
    """Enum for Rotation unit"""

    DEG_PER_M = 1

    RAD_PER_M = 180 / np.pi

    DEG_PER_FT = 3.28084

    DEG_PER_DEG = 0

    RAD_PER_RAD = DEG_PER_DEG

def _recursive_group_names(groups: dict, parent=None):
    """Recursively get the group names from a dictionary of groups"""
    for key, value in groups.items():
        if parent is None:
            name = key
        else:
            name = f"{parent}/{key}"
        if len(value.groups) > 0:
            yield from _recursive_group_names(value.groups, name)
        else:
            yield name

class RAO(xr.Dataset, ABC):
    """
    This is the parent class for motion and force RAOs
    """

    __slots__ = ()

    @abstractmethod

    def translate_rao(self, offset):
        pass

    @staticmethod

    def default_rao_path(VesselName, revision=0):
        dir = Path(
            f"O:/Engineering/Database/Vessel Motions/Vessel RAOs and time traces/{VesselName}/Processed data/PyBM Rev{revision}"
        )
        return dir / f"{VesselName}.nc"

    @staticmethod

    def group_name(Vessel_LC):
        """Return the group name for the RAOs in the database

        :param Vessel_LC: Load Case
        """
        return f"{Vessel_LC}"

    @property

    def group(self):
        return self.group_name(self.Vessel_LC)

    def modify_conventions(
        self,
        surge: SurgeDir = SurgeDir.FWD,
        sway: SwayDir = SwayDir.PORT,
        heave: HeaveDir = HeaveDir.UP,
        roll: RollDir = RollDir.PORT_UP,
        pitch: PitchDir = PitchDir.BOW_DOWN,
        yaw: YawDir = YawDir.BOW_PORT,
        wave_origin: WaveOrigin = WaveOrigin.STERN,
        rot_unit: RotationUnit = RotationUnit.DEG_PER_M,
    ):
        """
        Modify the RAO conventions to match the PyBM default. The inputs are the conventions of the data BEFORE modification.

        :param surge: Surge direction convention BEFORE modification (default: SurgeDir.FWD)
        :type surge: SurgeDir, optional
        :param sway: Sway direction convention BEFORE modification (default: SwayDir.PORT)
        :type sway: SwayDir, optional
        :param heave: Heave direction convention BEFORE modification (default: HeaveDir.UP)
        :type heave: HeaveDir, optional
        :param roll: Roll direction convention BEFORE modification (default: RollDir.PORT_UP)
        :type roll: RollDir, optional
        :param pitch: Pitch direction convention BEFORE modification (default: PitchDir.BOW_DOWN)
        :type pitch: PitchDir, optional
        :param yaw: Yaw direction convention BEFORE modification (default: YawDir.BOW_PORT)
        :type yaw: YawDir, optional
        :param wave_origin: Wave direction convention BEFORE modification (default: WaveOrigin.STERN)
        :type wave_origin: WaveOrigin, optional
        :param rot_unit: Rotation unit convention BEFORE modification (default: RotationUnit.DEG_PER_M)
        :type rot_unit: RotationUnit, optional
        """
        # Axis conventions
        conventions = np.array([x.value for x in [surge, sway, heave, roll, pitch, yaw]])
        conventions = xr.DataArray(conventions, coords=[("DOF", ["X", "Y", "Z", "Rx", "Ry", "Rz"])])
        attrs = self.attrs
        modified = self.copy(deep=True)
        modified *= conventions
        # Rotation unit conventions
        T = 1 / modified["Frequency"]
        wave_length = g * T**2 / (2 * np.pi)  # deep water wave dispersion relation
        wave_slope_1 = np.pi / wave_length  # wave slope at 1 m wave amplitude
        wave_steepness_1 = 1 / wave_length  # wave steepness at 1 m wave amplitude
        if rot_unit == RotationUnit.RAD_PER_RAD:
            min_freq_arg = modified["Frequency"].argmin("Frequency")
            pitch_at_smallest_freq = modified["POS"].sel(DOF="Ry").isel(Frequency=min_freq_arg, Direction=0)
            # check if roll tends towards 1 for long wave periods, bc then it is by max. wave slope. otherwise it tends towards pi and then it is by max. wave steepness
            if np.abs(np.abs(pitch_at_smallest_freq) - 1) > np.abs(np.abs(pitch_at_smallest_freq) - np.pi):
                modified.loc[dict(DOF=["Rx", "Ry", "Rz"])] *= (
                    2 * wave_steepness_1 * 180 / np.pi
                )  # Convert to deg/m, add a factor of 2 due to amplitude/ wave height conversion
            else:
                modified.loc[dict(DOF=["Rx", "Ry", "Rz"])] *= (
                    2 * wave_slope_1 * 180 / np.pi
                )  # Convert to deg/m, add a factor of 2 due to amplitude/ wave height conversion
        else:
            modified.loc[dict(DOF=["Rx", "Ry", "Rz"])] *= rot_unit.value
        # Wave direction conventions
        modified["Direction"] = (modified["Direction"] + wave_origin.value) % 360
        modified = modified.drop_duplicates("Direction")
        modified = xr.concat([modified, modified.loc[dict(Direction=0)].assign_coords(Direction=360)], "Direction")
        modified = modified.sortby("Direction")
        # Add attributes
        modified.attrs.update(attrs)
        return modified

    @classmethod

    def load_rao(cls, filename, Vessel_LC):
        """
        Load RAO from database.
        """
        group = cls.group_name(Vessel_LC)
        with netCDF4.Dataset(filename, "r") as f:
            available_groups = list(_recursive_group_names(f.groups))
        if group in available_groups:
            data = xr.load_dataset(filename, group=group, engine="netcdf4")
        else:
            group_list = "\n- ".join(available_groups)
            raise ValueError(
                f"Loading condition {group} not found in {filename}. The following LCs are available:\n- {group_list}"
            )
        attrs = data.attrs
        # Combine real and imaginary in complex number
        data = data.sel(Complex="Real") + 1j * data.sel(Complex="Imag")
        rao = cls(data)
        rao = rao.assign_attrs(attrs)
        return rao

    
    @classmethod

    def from_api(cls, VesselName, Vessel_LC):
        """
        Load RAO from API.
        
        :param VesselName: Name of the vessel
        :param Vessel_LC: Name of the load case
        :return: RAO object
        :raises ValueError: If RAO or load case not found (with available options listed)
        """
        from PyBM.marine.tools.api import api_calls
        
        # Get available RAOs
        try:
            raos_response = api_calls.get_raos()
            available_raos = raos_response.json()['raos']
        except Exception as e:
            raise ValueError(f"Failed to fetch RAOs from API: {e}")
        
        # Check if RAO exists
        if VesselName not in available_raos:
            rao_list = "\n- ".join(available_raos)
            raise ValueError(f"RAO for '{VesselName}' not found. Available RAOs:\n- {rao_list}")
        
        # Get available loadcases for this RAO
        try:
            loadcases_response = api_calls.get_rao_loadcases(VesselName)
            available_loadcases = loadcases_response.json()['loadcases']
        except Exception as e:
            raise ValueError(f"Failed to fetch loadcases for RAO '{VesselName}': {e}")
        
        # Check if loadcase exists
        if Vessel_LC not in available_loadcases:
            loadcase_list = "\n- ".join(available_loadcases)
            raise ValueError(f"Loadcase '{Vessel_LC}' not found in RAO '{VesselName}'. Available loadcases:\n- {loadcase_list}")
        
        # Load the RAO
        return api_calls.get_rao_loadcase(VesselName, Vessel_LC)

    def save_rao(self, filename=None, revision=None, replace=False):
        """Save RAO to NetCDF file

        :param filename: filepath to save the rao
        :param replace: Replace the file if it exists, otherwise append to the data
        """
        if filename is None:
            if revision is None:
                raise ValueError("Either filename or revision must be provided")
            else:
                filename = self.default_rao_path(self.VesselName, revision)
        real = np.real(self).assign_coords(Complex="Real")
        imag = np.imag(self).assign_coords(Complex="Imag")
        data = xr.concat([real, imag], dim="Complex")
        if replace:
            mode = "w"
        else:
            mode = "a"
        data.to_netcdf(filename, group=self.group, mode=mode)

    def get_roll_period(self):
        """
        Get the roll period from the RAOs
        """
        return 1 / np.abs(self["POS"].sel(DOF="Rx")).max("Direction").idxmax("Frequency")

    def plot(self, directions=None, amplitude=True, keys=None):
        """
        Plot the RAO for selected directions.

        :param directions: Vector of directions. Default: All directions are used
        :param amplitude: Plot RAO amplitudes if True. Plot phases if False.

        """
        # Use all directions if none is selected
        if directions is None:
            try:
                directions = self["Direction"].values
            except:
                directions = [0]

        # Plot RAOs
        if keys is None:
            keys = self.keys()
        for P in keys:
            R = self[P]
            f, axes = plt.subplots(2, 3)
            axes = axes.reshape(-1)
            f.suptitle("RAO for: {}".format(P))
            for Dir in directions:
                try:
                    dir_rao = R.sel(Direction=Dir)
                except:
                    dir_rao = R

                for i, DOF in enumerate(dir_rao["DOF"].values):
                    ax = axes[i]
                    ax.set_title(DOF)
                    ax.set_xlabel("Frequency [Hz]")
                    ax.grid(True)
                    if amplitude:
                        values = np.abs(dir_rao.isel(DOF=i))
                    else:
                        values = np.unwrap(np.angle(dir_rao.isel(DOF=i)))
                    ax.plot(dir_rao["Frequency"], values)
            plt.legend(directions)
