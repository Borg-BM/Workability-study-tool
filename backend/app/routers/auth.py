"""Signing in and out (Authentik SSO, see sso.py), plus "who am I, and am I an admin" -- the
frontend calls /api/me on load so it can show admin-only UI (the Manage button on studies
the user doesn't own, see StudiesDashboard.tsx/StudyBuilder.tsx) without needing its own
copy of the admin list. That is a UI convenience only -- every actual permission check
still happens server-side (see routers/studies.py's _require_edit/_require_owner).
"""

from fastapi import APIRouter, Cookie, Depends, Request

from .. import roles, sso
from ..identity import get_current_user

router = APIRouter(prefix="/api", tags=["auth"])


@router.get("/me")
def me(user: dict = Depends(get_current_user)):
    return user


@router.get("/reviewers", dependencies=[Depends(get_current_user)])
def reviewers():
    """Who a report can be submitted to for review: the Authentik reviewer group's members (see
    roles.py). `restricted` is false when no group is configured -- then any colleague can be
    entered by email and name. The review routes enforce the group themselves (routers/studies.py)."""
    if not roles.REVIEWERS.configured:
        return {"restricted": False, "reviewers": []}
    return {"restricted": True, "reviewers": roles.reviewers()}


@router.get("/auth/login")
def login(request: Request, next: str = "/"):
    return sso.start_login(request, next)


@router.post("/auth/logout")
def logout(session_id: str | None = Cookie(None, alias=sso.SESSION_COOKIE)):
    return sso.logout(session_id)


# Authentik's redirect back after sign-in. Outside /api because /callback is the path PyBM's
# Authentik client accepts (see sso.py's module docstring).
callback_router = APIRouter(tags=["auth"])


@callback_router.get("/callback")
def callback(
    code: str = "",
    state: str = "",
    error: str = "",
    error_description: str = "",
    login_cookie: str | None = Cookie(None, alias=sso.LOGIN_COOKIE),
):
    return sso.finish_login(
        code=code, state=state, error=error, error_description=error_description, login_cookie=login_cookie
    )
