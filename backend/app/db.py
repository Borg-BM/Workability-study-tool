"""SQLite persistence -- studies, their calculation versions, supporting files, report
revisions and review comments, and sign-in sessions -- plus the on-disk folders for the
files that go with them (plot PNGs, uploads, report .docx files).

Data model: a *study* is one vessel/loadcase RAO plus metadata (name, project, status).
A *version* is one immutable calculation run under a study -- its machine/environment
params, the result, and a plot PNG filename. Studies accumulate versions as the user
tweaks parameters and re-generates; at most one version per study can be "approved".
Most functions here are thin CRUD wrappers, but two real invariants live directly in
this module's SQL rather than in the router layer (there's no ORM to hang them on
instead): set_study_rao() refuses to change an already-set vessel/loadcase, and
approve_version() clears any other version's approved flag before setting the new one.

One SQLite file, one process: no connection pooling and no migrations framework (see
init_db for the additive column migrations).
"""

import json
import sqlite3
import time
import uuid
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path

from .docx_anchors import ensure_paragraph_ids

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
PLOTS_DIR = DATA_DIR / "plots"
PLOTS_DIR.mkdir(parents=True, exist_ok=True)
HINDCAST_DIR = DATA_DIR / "hindcast"
HINDCAST_DIR.mkdir(parents=True, exist_ok=True)
STUDY_FILES_DIR = DATA_DIR / "study_files"
STUDY_FILES_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR = DATA_DIR / "reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = DATA_DIR / "studies.sqlite3"

SCHEMA = """
CREATE TABLE IF NOT EXISTS studies (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    vessel TEXT NOT NULL DEFAULT '',
    loadcase TEXT NOT NULL DEFAULT '',
    system_type TEXT NOT NULL DEFAULT '',
    project TEXT NOT NULL DEFAULT '',
    status TEXT NOT NULL DEFAULT 'draft',
    vessel_length_m REAL,
    vessel_breadth_m REAL,
    vessel_depth_m REAL,
    vessel_draft_m REAL,
    report_json TEXT NOT NULL DEFAULT '{}',
    revision INTEGER NOT NULL DEFAULT 0,
    report_version_id TEXT,
    owner_email TEXT NOT NULL DEFAULT '',
    owner_name TEXT NOT NULL DEFAULT '',
    archived INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

-- Per-study edit grants: the owner can let specific other people edit (add versions,
-- approve, write the report, upload material) without handing over ownership. Read access
-- itself is universal (every study is visible to everyone, see list_studies()) -- this
-- table only gates *writes*. Keyed on email, not a user id: there's no users table --
-- people are their Authentik account, identified by email (see identity.py).
CREATE TABLE IF NOT EXISTS study_collaborators (
    id TEXT PRIMARY KEY,
    study_id TEXT NOT NULL REFERENCES studies(id) ON DELETE CASCADE,
    email TEXT NOT NULL,
    created_at TEXT NOT NULL,
    UNIQUE(study_id, email)
);

CREATE TABLE IF NOT EXISTS versions (
    id TEXT PRIMARY KEY,
    study_id TEXT NOT NULL REFERENCES studies(id) ON DELETE CASCADE,
    label TEXT NOT NULL,
    diff_summary TEXT NOT NULL DEFAULT '',
    params_json TEXT NOT NULL,
    result_json TEXT NOT NULL,
    plot_filename TEXT,
    approved INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL
);

-- Supporting material for the report: photos, deck drawings, reference documents (see
-- routers/studies.py's file upload endpoints, UploadMaterial.tsx). ReportGeneration.tsx
-- picks specific rows here to fill the report's figure slots (concept drawing, axis
-- convention diagram, appendix images) by id -- see studies.report_json.
CREATE TABLE IF NOT EXISTS study_files (
    id TEXT PRIMARY KEY,
    study_id TEXT NOT NULL REFERENCES studies(id) ON DELETE CASCADE,
    filename TEXT NOT NULL,
    original_filename TEXT NOT NULL,
    kind TEXT NOT NULL DEFAULT 'document',
    caption TEXT NOT NULL DEFAULT '',
    sort_order INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL
);

-- One row per report revision submitted for review: who submitted it, who was asked to
-- review it, the outcome, and a frozen copy of the document as submitted (docx_filename, in
-- REPORTS_DIR). A submitted revision is never edited again -- changes go into the next one.
CREATE TABLE IF NOT EXISTS report_revisions (
    id TEXT PRIMARY KEY,
    study_id TEXT NOT NULL REFERENCES studies(id) ON DELETE CASCADE,
    revision INTEGER NOT NULL,
    author_email TEXT NOT NULL,
    author_name TEXT NOT NULL,
    reviewer_email TEXT NOT NULL,
    reviewer_name TEXT NOT NULL,
    status TEXT NOT NULL,
    comment TEXT NOT NULL DEFAULT '',
    docx_filename TEXT NOT NULL,
    submitted_at TEXT NOT NULL,
    decided_at TEXT,
    UNIQUE(study_id, revision)
);

-- Review comments on a submitted report revision (routers/studies.py, ReviewComments.tsx).
-- A thread is a top-level comment, optionally anchored to the text it's about -- the
-- paragraph's w14:paraId (see docx_anchors.py) plus the quoted text -- and its replies, whose
-- parent_id is the thread's top-level comment. Threads are resolved as a whole, so
-- resolved_at is only ever set on a top-level comment.
CREATE TABLE IF NOT EXISTS review_comments (
    id TEXT PRIMARY KEY,
    study_id TEXT NOT NULL REFERENCES studies(id) ON DELETE CASCADE,
    revision INTEGER NOT NULL,
    parent_id TEXT REFERENCES review_comments(id) ON DELETE CASCADE,
    author_email TEXT NOT NULL,
    author_name TEXT NOT NULL,
    body TEXT NOT NULL,
    para_id TEXT,
    quote TEXT NOT NULL DEFAULT '',
    resolved_at TEXT,
    resolved_by_name TEXT,
    created_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS review_comments_by_revision ON review_comments (study_id, revision);

-- Signed-in browser sessions (see sso.py). The cookie carries a random id; only its SHA-256
-- is stored here. The Authentik tokens are the user's own, used for PyBM's calls to the
-- Barge Master API on their behalf. Times are Unix seconds.
CREATE TABLE IF NOT EXISTS sessions (
    id_hash TEXT PRIMARY KEY,
    email TEXT NOT NULL,
    name TEXT NOT NULL,
    access_token TEXT NOT NULL,
    refresh_token TEXT,
    token_issued_at REAL NOT NULL,
    token_expires_at REAL NOT NULL,
    expires_at REAL NOT NULL
);
"""

