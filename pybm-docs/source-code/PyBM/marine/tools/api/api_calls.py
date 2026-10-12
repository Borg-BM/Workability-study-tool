import pickle
from PyBM.marine.motion_analysis.MotionRAO import MotionRAO
from PyBM.marine.motion_analysis.RAO import SurgeDir, SwayDir, HeaveDir, RollDir, PitchDir, YawDir, WaveOrigin, RotationUnit
from .oauth_session import get_authenticated_session, API_BASE_URL
import xarray as xr
import urllib.parse as parse
import io

def get_raos(session=None):
    """Get RAOs from API (auto-authenticates if needed)"""
    if session is None:
        session = get_authenticated_session()
    response = session.get(f'{API_BASE_URL}/api/raos')
    response.raise_for_status()
    return response

def get_rao_loadcases(VesselName: str, session=None):
    """Get loadcases for a specific RAO from API (auto-authenticates if needed)"""
    if session is None:
        session = get_authenticated_session()
    encoded_vessel_name = parse.quote(VesselName, safe='')
    response = session.get(f'{API_BASE_URL}/api/rao/{encoded_vessel_name}/loadcases')
    response.raise_for_status()
    return response

def get_rao_loadcase(VesselName: str, Vessel_LC: str, session=None):
    """Get specific loadcase details for a RAO from API (auto-authenticates if needed)"""
    if session is None:
        session = get_authenticated_session()
    encoded_vessel_name = parse.quote(VesselName, safe='')
    encoded_LC = parse.quote(Vessel_LC, safe='')
    response = session.get(f'{API_BASE_URL}/api/rao/{encoded_vessel_name}/loadcase/{encoded_LC}')
    response.raise_for_status()
    # Load pickled data directly into xarray
    ds = pickle.loads(response.content)
    rao = MotionRAO(ds)
    rao.attrs = ds.attrs
    conventions = ds.attrs.get('conventions', {})
    conventions.pop('Phase', None)  # Remove Phase item if it exists
    conventions = {k: eval(v) for k, v in conventions.items()} # Convert string back to PyBM-style enum
    rao = rao.modify_conventions(**conventions)

    return rao
