"""
convert TXT Orcaflex formats to useful xarray

See an example of the expected format here:
"O:\Engineering\Database\Vessel Motions\Vessel RAOs and time traces\EWB400\Processed data\RAO Rev0\OFMRAO.EWB400.MAXDRAFT.set"
More info here: https://www.orcina.com/webhelp/OrcaFlex/Content/html/Importinghydrodynamicdata,Generictextfiles.htm#GenericRAOImport
"""

import numpy as np
import pandas as pd
import xarray as xr
import re

from PyBM.marine.motion_analysis import MotionRAO
from PyBM.utils.helper_functions import (
    amp_phase_to_complex,
    differentiate,
    unwrap_angle,
)

DOFS = ["X", "Y", "Z", "Rx", "Ry", "Rz"]

def parse_TXT(filename):
    """Parse OrcaFlex .txt file into structured blocks per direction."""
    with open(filename, "r") as f:
        lines = f.readlines()

    data_blocks = []
    inside_block = False
    block_lines = []
    direction = None

    for line in lines:
        line = line.strip()
        if line.startswith("*** OrcaFlex Displacement RAO Start ***"):
            inside_block = True
            block_lines = []
            direction = None
        elif line.startswith("*** OrcaFlex Displacement RAO End ***"):
            inside_block = False
            if block_lines:
                data_blocks.append((direction, block_lines))
        elif inside_block:
            if line.startswith("Direction"):
                direction = int(line.split()[1])
            elif line.startswith("WP"):
                header = line.split()
            else:
                if line and line.startswith("Draught") is False:
                    block_lines.append(line)

    return data_blocks, header

def decode_RAO_TXT(filename, mirror=False):
    """Decode OrcaFlex .txt file to xarray DataArray."""
    data_blocks, header = parse_TXT(filename)
    temp_dirs = []

    # Map OrcaFlex headers to DOFs
    header_map = {
        "XA": "X", "XP": "X",
        "YA": "Y", "YP": "Y",
        "ZA": "Z", "ZP": "Z",
        "RXA": "Rx", "RXP": "Rx",
        "RYA": "Ry", "RYP": "Ry",
        "RZA": "Rz", "RZP": "Rz"
    }
    phase_cols = ["XP", "YP", "ZP", "RXP", "RYP", "RZP"]

    for dir_deg, block in data_blocks:
        df = pd.DataFrame([list(map(float, re.split(r"\s+", row))) for row in block], columns=header)
        
        # Convert WP = wave period [s] or WFR = wave frequency [rad/s] → wave frequency [Hz]
        if "WP" in df.columns:
            freq = 1 / df["WP"].values
        elif "WFH" in df.columns:
            freq = df["WFH"].values
        elif "WFR" in df.columns:
            freq = df["WFR"].values / (2 * np.pi)

        # ensure ascending order
        if freq[0] > freq[-1]:
            freq = freq[::-1]
            df = df.iloc[::-1].reset_index(drop=True)

        temp_dof = []
        for dof in DOFS:
            amp_col = [k for k, v in header_map.items() if v == dof and k not in phase_cols][0]
            ph_col = [k for k, v in header_map.items() if v == dof and k in phase_cols][0]

            comp = amp_phase_to_complex(df[amp_col], df[ph_col])
            da = xr.DataArray(
                comp,
                coords={
                    "Frequency": freq,
                    "Direction": unwrap_angle(dir_deg),
                    "DOF": dof
                },
                dims=["Frequency"]
            )
            temp_dof.append(da)

        temp_dirs.append(xr.concat(temp_dof, dim="DOF"))

    da = xr.concat(temp_dirs, dim="Direction")

    if mirror:
        mirrored = da.assign_coords(Direction=(360 - da["Direction"])) * xr.DataArray(
            [1, -1, 1, -1, 1, 1], dims=["DOF"], coords={"DOF": DOFS}
        )
        da = xr.concat([da, mirrored], "Direction").sortby("Direction")
    else:
        da = xr.concat(
            [da, da.sel(Direction=0).assign_coords(Direction=360)], "Direction"
        )

    da = da.sortby("Direction").drop_duplicates("Direction")
    return da

def load_TXT(filename, mirror=False):
    ds = xr.Dataset()
    ds["POS"] = decode_RAO_TXT(filename, mirror)
    ds["VEL"] = differentiate(ds["POS"], ds["Frequency"])
    ds["ACC"] = differentiate(ds["VEL"], ds["Frequency"])
    return ds

def TXT_to_RAO(filename, VesselName, Vessel_LC, origin, mirror=False):
    """Convert OrcaFlex .txt file to MotionRAO object."""
    data = load_TXT(filename, mirror)
    rao = MotionRAO(data)
    rao = rao.assign_attrs(VesselName=VesselName, Vessel_LC=Vessel_LC, origin=origin)
    return rao