# A study's status is its place in the workflow, and decides what can still be changed:
#   draft / in_progress  -- building the study (calculations); nothing approved yet
#   reporting            -- a result is approved and locked; supporting material and the
#                           report are being written
#   in_review            -- the current revision was submitted to a reviewer; all locked
#   approved / changes_requested -- the reviewer's decision; still locked, further changes
#                           need a new revision (start_revision)
BUILD_STATUSES = {"draft", "in_progress"}
REVIEW_STATUSES = {"in_review", "approved", "changes_requested"}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def new_id() -> str:
    return uuid.uuid4().hex[:12]


@contextmanager
def get_conn():
    """One connection per call, auto-committed on success. `row_factory = sqlite3.Row`
    lets the _*_row_to_dict() helpers below index rows by column name instead of position.
    Foreign keys are off by default in SQLite -- turned on per-connection so the versions
    table's ON DELETE CASCADE actually fires when a study is deleted."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


# Columns added to `studies` after the first databases were made, as (name, definition) --
# CREATE TABLE IF NOT EXISTS leaves an existing table as it is, so init_db adds them.
_ADDED_STUDY_COLUMNS = (
    ("loadcase", "TEXT NOT NULL DEFAULT ''"),
    ("system_type", "TEXT NOT NULL DEFAULT ''"),
    ("report_json", "TEXT NOT NULL DEFAULT '{}'"),
    ("owner_email", "TEXT NOT NULL DEFAULT ''"),
    ("owner_name", "TEXT NOT NULL DEFAULT ''"),
    ("archived", "INTEGER NOT NULL DEFAULT 0"),
    ("vessel_length_m", "REAL"),
    ("vessel_breadth_m", "REAL"),
    ("vessel_depth_m", "REAL"),
    ("vessel_draft_m", "REAL"),
    ("revision", "INTEGER NOT NULL DEFAULT 0"),
    ("report_version_id", "TEXT"),
)


def init_db():
    """Creates the schema if it doesn't exist, then adds any of _ADDED_STUDY_COLUMNS an
    older database is missing. Additive only: it can't rename or drop columns."""
    with get_conn() as conn:
        conn.executescript(SCHEMA)
        existing_cols = {row["name"] for row in conn.execute("PRAGMA table_info(studies)")}
        for name, definition in _ADDED_STUDY_COLUMNS:
            if name not in existing_cols:
                conn.execute(f"ALTER TABLE studies ADD COLUMN {name} {definition}")
        if "revision" not in existing_cols:
            # Before the review workflow, 'approved' meant "a calculation result is approved"
            # and 'sent' was bookkeeping only -- both are now the reporting stage.
            conn.execute("UPDATE studies SET status = 'reporting' WHERE status IN ('approved', 'sent')")


