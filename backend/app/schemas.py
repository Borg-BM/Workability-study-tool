"""Pydantic request/response models for the FastAPI routes in routers/.

These are the wire format the frontend's src/api.ts talks to -- keep the two in sync by
hand (there's no shared codegen between them): a field added/removed/renamed here needs
the matching change in api.ts's VersionParams (or whichever interface mirrors it).
"""

from typing import Literal

from pydantic import BaseModel, Field


class SetRaoRequest(BaseModel):
    """Body for PUT /api/studies/{id}/rao -- locks a study to one vessel + loadcase RAO.

    Vessel dimensions are optional and purely cosmetic (used in the eventual report),
    not fed into the calculation itself -- PyBM gets everything it needs about the
    vessel's motion behaviour from the RAO (vessel, loadcase) pair alone.
    """

    vessel: str
    loadcase: str
    system_type: str  # "mcg30" | "t700" | "heavy_feeder" -- see pybm_service.system_type_list()
    vessel_length_m: float | None = None
    vessel_breadth_m: float | None = None
    vessel_depth_m: float | None = None
    vessel_draft_m: float | None = None


class UpdateStudyRequest(BaseModel):
    """Body for PATCH /api/studies/{id} -- renames a study or changes its project tag.
    Both fields are optional so the frontend can send just the one that changed."""

    name: str | None = None
    project: str | None = None


class AddCollaboratorRequest(BaseModel):
    """Body for POST /api/studies/{id}/collaborators -- grants the given email edit
    rights on the study (see db.can_edit). Owner-only action."""

    email: str


class TransferOwnershipRequest(BaseModel):
    """Body for POST /api/studies/{id}/transfer -- reassigns the study to a new owner
    (e.g. when the current owner leaves the company). Owner-or-admin action."""

    new_owner_email: str
    new_owner_name: str | None = None


class MachineParams(BaseModel):
    """The equipment side of a calculation: which system, where it sits on the vessel, and
    how it's oriented/configured. Mirrors run_calculation()'s machine-related arguments in
    pybm_service.py one-for-one.

    Fields below are grouped by which system_type actually reads them (see
    pybm_service.MachineSpec.system_type / MACHINE_TYPES) -- every field is optional here
    since this one model is shared across all system types; run_calculation() raises
    CalculationError if a field its branch actually needs is missing."""

    machine_type: str
    position_x_m: float = Field(..., description="w.r.t. vessel APP/CL/K reference point")
    position_y_m: float
    position_z_m: float

    # MCG30 only
    luffing_angle_deg: float | None = None
    slewing_angle_deg: float | None = Field(None, description="90=port, 270=starboard")
    dp_accuracy_m: float | None = 0.5
    lifting_radius_m: float | None = None

    # T700 / Heavy Feeder family -- overall yaw orientation ("w.r.t. RAO definitions")
    orientation_deg: float | None = None

    # T700 only -- hydraulic passive pressure (Pa); None = PyBM's own class default
    p_passive_pa: float | None = None

    # Heavy Feeder family only -- surge/sway compensation point, as a local offset from
    # the central bearing (not w.r.t. the vessel APP/CL/K reference point like position_*_m
    # above). comp_point_z_m must be a real positive value for the surge/sway-compensated
    # variant (see HeavyFeederSurgeSway.py's assertion / MachineSpec.needs_comp_point_z).
    comp_point_x_m: float | None = None
    comp_point_y_m: float | None = None
    comp_point_z_m: float | None = None


# Which of the app's four metocean data sources a study version uses (or none at all).
# Each value beyond "none" has its own block of fields below that only apply to it -- see
# pybm_service.py's _build_hindcast() for how each one is actually turned into a Hindcast.
ScatterSource = Literal["none", "weibull_builtin", "hindcast_upload", "copernicus", "ndbc"]


