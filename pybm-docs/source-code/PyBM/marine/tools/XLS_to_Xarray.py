"""
convert XLS format to useful xarray
"""

import numpy as np
import pandas as pd
import xarray as xr

from PyBM.marine.motion_analysis import MotionRAO
from PyBM.utils.helper_functions import (
    amp_phase_to_complex,
    differentiate,
    unwrap_angle,
)

DOFS = ["X", "Y", "Z", "Rx", "Ry", "Rz"]

def decode_RAO_XLS(filename, mirror):
    excf = pd.read_excel(filename)
    arrs = excf.to_numpy("str")
    # drop empty arrays
    arrs = [arr for arr in arrs if len(arr) != 0]

    # Get all headings
    headings = [float(arr[1]) for arr in arrs if arr[0] == "Heading"]
    # Get values
    vals = np.split(excf.apply(pd.to_numeric, errors="coerce").dropna().to_numpy(), len(headings))

    COLMNS = [
        "Freq_rad/s",
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

    temp_dir = []
    for i, heading in enumerate(headings):
        data = pd.DataFrame(vals[i], columns=COLMNS)
        temp_dof = []
        for dof in DOFS:
            freq = data["Freq_rad/s"] / (2 * np.pi)
            if freq[0] > freq[len(freq) - 1]:
                print(
                    UserWarning(
                        "Frequency is not in ascending order. Flipping frequencies. Please check whether this is correct."
                    )
                )
                freq = freq[::-1]
            comp = amp_phase_to_complex(data["amp_" + dof], data["ph_" + dof])
            temp_dof.append(
                xr.DataArray(
                    comp,
                    {
                        "Frequency": freq,
                        "Direction": unwrap_angle(heading),
                        "DOF": dof,
                    },
                    dims=["Frequency"],
                )
            )
        temp_dir.append(xr.concat(temp_dof, dim="DOF"))
    da = xr.concat(temp_dir, dim="Direction")
    if mirror:
        # Mirror Rx and Y by 180 degree phase offset.
        mirrored = da.assign_coords(Direction=(360 - da["Direction"])) * xr.DataArray(
            [1, -1, 1, -1, 1, 1], dims=["DOF"], coords={"DOF": DOFS}
        )
        da = xr.concat([da, mirrored], "Direction").sortby("Direction")  # mirror sides
    else:
        da = xr.concat(
            [da, da.loc[dict(Direction=0)].assign_coords(Direction=360)], "Direction"
        )  # Add coordinate at 360deg for easier interpolation
    da = da.sortby("Direction").drop_duplicates("Direction")
    return da

def load_XLS(filename, mirror):
    ds = xr.Dataset()
    ds["POS"] = decode_RAO_XLS(filename, mirror)
    ds["VEL"] = differentiate(ds["POS"], ds["Frequency"])
    ds["ACC"] = differentiate(ds["VEL"], ds["Frequency"])
    return ds

def XLS_to_RAO(filename, VesselName, Vessel_LC, origin, mirror=False):
    """Convert excel file to Xarray RAO object

    :param filename: Excel file with RAO data
    :param VesselName: Name of vessel
    :param Vessel_LC: Loading condition of the vessel
    :param origin: [m] [x, y, z] origin of the RAOs w.r.t to vessel APP/CL/Keel
    :return: MotionRAO object
    :rtype: MotionRAO
    """
    data = load_XLS(filename, mirror)
    rao = MotionRAO(data)
    rao = rao.assign_attrs(VesselName=VesselName, Vessel_LC=Vessel_LC, origin=origin)
    return rao
