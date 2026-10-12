"""
tools to read AQWA RAO files (*.LIS)
"""

import numpy as np
import pandas as pd
import xarray as xr

from PyBM.marine.motion_analysis import MotionRAO
from PyBM.utils.helper_functions import amp_phase_to_complex, unwrap_angle

DOFs = ["X", "Y", "Z", "Rx", "Ry", "Rz"]

RAO_TYPES = {
    "POS": "                                      R.A.O.S-VARIATION WITH WAVE PERIOD/FREQUENCY",
    "VEL": "                                  VEL R.A.O.S-VARIATION WITH WAVE PERIOD/FREQUENCY",
    "ACC": "                                  ACC R.A.O.S-VARIATION WITH WAVE PERIOD/FREQUENCY",
}

COG_TYPE = "                          CENTRE OF GRAVITY"

N_FREQS_TYPE = "    * * * * W A V E   F R E Q U E N C I E S / P E R I O D S   A N D   D I R E C T I O N S * * * *"

DRAFT_TYPE = "          DEPTH OF LOWEST POINT ON VESSEL . . . . . . ."

def get_cog(filename):
    with open(filename, "r") as ifile:
        for line in ifile:
            if line.startswith(COG_TYPE):
                return list(map(float, line.split()[3:]))
    raise ValueError("COG not found in file")

def get_n_freqs(filename):
    n_freq = 0
    with open(filename, "r") as ifile:
        for line in ifile:
            if line.startswith(N_FREQS_TYPE):
                for _ in range(3):
                    line = ifile.readline()  # Skip 3 lines
                if not "FREQUENCY" in line:
                    continue
                for _ in range(3):
                    line = ifile.readline()  # Skip 3 lines
                while True:
                    # Remove *UNDEFINED and other non-numeric markers, then split and rejoin
                    # This ensures we only keep valid numeric tokens
                    cleaned_line = line.replace('*UNDEFINED', '')
                    # Split and filter to keep only numeric values
                    tokens = cleaned_line.split()
                    numeric_tokens = []
                    for token in tokens:
                        try:
                            numeric_tokens.append(float(token))
                        except ValueError:
                            pass
                    if len(numeric_tokens) < 2:
                        break
                    data = np.array(numeric_tokens, dtype=float)
                    line = ifile.readline()
                    n_freq = data[0]
    if n_freq:
        return n_freq
    raise ValueError("N_FREQS not found in file")

def get_draft(filename):
    with open(filename, "r") as ifile:
        for line in ifile:
            if line.startswith(DRAFT_TYPE):
                return float(line.split()[-1])
    raise ValueError("Draft not found in file")

def decode_RAO(filename, rao_type, n_freqs):
    with open(filename, "r") as ifile:
        temp_dir = []
        for line in ifile:
            if line.startswith(rao_type):
                names = [
                    "Period_s",
                    "Frequency_rad/s",
                    "Direction_deg",
                    "amp_X",
                    "ph_X",
                    "amp_Y",
                    "ph_Y",
                    "amp_Z",
                    "ph_Z",
                    "amp_Rx",
                    "ph_Rx",
                    "amp_Ry",
                    "ph_Ry",
                    "amp_Rz",
                    "ph_Rz",
                ]
                data = pd.read_fwf(
                    ifile,
                    nrows=n_freqs,
                    header=None,
                    skiprows=6,
                    names=names,
                    colspecs=(
                        [3, 9],
                        [11, 17],
                        [19, 27],
                        [30, 37],
                        [37, 45],
                        [45, 55],
                        [55, 63],
                        [63, 73],
                        [73, 81],
                        [81, 91],
                        [91, 99],
                        [99, 109],
                        [109, 117],
                        [117, 127],
                        [127, 135],
                    ),
                )
                temp_dof = []
                if data["Direction_deg"][0] != -180:
                    for dof in DOFs:
                        comp = amp_phase_to_complex(data["amp_" + dof], data["ph_" + dof])
                        temp_dof.append(
                            xr.DataArray(
                                comp,
                                {
                                    "Frequency": data["Frequency_rad/s"] / (2 * np.pi),
                                    "Direction": unwrap_angle(data["Direction_deg"][0]),
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

def load_LIS(filename):
    ds = xr.Dataset()
    n_freqs = get_n_freqs(filename)
    for rao_type, type_def in RAO_TYPES.items():
        ds[rao_type] = decode_RAO(filename, type_def, n_freqs=n_freqs)
    cog = get_cog(filename)
    ds = ds.assign_attrs(origin=cog)
    draft = get_draft(filename)
    ds = ds.assign_attrs(Draft=draft)
    ds = ds.assign_attrs(KG=cog[2])
    return ds

def LIS_to_RAO(filename, VesselName, Vessel_LC):
    """
    Convert LIS data to MotionRAO object.

    :param filename: path to LIS file
    :param VesselName: Name of the vessel
    :param Vessel_LC: Vessel Loading condition
    """
    data = load_LIS(filename)
    rao = MotionRAO(data, attrs=data.attrs)
    rao = rao.assign_attrs(VesselName=VesselName, Vessel_LC=Vessel_LC)
    return rao
