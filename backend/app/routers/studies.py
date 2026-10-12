"""CRUD for studies + running calculations ("versions").

A study is a durable record (survives across the "Studies" dashboard) tied to exactly one
vessel/loadcase RAO. Each time the user clicks "Generate workability study" in the
StudyBuilder screen, that's a POST to /versions here: it runs one full PyBM calculation
and stores the result as an immutable "version" under the study, so past results stay
available for comparison even as the user tweaks parameters and re-runs.
"""

import uuid
from datetime import datetime, timezone
from pathlib import Path

from fastapi import APIRouter, Depends, Form, HTTPException, Request, UploadFile
from fastapi.responses import FileResponse, Response
from starlette.concurrency import run_in_threadpool

from .. import db, roles
from ..diffs import summarize_diff
from ..docx_comments import add_review_comments, strip_comments
from ..identity import get_current_user
from ..pybm_service import MACHINE_TYPES, CalculationError, run_calculation, system_type_list
from ..report_docx import build_report_docx, bump_ref_revision, title_block_values, today_label, update_title_block
from ..sso import ApiSession, LoginRequired, pybm_api
from .convert import read_docx_body
from ..schemas import (
    AddCollaboratorRequest,
    ApproveVersionRequest,
    CreateCommentRequest,
    CreateStudyRequest,
    CreateVersionRequest,
    ReviewDecisionRequest,
    ReviewerRequest,
    SaveReportRequest,
    SetRaoRequest,
    TransferOwnershipRequest,
    UpdateCommentRequest,
    UpdateStudyFileRequest,
    UpdateStudyRequest,
)

# Supporting-material uploads (UploadMaterial.tsx) accept either an image (previewable
# inline, selectable as a report figure) or a reference document -- anything else is
# rejected outright rather than stored with a guessed kind.
_IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
_DOCUMENT_EXTS = {".pdf", ".dwg", ".doc", ".docx", ".xls", ".xlsx"}

# Supporting material feeds the report, so it's frozen along with it once a revision is submitted.
_MATERIAL_STATUSES = db.BUILD_STATUSES | {"reporting"}

router = APIRouter(prefix="/api/studies", tags=["studies"])


def _require_edit(study: dict, user: dict):
    """403s unless `user` is the study's owner, an explicitly granted collaborator (see
    db.can_edit), or an admin (see roles.is_admin -- admins have owner-equivalent rights on
    every study). Every endpoint that mutates a study's content -- not just its
    owner/collaborator list, see _require_owner for that -- goes through this."""
    if not (user["is_admin"] or db.can_edit(study, user["email"])):
        raise HTTPException(status_code=403, detail="You don't have edit access to this study -- ask the owner to add you as a collaborator, or make your own copy.")


def _require_owner(study: dict, user: dict):
    """403s unless `user` is the study's owner or an admin. Stricter than _require_edit --
    collaborators can edit a study's content but can't manage who else can, archive/
    unarchive, delete it, or transfer ownership."""
    if not (user["is_admin"] or db.is_owner(study, user["email"])):
        raise HTTPException(status_code=403, detail="Only this study's owner (or an admin) can do that.")


def _require_status(study: dict, allowed: set[str], action: str):
    """409s unless the study's workflow stage (see db.BUILD_STATUSES) still allows `action`."""
    if study["status"] in allowed:
        return
    if study["status"] in db.REVIEW_STATUSES:
        reason = f"revision {study['revision']} has been submitted for review and is locked -- start a new revision to make changes"
    elif study["status"] == "reporting":
        reason = "the study's result is approved and locked -- reopen the study to change it"
    else:
        reason = "the study hasn't reached that stage yet -- approve a result first"
    raise HTTPException(status_code=409, detail=f"Can't {action}: {reason}.")


def _get_study(study_id: str) -> dict:
    """The study with everything db.get_study loads, or a 404."""
    study = db.get_study(study_id)
    if study is None:
        raise HTTPException(status_code=404, detail="Study not found")
    return study


