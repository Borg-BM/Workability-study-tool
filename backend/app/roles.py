"""Roles managed in Authentik: who may check (review) reports, and who are admins -- each the
members of one Authentik group. The app reads a group's members through Authentik's API, with
the API token of a service account that may view users (AUTHENTIK_API_TOKEN); see
backend/README.md, "Reviewers and admins", for setting that up in Authentik.

  REVIEWER_GROUP  its members can be asked to check a report, and decide on it; their Authentik
                  name goes into the report's Check and Approval fields. Unset (a development
                  PC): anyone can be asked, entered by email and name.
  ADMIN_GROUP     its members have owner rights on every study (see routers/studies.py's
                  _require_edit/_require_owner). Unset: the fallback list below.

A group's members are cached for _CACHE_S, so a change in Authentik reaches the app within that
time. A group that can't be read fails closed: no reviewer can be assigned and nobody is an
admin, until Authentik answers again.
"""

import logging
import os
import threading
import time

import requests
from fastapi import HTTPException

from . import sso

log = logging.getLogger("uvicorn.error")

_API_TOKEN = (os.getenv("AUTHENTIK_API_TOKEN") or "").strip()
_CACHE_S = 300
# After a failed lookup, wait this long before asking Authentik again: the admin check runs on
# every request, and those shouldn't each wait for an Authentik that isn't answering.
_RETRY_S = 30

# The admins when ADMIN_GROUP isn't set (a development PC).
_FALLBACK_ADMINS = {"b.swen@barge-master.com"}


class GroupUnavailable(Exception):
    """A group's members couldn't be read from Authentik."""


class Group:
    def __init__(self, name: str | None):
        self.name = (name or "").strip()
        self._lock = threading.Lock()
        self._checked_at = 0.0
        self._members: list[dict] | None = None
        self._error: str | None = None

    @property
    def configured(self) -> bool:
        return bool(self.name)

    def members(self) -> list[dict]:
        """The group's active members as {"email", "name"}, sorted by name. Raises GroupUnavailable."""
        with self._lock:
            age = time.time() - self._checked_at
            if self._members is not None and age < _CACHE_S:
                return self._members
            if self._error is not None and age < _RETRY_S:
                raise GroupUnavailable(self._error)
            self._checked_at = time.time()
            try:
                self._members, self._error = self._fetch(), None
            except GroupUnavailable as exc:
                self._members, self._error = None, str(exc)
                log.warning("Authentik group lookup failed: %s", exc)
                raise
            return self._members

    def member(self, email: str) -> dict | None:
        """This person's entry in the group, or None if they aren't in it. Raises GroupUnavailable."""
        email = email.strip().lower()
        return next((m for m in self.members() if m["email"] == email), None)

    def _fetch(self) -> list[dict]:
        if not _API_TOKEN:
            raise GroupUnavailable(f"group {self.name!r} can't be read: AUTHENTIK_API_TOKEN isn't set")
        try:
            r = requests.get(
                f"{sso.authentik_url()}/api/v3/core/users/",
                params={"groups_by_name": self.name, "is_active": "true", "page_size": 500},
                headers={"Authorization": f"Bearer {_API_TOKEN}"},
                timeout=10,
            )
            if not r.ok:
                # Authentik says why: an unknown group name, a token without permission, ...
                raise GroupUnavailable(f"Authentik refused to list group {self.name!r} (HTTP {r.status_code}): {r.text[:300]}")
            users = r.json()["results"]
        except (requests.RequestException, ValueError, KeyError) as exc:
            raise GroupUnavailable(f"couldn't read group {self.name!r} from Authentik: {exc}") from exc
        found: dict[str, dict] = {}
        for user in users:
            email = (user.get("email") or "").strip().lower()
            if email:
                found[email] = {"email": email, "name": (user.get("name") or user.get("username") or email).strip()}
        return sorted(found.values(), key=lambda m: m["name"].lower())


REVIEWERS = Group(os.getenv("REVIEWER_GROUP"))
ADMINS = Group(os.getenv("ADMIN_GROUP"))


def reviewers() -> list[dict]:
    """The reviewer group's members, for a route: a 503 when Authentik can't be asked."""
    try:
        return REVIEWERS.members()
    except GroupUnavailable as exc:
        raise HTTPException(status_code=503, detail=f"The reviewer list isn't available: {exc}.") from exc


def reviewer(email: str) -> dict | None:
    """This person's entry in the reviewer group, or None -- a 503 when Authentik can't be asked."""
    try:
        return REVIEWERS.member(email)
    except GroupUnavailable as exc:
        raise HTTPException(status_code=503, detail=f"The reviewer list isn't available: {exc}.") from exc


def is_admin(email: str) -> bool:
    """Owner rights on every study: a member of ADMIN_GROUP, or of the fallback list without one.
    False while the group can't be read -- this runs on every request, so it never raises."""
    if not ADMINS.configured:
        return email.strip().lower() in _FALLBACK_ADMINS
    try:
        return ADMINS.member(email) is not None
    except GroupUnavailable:
        return False
