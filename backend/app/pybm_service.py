"""The calculation engine: everything that talks to PyBM (Barge Master's in-house marine
engineering library) lives here, so routers/ stays pure HTTP plumbing. Three kinds of
things happen in this module:
  1. Reference data + caches for the picklists behind the StudyBuilder form (machine
     types, vessels/RAOs, DNV Weibull zones via weibull_locations.py, Copernicus products,
     NDBC buoys).
  2. _build_hindcast(): turns whichever metocean data source the user picked into one
     PyBM Hindcast object.
  3. run_calculation(): the actual per-version calculation -- load the RAO, build the
     machine + wave inputs, run PyBM's directional_workability(), derive the operating
     envelope and (if metocean data was supplied) an overall workability %, and render
     the polar plot PNG. This is what routers/studies.py's create_version() calls.
"""

# matplotlib must be set to a non-interactive backend before PyBM (which imports
# matplotlib.pyplot at module load time) is imported anywhere in this process.
import matplotlib

matplotlib.use("Agg")

import io
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import numpy as np
import requests
from PyBM.marine import (
    HeavyFeeder,
    HeavyFeederSurgeSway,
    Jonswap,
    MCG30LHIGHLOAD_Linear,
    MCG30LLOWLOAD_Linear,
    MCG30LTRANSFER_Linear,
    MCG30MHIGHLOAD_Linear,
    MCG30MLOWLOAD_Linear,
    MCG30MTRANSFER_Linear,
    MotionRAO,
    T700,
    directional_workability,
)
from PyBM.marine.tools.api import api_calls
from PyBM.marine.weather_hindcast import CopernicusLoader, DNVLoader, ExcelScatterLoader, Hindcast, NDBCLoader

from .sso import ApiSession, LoginRequired
from .weibull_locations import resolve_weibull_params

import matplotlib.pyplot as plt

# Copernicus Marine Service product catalogue exposed by PyBM's CopernicusLoader (see its
# docstring / the example scripts). PyBM ships with its own Barge Master service account,
# so no separate login/credentials are needed to use these.
COPERNICUS_PRODUCTS = [
    {"id": 0, "label": "Global Ocean Waves Reanalysis (0.2 deg, 3-hourly)"},
    {"id": 1, "label": "Arctic Ocean Wave Hindcast (3 km, hourly)"},
    {"id": 2, "label": "Baltic Sea Wave Hindcast (hourly)"},
    {"id": 3, "label": "Black Sea Waves Reanalysis (2.5 km, hourly)"},
    {"id": 4, "label": "Atlantic (Iberia/Biscay/Ireland) Wave Reanalysis (0.027 deg, hourly)"},
    {"id": 5, "label": "Mediterranean Sea Waves Reanalysis (hourly)"},
    {"id": 6, "label": "Atlantic (European North West Shelf) Wave Physics Reanalysis (hourly)"},
]


class CalculationError(Exception):
    """A user-fixable error from the calculation engine (bad params, not a bug)."""


@dataclass
class MachineSpec:
    """Static facts about one selectable "System" in the frontend -- everything
    machine_type_list() exposes to populate the dropdown, plus the bits run_calculation()
    needs to actually build the right PyBM machine object.

    `system_type` is the coarser grouping a study is fixed to once, at Study Setup (see
    db.py's system_type column) -- StudyBuilder.tsx's "System" dropdown then only offers
    the machine_type entries whose system_type matches the study's. MCG30's 6 variants all
    share system_type "mcg30"; Heavy Feeder's plain and surge/sway-compensated variants
    both share "heavy_feeder"; T700 has just the one variant, "t700"."""

    label: str
    system_type: str  # "mcg30" | "t700" | "heavy_feeder"
    cls: type  # the PyBM machine class this machine_type constructs
    default_n_sigma: float | None  # None = let PyBM's directional_workability() use its own default
    needs_lifting_radius: bool  # MCG30 lifting variants need an operating radius; transfer (gangway) ones don't
    needs_comp_point_z: bool  # HeavyFeederSurgeSway requires comp_point's Z to be a real positive value (see HeavyFeederSurgeSway.py's assertion) -- plain HeavyFeeder's comp_point is optional
    default_max_hs_plot: float  # polar plot radial axis max, in meters


