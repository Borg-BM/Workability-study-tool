"""Sign-in through Barge Master's Authentik SSO, and the Barge Master API access that comes
with it.

PyBM's own login (PyBM.marine.tools.api.oauth_session) is built for a desktop: it opens a
browser on the machine running Python, catches the redirect on a localhost port, and caches
one person's token in ~/.pybm. On a server none of that works -- there's no browser, the
user's browser can't reach the server's localhost, and one cached token would make every
request that one person. So this app runs the same OAuth2 authorization-code + PKCE flow
itself, as an ordinary web login:

  /api/auth/login  -> redirect to Authentik (state + PKCE verifier kept server-side)
  /callback        -> exchange the code for the user's tokens, look up who they are, and
                      start a session: an HttpOnly cookie, with the tokens kept server-side
                      in db's sessions table

Every API route then knows who's asking (identity.get_current_user), and PyBM's RAO calls
are made with that user's own access token (pybm_api), renewed with the refresh token when
Authentik issued one. The path is /callback because that's what PyBM's Authentik client
already accepts on localhost; a server needs its own https://<host>/callback added to that
client (see backend/README.md).
"""

import base64
import hashlib
import html
import logging
import os
import secrets
import threading
import time
from collections.abc import Callable
from urllib.parse import urlencode, urlparse

import requests
from fastapi import Cookie, Depends, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse

from . import db

log = logging.getLogger("uvicorn.error")

SESSION_COOKIE = "wst_session"
LOGIN_COOKIE = "wst_login"
_SESSION_TTL_S = float(os.getenv("SESSION_HOURS") or 12) * 3600
_LOGIN_TTL_S = 600
# Renew a little before the access token runs out, so it can't expire mid-request.
_REFRESH_MARGIN_S = 60
# A token this fresh being rejected isn't an expiry, and sending the user to sign in again
# would just loop -- so it's reported as an API error instead (see _check_api_response).
_FRESH_TOKEN_S = 120
# offline_access asks for a refresh token; Authentik leaves it out if the client isn't set
# up for it, and then an expired access token means signing in again.
_SCOPES = "openid profile email offline_access"


class LoginRequired(Exception):
    """The user has to sign in (again). main.py answers it with a 401, which the frontend
    turns into a redirect to /api/auth/login."""


# ---- Authentik client ----

_config: dict | None = None


def _oauth() -> dict:
    """Client id and endpoints, from the same place PyBM's own login gets them: the API's
    public /.well-known/oauth-config, so a client change on the API side reaches this app
    too. AUTHENTIK_CLIENT_ID / AUTHENTIK_CLIENT_SECRET / AUTHENTIK_URL override it for a
    dedicated client. Cached once fetched; PyBM's built-in defaults if the API is down."""
    global _config
    if _config is not None:
        return _config
    # Imported here, not at the top: importing PyBM loads matplotlib.pyplot, which has to
    # wait for pybm_service's matplotlib.use("Agg").
    from PyBM.marine.tools.api.oauth_session import API_BASE_URL, AUTHENTIK_URL, CLIENT_ID

    remote = {}
    try:
        r = requests.get(f"{API_BASE_URL}/.well-known/oauth-config", timeout=5)
        if r.ok:
            remote = r.json()
    except (requests.RequestException, ValueError):
        pass
    auth_url = (os.getenv("AUTHENTIK_URL") or remote.get("auth_url") or AUTHENTIK_URL).rstrip("/")
    config = {
        "base_url": auth_url,
        "client_id": os.getenv("AUTHENTIK_CLIENT_ID") or remote.get("client_id") or CLIENT_ID,
        "client_secret": os.getenv("AUTHENTIK_CLIENT_SECRET") or None,
        "authorize_url": f"{auth_url}/application/o/authorize/",
        "token_url": f"{auth_url}/application/o/token/",
        "userinfo_url": f"{auth_url}/application/o/userinfo/",
        # Authentik's default invalidation flow -- ends the SSO session itself, not just ours.
        "logout_url": f"{auth_url}/flows/-/default/invalidation/",
        "auth_host": urlparse(auth_url).netloc,
    }
    if remote:
        _config = config
    return config


def authentik_url() -> str:
    """Authentik's own address (its API lives under /api/v3) -- see roles.py."""
    return _oauth()["base_url"]