def _study_row_to_dict(row: sqlite3.Row) -> dict:
    return {
        "id": row["id"],
        "name": row["name"],
        "vessel": row["vessel"],
        "loadcase": row["loadcase"],
        "system_type": row["system_type"],
        "project": row["project"],
        "status": row["status"],
        "vessel_length_m": row["vessel_length_m"],
        "vessel_breadth_m": row["vessel_breadth_m"],
        "vessel_depth_m": row["vessel_depth_m"],
        "vessel_draft_m": row["vessel_draft_m"],
        "report": json.loads(row["report_json"] or "{}"),
        "revision": row["revision"],
        # The approved version the current report document was generated from, so the
        # frontend can warn when the approval has moved on since.
        "report_version_id": row["report_version_id"],
        "owner_email": row["owner_email"],
        "owner_name": row["owner_name"],
        "archived": bool(row["archived"]),
        "created_at": row["created_at"],
        "updated_at": row["updated_at"],
    }


def _study_file_row_to_dict(row: sqlite3.Row) -> dict:
    return {
        "id": row["id"],
        "study_id": row["study_id"],
        "filename": row["filename"],
        "original_filename": row["original_filename"],
        "kind": row["kind"],
        "caption": row["caption"],
        "sort_order": row["sort_order"],
        "url": f"/study-files/{row['filename']}",
        "created_at": row["created_at"],
    }


def _version_row_to_dict(row: sqlite3.Row) -> dict:
    # params/result are stored as opaque JSON text columns (params_json/result_json) since
    # their shape is whatever pybm_service.run_calculation() and the CreateVersionRequest
    # schema produce -- no need for a fixed relational shape for data that's only ever
    # read back out whole, never queried/filtered on.
    return {
        "id": row["id"],
        "study_id": row["study_id"],
        "label": row["label"],
        "diff_summary": row["diff_summary"],
        "params": json.loads(row["params_json"]),
        "result": json.loads(row["result_json"]),
        "plot_url": f"/plots/{row['plot_filename']}" if row["plot_filename"] else None,
        "approved": bool(row["approved"]),
        "created_at": row["created_at"],
    }


def _revision_row_to_dict(row: sqlite3.Row) -> dict:
    return {
        "revision": row["revision"],
        "author_email": row["author_email"],
        "author_name": row["author_name"],
        "reviewer_email": row["reviewer_email"],
        "reviewer_name": row["reviewer_name"],
        "status": row["status"],
        "comment": row["comment"],
        "submitted_at": row["submitted_at"],
        "decided_at": row["decided_at"],
    }


def _current_review(conn: sqlite3.Connection, study: dict) -> dict | None:
    """The submission record of the study's current revision -- None until it's been submitted."""
    row = conn.execute(
        "SELECT * FROM report_revisions WHERE study_id = ? AND revision = ?", (study["id"], study["revision"])
    ).fetchone()
    return _revision_row_to_dict(row) if row else None


def _collaborator_emails(conn: sqlite3.Connection, study_id: str) -> list[str]:
    return [r["email"] for r in conn.execute("SELECT email FROM study_collaborators WHERE study_id = ? ORDER BY created_at ASC", (study_id,))]


def list_studies() -> list[dict]:
    """Every study is visible to everyone (see is_owner()/can_edit() for where the real
    permission line actually is -- it's on writes, not reads) -- StudiesDashboard.tsx
    builds its "My Studies" vs "All Studies" tabs by filtering this same list client-side
    on owner_email/collaborators rather than two separate endpoints.

    Three queries in all (not two more per study): the studies, every collaborator, and
    every study's current-revision submission."""
    with get_conn() as conn:
        studies = [_study_row_to_dict(r) for r in conn.execute("SELECT * FROM studies ORDER BY updated_at DESC")]
        collaborators: dict[str, list[str]] = {}
        for r in conn.execute("SELECT study_id, email FROM study_collaborators ORDER BY created_at ASC"):
            collaborators.setdefault(r["study_id"], []).append(r["email"])
        reviews = {
            r["study_id"]: _revision_row_to_dict(r)
            for r in conn.execute(
                "SELECT rr.* FROM report_revisions rr "
                "JOIN studies s ON s.id = rr.study_id AND s.revision = rr.revision"
            )
        }
    for study in studies:
        study["collaborators"] = collaborators.get(study["id"], [])
        study["review"] = reviews.get(study["id"])
    return studies


def count_studies() -> int:
    with get_conn() as conn:
        return conn.execute("SELECT COUNT(*) AS n FROM studies").fetchone()["n"]


def create_study(name: str, project: str = "", *, owner_email: str = "", owner_name: str = "") -> dict:
    study_id = new_id()
    now = _now()
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO studies (id, name, vessel, loadcase, project, status, owner_email, owner_name, created_at, updated_at) "
            "VALUES (?, ?, '', '', ?, 'draft', ?, ?, ?, ?)",
            (study_id, name, project, owner_email, owner_name, now, now),
        )
        row = conn.execute("SELECT * FROM studies WHERE id = ?", (study_id,)).fetchone()
    study = _study_row_to_dict(row)
    study["collaborators"] = []
    return study