@router.get("")
def list_studies():
    return {"studies": db.list_studies()}


@router.post("")
def create_study(body: CreateStudyRequest, user: dict = Depends(get_current_user)):
    # A "WS-<year>-<n>" reference when the caller didn't supply a name. n is the study count
    # + 1: sequential, but deleting an earlier study can make the next n repeat an existing
    # one -- it's only a default, renamed freely afterwards.
    name = body.name or f"WS-{datetime.now(timezone.utc).year}-{db.count_studies() + 1:03d}"
    return db.create_study(name=name, project=body.project, owner_email=user["email"], owner_name=user["name"])


@router.get("/{study_id}")
def get_study(study_id: str):
    # No permission check -- every study is readable by everyone (see db.list_studies()'s
    # docstring); only writes are gated by ownership/collaborator status.
    return _get_study(study_id)


@router.delete("/{study_id}", status_code=204)
def delete_study(study_id: str, user: dict = Depends(get_current_user)):
    study = _get_study(study_id)
    _require_owner(study, user)
    db.delete_study(study_id)


@router.post("/{study_id}/archive")
def archive_study(study_id: str, user: dict = Depends(get_current_user)):
    """Hides the study from the main dashboard tabs (see StudiesDashboard.tsx's "Archived"
    tab) -- purely a display-state flag, fully reversible, owner-only like delete/sharing."""
    study = _get_study(study_id)
    _require_owner(study, user)
    return db.set_study_archived(study_id, True)


@router.post("/{study_id}/unarchive")
def unarchive_study(study_id: str, user: dict = Depends(get_current_user)):
    study = _get_study(study_id)
    _require_owner(study, user)
    return db.set_study_archived(study_id, False)


@router.post("/{study_id}/copy")
def copy_study(study_id: str, user: dict = Depends(get_current_user)):
    """"Copy to my studies" -- anyone can do this (read access is universal), regardless of
    whether they have edit rights on the original. Gives them their own editable study,
    locked to the same vessel/loadcase/system_type, with a fresh version history."""
    copy = db.copy_study(study_id, owner_email=user["email"], owner_name=user["name"])
    if copy is None:
        raise HTTPException(status_code=404, detail="Study not found")
    return copy


@router.post("/{study_id}/collaborators")
def add_collaborator(study_id: str, body: AddCollaboratorRequest, user: dict = Depends(get_current_user)):
    study = _get_study(study_id)
    _require_owner(study, user)
    email = body.email.strip().lower()
    if not email:
        raise HTTPException(status_code=422, detail="An email is required.")
    if email == study["owner_email"]:
        raise HTTPException(status_code=422, detail="This person already owns the study.")
    collaborators = db.add_collaborator(study_id, email)
    return {"collaborators": collaborators}


@router.delete("/{study_id}/collaborators/{email}")
def remove_collaborator(study_id: str, email: str, user: dict = Depends(get_current_user)):
    study = _get_study(study_id)
    _require_owner(study, user)
    collaborators = db.remove_collaborator(study_id, email.strip().lower())
    return {"collaborators": collaborators}


@router.post("/{study_id}/transfer")
def transfer_ownership(study_id: str, body: TransferOwnershipRequest, user: dict = Depends(get_current_user)):
    """Reassigns the study to a new owner -- for when the current owner leaves the
    company and someone (them, while they still can, or an admin afterwards) needs to
    hand it off. See db.transfer_study_ownership for what happens to the collaborator list."""
    study = _get_study(study_id)
    _require_owner(study, user)
    new_email = body.new_owner_email.strip().lower()
    if not new_email:
        raise HTTPException(status_code=422, detail="A new owner's email is required.")
    updated = db.transfer_study_ownership(study_id, new_owner_email=new_email, new_owner_name=(body.new_owner_name or new_email).strip())
    return updated


@router.patch("/{study_id}")
def update_study(study_id: str, body: UpdateStudyRequest, user: dict = Depends(get_current_user)):
    study = _get_study(study_id)
    _require_edit(study, user)
    updated = db.update_study_meta(study_id, name=body.name, project=body.project)
    return updated