def _token_request(data: dict) -> dict:
    cfg = _oauth()
    data = {**data, "client_id": cfg["client_id"]}
    if cfg["client_secret"]:
        data["client_secret"] = cfg["client_secret"]
    r = requests.post(cfg["token_url"], data=data, timeout=15)
    if not r.ok:
        try:
            body = r.json()
            reason = body.get("error_description") or body.get("error") or ""
        except ValueError:
            reason = ""
        raise RuntimeError(f"Authentik refused the token request (HTTP {r.status_code}){': ' + reason if reason else ''}")
    token = r.json()
    if "access_token" not in token:
        raise RuntimeError("Authentik's token response had no access token.")
    return token


def _token_expiry(token: dict) -> float:
    expires_in = token.get("expires_in")
    return time.time() + (float(expires_in) if expires_in else _SESSION_TTL_S)


# ---- Signing in and out ----

# Sign-ins between /api/auth/login and /callback: state -> (PKCE verifier, redirect_uri,
# where to go afterwards, started at). In memory -- a restart mid-sign-in just means
# clicking through again.
_pending: dict[str, tuple[str, str, str, float]] = {}
_pending_lock = threading.Lock()


def _public_base(request: Request) -> str:
    """This app's address as the browser sees it: PUBLIC_URL when set (a server behind a
    proxy), else taken from the request -- nginx and Vite's dev proxy both pass the original
    Host on."""
    return (os.getenv("PUBLIC_URL") or str(request.base_url)).rstrip("/")


def _safe_next(path: str | None) -> str:
    # Only a path on this site -- never an absolute or protocol-relative URL (open redirect).
    if not path or not path.startswith("/") or path.startswith("//") or "\\" in path:
        return "/"
    return path


def _hash(session_id: str) -> str:
    return hashlib.sha256(session_id.encode()).hexdigest()


def start_login(request: Request, next_path: str | None) -> RedirectResponse:
    cfg = _oauth()
    redirect_uri = f"{_public_base(request)}/callback"
    state = secrets.token_urlsafe(32)
    verifier = secrets.token_urlsafe(64)
    challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).decode().rstrip("=")
    now = time.time()
    with _pending_lock:
        for stale in [k for k, v in _pending.items() if now - v[3] > _LOGIN_TTL_S]:
            del _pending[stale]
        _pending[state] = (verifier, redirect_uri, _safe_next(next_path), now)
    params = {
        "client_id": cfg["client_id"],
        "response_type": "code",
        "redirect_uri": redirect_uri,
        "scope": _SCOPES,
        "state": state,
        "code_challenge": challenge,
        "code_challenge_method": "S256",
    }
    response = RedirectResponse(f"{cfg['authorize_url']}?{urlencode(params)}", status_code=302)
    # Ties the callback to this browser, so a sign-in started elsewhere can't be completed here.
    response.set_cookie(
        LOGIN_COOKIE, state, max_age=_LOGIN_TTL_S, httponly=True, samesite="lax", secure=redirect_uri.startswith("https://")
    )
    return response


def _login_failed(message: str) -> HTMLResponse:
    page = (
        '<html><body style="font-family:Arial;text-align:center;padding:50px">'
        '<h1 style="color:#051642">Sign-in failed</h1>'
        f"<p>{html.escape(message)}</p>"
        '<p><a href="/api/auth/login" style="color:#00ADEF">Try again</a></p></body></html>'
    )
    return HTMLResponse(page, status_code=400)


def finish_login(*, code: str, state: str, error: str, error_description: str, login_cookie: str | None):
    if error:
        return _login_failed(f"Authentik reported: {error_description or error}")
    with _pending_lock:
        pending = _pending.pop(state, None) if state else None
    if (
        pending is None
        or not login_cookie
        or not secrets.compare_digest(login_cookie, state)
        or time.time() - pending[3] > _LOGIN_TTL_S
    ):
        return _login_failed("This sign-in expired or was started in another browser.")
    verifier, redirect_uri, next_path, _ = pending

    cfg = _oauth()
    try:
        token = _token_request(
            {"grant_type": "authorization_code", "code": code, "redirect_uri": redirect_uri, "code_verifier": verifier}
        )
        r = requests.get(cfg["userinfo_url"], headers={"Authorization": f"Bearer {token['access_token']}"}, timeout=10)
        r.raise_for_status()
        info = r.json()
    except (requests.RequestException, RuntimeError, ValueError) as exc:
        return _login_failed(f"Couldn't complete sign-in with Authentik: {exc}")
    email = (info.get("email") or "").strip().lower()
    if not email:
        return _login_failed("Your Barge Master account has no email address, which this app identifies people by.")
    name = (info.get("name") or info.get("preferred_username") or email).strip()

    session_id = secrets.token_urlsafe(32)
    db.create_session(
        _hash(session_id),
        email=email,
        name=name,
        access_token=token["access_token"],
        refresh_token=token.get("refresh_token"),
        token_expires_at=_token_expiry(token),
        expires_at=time.time() + _SESSION_TTL_S,
    )
    log.info(
        "Signed in %s (API token valid for %s s, refresh token: %s)",
        email,
        token.get("expires_in", "?"),
        "yes" if token.get("refresh_token") else "no",
    )
    response = RedirectResponse(next_path, status_code=302)
    response.set_cookie(
        SESSION_COOKIE,
        session_id,
        max_age=int(_SESSION_TTL_S),
        httponly=True,
        samesite="lax",
        secure=redirect_uri.startswith("https://"),
    )
    response.delete_cookie(LOGIN_COOKIE)
    return response