# Every selectable "System" variant PyBM ships, across the 3 system types this app
# supports (see MachineSpec.system_type above). PyBM also exposes a "_Nonlinear"
# motion-response model alongside every one of the MCG30 "_Linear" classes below -- this
# app only ever uses the linear ones; there's no UI path to the nonlinear variants.
MACHINE_TYPES: dict[str, MachineSpec] = {
    # The 6 MCG30 gangway/crane variants: 2 boom lengths (M/L) x 3 duty types (personnel
    # transfer, high-load lift, low-load lift).
    "mcg30m_transfer": MachineSpec(
        "MCG30 M - Personnel transfer (gangway)", "mcg30",
        MCG30MTRANSFER_Linear, None, False, False, 4.0,
    ),
    "mcg30l_transfer": MachineSpec(
        "MCG30 L - Personnel transfer (gangway, long boom)", "mcg30",
        MCG30LTRANSFER_Linear, None, False, False, 4.0,
    ),
    "mcg30m_highload": MachineSpec(
        "MCG30 M - Lifting, high load (1000 kg)", "mcg30",
        MCG30MHIGHLOAD_Linear, 2.3, True, False, 3.0,
    ),
    "mcg30l_highload": MachineSpec(
        "MCG30 L - Lifting, high load (1000 kg, long boom)", "mcg30",
        MCG30LHIGHLOAD_Linear, 2.3, True, False, 3.0,
    ),
    "mcg30m_lowload": MachineSpec(
        "MCG30 M - Lifting, low load (500 kg)", "mcg30",
        MCG30MLOWLOAD_Linear, 3.0, True, False, 3.0,
    ),
    "mcg30l_lowload": MachineSpec(
        "MCG30 L - Lifting, low load (500 kg, long boom)", "mcg30",
        MCG30LLOWLOAD_Linear, 3.0, True, False, 3.0,
    ),
    "t700": MachineSpec(
        "T700", "t700",
        T700, None, False, False, 4.0,
    ),
    "heavy_feeder": MachineSpec(
        "Heavy Feeder", "heavy_feeder",
        HeavyFeeder, None, False, False, 4.0,
    ),
    "heavy_feeder_surge_sway": MachineSpec(
        "Heavy Feeder - Surge/sway compensated", "heavy_feeder",
        HeavyFeederSurgeSway, None, False, True, 4.0,
    ),
}

# Display labels for the 3 system types a study can be fixed to at Study Setup -- see
# system_type_list() below and db.py's system_type column.
SYSTEM_TYPE_LABELS: dict[str, str] = {
    "mcg30": "MCG30 (gangway / crane)",
    "t700": "T700",
    "heavy_feeder": "Heavy Feeder",
}

# Fetching a RAO from the API is a few HTTP round trips plus an unpickle of the
# whole motion dataset; it's also the same object we need both for the metadata
# card and for the calculation itself, so keep fetched RAOs around for the life
# of the process (one process, so a plain in-memory dict is enough).
_rao_cache: dict[tuple[str, str], MotionRAO] = {}
_rao_cache_lock = threading.Lock()

_vessel_list_cache: list[str] | None = None
_vessel_list_lock = threading.Lock()

# The NDBC station table (~1400 rows incl. tsunami/oilrig/fixed platforms) is a slow
# scrape of a NOAA webpage -- fetch it once per process and keep only the wave-relevant
# moored buoys, so the map picker has real station locations instead of a raw lat/long
# that silently resolves to whatever's nearest (which can be very far away).
#
# Not every "buoy"-type station carries a wave sensor, and plenty are offline/decommissioned
# without NDBC's station table reflecting that. We check each station's
# `available_historical()` for a 'Standard meteorological data' entry -- this is the *exact*
# check PyBM's own NDBCLoader.fetch() makes before it raises "No historical data available
# for the specified buoy", so filtering on it here means the picker can't offer a buoy that
# PyBM would reject anyway. Deliberately *not* filtered on "currently reporting": a
# decommissioned buoy can still have decades of good historical data.
#
# We also keep each surviving buoy's actual covered years, so the picker can show them and
# the UI can steer the date range onto a period the buoy actually has data for.
_ndbc_buoys_cache: list[dict] | None = None
_ndbc_buoys_lock = threading.Lock()