@router.put("/{study_id}/rao")
def set_rao(study_id: str, body: SetRaoRequest, user: dict = Depends(get_current_user)):
    """Locks a study to one vessel + loadcase RAO. This can only be done once per study --
    db.set_study_rao raises ValueError (-> 409) if the study already has a different RAO
    set, since every version under a study has to be comparable against the same vessel
    motion behaviour. To pick a different vessel, the user has to delete the study and
    start over (see StudySetup.tsx's warning text)."""
    study = _get_study(study_id)
    _require_edit(study, user)
    valid_system_types = {s["id"] for s in system_type_list()}
    if body.system_type not in valid_system_types:
        raise HTTPException(status_code=422, detail=f"Unknown system type '{body.system_type}'.")
    try:
        updated = db.set_study_rao(
            study_id,
            body.vessel,
            body.loadcase,
            body.system_type,
            vessel_length_m=body.vessel_length_m,
            vessel_breadth_m=body.vessel_breadth_m,
            vessel_depth_m=body.vessel_depth_m,
            vessel_draft_m=body.vessel_draft_m,
        )
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc))
    return updated


@router.post("/{study_id}/hindcast-upload")
async def upload_hindcast(study_id: str, file: UploadFile, user: dict = Depends(get_current_user)):
    """Stores an uploaded .xlsx scatter table under a random id and hands that id back --
    it's *not* attached to a version yet. The frontend holds the id in memory and only
    sends it along when the user actually clicks "Generate" with scatter_source ==
    "hindcast_upload" (see CreateVersionRequest.environment.hindcast_upload_id), so an
    upload with no follow-up "Generate" just leaves an orphaned file in HINDCAST_DIR."""
    study = _get_study(study_id)
    _require_edit(study, user)
    _require_status(study, db.BUILD_STATUSES, "upload metocean data")
    if not file.filename or not file.filename.lower().endswith(".xlsx"):
        raise HTTPException(status_code=422, detail="Please upload an .xlsx scatter table (see HindcastScatterTable_template.xlsx).")
    upload_id = uuid.uuid4().hex[:12]
    dest = db.HINDCAST_DIR / f"{upload_id}.xlsx"
    dest.write_bytes(await file.read())
    return {"id": upload_id, "filename": file.filename}