def logout(session_id: str | None) -> JSONResponse:
    """Ends this app's session; the frontend then sends the browser to `logout_url` to end
    the Authentik session too (otherwise the next visit would sign straight back in)."""
    if session_id:
        db.delete_session(_hash(session_id))
    response = JSONResponse({"logout_url": _oauth()["logout_url"]})
    response.delete_cookie(SESSION_COOKIE)
    return response


# ---- Sessions ----


def session_from_cookie(session_id: str | None) -> dict | None:
    return db.get_session(_hash(session_id)) if session_id else None


def require_session(session_id: str | None = Cookie(None, alias=SESSION_COOKIE)) -> dict:
    """Route dependency: the signed-in session, or a 401 (LoginRequired) if there isn't one."""
    session = session_from_cookie(session_id)
    if session is None:
        raise LoginRequired("Not signed in.")
    return session


# ---- Barge Master API access for PyBM ----

# What pybm_service hands PyBM's api_calls as `session=`: a zero-argument callable returning
# a requests.Session that carries the signed-in user's access token. A callable rather than
# the session itself, so a request answered from pybm_service's caches never needs a token.
ApiSession = Callable[[], requests.Session]

_refresh_lock = threading.Lock()


def _access_token(id_hash: str) -> tuple[str, float]:
    """The session's access token and when it was issued -- renewed first if it's about to
    run out."""
    with _refresh_lock:
        session = db.get_session(id_hash)
        if session is None:
            raise LoginRequired("Your sign-in has expired.")
        if session["token_expires_at"] - _REFRESH_MARGIN_S > time.time():
            return session["access_token"], session["token_issued_at"]
        if not session["refresh_token"]:
            raise LoginRequired("Your Barge Master API sign-in has expired.")
        try:
            token = _token_request({"grant_type": "refresh_token", "refresh_token": session["refresh_token"]})
        except (requests.RequestException, RuntimeError) as exc:
            raise LoginRequired(f"Couldn't renew your Barge Master API sign-in: {exc}") from exc
        db.update_session_tokens(
            id_hash,
            access_token=token["access_token"],
            # Authentik may rotate the refresh token; keep the old one if it didn't send a new one.
            refresh_token=token.get("refresh_token") or session["refresh_token"],
            token_expires_at=_token_expiry(token),
        )
        return token["access_token"], time.time()


def _check_api_response(response: requests.Response, issued_at: float) -> None:
    """requests response hook: turns the API refusing the token -- a 401, or a redirect to
    Authentik's login -- into LoginRequired, so the user signs in again instead of seeing an
    opaque PyBM error."""
    location = response.headers.get("Location", "") if response.is_redirect else ""
    refused = response.status_code == 401 or (
        response.is_redirect
        and (urlparse(location).netloc == _oauth()["auth_host"] or "/outpost.goauthentik.io/" in location)
    )
    if not refused:
        return
    if time.time() - issued_at < _FRESH_TOKEN_S:
        raise RuntimeError(
            f"the Barge Master API refused a fresh sign-in (HTTP {response.status_code}) -- "
            "this app's Authentik client may not be allowed to use the API"
        )
    raise LoginRequired("The Barge Master API no longer accepts your sign-in.")


def pybm_api(session: dict = Depends(require_session)) -> ApiSession:
    """Route dependency: the signed-in user's Barge Master API access, for pybm_service."""
    id_hash = session["id_hash"]

    def make() -> requests.Session:
        token, issued_at = _access_token(id_hash)
        api = requests.Session()
        api.headers["Authorization"] = f"Bearer {token}"
        api.hooks["response"].append(lambda r, **_: _check_api_response(r, issued_at))
        return api

    return make
