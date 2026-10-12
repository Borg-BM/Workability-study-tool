"""Read-only browsing of PyBM's RAO database -- used by StudySetup.tsx's vessel/loadcase
picker, before a study's RAO is locked in via PUT /api/studies/{id}/rao. Everything here
is a thin passthrough to pybm_service, with any failure reported as 502 (upstream/PyBM
problem) rather than 500 -- these calls hit PyBM's own API layer (api_calls), which is
effectively an external dependency from this app's point of view even though it may be
running locally. The one exception is the user's sign-in no longer being accepted
(LoginRequired), which main.py turns into a 401 so the frontend signs them in again."""

from contextlib import contextmanager

from fastapi import APIRouter, Depends, HTTPException

from .. import pybm_service
from ..sso import ApiSession, LoginRequired, pybm_api

router = APIRouter(prefix="/api/raos", tags=["raos"])


@contextmanager
def _upstream(failure: str):
    """Reports any failure inside as a 502 starting with `failure` -- except LoginRequired,
    which main.py turns into the 401 that sends the user to sign in again."""
    try:
        yield
    except LoginRequired:
        raise
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"{failure}: {exc}") from exc


@router.get("")
def get_raos(api: ApiSession = Depends(pybm_api)):
    """All vessels with an RAO on file -- populates the searchable vessel list."""
    with _upstream("Could not reach the RAO database"):
        return {"vessels": pybm_service.list_vessels(api)}


@router.get("/{vessel}/loadcases")
def get_loadcases(vessel: str, api: ApiSession = Depends(pybm_api)):
    """Loadcases available for one vessel (e.g. FULLLOAD/LOWLOAD/TRANSFER) -- shown as
    chips once a vessel is picked, since a study needs one specific (vessel, loadcase) pair."""
    with _upstream(f"Could not load loadcases for {vessel}"):
        return {"loadcases": pybm_service.list_loadcases(vessel, api)}


@router.get("/{vessel}/{loadcase}/metadata")
def get_metadata(vessel: str, loadcase: str, api: ApiSession = Depends(pybm_api)):
    """Descriptive attributes for one RAO. StudyBuilder.tsx fetches this once a study's
    RAO is set and uses its presence to gate a small "RAO: vessel/loadcase" caption in the
    empty-result placeholder -- it's not fed into the calculation itself, which only needs
    (vessel, loadcase) to look up the actual MotionRAO. It does warm the RAO cache, though,
    so the first calculation doesn't have to fetch it."""
    with _upstream(f"Could not load RAO {vessel}/{loadcase}"):
        return pybm_service.get_rao_metadata(vessel, loadcase, api)