@router.post("/{study_id}/versions")
def create_version(
    study_id: str,
    body: CreateVersionRequest,
    user: dict = Depends(get_current_user),
    api: ApiSession = Depends(pybm_api),
):
    """Runs one calculation and stores it as a new, numbered version under the study.
    This is the single most involved endpoint in the app -- it validates the request,
    resolves whichever metocean data source was picked into the shape run_calculation()
    expects, runs the (potentially slow -- Copernicus/NDBC do real network fetches)
    calculation, and persists everything: the result JSON, the polar plot PNG, and a
    human-readable diff summary against the previous version.
    """
    study = _get_study(study_id)
    _require_edit(study, user)
    _require_status(study, db.BUILD_STATUSES, "generate a new result")
    if not study["vessel"] or not study["loadcase"]:
        raise HTTPException(status_code=409, detail="This study has no RAO set yet -- select a vessel and loadcase first.")
    machine_spec = MACHINE_TYPES.get(body.machine.machine_type)
    if machine_spec is None:
        raise HTTPException(status_code=422, detail=f"Unknown system '{body.machine.machine_type}'.")
    if machine_spec.system_type != study["system_type"]:
        raise HTTPException(
            status_code=422,
            detail=f"'{machine_spec.label}' is not a {study['system_type']} system -- this study is fixed to {study['system_type']}.",
        )

    # Keep the full request verbatim -- this is what gets diffed against the previous
    # version (see summarize_diff below) and stored for the record, independent of
    # whatever subset of it run_calculation() actually consumes.
    params = {
        "machine": body.machine.model_dump(),
        "environment": body.environment.model_dump(),
    }

    # Each scatter_source has its own required fields; only validate/build the one that's
    # actually selected; the schema itself declares all of them optional since the model
    # is shared across mutually-exclusive choices.
    hindcast_upload_path = None
    if body.environment.scatter_source == "hindcast_upload":
        if not body.environment.hindcast_upload_id:
            raise HTTPException(status_code=422, detail="No hindcast file selected for this version.")
        candidate = db.HINDCAST_DIR / f"{body.environment.hindcast_upload_id}.xlsx"
        if not candidate.exists():
            raise HTTPException(status_code=404, detail="Uploaded hindcast file not found -- please upload it again.")
        hindcast_upload_path = candidate

    copernicus = None
    if body.environment.scatter_source == "copernicus":
        copernicus = {
            "lat": body.environment.copernicus_lat,
            "long": body.environment.copernicus_long,
            "product_id": body.environment.copernicus_product_id,
            "start_date": body.environment.copernicus_start_date,
            "end_date": body.environment.copernicus_end_date,
        }

    ndbc = None
    if body.environment.scatter_source == "ndbc":
        ndbc = {
            "buoy_id": body.environment.ndbc_buoy_id,
            "start_date": body.environment.ndbc_start_date,
            "end_date": body.environment.ndbc_end_date,
        }

    try:
        result = run_calculation(
            vessel=study["vessel"],
            loadcase=study["loadcase"],
            machine_type=body.machine.machine_type,
            position_m=(body.machine.position_x_m, body.machine.position_y_m, body.machine.position_z_m),
            luffing_angle_deg=body.machine.luffing_angle_deg,
            slewing_angle_deg=body.machine.slewing_angle_deg,
            dp_accuracy_m=body.machine.dp_accuracy_m,
            lifting_radius_m=body.machine.lifting_radius_m,
            orientation_deg=body.machine.orientation_deg,
            p_passive_pa=body.machine.p_passive_pa,
            comp_point_x_m=body.machine.comp_point_x_m,
            comp_point_y_m=body.machine.comp_point_y_m,
            comp_point_z_m=body.machine.comp_point_z_m,
            tp_min_s=body.environment.tp_min_s,
            tp_max_s=body.environment.tp_max_s,
            tp_step_s=body.environment.tp_step_s,
            wave_dir_step_deg=body.environment.wave_dir_step_deg,
            spreading=body.environment.spreading,
            standard_deviations=body.environment.standard_deviations,
            scatter_source=body.environment.scatter_source,
            location_id=body.environment.location_id,
            hindcast_upload_path=hindcast_upload_path,
            hindcast_filename=body.environment.hindcast_filename,
            copernicus=copernicus,
            ndbc=ndbc,
            api=api,
        )
    except CalculationError as exc:
        # A user-fixable problem (bad params, missing data, upstream data source rejected
        # the request) -- 422 so the frontend shows it as a form error, not a crash.
        raise HTTPException(status_code=422, detail=str(exc))
    except LoginRequired:
        # Fetching the RAO needs the user to sign in again -- a 401, see main.py.
        raise
    except Exception as exc:
        # Anything else is a genuine bug/unexpected engine failure -- 500, and we still
        # surface the raw exception text since this is an internal tool, not a public API.
        raise HTTPException(status_code=500, detail=f"Calculation engine failed: {exc}")

    # The plot comes back as PNG bytes embedded in the result dict; pull it out and write
    # it to disk under its own filename so the API can serve it as a static file (see
    # db.py/main.py's static mount) instead of re-encoding it into every /versions response.
    version_n = db.count_versions(study_id) + 1
    plot_filename = f"{study_id}_v{version_n}.png"
    (db.PLOTS_DIR / plot_filename).write_bytes(result.pop("plot_png"))

    previous_params = db.last_version_params(study_id)
    diff_summary = summarize_diff(previous_params, params)

    version = db.add_version(
        study_id,
        label=f"v{version_n}",
        diff_summary=diff_summary,
        params=params,
        result=result,
        plot_filename=plot_filename,
    )
    return version


