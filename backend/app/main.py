"""FastAPI app entrypoint: wires up the routers, the static file mounts for generated plot
PNGs and uploaded study files, sign-in enforcement (see sso.py), and a startup step that
creates (or updates) the SQLite schema. Run with `python -m uvicorn app.main:app
--port 8000` from the backend/ directory (see backend/README.md).

The frontend is always served from the same origin as this API -- through nginx in Docker,
or Vite's dev proxy (vite.config.ts) -- so there's no CORS: the session cookie is
first-party."""

from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from . import db, sso
from .identity import get_current_user
from .routers import auth, convert, machines, raos, studies


@asynccontextmanager
async def lifespan(_app: FastAPI):
    db.init_db()
    yield


app = FastAPI(title="Workability Study Tool API", lifespan=lifespan)


@app.exception_handler(sso.LoginRequired)
async def login_required(request: Request, exc: sso.LoginRequired):
    # The frontend answers any 401 by sending the browser to /api/auth/login.
    return JSONResponse({"detail": str(exc) or "Not signed in."}, status_code=401)


# Plots and uploads are served straight from disk (below), outside any route's
# dependencies -- so they're checked against the session cookie here instead.
_SIGNED_IN_FILES = ("/plots/", "/study-files/")


@app.middleware("http")
async def require_sign_in_for_files(request: Request, call_next):
    if request.url.path.startswith(_SIGNED_IN_FILES) and sso.session_from_cookie(
        request.cookies.get(sso.SESSION_COOKIE)
    ) is None:
        return JSONResponse({"detail": "Not signed in."}, status_code=401)
    return await call_next(request)


# Everything but signing in and the health check needs a signed-in user -- including the
# read-only routes that don't otherwise care who's asking.
_signed_in = [Depends(get_current_user)]

app.include_router(auth.router)
app.include_router(auth.callback_router)
app.include_router(raos.router, dependencies=_signed_in)
app.include_router(machines.router, dependencies=_signed_in)
app.include_router(studies.router, dependencies=_signed_in)
app.include_router(convert.router, dependencies=_signed_in)

# Every version's polar plot PNG (written by studies.create_version) is served straight
# from disk at /plots/<filename> -- ApiVersion.plot_url in the frontend just points an
# <img> tag at this, no separate "get plot" endpoint needed.
app.mount("/plots", StaticFiles(directory=str(db.PLOTS_DIR)), name="plots")

# Supporting-material uploads (photos, deck drawings, reference documents -- see
# routers/studies.py's upload_study_file) are served the same way, at /study-files/<filename>.
app.mount("/study-files", StaticFiles(directory=str(db.STUDY_FILES_DIR)), name="study-files")


@app.get("/api/health")
def health():
    # Not called by the frontend (StudiesDashboard.tsx's error banner just reacts to
    # /api/studies failing) -- this is purely for a quick `curl` check that the server has
    # finished starting up after a restart, and the Docker healthcheck.
    return {"status": "ok"}