def _stdmet_years(station_id: str, api) -> list[int] | None:
    """Years with a 'Standard meteorological data' entry for this station (PyBM's own
    NDBCLoader requires this exact key), or None if there's no such archive at all."""
    try:
        available = api.available_historical(station_id=station_id)
    except Exception:
        return None
    stdmet = available.get("Standard meteorological data")
    if not stdmet:
        return None

    # Each key either starts with its year or reads like "Jan 2025".
    years: set[int] = set()
    for key in stdmet:
        if key[:4].isdigit():
            years.add(int(key[:4]))
        else:
            try:
                years.add(datetime.strptime(key, "%b %Y").year)
            except ValueError:
                continue
    return sorted(years) if years else None


def list_ndbc_buoys() -> list[dict]:
    """Real NOAA buoy stations for the map picker: each dict has id/lat/lon/name/years.
    Backs /api/ndbc-buoys. The first call is slow (~1-2 min: a concurrent
    available_historical() check against every buoy-type station, see _stdmet_years);
    cached for the life of the process afterwards. The frontend only asks for it once NDBC
    is picked as the metocean source."""
    global _ndbc_buoys_cache
    with _ndbc_buoys_lock:
        if _ndbc_buoys_cache is None:
            # Imported here: ndbc_api is only needed for this one (rare) call.
            from ndbc_api import NdbcApi

            api = NdbcApi()
            df = api.stations()
            buoys = df[df["Type"] == "buoy"]
            candidates = list(buoys.itertuples())
            years_by_id: dict[str, list[int]] = {}
            with ThreadPoolExecutor(max_workers=15) as ex:
                futures = {ex.submit(_stdmet_years, str(row.Station), api): str(row.Station) for row in candidates}
                for fut in as_completed(futures):
                    station_id = futures[fut]
                    years = fut.result()
                    if years:
                        years_by_id[station_id] = years

            _ndbc_buoys_cache = [
                {
                    "id": str(row.Station),
                    "lat": float(row.Lat),
                    "lon": float(row.Lon),
                    "name": row.Name or None,
                    "years": years_by_id[str(row.Station)],
                }
                for row in candidates
                if str(row.Station) in years_by_id
            ]
        return _ndbc_buoys_cache


# Every call to Barge Master's API below goes through `api` -- the signed-in user's own
# access (sso.pybm_api), passed to PyBM's api_calls as `session=`. The caches are shared by
# all users: the RAO database is the same for everyone at Barge Master.


def list_vessels(api: ApiSession) -> list[str]:
    """All vessel names with an RAO on file in PyBM's API -- cached for the life of the
    process, since the list changes rarely (a newly added vessel shows up after a backend
    restart)."""
    global _vessel_list_cache
    with _vessel_list_lock:
        if _vessel_list_cache is None:
            response = api_calls.get_raos(session=api())
            _vessel_list_cache = sorted(response.json()["raos"])
        return _vessel_list_cache


def list_loadcases(vessel: str, api: ApiSession) -> list[str]:
    """Loadcases (e.g. FULLLOAD/LOWLOAD/TRANSFER) available for one vessel -- not cached,
    since it's only requested once per vessel pick, not on every keystroke."""
    response = api_calls.get_rao_loadcases(vessel, session=api())
    return sorted(response.json()["loadcases"])


def get_rao(vessel: str, loadcase: str, api: ApiSession) -> MotionRAO:
    """Loads one vessel's motion RAO (response amplitude operator -- how much the vessel
    moves per unit wave height, by frequency/heading) and caches it, since fetching one is
    a few HTTP round trips plus unpickling the whole motion dataset, and the same object
    is reused for both the metadata endpoint and every calculation against that RAO.
    (api_calls.get_rao_loadcase is what MotionRAO.from_api ends with, minus from_api's
    existence checks -- which can't take a session -- so a missing RAO is reported here.)"""
    key = (vessel, loadcase)
    with _rao_cache_lock:
        cached = _rao_cache.get(key)
    if cached is not None:
        return cached
    try:
        rao = api_calls.get_rao_loadcase(vessel, loadcase, session=api())
    except requests.HTTPError as exc:
        if exc.response is not None and exc.response.status_code == 404:
            raise ValueError(f"No RAO for {vessel} / {loadcase} in the RAO database.") from exc
        raise
    with _rao_cache_lock:
        _rao_cache[key] = rao
    return rao