@router.post("/{study_id}/versions/approve")
def approve_version(study_id: str, body: ApproveVersionRequest, user: dict = Depends(get_current_user)):
    """Marks one version as the study's approved result and completes the build stage: the
    study builder locks (see reopen_study) and the study moves on to the report."""
    study = _get_study(study_id)
    _require_edit(study, user)
    _require_status(study, db.BUILD_STATUSES, "approve a result")
    version = db.approve_version(study_id, body.version_id)
    if version is None:
        raise HTTPException(status_code=404, detail="Version not found")
    return version


@router.post("/{study_id}/reopen")
def reopen_study(study_id: str, user: dict = Depends(get_current_user)):
    """The deliberate "overwrite": unlocks the study builder again so new results can be
    generated and a different one approved. Only until the report is submitted for review --
    after that, changes need a new revision."""
    study = _get_study(study_id)
    _require_edit(study, user)
    _require_status(study, {"reporting"}, "reopen the study")
    db.touch_study(study_id, status="in_progress")
    return db.get_study(study_id)


@router.put("/{study_id}/report")
def save_report(study_id: str, body: SaveReportRequest, user: dict = Depends(get_current_user)):
    """Persists the report document's generation choices -- see SaveReportRequest for why
    this takes/returns an opaque dict rather than a fixed schema."""
    study = _get_study(study_id)
    _require_edit(study, user)
    _require_status(study, {"reporting"}, "change the report setup")
    updated = db.save_study_report(study_id, body.report)
    return {"report": updated}


@router.get("/{study_id}/report/docx")
def get_report_docx(study_id: str):
    """The study's report document -- 404 until one has been generated (or uploaded)."""
    _get_study(study_id)
    path = db.report_docx_path(study_id)
    if not path.exists():
        raise HTTPException(status_code=404, detail="No report document yet -- generate one first.")
    return FileResponse(
        path,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Cache-Control": "no-store"},
    )


@router.post("/{study_id}/report/docx/generate", status_code=204)
def generate_report_docx(study_id: str, user: dict = Depends(get_current_user)):
    """(Re)builds the report document from the saved header/figure choices and the approved result,
    replacing any existing one. Whoever generates it is its Author."""
    study = _get_study(study_id)
    _require_edit(study, user)
    _require_status(study, {"reporting"}, "generate the report")
    db.write_report_docx(study_id, build_report_docx(study, author=user["name"]))
    approved = next((v for v in study["versions"] if v["approved"]), None)
    db.record_report_generated(study_id, approved["id"] if approved else None)


@router.put("/{study_id}/report/docx")
async def save_report_docx(study_id: str, request: Request, user: dict = Depends(get_current_user)):
    """Stores edited document bytes -- from the in-app editor's autosave, or a .docx edited in Word.
    Word comments are taken out (docx_comments.strip_comments): a file edited in Word after
    "Download for Word, with comments" comes back with them, and review comments live in the
    app. Answers how many there were, so the upload can say so."""
    # Read before any refusal: answering mid-upload drops the connection, and the client sees a
    # network error instead of the reason (e.g. a colleague just submitted it for review).
    docx = await read_docx_body(request)
    study = _get_study(study_id)
    _require_edit(study, user)
    _require_status(study, {"reporting"}, "edit the report")
    try:
        docx, removed = await run_in_threadpool(strip_comments, docx)
    except Exception as exc:  # not a zip python can read
        raise HTTPException(status_code=422, detail=f"That document can't be read: {exc}")
    db.write_report_docx(study_id, docx)
    return {"word_comments_removed": removed}


def _reviewer(body: ReviewerRequest, user: dict) -> tuple[str, str]:
    """The requested reviewer as (email, name), or a 422 when they can't review this: not in
    the reviewer group (when there is one), incomplete, or the person submitting."""
    email, name = body.reviewer_email.strip().lower(), body.reviewer_name.strip()
    if roles.REVIEWERS.configured:
        # Only members of the Authentik reviewer group can check a report, under their Authentik name.
        listed = roles.reviewer(email)
        if listed is None:
            raise HTTPException(status_code=422, detail=f"{email or 'That person'} isn't in the reviewer group -- pick a reviewer from the list.")
        name = listed["name"]
    if not email or not name:
        raise HTTPException(status_code=422, detail="The reviewer's email and name are both required.")
    if email == user["email"]:
        raise HTTPException(status_code=422, detail="The report has to be checked by a different engineer than you.")
    return email, name