def get_study(study_id: str) -> dict | None:
    """Unlike list_studies() (which is the dashboard's flat table view), this eagerly
    loads every version for the study too -- StudyBuilder.tsx needs the full version
    history to populate its version tray and let the user flip between past results."""
    with get_conn() as conn:
        row = conn.execute("SELECT * FROM studies WHERE id = ?", (study_id,)).fetchone()
        if row is None:
            return None
        study = _study_row_to_dict(row)
        versions = conn.execute(
            "SELECT * FROM versions WHERE study_id = ? ORDER BY created_at ASC", (study_id,)
        ).fetchall()
        study["versions"] = [_version_row_to_dict(v) for v in versions]
        files = conn.execute(
            "SELECT * FROM study_files WHERE study_id = ? ORDER BY sort_order ASC", (study_id,)
        ).fetchall()
        study["files"] = [_study_file_row_to_dict(f) for f in files]
        study["collaborators"] = _collaborator_emails(conn, study_id)
        study["has_report_docx"] = report_docx_path(study_id).exists()
        study["review"] = _current_review(conn, study)
        threads = {
            r["revision"]: r
            for r in conn.execute(
                "SELECT revision, COUNT(*) AS total, SUM(resolved_at IS NULL) AS open FROM review_comments "
                "WHERE study_id = ? AND parent_id IS NULL GROUP BY revision",
                (study_id,),
            )
        }
        study["revisions"] = []
        for r in conn.execute("SELECT * FROM report_revisions WHERE study_id = ? ORDER BY revision ASC", (study_id,)):
            counts = threads.get(r["revision"])
            study["revisions"].append(
                {
                    **_revision_row_to_dict(r),
                    "comment_count": counts["total"] if counts else 0,
                    "open_comment_count": counts["open"] if counts else 0,
                }
            )
        return study


def set_study_rao(
    study_id: str,
    vessel: str,
    loadcase: str,
    system_type: str,
    *,
    vessel_length_m: float | None = None,
    vessel_breadth_m: float | None = None,
    vessel_depth_m: float | None = None,
    vessel_draft_m: float | None = None,
) -> dict | None:
    """Fix the study's RAO and system type (and optionally its vessel dimensions). A study
    covers exactly one vessel and one system type, so this only succeeds once -- call
    delete_study and start a new one to change either."""
    with get_conn() as conn:
        row = conn.execute("SELECT vessel FROM studies WHERE id = ?", (study_id,)).fetchone()
        if row is None:
            return None
        if row["vessel"]:
            raise ValueError("This study's RAO is already fixed. Delete the study to pick a different vessel.")
        conn.execute(
            "UPDATE studies SET vessel = ?, loadcase = ?, system_type = ?, vessel_length_m = ?, vessel_breadth_m = ?, "
            "vessel_depth_m = ?, vessel_draft_m = ?, updated_at = ? WHERE id = ?",
            (vessel, loadcase, system_type, vessel_length_m, vessel_breadth_m, vessel_depth_m, vessel_draft_m, _now(), study_id),
        )
        updated = conn.execute("SELECT * FROM studies WHERE id = ?", (study_id,)).fetchone()
    return _study_row_to_dict(updated)


def update_study_meta(study_id: str, *, name: str | None = None, project: str | None = None) -> dict | None:
    fields = ["updated_at = ?"]
    values: list = [_now()]
    if name is not None:
        fields.append("name = ?")
        values.append(name)
    if project is not None:
        fields.append("project = ?")
        values.append(project)
    values.append(study_id)
    with get_conn() as conn:
        conn.execute(f"UPDATE studies SET {', '.join(fields)} WHERE id = ?", values)
        row = conn.execute("SELECT * FROM studies WHERE id = ?", (study_id,)).fetchone()
    return _study_row_to_dict(row) if row else None


def is_owner(study: dict, email: str) -> bool:
    return bool(email) and study["owner_email"] == email


def can_edit(study: dict, email: str) -> bool:
    """Write access: the owner, or anyone the owner has explicitly granted edit rights to
    (see add_collaborator). Read access is separate and universal -- see list_studies().
    Deliberately does NOT fold in admin rights (roles.is_admin) -- admin override is an
    *authorization* decision (see routers/studies.py's _require_edit/_require_owner, the only
    callers that should special-case it), kept separate from "is this person meaningfully
    attached to this study" (which is also what the frontend's canEditStudy() mirrors, given
    is_admin from /api/me)."""
    return is_owner(study, email) or email in study.get("collaborators", [])