class EnvironmentParams(BaseModel):
    """The sea-state side of a calculation: the Tp/heading grid to sweep, and (optionally)
    which real or statistical metocean data source to weight the results by.

    Metocean data is optional: without it you still get the operating envelope (limiting
    Hs per heading/Tp) and the polar plot, just no single "overall workability %" number --
    that number needs real occurrence statistics (how often each sea state actually
    happens) to weight the envelope by, which is exactly what a scatter_source provides.
    """

    tp_min_s: float = 4.0
    tp_max_s: float = 18.0
    tp_step_s: float = 2.0
    wave_dir_step_deg: float = 30.0
    spreading: float = 3.0
    standard_deviations: float | None = None  # None = let PyBM use the machine's own MPE default

    scatter_source: ScatterSource = "none"
    location_id: str | None = None  # scatter_source == "weibull_builtin" -- a weibull_locations.py key, e.g. "gws_zone_11"
    hindcast_upload_id: str | None = None  # scatter_source == "hindcast_upload" -- id returned by POST .../hindcast-upload
    hindcast_filename: str | None = None  # original filename, for display only (the id above is what's actually read)

    # scatter_source == "copernicus" -- any lat/long works, PyBM's CopernicusLoader
    # downloads and regrids the nearest reanalysis model cell itself.
    copernicus_lat: float | None = None
    copernicus_long: float | None = None
    copernicus_product_id: int = 0  # index into pybm_service.COPERNICUS_PRODUCTS
    copernicus_start_date: str | None = None  # 'YYYY-MM-DD'
    copernicus_end_date: str | None = None

    # scatter_source == "ndbc" -- a specific real NOAA buoy, picked from the map in
    # NdbcBuoyPickerModal.tsx (which only offers buoys confirmed to have a real historical
    # record -- see pybm_service.list_ndbc_buoys). Unlike Copernicus there's no lat/long
    # fallback here: an arbitrary coordinate would silently resolve to "whichever buoy
    # happens to be nearest," which can be hundreds of km away and give misleading data.
    ndbc_buoy_id: str | None = None
    ndbc_start_date: str | None = None  # 'YYYY-MM-DD'
    ndbc_end_date: str | None = None


class CreateVersionRequest(BaseModel):
    """Body for POST /api/studies/{id}/versions -- runs one full calculation and stores
    the result as a new version. Every "Generate workability study" click sends one of these."""

    machine: MachineParams
    environment: EnvironmentParams


class CreateStudyRequest(BaseModel):
    """Body for POST /api/studies -- both fields are optional; db.create_study() fills in
    a default name (WS-<year>-<n>) and an empty project if omitted."""

    name: str | None = None
    project: str = ""


class ApproveVersionRequest(BaseModel):
    """Body for POST /api/studies/{id}/versions/approve -- marks one existing version as
    the study's approved result (only one version can be approved at a time)."""

    version_id: str


class SaveReportRequest(BaseModel):
    """Body for PUT /api/studies/{id}/report -- the choices the report document is generated
    from (header fields, which study_files fill which figure slot; older saves also carry the
    pre-.docx narrative text), saved wholesale. Deliberately a loose dict, not a fixed model:
    the shape is owned by the frontend (see reportModel.ts's ReportState type) and
    stored/returned as opaque JSON, the same pattern as a version's params/result."""

    report: dict


class UpdateStudyFileRequest(BaseModel):
    """Body for PATCH /api/studies/{id}/files/{file_id} -- edits a supporting-material
    file's caption or its position in the list; both optional so the frontend can send
    just the one that changed (same pattern as UpdateStudyRequest)."""

    caption: str | None = None
    sort_order: int | None = None


class ReviewerRequest(BaseModel):
    """Who should review (check) the current report revision -- like sharing, by email and name."""

    reviewer_email: str
    reviewer_name: str


class ReviewDecisionRequest(BaseModel):
    decision: Literal["approve", "changes"]
    comment: str = ""


class CreateCommentRequest(BaseModel):
    """Body for POST /api/studies/{id}/revisions/{revision}/comments: a new thread -- anchored
    to `para_id` (the paragraph's w14:paraId) and `quote` (the selected text) when made on a
    selection, or a general comment without them -- or, with `parent_id`, a reply to one."""

    body: str = Field(min_length=1, max_length=5000)
    parent_id: str | None = None
    para_id: str | None = Field(default=None, pattern=r"^[0-9A-Fa-f]{8}$")
    quote: str = Field(default="", max_length=1000)


class UpdateCommentRequest(BaseModel):
    """Body for PATCH /api/studies/{id}/comments/{comment_id}: resolve or reopen a thread."""

    resolved: bool