def _json_safe(value):
    """Recursively converts numpy scalars/arrays (which FastAPI's default JSON encoder
    can't serialize) into plain Python types, so a PyBM RAO's raw `.attrs` dict -- whose
    values can be anything numpy produced -- can go straight into an API response.
    Anything not covered by an explicit case (e.g. a custom PyBM object) falls back to
    str(value) rather than raising, since this is metadata for display, not for
    round-tripping back into a calculation."""
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, (np.floating,)):
        return float(value)
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, dict):
        return {str(k): _json_safe(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_safe(v) for v in value]
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return str(value)


def get_rao_metadata(vessel: str, loadcase: str, api: ApiSession) -> dict:
    """Descriptive info about one RAO for display only (see routers/raos.py) -- `origin`
    is the RAO's own reference point, in the same frame that machine position_x/y/z_m
    (see MachineParams) are specified relative to."""
    rao = get_rao(vessel, loadcase, api)
    attrs = {k: _json_safe(v) for k, v in rao.attrs.items()}
    origin = getattr(rao, "origin", None)
    return {
        "vessel": vessel,
        "loadcase": loadcase,
        "origin_m": _json_safe(origin) if origin is not None else None,
        "attrs": attrs,
    }


def machine_type_list() -> list[dict]:
    """MACHINE_TYPES trimmed to what the frontend's dropdown actually needs -- `cls` and
    `default_max_hs_plot` stay backend-only (cls isn't serializable; default_max_hs_plot is
    only relevant once run_calculation() renders the plot, not for populating a dropdown)."""
    return [
        {
            "id": machine_id,
            "label": spec.label,
            "system_type": spec.system_type,
            "default_n_sigma": spec.default_n_sigma,
            "needs_lifting_radius": spec.needs_lifting_radius,
            "needs_comp_point_z": spec.needs_comp_point_z,
        }
        for machine_id, spec in MACHINE_TYPES.items()
    ]


def system_type_list() -> list[dict]:
    """The distinct system types a study can be fixed to once, at Study Setup (see
    StudySetup.tsx + db.py's system_type column) -- in the order MACHINE_TYPES first
    introduces each one (mcg30, t700, heavy_feeder)."""
    seen: list[dict] = []
    seen_ids: set[str] = set()
    for spec in MACHINE_TYPES.values():
        if spec.system_type not in seen_ids:
            seen_ids.add(spec.system_type)
            seen.append({"id": spec.system_type, "label": SYSTEM_TYPE_LABELS[spec.system_type]})
    return seen


def _build_hindcast(
    scatter_source: str,
    location_id: str | None,
    hindcast_upload_path: Path | None,
    hindcast_filename: str | None,
    copernicus: dict | None,
    ndbc: dict | None,
):
    """Turn one of the app's "metocean data" source choices into a PyBM Hindcast object
    (or (None, None) if the study has no metocean data at all).

    Returns (hindcast_or_None, location_label_or_None). Hindcast() is a factory function --
    not a class you construct directly -- that inspects the loader you pass it and returns
    either a HindcastScatterTable (for statistical sources: DNV Weibull, an uploaded scatter
    table) or a HindcastTimeSeries (for sources backed by a real measured/reanalysis time
    series: Copernicus, NDBC). Both expose the same get_workability_percentage() method,
    which is the only thing run_calculation() below actually needs from either of them --
    that's what lets this function treat four very different data sources uniformly.
    """
    if scatter_source == "none":
        # No metocean data selected -- caller still gets the operating envelope (which sea
        # states the system can handle), just no weighted "overall workability %" on top.
        return None, None

    if scatter_source == "hindcast_upload":
        if not hindcast_upload_path or not hindcast_upload_path.exists():
            raise CalculationError("No hindcast scatter file was uploaded for this version.")
        display_name = hindcast_filename or hindcast_upload_path.name
        # We don't ask the user which sheet layout their file uses -- just try both supported
        # orientations and use whichever one parses. Whatever exception the second attempt
        # raises is the one surfaced, since by then both have failed.
        last_exc = None
        for sheet_name in ("Hs-Tp", "Tp-Hs"):
            try:
                loader = ExcelScatterLoader(file_path=str(hindcast_upload_path), sheet_name=sheet_name)
                return Hindcast(loader), f"Uploaded hindcast scatter ({display_name})"
            except Exception as exc:  # genuinely trying two formats
                last_exc = exc
        raise CalculationError(
            f"Could not read the uploaded scatter file as a 'Hs-Tp' or 'Tp-Hs' sheet: {last_exc}"
        )

    if scatter_source == "copernicus":
        # Copernicus Marine is a global reanalysis grid, so any lat/long works -- PyBM's
        # CopernicusLoader downloads and regrids the nearest model cell itself. Leaving
        # start/end date blank (None) fetches the whole available dataset rather than
        # defaulting to any particular year.
        if not copernicus or copernicus.get("lat") is None or copernicus.get("long") is None:
            raise CalculationError("Latitude and longitude are required to fetch Copernicus wave data.")
        try:
            loader = CopernicusLoader(
                lat=copernicus["lat"],
                long=copernicus["long"],
                product_id=copernicus.get("product_id", 0),
                start_date=copernicus.get("start_date"),
                end_date=copernicus.get("end_date"),
            )
            hindcast = Hindcast(loader)
        except Exception as exc:
            raise CalculationError(f"Could not fetch Copernicus wave data: {exc}") from exc
        # hindcast.start_date/end_date -- not copernicus["start_date"]/["end_date"] -- because
        # CopernicusLoader never resolves a blank date itself (it stays None all the way
        # through fetch()); it's PyBM's HindcastTimeSeries.__init__ that fills a still-None
        # start_date/end_date in from the actual fetched data's real min/max date. Reading
        # it off the hindcast object (rather than echoing back what we asked for) is what
        # lets the label show the true range actually used, blank request or not.
        period = f"{hindcast.start_date} to {hindcast.end_date}"
        label = f"Copernicus Marine ({copernicus['lat']}, {copernicus['long']}, {period})"
        return hindcast, label

    if scatter_source == "ndbc":
        # Unlike Copernicus, NDBC only has data at fixed, sparse real buoy locations -- so
        # (unlike Copernicus) the frontend's map picker only ever hands us a specific
        # `buoy_id`, never a raw lat/long to resolve to "whichever buoy happens to be
        # nearest" (that was tried and dropped: a nearby-but-wrong buoy silently produces
        # misleading results, see NdbcBuoyPickerModal.tsx). PyBM's NDBCLoader still accepts
        # lat/long as a fallback path for programmatic/API callers who bypass the UI.
        if not ndbc or not ndbc.get("buoy_id"):
            raise CalculationError("A buoy ID is required to fetch NOAA buoy data.")
        try:
            loader = NDBCLoader(
                buoy_id=ndbc["buoy_id"],
                start_date=ndbc.get("start_date"),
                end_date=ndbc.get("end_date"),
            )
            hindcast = Hindcast(loader)
        except Exception as exc:
            raise CalculationError(f"Could not fetch NOAA NDBC buoy data: {exc}") from exc
        # Same reasoning as Copernicus above, except NDBCLoader.fetch() *does* resolve a
        # blank date itself (earliest historical year / today) before Hindcast even builds
        # the HindcastTimeSeries -- so hindcast.start_date/end_date reflect that resolution
        # either way, blank request or not.
        period = f"{hindcast.start_date} to {hindcast.end_date}"
        label = f"NOAA NDBC buoy ({ndbc['buoy_id']}, {period})"
        return hindcast, label

    # Only "weibull_builtin" (one of the 104 DNV-RP-C205 nautic zones) falls through to
    # here; see resolve_weibull_params().
    weibull_params, label = resolve_weibull_params(location_id)
    try:
        loader = DNVLoader(**weibull_params)
        return Hindcast(loader), label
    except Exception as exc:
        raise CalculationError(f"Could not build the Weibull scatter distribution: {exc}") from exc


def run_calculation(
    *,
    vessel: str,
    loadcase: str,
    machine_type: str,
    position_m: tuple[float, float, float],
    luffing_angle_deg: float | None,
    slewing_angle_deg: float | None,
    dp_accuracy_m: float | None,
    lifting_radius_m: float | None,
    orientation_deg: float | None,
    p_passive_pa: float | None,
    comp_point_x_m: float | None,
    comp_point_y_m: float | None,
    comp_point_z_m: float | None,
    tp_min_s: float,
    tp_max_s: float,
    tp_step_s: float,
    wave_dir_step_deg: float,
    spreading: float,
    standard_deviations: float | None,
    scatter_source: str,
    location_id: str | None,
    hindcast_upload_path: Path | None,
    hindcast_filename: str | None,
    copernicus: dict | None,
    ndbc: dict | None,
    api: ApiSession,
) -> dict:
    """Runs one full workability calculation and returns everything routers/studies.py's
    create_version() needs to persist as a version: the operating envelope table, an
    optional overall workability %, and a rendered plot PNG.

    Broad shape: (1) resolve the vessel's RAO and build a PyBM machine object at its
    position/orientation, (2) build the Tp/heading wave grid to evaluate, (3) call PyBM's
    directional_workability() to get, for every (Tp, heading, limit-type) combination, the
    limiting Hs the machine can handle, (4) collapse that into the per-heading envelope
    table + worst case, (5) if metocean data was supplied, weight the envelope by how often
    each sea state actually occurs to get one overall %, (6) render the polar plot.
    """
    if machine_type not in MACHINE_TYPES:
        raise CalculationError(f"Unknown system '{machine_type}'.")
    spec = MACHINE_TYPES[machine_type]

    try:
        rao = get_rao(vessel, loadcase, api)
    except LoginRequired:
        raise
    except Exception as exc:
        raise CalculationError(f"Could not load RAO for {vessel} / {loadcase}: {exc}") from exc

    # Machine position comes in relative to the vessel's APP/CL/K reference point (see
    # MachineParams), but PyBM's machine classes want it relative to the RAO's own origin
    # -- the two aren't necessarily the same point, hence the subtraction.
    pos = np.array(position_m, dtype=float) - np.asarray(rao.origin, dtype=float)

    # Machine construction is the one place system_type-specific logic lives --
    # everything downstream (the Tp/heading wave grid, directional_workability() itself,
    # the envelope table, hindcast weighting, the plot) is machine-agnostic and unchanged
    # regardless of which system this is (see workability_limits.py's directional_workability,
    # which only ever touches `machine` through the shared Machine_Linear interface).
    if spec.system_type == "mcg30":
        if luffing_angle_deg is None or slewing_angle_deg is None or dp_accuracy_m is None:
            raise CalculationError(f"{spec.label} requires a luffing angle, slewing angle, and DP accuracy.")
        gw_telescope_mean = None
        if spec.needs_lifting_radius:
            if not lifting_radius_m:
                raise CalculationError(f"{spec.label} requires a lifting radius (m).")
            # The user gives a horizontal working radius; the boom is luffed up at
            # luffing_angle_deg from horizontal, so the actual (telescoping) boom length
            # needed to reach that radius is radius / cos(luffing angle) -- basic trig, not
            # a PyBM-specific formula.
            gw_telescope_mean = lifting_radius_m / np.cos(np.radians(luffing_angle_deg))
        # dp_accuracy_m is the vessel's dynamic-positioning station-keeping accuracy --
        # PyBM folds this into the machine's effective motion envelope as an extra
        # position uncertainty on top of the wave-induced motion itself.
        machine = spec.cls(
            pos,
            luffing_angle_deg,
            slewing_angle_deg,
            dp_accuracy=dp_accuracy_m,
            gw_telescope_mean=gw_telescope_mean,
        )
    elif spec.system_type == "t700":
        if orientation_deg is None:
            raise CalculationError(f"{spec.label} requires an orientation angle (deg).")
        machine_kwargs = {}
        if p_passive_pa is not None:
            machine_kwargs["P_passive"] = p_passive_pa
        machine = spec.cls(pos, orientation_deg, **machine_kwargs)
    elif spec.system_type == "heavy_feeder":
        if orientation_deg is None:
            raise CalculationError(f"{spec.label} requires an orientation angle (deg).")
        comp_point = [comp_point_x_m or 0.0, comp_point_y_m or 0.0, comp_point_z_m or 0.0]
        if spec.needs_comp_point_z and comp_point[2] <= 0:
            raise CalculationError(
                f"{spec.label} requires a compensation point height (Z, m) above the central bearing, greater than 0."
            )
        machine = spec.cls(pos, orientation_deg, comp_point)
    else:
        raise CalculationError(f"Unknown system type '{spec.system_type}' for {machine_type}.")

    if tp_max_s <= tp_min_s:
        raise CalculationError("Tp max must be greater than Tp min.")
    # The grid of sea states to evaluate: one JONSWAP wave spectrum per (Tp, heading) pair.
    # Heading convention (PyBM's, not this app's own): 0deg = from stern, 180deg = from bow,
    # 90deg = from starboard. `spreading` controls how directionally concentrated each
    # spectrum is (<=0 means unidirectional). The `1` is a nominal 1m significant wave
    # height (Hs) -- directional_workability() doesn't need Hs swept as an input; it takes
    # this one reference spectrum per (Tp, heading) and works out the *limiting* Hs (how
    # high the actual sea state could get before exceeding the machine's operational
    # limit) as its output.
    Tps = np.arange(tp_min_s, tp_max_s + tp_step_s, tp_step_s)
    WaveDirs = np.arange(0, 360, wave_dir_step_deg)
    wave = Jonswap(1, Tps, main_direction=WaveDirs, spreading=spreading)

    # n_sigma (a.k.a. standard_deviations) sets how many standard deviations of the
    # response spectrum's statistical distribution count as "the" motion amplitude to
    # compare against the machine's operational limit -- i.e. how conservative the
    # limiting-Hs calculation is. Each machine type has its own sensible default (higher
    # for lifting than transfer -- see MACHINE_TYPES); an explicit standard_deviations
    # from the request always overrides that default.
    n_sigma = standard_deviations if standard_deviations is not None else spec.default_n_sigma
    kwargs = {}
    if n_sigma is not None:
        kwargs["standard_deviations"] = n_sigma

    try:
        result = directional_workability(rao, wave, machine, **kwargs)
    except Exception as exc:
        raise CalculationError(f"Calculation engine failed: {exc}") from exc

    # `result` holds one limiting Hs per (Tp, heading, lim_type) -- lim_type indexes
    # whichever distinct machine limits PyBM checks (e.g. different motion/response
    # criteria). The governing (most restrictive) limit at each (Tp, heading) is whichever
    # lim_type gives the smallest limiting Hs, hence min("lim_type"). What's left,
    # `limiting`, is the operating envelope itself: the max Hs the machine can handle at
    # each Tp/heading.
    limiting = result.min("lim_type")  # dims: Tp, WaveDirection -- [m] limiting Hs (operating envelope)

    headings = [int(h) for h in limiting["WaveDirection"].values]
    table = []
    tps = [float(tp) for tp in (limiting["Tp"].values if "Tp" in limiting.coords else Tps)]
    for heading in headings:
        hs_curve = limiting.sel(WaveDirection=heading)
        # null where PyBM found no finite limit -- NaN/inf aren't valid JSON
        hs_values = [round(float(hs), 2) if np.isfinite(hs) else None for hs in hs_curve.values]
        table.append(
            {
                "heading_from_deg": heading,
                "heading_to_deg": (heading + int(wave_dir_step_deg)) % 360,
                # min/max across the Tp axis for this heading -- the envelope narrows or
                # widens with Tp, so both bounds matter for the per-heading summary table.
                "hs_limit_min_m": round(float(hs_curve.min()), 2),
                "hs_limit_max_m": round(float(hs_curve.max()), 2),
                "tp_min_s": float(tp_min_s),
                "tp_max_s": float(Tps[-1]),
                # The whole limiting-Hs-vs-Tp curve, and the Tp its minimum falls at: the report's
                # overview ("2.0 m Hs @ Tp = 10 s") and its Hs-vs-Tp results figure are made from these.
                "tp_at_min_s": tps[int(np.nanargmin(hs_curve.values))],
                "hs_limit_by_tp_m": hs_values,
            }
        )
    worst_row = min(table, key=lambda r: r["hs_limit_min_m"])

    # Overall workability % needs real metocean data (a Weibull scatter or an
    # uploaded hindcast table) to weight the operating envelope by how often each
    # sea state actually occurs -- without it there's nothing to weight by, so we
    # only report the envelope itself (this matches how the original calculation
    # scripts work: no scatter data in, no percentage out).
    overall_pct = None
    monthly_pct = None
    hindcast, location_label = _build_hindcast(
        scatter_source, location_id, hindcast_upload_path, hindcast_filename, copernicus, ndbc
    )
    if hindcast is not None:
        # Collapse to one limiting-Hs-vs-Tp curve using the worst (most restrictive)
        # heading at every Tp -- a single, heading-agnostic, conservative basis to weight
        # against the metocean source's omnidirectional sea-state statistics, since real
        # operations can't guarantee the vessel always sits at its best heading.
        all_headings_worst = limiting.min("WaveDirection")  # dims: Tp -- worst case across all headings
        try:
            overall_pct = round(float(hindcast.get_workability_percentage(all_headings_worst, period="overall")), 1)
        except Exception as exc:
            raise CalculationError(f"Workability percentage calculation failed: {exc}") from exc

        # Monthly breakdown -- only meaningful for a real dated time series (Copernicus,
        # NDBC): PyBM buckets every sample by *calendar* month across however many years
        # the data spans (e.g. every January in a 5-year dataset becomes one "Jan" figure),
        # so this shows seasonal pattern, not a per-project-month timeline. Useful for a
        # project that only runs a few months, to see whether it lands in a good or bad
        # season rather than reading one blended year-round percentage. A statistical
        # scatter source (DNV Weibull, or an uploaded scatter table) has no real dates to
        # bucket by, so PyBM raises NotImplementedError there -- caught, not surfaced as an
        # error, since "no monthly breakdown for this source" is expected, not a failure.
        try:
            monthly_series = hindcast.get_workability_percentage(all_headings_worst, period="monthly")
            monthly_pct = {month: round(float(pct), 1) for month, pct in monthly_series.items()}
        except NotImplementedError:
            pass

    # Plotting all Tp values would make an unreadably dense polar chart -- pick up to 6,
    # evenly spaced across the full Tp range (np.unique guards against duplicate indices
    # if there are fewer than 6 distinct Tps to begin with).
    n_plot_tps = min(6, Tps.size)
    plot_tp_idx = np.unique(np.linspace(0, Tps.size - 1, n_plot_tps).round().astype(int))
    plot_result = result.isel(Tp=plot_tp_idx)

    fig = plt.figure(figsize=(6.5, 8.5))
    plot_result.workability.plot_combined_workability(max_hs=spec.default_max_hs_plot, fig=fig)
    # PyBM's own plotting helper adds a legend that duplicates information already visible
    # in the per-Tp subplot titles/colors at this figure size -- drop it if present (some
    # PyBM versions/plot configurations don't add one at all).
    if fig.legends:
        fig.legends[0].remove()
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=130, bbox_inches="tight")
    plt.close(fig)  # release the figure now -- matplotlib keeps closed figures around otherwise, a slow memory leak across many calculations in one long-running process
    buf.seek(0)

    return {
        "overall_workability_pct": overall_pct,
        "monthly_workability_pct": monthly_pct,  # {"Jan": 95.6, ...} by calendar month, or None -- see comment above
        "worst_case": {
            "heading_from_deg": worst_row["heading_from_deg"],
            "heading_to_deg": worst_row["heading_to_deg"],
            "hs_limit_min_m": worst_row["hs_limit_min_m"],
        },
        "table": table,
        "tps_s": tps,  # the Tp axis of every row's hs_limit_by_tp_m
        "location_label": location_label,
        "n_sigma_used": n_sigma,  # echoed back so the frontend/report can show which n-sigma was actually used, including the machine's own default when the request didn't override it
        "plot_png": buf.read(),  # popped out and written to disk by routers/studies.py before the rest of this dict is stored as JSON
    }