def transfer_study_ownership(study_id: str, *, new_owner_email: str, new_owner_name: str) -> dict | None:
    """Reassigns a study to a new owner -- for when someone leaves the company and their
    studies need a new home. Drops the new owner from the collaborator list if they were
    already on it (redundant once they're the owner); does NOT add the old owner as a
    collaborator -- if continued access is wanted, the new owner can grant that explicitly
    via add_collaborator."""
    with get_conn() as conn:
        cur = conn.execute(
            "UPDATE studies SET owner_email = ?, owner_name = ?, updated_at = ? WHERE id = ?",
            (new_owner_email, new_owner_name, _now(), study_id),
        )
        if cur.rowcount == 0:
            return None
        conn.execute(
            "DELETE FROM study_collaborators WHERE study_id = ? AND email = ?", (study_id, new_owner_email)
        )
        row = conn.execute("SELECT * FROM studies WHERE id = ?", (study_id,)).fetchone()
        study = _study_row_to_dict(row)
        study["collaborators"] = _collaborator_emails(conn, study_id)
        return study


def add_collaborator(study_id: str, email: str) -> list[str] | None:
    """Grants `email` edit rights on this study. Idempotent (re-adding an existing
    collaborator is a no-op, not an error) thanks to the UNIQUE(study_id, email) constraint."""
    with get_conn() as conn:
        if conn.execute("SELECT id FROM studies WHERE id = ?", (study_id,)).fetchone() is None:
            return None
        conn.execute(
            "INSERT OR IGNORE INTO study_collaborators (id, study_id, email, created_at) VALUES (?, ?, ?, ?)",
            (new_id(), study_id, email, _now()),
        )
        return _collaborator_emails(conn, study_id)


def remove_collaborator(study_id: str, email: str) -> list[str] | None:
    with get_conn() as conn:
        if conn.execute("SELECT id FROM studies WHERE id = ?", (study_id,)).fetchone() is None:
            return None
        conn.execute("DELETE FROM study_collaborators WHERE study_id = ? AND email = ?", (study_id, email))
        return _collaborator_emails(conn, study_id)


def set_study_archived(study_id: str, archived: bool) -> dict | None:
    """Archiving is purely a display-state flag (see StudiesDashboard.tsx's "Archived" tab)
    -- it doesn't touch calculation data, files, or the report, and is fully reversible."""
    with get_conn() as conn:
        cur = conn.execute(
            "UPDATE studies SET archived = ?, updated_at = ? WHERE id = ?", (1 if archived else 0, _now(), study_id)
        )
        if cur.rowcount == 0:
            return None
        row = conn.execute("SELECT * FROM studies WHERE id = ?", (study_id,)).fetchone()
        study = _study_row_to_dict(row)
        study["collaborators"] = _collaborator_emails(conn, study_id)
        return study


def copy_study(source_study_id: str, *, owner_email: str, owner_name: str) -> dict | None:
    """"Copy to my studies" -- clones the vessel/loadcase/system_type lock-in (and vessel
    dimensions) into a brand-new study owned by the requesting user, so they get their own
    editable version history to iterate in rather than needing edit rights on the
    original. Deliberately does NOT copy versions, report, files, or review history -- those
    belong to the original study's own history, not the copy's fresh start."""
    with get_conn() as conn:
        source = conn.execute("SELECT * FROM studies WHERE id = ?", (source_study_id,)).fetchone()
        if source is None:
            return None
        study_id = new_id()
        now = _now()
        conn.execute(
            "INSERT INTO studies (id, name, vessel, loadcase, system_type, project, status, "
            "vessel_length_m, vessel_breadth_m, vessel_depth_m, vessel_draft_m, owner_email, owner_name, "
            "created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, 'draft', ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                study_id,
                f"Copy of {source['name']}",
                source["vessel"],
                source["loadcase"],
                source["system_type"],
                source["project"],
                source["vessel_length_m"],
                source["vessel_breadth_m"],
                source["vessel_depth_m"],
                source["vessel_draft_m"],
                owner_email,
                owner_name,
                now,
                now,
            ),
        )
        row = conn.execute("SELECT * FROM studies WHERE id = ?", (study_id,)).fetchone()
    study = _study_row_to_dict(row)
    study["collaborators"] = []
    return study


def save_study_report(study_id: str, report: dict) -> dict | None:
    """Overwrites the study's report_json wholesale -- the report document's generation choices
    (header fields, which study_files fill which figure slot), sent as one object rather than a
    partial patch. The document itself is a separate .docx file (see report_docx_path)."""
    with get_conn() as conn:
        cur = conn.execute(
            "UPDATE studies SET report_json = ?, updated_at = ? WHERE id = ?",
            (json.dumps(report), _now(), study_id),
        )
        if cur.rowcount == 0:
            return None
    return report


def record_report_generated(study_id: str, version_id: str | None):
    with get_conn() as conn:
        conn.execute("UPDATE studies SET report_version_id = ? WHERE id = ?", (version_id, study_id))