@router.post("/{study_id}/review")
def submit_for_review(study_id: str, body: ReviewerRequest, user: dict = Depends(get_current_user)):
    """Submits the current revision to a reviewer, who becomes the document's Check and Approval. Freezes
    it: from here on, changes need a new revision (start_revision)."""
    study = _get_study(study_id)
    _require_edit(study, user)
    _require_status(study, {"reporting"}, "submit for review")
    reviewer_email, reviewer_name = _reviewer(body, user)
    path = db.report_docx_path(study_id)
    if not path.exists():
        raise HTTPException(status_code=409, detail="Generate the report document before submitting it for review.")
    docx = update_title_block(path.read_bytes(), {"Check": reviewer_name, "Approval": reviewer_name})
    db.submit_revision(study_id, study["revision"], author=user, reviewer_email=reviewer_email, reviewer_name=reviewer_name, docx=docx)
    return db.get_study(study_id)


@router.put("/{study_id}/review/reviewer")
def change_reviewer(study_id: str, body: ReviewerRequest, user: dict = Depends(get_current_user)):
    """Hands a revision that's waiting for review to someone else (and updates its Check and Approval)."""
    study = _get_study(study_id)
    _require_edit(study, user)
    _require_status(study, {"in_review"}, "change the reviewer")
    reviewer_email, reviewer_name = _reviewer(body, user)
    if reviewer_email == study["review"]["author_email"]:
        raise HTTPException(status_code=422, detail="The report has to be checked by a different engineer than its author.")
    docx = update_title_block(
        db.revision_docx_path(study_id, study["revision"]).read_bytes(), {"Check": reviewer_name, "Approval": reviewer_name}
    )
    db.reassign_reviewer(study_id, study["revision"], reviewer_email=reviewer_email, reviewer_name=reviewer_name, docx=docx)
    return db.get_study(study_id)


@router.post("/{study_id}/review/decision")
def decide_review(study_id: str, body: ReviewDecisionRequest, user: dict = Depends(get_current_user)):
    """The assigned reviewer approves the revision, or sends it back with comments."""
    study = _get_study(study_id)
    _require_status(study, {"in_review"}, "review this report")
    if user["email"] != study["review"]["reviewer_email"]:
        raise HTTPException(status_code=403, detail=f"Only the assigned reviewer ({study['review']['reviewer_name']}) can review this revision.")
    if roles.REVIEWERS.configured and roles.reviewer(user["email"]) is None:
        # Taken out of the reviewer group after being assigned -- the author picks another reviewer.
        raise HTTPException(status_code=403, detail="You're no longer in the reviewer group, so you can't decide on this review.")
    comment = body.comment.strip()
    if body.decision == "changes" and not comment and not db.count_open_threads(study_id, study["revision"]):
        raise HTTPException(status_code=422, detail="Describe the changes you're asking for, or comment on the document.")
    db.decide_revision(study_id, study["revision"], approved=body.decision == "approve", comment=comment)
    return db.get_study(study_id)


@router.post("/{study_id}/revisions")
def start_revision(study_id: str, user: dict = Depends(get_current_user)):
    """Starts the next revision from the last submitted document: its Ref. gets the new Rev
    number, the person starting it becomes Author, and Check and Approval are cleared until it's submitted."""
    study = _get_study(study_id)
    _require_edit(study, user)
    _require_status(study, {"approved", "changes_requested"}, "start a new revision")
    revision = study["revision"] + 1
    previous = db.revision_docx_path(study_id, study["revision"]).read_bytes()
    report = study["report"]
    header = report.get("header") or {}
    ref = bump_ref_revision(title_block_values(previous).get("Ref.") or header.get("ref") or "", revision)
    fields = {"Ref.": ref, "Date": today_label(), "Author": user["name"], "Check": "", "Approval": ""}
    docx = update_title_block(previous, fields)
    report = {**report, "header": {**header, "ref": ref, "date": fields["Date"]}}
    db.start_revision(study_id, revision, docx=docx, report=report)
    return db.get_study(study_id)


