"""Who's asking: the user signed in through Authentik SSO (see sso.py). Every route that
needs to know depends on get_current_user(), and the ownership/permission logic built on
top of it (routers/studies.py's _require_edit/_require_owner) keys off `email`. is_admin is
membership of the Authentik admin group (see roles.py).
"""

from fastapi import Depends

from . import roles, sso


def get_current_user(session: dict = Depends(sso.require_session)) -> dict:
    return {"email": session["email"], "name": session["name"], "is_admin": roles.is_admin(session["email"])}