def revision_docx_path(study_id: str, revision: int) -> Path:
    return REPORTS_DIR / f"{study_id}_rev{revision}.docx"


def submit_revision(study_id: str, revision: int, *, author: dict, reviewer_email: str, reviewer_name: str, docx: bytes):
    """Freezes `docx` as this revision's submitted document and hands it to the reviewer.
    Every paragraph gets an id first, so review comments can point at it (docx_anchors.py)."""
    docx = ensure_paragraph_ids(docx)
    revision_docx_path(study_id, revision).write_bytes(docx)
    write_report_docx(study_id, docx)
    now = _now()
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO report_revisions (id, study_id, revision, author_email, author_name, reviewer_email, "
            "reviewer_name, status, docx_filename, submitted_at) VALUES (?, ?, ?, ?, ?, ?, ?, 'in_review', ?, ?)",
            (
                new_id(),
                study_id,
                revision,
                author["email"],
                author["name"],
                reviewer_email,
                reviewer_name,
                revision_docx_path(study_id, revision).name,
                now,
            ),
        )
        conn.execute("UPDATE studies SET status = 'in_review', updated_at = ? WHERE id = ?", (now, study_id))


def reassign_reviewer(study_id: str, revision: int, *, reviewer_email: str, reviewer_name: str, docx: bytes):
    docx = ensure_paragraph_ids(docx)  # keeps the ids comments already point at
    revision_docx_path(study_id, revision).write_bytes(docx)
    write_report_docx(study_id, docx)
    with get_conn() as conn:
        conn.execute(
            "UPDATE report_revisions SET reviewer_email = ?, reviewer_name = ? WHERE study_id = ? AND revision = ?",
            (reviewer_email, reviewer_name, study_id, revision),
        )


def decide_revision(study_id: str, revision: int, *, approved: bool, comment: str):
    status = "approved" if approved else "changes_requested"
    now = _now()
    with get_conn() as conn:
        conn.execute(
            "UPDATE report_revisions SET status = ?, comment = ?, decided_at = ? WHERE study_id = ? AND revision = ?",
            (status, comment, now, study_id, revision),
        )
        conn.execute("UPDATE studies SET status = ?, updated_at = ? WHERE id = ?", (status, now, study_id))


def start_revision(study_id: str, revision: int, *, docx: bytes, report: dict):
    """Opens `revision` for editing, starting from `docx` (the previous revision, as submitted)."""
    write_report_docx(study_id, docx)
    with get_conn() as conn:
        conn.execute(
            "UPDATE studies SET revision = ?, status = 'reporting', report_json = ?, updated_at = ? WHERE id = ?",
            (revision, json.dumps(report), _now(), study_id),
        )


def add_study_file(
    study_id: str, *, filename: str, original_filename: str, kind: str, caption: str = ""
) -> dict:
    """Appends one uploaded file (photo, drawing, reference document) to the study's
    supporting-material list, at the end of the current sort order."""
    file_id = new_id()
    now = _now()
    with get_conn() as conn:
        max_order = conn.execute(
            "SELECT COALESCE(MAX(sort_order), -1) AS m FROM study_files WHERE study_id = ?", (study_id,)
        ).fetchone()["m"]
        conn.execute(
            "INSERT INTO study_files (id, study_id, filename, original_filename, kind, caption, sort_order, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (file_id, study_id, filename, original_filename, kind, caption, max_order + 1, now),
        )
        row = conn.execute("SELECT * FROM study_files WHERE id = ?", (file_id,)).fetchone()
    return _study_file_row_to_dict(row)


def update_study_file(
    study_id: str, file_id: str, *, caption: str | None = None, sort_order: int | None = None
) -> dict | None:
    fields = []
    values: list = []
    if caption is not None:
        fields.append("caption = ?")
        values.append(caption)
    if sort_order is not None:
        fields.append("sort_order = ?")
        values.append(sort_order)
    with get_conn() as conn:
        if fields:
            conn.execute(
                f"UPDATE study_files SET {', '.join(fields)} WHERE id = ? AND study_id = ?",
                [*values, file_id, study_id],
            )
        row = conn.execute(
            "SELECT * FROM study_files WHERE id = ? AND study_id = ?", (file_id, study_id)
        ).fetchone()
    return _study_file_row_to_dict(row) if row else None


def delete_study_file(study_id: str, file_id: str) -> str | None:
    """Returns the on-disk filename to remove (the caller unlinks it -- see plot cleanup in
    delete_study() for why this can't happen after the DELETE), or None if not found."""
    with get_conn() as conn:
        row = conn.execute(
            "SELECT filename FROM study_files WHERE id = ? AND study_id = ?", (file_id, study_id)
        ).fetchone()
        if row is None:
            return None
        conn.execute("DELETE FROM study_files WHERE id = ? AND study_id = ?", (file_id, study_id))
    return row["filename"]