@router.get("/{study_id}/revisions/{revision}/docx")
def get_revision_docx(study_id: str, revision: int):
    """A submitted revision's document, exactly as it was submitted."""
    _get_study(study_id)
    path = db.revision_docx_path(study_id, revision)
    if not path.exists():
        raise HTTPException(status_code=404, detail=f"Revision {revision} hasn't been submitted.")
    return FileResponse(
        path,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Cache-Control": "no-store"},
    )


# ---- Review comments ----
#
# Threads on a submitted revision (see db.py's review_comments). New threads go on the
# revision while it's in review; replies and resolving carry on after the decision, while
# the author works through them in the next revision. Taking part is for the revision's
# reviewer and the study's editors; reading is for everyone, like the rest of a study.


def _revision_record(study: dict, revision: int) -> dict:
    """The submission record of one revision (see db.get_study's "revisions"), or a 404."""
    record = next((r for r in study["revisions"] if r["revision"] == revision), None)
    if record is None:
        raise HTTPException(status_code=404, detail=f"Revision {revision} hasn't been submitted for review.")
    return record


def _require_review_participant(study: dict, record: dict, user: dict):
    """403s unless `user` reviews this revision or can edit the study (admins included)."""
    if user["email"] == record["reviewer_email"] or user["is_admin"] or db.can_edit(study, user["email"]):
        return
    raise HTTPException(status_code=403, detail="Only the reviewer and the people working on this study can comment on its review.")


def _require_open_review(record: dict, action: str):
    """409s once the revision's review is decided: new threads and deletions stop then."""
    if record["status"] != "in_review":
        raise HTTPException(
            status_code=409,
            detail=f"Can't {action}: revision {record['revision']}'s review is closed, so its comments are part of the record.",
        )


@router.get("/{study_id}/revisions/{revision}/comments")
def list_review_comments(study_id: str, revision: int):
    study = _get_study(study_id)
    _revision_record(study, revision)
    return {"comments": db.list_comments(study_id, revision)}


