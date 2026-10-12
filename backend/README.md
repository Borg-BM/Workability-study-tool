# Workability Study Tool — backend

FastAPI service that wraps the real PyBM calculation engine (RAO database +
`directional_workability` + metocean workability percentages) for the Study Builder
frontend, and stores studies, their report documents and reviews. It needs PyBM, and
runs either on your own machine or in Docker (locally or on a server).

## Sign-in

Everyone signs in with their Barge Master account (Authentik SSO): opening the app
redirects to Authentik and back. The app then knows who you are — study ownership,
sharing and admin rights key off that account's email — and PyBM's calls to Barge
Master's API (the RAO database) are made with **your own** access token, kept
server-side in the session (`app/sso.py`). Nothing uses `~/.pybm` any more; that's
only PyBM's own desktop login, for scripts.

It uses PyBM's existing Authentik client, which accepts `http://localhost:<port>/callback`
as the return address — so it works out of the box on any PC. A server needs one
addition there (see "Hosting on a server" below).

If Authentik issues a refresh token (it's asked for one), the API token is renewed
in the background; if not, an expired token sends you through Authentik again —
usually a quick redirect, since Authentik remembers you. Either way the session
itself lasts 12 hours (`SESSION_HOURS`). The backend log shows, at each sign-in,
how long the token is valid and whether a refresh token came with it.

## Run it

```
pip install -r backend/requirements.txt
python -m uvicorn app.main:app --reload --port 8000
```

(run from the `backend/` folder, or `cd backend` first), plus the frontend:
`npm run dev` in the project root, then open **http://localhost:8443**. The Vite
dev server proxies `/api`, `/plots`, `/study-files` and `/callback` to this backend,
so the browser only ever sees one origin (the sign-in cookie is first-party).

## Run it in Docker

```
docker-up.cmd
```

(from the project root; needs Docker Desktop running.) This builds two images and
starts them; open **http://localhost:8090** (set `APP_PORT` to use another port):

- `frontend` — the production Vite build served by nginx, which also proxies
  `/api`, `/plots`, `/study-files` and `/callback` to the backend, so everything
  is one origin.
- `backend` — this FastAPI service with PyBM and LibreOffice. It isn't published
  to the host; only nginx talks to it.

Things that differ from the native run:

- **PyBM** is copied into the image from the PyBM package installed on the
  building machine (`docker-up.cmd` finds it and passes it to the build as
  `PYBM_DIR`), so the build doesn't need the private package index. Rebuild with
  `docker-up.cmd` after updating PyBM or changing any code. Other dependency
  versions are pinned in `docker-constraints.txt` to match the native setup.
- **Data** is the same `backend/data` folder, mounted into the container. Don't
  run the native backend and the container at the same time — SQLite's locking
  doesn't work across the Windows/container boundary.
- **PDF export** uses LibreOffice instead of Word, with metric-compatible fonts
  (Carlito for Calibri, Liberation Sans for Arial). Layout can differ slightly
  from a Word-made PDF.

`docker compose logs -f backend` shows the backend log, `docker compose down`
stops everything. Both containers restart with Docker Desktop.

## Hosting on a server

The same two containers, with:

1. **Authentik**: add `https://<server address>/callback` as an allowed redirect
   URI on PyBM's Authentik provider (client id: the one in
   `https://api.app.barge-master.com/.well-known/oauth-config`). That's the only
   change needed there, and it keeps tokens acceptable to the Barge Master API.
   A dedicated Authentik application works too — set `AUTHENTIK_CLIENT_ID` (and
   `AUTHENTIK_CLIENT_SECRET` if it's a confidential client) — but then the API
   has to accept that client's tokens as well. Enabling the `offline_access`
   scope on the provider lets the app renew tokens without sending people back
   through Authentik.
2. **HTTPS** in front of the `frontend` container (the session cookie is marked
   Secure when the address is https).
3. **`PUBLIC_URL=https://<server address>`** in the environment, so the sign-in
   redirect uses the public address whatever proxies sit in between.
4. **PyBM in the image**: `docker-up.cmd` copies it from a local install, so
   either build on a machine with PyBM and push the image, or change
   `backend/Dockerfile` to install PyBM from the private package index (as a
   BuildKit secret, not a build arg, so the index credentials don't end up in
   the image).

Reviewers and admins come from Authentik groups — see the next section.

## Reviewers and admins

Both are managed in Authentik (`https://auth.app.barge-master.com`), as group
membership (`app/roles.py`):

- **Reviewers** (`REVIEWER_GROUP`) — only they can check (review) a report. The
  Review page offers them in a dropdown, their Authentik name goes into the
  report's Check and Approval fields, and someone taken out of the group can no
  longer decide on a review they were assigned.
- **Admins** (`ADMIN_GROUP`) — owner rights on every study: manage sharing,
  archive, delete, transfer ownership.

The app reads the groups' members through Authentik's API, as a service account,
and caches them for 5 minutes — so a membership change reaches the app within 5
minutes, without a restart.

### Setting it up in Authentik (once, as an Authentik admin)

All in the Admin interface:

1. **The two groups** — Directory → Groups → *Create*: `workability-reviewers`,
   then `workability-admins` (leave *Is superuser* off). Open each group →
   *Users* tab → *Add existing user* to add its members. A member needs an email
   address in Authentik; the app identifies people by it.
2. **A service account for the app** — Directory → Users → *Create Service
   account*: username `workability-study-tool`, with *Create group* switched on (it
   makes a group of the same name, holding just this account). Ignore the password
   it shows — that's an app password, which the API doesn't accept.
3. **Permission to read users** — Directory → Roles → *Create*:
   `workability-study-tool`. Open the role → *Assigned global permissions* →
   *Assign permission*: add **Can view User** and **Can view Group**. Then
   Directory → Groups → `workability-study-tool` → *Roles* tab → *Assign role* →
   the new role. (Read-only: the app never changes anything in Authentik.)
4. **An API token** — Directory → Tokens and App passwords → *Create*:
   identifier `workability-study-tool-api`, user `workability-study-tool`,
   intent **API**. Switch *Expiring* off, or note the date and renew it before
   then. In the token list, use *Copy token* to get its key.

Check it before configuring the app (PowerShell; it should list the admins):

```
Invoke-RestMethod -Headers @{ Authorization = "Bearer <token key>" } "https://auth.app.barge-master.com/api/v3/core/users/?groups_by_name=workability-admins&is_active=true" | Select-Object -ExpandProperty results | Select-Object name, email
```

### Configuring the app

```
REVIEWER_GROUP=workability-reviewers
ADMIN_GROUP=workability-admins
AUTHENTIK_API_TOKEN=<the token's key>
```

For Docker, put those lines in a `.env` file next to `docker-compose.yml` (it's
gitignored; Docker Compose reads it automatically) and run `docker-up.cmd` again;
for the native backend, set them in the shell before starting uvicorn.

- `REVIEWER_GROUP` unset: anyone can be asked to review, entered by email and
  name. `ADMIN_GROUP` unset: the fallback list in `app/roles.py` are the admins.
  Both are meant for a development PC, not a server.
- A group set but unreadable (no or a wrong token, a misspelled group name,
  Authentik down) fails closed: no reviewer can be assigned and nobody is an
  admin until it's fixed. The backend log (`docker compose logs backend`) shows
  why, e.g. Authentik's answer to the lookup.

## What's where

- **Calculation** (`app/pybm_service.py`): RAO list, loadcases and the
  workability calculation itself (`directional_workability`) call PyBM against
  the live API. The overall workability % weights the result by one of four
  metocean sources: an uploaded hindcast scatter table, Copernicus Marine, a
  NOAA NDBC buoy, or the 104 DNV-RP-C205 Weibull zones
  (`app/weibull_locations.py`, a last resort — highly conservative).
- **Data** is stored in `backend/data/` (gitignored): `studies.sqlite3`, polar
  plots in `plots/`, uploaded material in `study_files/`, uploaded scatter
  tables in `hindcast/`, and report documents in `reports/`.
- **The report** is a real Word document: `app/report_docx.py` generates a
  first draft in Barge Master's report style (python-docx), stored as
  `reports/<study id>.docx`, which the frontend then edits in docx-editor. A
  revision submitted for review is frozen as `reports/<study id>_rev<n>.docx`;
  review comments live in the database and can be put into a .docx as Word
  comments (`app/docx_comments.py`).
- **PDF export** (`app/docx_pdf.py`) uses Microsoft Word on the machine running
  this backend, so nothing extra is needed on a Barge Master PC. On a machine
  without Word (e.g. a Linux server) it falls back to headless LibreOffice,
  found in its standard install location or via `SOFFICE_PATH`.