def report_docx_path(study_id: str) -> Path:
    return REPORTS_DIR / f"{study_id}.docx"


def write_report_docx(study_id: str, data: bytes):
    """Replaces the study's report document atomically, so a reader never sees a half-written file."""
    path = report_docx_path(study_id)
    tmp = path.with_name(f"{path.name}.{uuid.uuid4().hex[:8]}.tmp")
    tmp.write_bytes(data)
    # Windows refuses to replace a file another process has open (a download in flight, OneDrive syncing).
    for attempt in range(5):
        try:
            tmp.replace(path)
            break
        except PermissionError:
            if attempt == 4:
                tmp.unlink(missing_ok=True)
                raise
            time.sleep(0.2)
    touch_study(study_id)


def touch_study(study_id: str, *, status: str | None = None):
    """Bumps updated_at (so the dashboard's "last edited" column and its sort order stay
    current) and optionally the status -- after a new version, an approval, a report save,
    or reopening the study."""
    fields = ["updated_at = ?"]
    values: list = [_now()]
    if status is not None:
        fields.append("status = ?")
        values.append(status)
    values.append(study_id)
    with get_conn() as conn:
        conn.execute(f"UPDATE studies SET {', '.join(fields)} WHERE id = ?", values)


def delete_study(study_id: str) -> bool:
    """The DB row cascades to its versions and study_files automatically (ON DELETE
    CASCADE + the foreign keys pragma above), but SQLite can't cascade into deleting files
    on disk -- so plot PNGs and uploaded study files have to be collected and removed
    manually here, *before* the DELETE (once the rows are gone, there's no query left that
    could tell us which files belonged to them)."""
    with get_conn() as conn:
        plot_files = [
            r["plot_filename"]
            for r in conn.execute(
                "SELECT plot_filename FROM versions WHERE study_id = ? AND plot_filename IS NOT NULL",
                (study_id,),
            )
        ]
        study_files = [
            r["filename"] for r in conn.execute("SELECT filename FROM study_files WHERE study_id = ?", (study_id,))
        ]
        cur = conn.execute("DELETE FROM studies WHERE id = ?", (study_id,))
        deleted = cur.rowcount > 0
    for filename in plot_files:
        (PLOTS_DIR / filename).unlink(missing_ok=True)
    for filename in study_files:
        (STUDY_FILES_DIR / filename).unlink(missing_ok=True)
    report_docx_path(study_id).unlink(missing_ok=True)
    for snapshot in REPORTS_DIR.glob(f"{study_id}_rev*.docx"):
        snapshot.unlink(missing_ok=True)
    return deleted


def add_version(
    study_id: str,
    *,
    label: str,
    diff_summary: str,
    params: dict,
    result: dict,
    plot_filename: str | None,
) -> dict:
    version_id = new_id()
    now = _now()
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO versions (id, study_id, label, diff_summary, params_json, result_json, "
            "plot_filename, approved, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, 0, ?)",
            (
                version_id,
                study_id,
                label,
                diff_summary,
                json.dumps(params),
                json.dumps(result),
                plot_filename,
                now,
            ),
        )
        row = conn.execute("SELECT * FROM versions WHERE id = ?", (version_id,)).fetchone()
    touch_study(study_id, status="in_progress")
    return _version_row_to_dict(row)


def approve_version(study_id: str, version_id: str) -> dict | None:
    """Clears any existing approval for the study before setting the new one, so exactly
    one version is ever approved at a time -- and moves the study on to the reporting stage,
    which locks the study builder (see routers/studies.py's reopen_study to unlock it)."""
    with get_conn() as conn:
        exists = conn.execute(
            "SELECT id FROM versions WHERE id = ? AND study_id = ?", (version_id, study_id)
        ).fetchone()
        if exists is None:
            return None
        conn.execute("UPDATE versions SET approved = 0 WHERE study_id = ?", (study_id,))
        conn.execute("UPDATE versions SET approved = 1 WHERE id = ?", (version_id,))
        row = conn.execute("SELECT * FROM versions WHERE id = ?", (version_id,)).fetchone()
    touch_study(study_id, status="reporting")
    return _version_row_to_dict(row)


def count_versions(study_id: str) -> int:
    """Used only to compute the next version's label ("v{n}") in studies.create_version --
    not a general-purpose count, so it doesn't need to survive version deletion (there is
    no version-delete endpoint)."""
    with get_conn() as conn:
        row = conn.execute(
            "SELECT COUNT(*) AS n FROM versions WHERE study_id = ?", (study_id,)
        ).fetchone()
        return row["n"]


