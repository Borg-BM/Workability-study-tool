"""
convert CSV and CSV-like formats to useful xarray

See an example of the expected format here:
"O:\Engineering\Database\Vessel Motions\Vessel RAOs and time traces\EWB400\Processed data\RAO Rev0\BasisR.set"
"""

import numpy as np
import pandas as pd
import xarray as xr
import re
from io import StringIO

from PyBM.marine.motion_analysis import MotionRAO
from PyBM.utils.helper_functions import (
    amp_phase_to_complex,
    differentiate,
    unwrap_angle,
)

DOFS = ["X", "Y", "Z", "Rx", "Ry", "Rz"]

def parse_csv_sections(filename):
    """Split the .csv file into sections by '&buildg -csv' / 'END'."""
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()

    # Split by section markers
    sections = re.split(r"&buildg -csv", content)
    sections = [s.strip() for s in sections if s.strip() and not s.strip().startswith("END")]
    return sections

def parse_section(section_text):
    """Parse a single amplitude or phase section."""
    lines = [l.strip().strip('"') for l in section_text.splitlines() if l.strip() and l.strip() != "END"]

    # Find header line (the one starting with 'Frequency')
    header_idx = next(i for i, l in enumerate(lines) if l.startswith("Frequency"))
    section_body = "\n".join(lines[header_idx:])
    section_body = section_body.strip("'").strip('"')
    df = pd.read_csv(StringIO(section_body), sep='","', engine='python')
    return df

def extract_dof_name(section_text):
    """Extract DOF name like 'Surge', 'Sway', etc. from the section header."""
    dof_map = {
        "Surge": "X",
        "Sway": "Y",
        "Heave": "Z",
        "Roll": "Rx",
        "Pitch": "Ry",
        "Yaw": "Rz",
    }

    match = re.search(r"for DOF\s+(\w+)", section_text)
    if match:
        name = match.group(1)
        return dof_map.get(name, None)
    
    # fallback — try common labels manually
    for candidate, axis in dof_map.items():
        if candidate.lower() in section_text.lower():
            return axis
    
    return None

def decode_RAO_CSV(filename, mirror):

    sections = parse_csv_sections(filename)
    # Group sections by DOF and type (Amplitude/Phase)
    grouped = {}
    for sec in sections:
        dof = extract_dof_name(sec)
        is_phase = "phase" in sec.lower()
        grouped.setdefault(dof, {})["phase" if is_phase else "amp"] = sec

    temp_dofs = []
    for dof, parts in grouped.items():
        if "amp" not in parts or "phase" not in parts:
            continue  # skip incomplete DOFs

        amp_df = parse_section(parts["amp"])
        ph_df = parse_section(parts["phase"])

        amp_cols = [c for c in amp_df.columns if "Hed_" in c]
        headings = [float(c.split("_")[-1]) for c in amp_cols]
        freq = amp_df["Frequency"].astype(float) / (2 * np.pi)  # rad/s → Hz

        temp_dir = []
        for j, head in enumerate(headings):
            amp = amp_df[amp_cols[j]].astype(float)
            ph_col = [c for c in ph_df.columns if f"Hed_{head}" in c][0]
            ph = ph_df[ph_col].astype(float)
            comp = amp_phase_to_complex(amp, ph)
            da = xr.DataArray(
                comp,
                coords={
                    "Frequency": freq,
                    "Direction": unwrap_angle(head),
                    "DOF": dof,
                },
                dims=["Frequency"],
            )
            temp_dir.append(da)
        
        dof_da = xr.concat(temp_dir, dim="Direction")
        temp_dofs.append(dof_da)
    
    da = xr.concat(temp_dofs, dim="DOF")

    if mirror:
        mirrored = da.assign_coords(Direction=(360 - da["Direction"])) * xr.DataArray(
            [1, -1, 1, -1, 1, 1], dims=["DOF"], coords={"DOF": DOFS}
        )
        da = xr.concat([da, mirrored], "Direction").sortby("Direction")
    else:
        da = xr.concat(
            [da, da.loc[dict(Direction=0)].assign_coords(Direction=360)], "Direction"
        )

    da = da.sortby("Direction").drop_duplicates("Direction")
    return da

def load_CSV(filename, mirror):
    ds = xr.Dataset()
    ds["POS"] = decode_RAO_CSV(filename, mirror)
    ds["VEL"] = differentiate(ds["POS"], ds["Frequency"])
    ds["ACC"] = differentiate(ds["VEL"], ds["Frequency"])
    return ds

def CSV_to_RAO(filename, VesselName, Vessel_LC, origin, mirror=False):
    """Convert CSV file to Xarray RAO object

    :param filename: CSV file with RAO data
    :param VesselName: Name of vessel
    :param Vessel_LC: Loading condition of the vessel
    :param origin: [m] [x, y, z] origin of the RAOs w.r.t to vessel APP/CL/Keel
    :return: MotionRAO object
    :rtype: MotionRAO
    """
    data = load_CSV(filename, mirror)
    rao = MotionRAO(data)
    rao = rao.assign_attrs(VesselName=VesselName, Vessel_LC=Vessel_LC, origin=origin)
    return rao