@router.post("/{study_id}/revisions/{revision}/comments/docx")
async def docx_with_review_comments(study_id: str, revision: int, request: Request):
    """The posted .docx with this revision's comment threads in it as Word comments, to rewrite
    the report in Word after its review (docx_comments.py). The document comes from the browser,
    so it's exactly what's on screen -- the frozen revision, or the next revision's draft with
    any unsaved edits."""
    docx = await read_docx_body(request)
    study = _get_study(study_id)
    _revision_record(study, revision)
    comments = db.list_comments(study_id, revision)
    try:
        annotated = await run_in_threadpool(add_review_comments, docx, comments)
    except Exception as exc:  # a .docx python-docx can't read
        raise HTTPException(status_code=422, detail=f"Couldn't add the comments to this document: {exc}")
    return Response(content=annotated, media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")


@router.post("/{study_id}/revisions/{revision}/comments")
def add_review_comment(study_id: str, revision: int, body: CreateCommentRequest, user: dict = Depends(get_current_user)):
    study = _get_study(study_id)
    record = _revision_record(study, revision)
    _require_review_participant(study, record, user)
    text = body.body.strip()
    if not text:
        raise HTTPException(status_code=422, detail="Write a comment first.")
    if body.parent_id:
        parent = db.get_comment(study_id, body.parent_id)
        if parent is None or parent["revision"] != revision:
            raise HTTPException(status_code=404, detail="That comment no longer exists.")
        # Threads are one level deep, like Word's: a reply to a reply joins the same thread.
        return db.add_comment(study_id, revision, author=user, body=text, parent_id=parent["parent_id"] or parent["id"])
    _require_open_review(record, "add a comment")
    return db.add_comment(
        study_id,
        revision,
        author=user,
        body=text,
        para_id=body.para_id.upper() if body.para_id else None,
        quote=body.quote.strip(),
    )


@router.patch("/{study_id}/comments/{comment_id}")
def update_review_comment(study_id: str, comment_id: str, body: UpdateCommentRequest, user: dict = Depends(get_current_user)):
    """Resolves or reopens a thread."""
    study = _get_study(study_id)
    comment = db.get_comment(study_id, comment_id)
    if comment is None:
        raise HTTPException(status_code=404, detail="That comment no longer exists.")
    if comment["parent_id"]:
        raise HTTPException(status_code=422, detail="Resolve the thread, not a reply in it.")
    _require_review_participant(study, _revision_record(study, comment["revision"]), user)
    return db.set_comment_resolved(comment_id, user if body.resolved else None)


@router.delete("/{study_id}/comments/{comment_id}", status_code=204)
def delete_review_comment(study_id: str, comment_id: str, user: dict = Depends(get_current_user)):
    """Takes back your own comment -- while the review is still open, and nobody has replied."""
    study = _get_study(study_id)
    comment = db.get_comment(study_id, comment_id)
    if comment is None:
        raise HTTPException(status_code=404, detail="That comment no longer exists.")
    if comment["author_email"] != user["email"]:
        raise HTTPException(status_code=403, detail="You can only delete your own comments.")
    if comment["reply_count"]:
        raise HTTPException(status_code=409, detail="This comment has replies -- resolve it instead.")
    _require_open_review(_revision_record(study, comment["revision"]), "delete a comment")
    db.delete_comment(comment_id)


@router.post("/{study_id}/files")
async def upload_study_file(study_id: str, file: UploadFile, caption: str = Form(""), user: dict = Depends(get_current_user)):
    """Uploads one piece of supporting material (photo, deck drawing, reference document)
    for UploadMaterial.tsx's list -- ReportGeneration.tsx later picks specific uploads by
    id to fill the report's figure slots."""
    study = _get_study(study_id)
    _require_edit(study, user)
    _require_status(study, _MATERIAL_STATUSES, "change the supporting material")
    if not file.filename:
        raise HTTPException(status_code=422, detail="No file given.")
    ext = Path(file.filename).suffix.lower()
    if ext in _IMAGE_EXTS:
        kind = "image"
    elif ext in _DOCUMENT_EXTS:
        kind = "document"
    else:
        raise HTTPException(status_code=422, detail=f"Unsupported file type '{ext}'.")
    file_id = uuid.uuid4().hex[:12]
    dest = db.STUDY_FILES_DIR / f"{file_id}{ext}"
    dest.write_bytes(await file.read())
    return db.add_study_file(study_id, filename=dest.name, original_filename=file.filename, kind=kind, caption=caption)


@router.patch("/{study_id}/files/{file_id}")
def update_study_file(study_id: str, file_id: str, body: UpdateStudyFileRequest, user: dict = Depends(get_current_user)):
    study = _get_study(study_id)
    _require_edit(study, user)
    _require_status(study, _MATERIAL_STATUSES, "change the supporting material")
    updated = db.update_study_file(study_id, file_id, caption=body.caption, sort_order=body.sort_order)
    if updated is None:
        raise HTTPException(status_code=404, detail="File not found")
    return updated


@router.delete("/{study_id}/files/{file_id}", status_code=204)
def delete_study_file(study_id: str, file_id: str, user: dict = Depends(get_current_user)):
    study = _get_study(study_id)
    _require_edit(study, user)
    _require_status(study, _MATERIAL_STATUSES, "change the supporting material")
    filename = db.delete_study_file(study_id, file_id)
    if filename is None:
        raise HTTPException(status_code=404, detail="File not found")
    (db.STUDY_FILES_DIR / filename).unlink(missing_ok=True)