def last_version_params(study_id: str) -> dict | None:
    """The previous version's raw params dict, fed into diffs.summarize_diff() alongside
    the new version's params so create_version can show what changed between runs."""
    with get_conn() as conn:
        row = conn.execute(
            "SELECT params_json FROM versions WHERE study_id = ? ORDER BY created_at DESC LIMIT 1",
            (study_id,),
        ).fetchone()
        return json.loads(row["params_json"]) if row else None


# ---- Review comments ----


def _comment_row_to_dict(row: sqlite3.Row) -> dict:
    return {
        "id": row["id"],
        "revision": row["revision"],
        "parent_id": row["parent_id"],
        "author_email": row["author_email"],
        "author_name": row["author_name"],
        "body": row["body"],
        "para_id": row["para_id"],
        "quote": row["quote"],
        "resolved_at": row["resolved_at"],
        "resolved_by_name": row["resolved_by_name"],
        "created_at": row["created_at"],
    }


def list_comments(study_id: str, revision: int) -> list[dict]:
    """Every comment and reply on one revision, oldest first -- the frontend builds the threads."""
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM review_comments WHERE study_id = ? AND revision = ? ORDER BY created_at ASC",
            (study_id, revision),
        ).fetchall()
        return [_comment_row_to_dict(r) for r in rows]


def get_comment(study_id: str, comment_id: str) -> dict | None:
    with get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM review_comments WHERE id = ? AND study_id = ?", (comment_id, study_id)
        ).fetchone()
        if row is None:
            return None
        comment = _comment_row_to_dict(row)
        comment["reply_count"] = conn.execute(
            "SELECT COUNT(*) AS n FROM review_comments WHERE parent_id = ?", (comment_id,)
        ).fetchone()["n"]
        return comment


def add_comment(
    study_id: str,
    revision: int,
    *,
    author: dict,
    body: str,
    parent_id: str | None = None,
    para_id: str | None = None,
    quote: str = "",
) -> dict:
    comment_id = new_id()
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO review_comments (id, study_id, revision, parent_id, author_email, author_name, body, "
            "para_id, quote, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (comment_id, study_id, revision, parent_id, author["email"], author["name"], body, para_id, quote, _now()),
        )
        row = conn.execute("SELECT * FROM review_comments WHERE id = ?", (comment_id,)).fetchone()
    return _comment_row_to_dict(row)


def set_comment_resolved(comment_id: str, resolved_by: dict | None) -> dict:
    """Resolves a thread (`resolved_by` is who), or reopens it (None)."""
    with get_conn() as conn:
        conn.execute(
            "UPDATE review_comments SET resolved_at = ?, resolved_by_name = ? WHERE id = ?",
            (_now() if resolved_by else None, resolved_by["name"] if resolved_by else None, comment_id),
        )
        row = conn.execute("SELECT * FROM review_comments WHERE id = ?", (comment_id,)).fetchone()
    return _comment_row_to_dict(row)


def delete_comment(comment_id: str) -> None:
    with get_conn() as conn:
        conn.execute("DELETE FROM review_comments WHERE id = ?", (comment_id,))


def count_open_threads(study_id: str, revision: int) -> int:
    with get_conn() as conn:
        return conn.execute(
            "SELECT COUNT(*) AS n FROM review_comments "
            "WHERE study_id = ? AND revision = ? AND parent_id IS NULL AND resolved_at IS NULL",
            (study_id, revision),
        ).fetchone()["n"]


# ---- Sign-in sessions (see sso.py) ----


def create_session(
    id_hash: str,
    *,
    email: str,
    name: str,
    access_token: str,
    refresh_token: str | None,
    token_expires_at: float,
    expires_at: float,
) -> None:
    now = time.time()
    with get_conn() as conn:
        # Expired rows are only ever cleared here -- signing in is rare enough to piggyback on.
        conn.execute("DELETE FROM sessions WHERE expires_at < ?", (now,))
        conn.execute(
            "INSERT INTO sessions (id_hash, email, name, access_token, refresh_token, token_issued_at, "
            "token_expires_at, expires_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (id_hash, email, name, access_token, refresh_token, now, token_expires_at, expires_at),
        )


def get_session(id_hash: str) -> dict | None:
    """The session for a cookie's hashed id, or None if there's none or it has expired."""
    with get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM sessions WHERE id_hash = ? AND expires_at >= ?", (id_hash, time.time())
        ).fetchone()
        return dict(row) if row else None


def update_session_tokens(id_hash: str, *, access_token: str, refresh_token: str | None, token_expires_at: float) -> None:
    with get_conn() as conn:
        conn.execute(
            "UPDATE sessions SET access_token = ?, refresh_token = ?, token_issued_at = ?, token_expires_at = ? "
            "WHERE id_hash = ?",
            (access_token, refresh_token, time.time(), token_expires_at, id_hash),
        )


def delete_session(id_hash: str) -> None:
    with get_conn() as conn:
        conn.execute("DELETE FROM sessions WHERE id_hash = ?", (id_hash,))
