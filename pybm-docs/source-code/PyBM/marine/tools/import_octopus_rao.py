import numpy as np
import xarray as xr

from PyBM.marine.motion_analysis import MotionRAO
from PyBM.utils.helper_functions import (
    amp_phase_to_complex,
    differentiate,
    unwrap_angle,
)

DOFs = ["X", "Y", "Z", "Rx", "Ry", "Rz"]

def Octopus_to_RAO(octopus_file, VesselName, Vessel_LC, speed=0):
    with open(octopus_file, "r") as file_iterator:
        origin = get_origin(file_iterator)
        # speeds = get_speeds(file_iterator)
        # wave_dirs = get_wave_directions(file_iterator)
        # for speed in speeds:
        #     freqs = get_wave_frequencies(file_iterator, speed)
        ds = xr.Dataset()
        ds["POS"] = get_rao(file_iterator, speed)
        ds["VEL"] = differentiate(ds["POS"], ds["Frequency"])
        ds["ACC"] = differentiate(ds["VEL"], ds["Frequency"])
        rao = MotionRAO(ds)
        rao = rao.assign_attrs(VesselName=VesselName, Vessel_LC=f"{Vessel_LC}_{speed:.1f}kn", origin=origin)
        return rao

def get_rao_parameter(file_iterator, param_string):
    for line in file_iterator:
        if line.startswith(param_string):
            n_points = float(line.split()[-1])
            data = []
            while len(data) < n_points:
                line = file_iterator.readline()
                data += read_data_line(line)
            return np.array(data)

def read_data_line(line):
    data = []
    for value in line.split(" "):
        try:
            data += [float(value)]
        except ValueError:
            pass
    return data

def get_origin(file_iterator):
    for line in file_iterator:
        if line.startswith("MOTION REF POINT (X Y Z)...............[m]:"):
            return read_data_line(line)

def get_wave_directions(file_iterator):
    return np.round(get_rao_parameter(file_iterator, "NUMBER OF WAVE DIRECTIONS"), decimals=2)

def get_speeds(file_iterator):
    return get_rao_parameter(file_iterator, "NUMBER OF FORWARD SPEEDS")

def get_wave_frequencies(file_iterator, speed):
    for line in file_iterator:
        if line.startswith("SPEED.................................[kn]"):
            data = float(line.split()[-1])
            if np.isclose(data, speed):
                return get_rao_parameter(file_iterator, "NUMBER OF WAVE FREQUENCIES") / (2 * np.pi)

def get_rao(file_iterator, desired_speed):
    temp_dir = []
    for line in file_iterator:
        if line.startswith("SPEED.................................[kn]"):
            speed = float(line.split()[-1])
        elif line.startswith("WAVE DIRECTION.......................[deg]"):
            wave_dir = np.round(float(line.split()[-1]), decimals=2)
        elif line.startswith(
            "--WAVE FREQ--  -SQRT(SL/WL)-  --ENC FREQ---  --------Surge Motion--------  --------Sway Motion---------  --------Heave Motion--------  --------Roll Motion---------  --------Pitch Motion--------  ---------Yaw Motion---------"
        ):
            if not np.isclose(speed, desired_speed):
                continue
            for _ in range(2):
                line = file_iterator.readline()  # Skip 2 lines
            data = None
            while True:
                line = file_iterator.readline()
                line_data = np.fromstring(line, dtype=float, sep=" ")[0:15]
                if len(line_data) < 15:
                    break
                if data is None:
                    data = line_data
                else:
                    data = np.vstack((data, line_data))
            freqs = data[:, 0] / (2 * np.pi)
            temp_dof = []
            for i, dof in enumerate(DOFs):
                comp = amp_phase_to_complex(data[:, (3 + 2 * i)], data[:, (4 + 2 * i)])
                temp_dof.append(
                    xr.DataArray(
                        comp,
                        {
                            "Frequency": freqs,
                            "Direction": wave_dir,
                            "DOF": dof,
                        },
                        dims=["Frequency"],
                    )
                )
            temp_dir.append(xr.concat(temp_dof, "DOF"))
    da = xr.concat(temp_dir, dim="Direction")
    da = da.reindex(Direction=sorted(da.Direction))
    da = xr.concat(
        [da, da.loc[dict(Direction=0)].assign_coords(Direction=360.0)], "Direction"
    )  # Add Coordinate at 360deg for easier value interpolation
    return da
