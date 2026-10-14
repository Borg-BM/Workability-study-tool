# BM Workability Study Builder

This APP was mostly written bij claude code, frontend by figma and checked by BSW.

Barge Master's workability study tool. Build a machine's operating envelope and the overall
workability percentage from a vessel RAO, machine parameters and (optionally) metocean data,
then turn the result into a Word report.

The calculations are done by the in-house **PyBM** engine; this repository is the web
application around it.

## Architecture

| Part | Folder | Stack |
| --- | --- | --- |
| Frontend (Study Builder, report editor) | `src/`, `public/` | React 19, Vite, Tailwind, [docx-editor](https://github.com/eigenpal/docx-editor) |
| Backend (calculations, studies, reports, reviews) | `backend/` | FastAPI, PyBM, python-docx, SQLite |
| Container setup | `Dockerfile`, `docker/`, `docker-compose.yml` | nginx + backend image |
| PyBM reference docs | `pybm-docs/` | Documentation of the PyBM package |

Users sign in with their Barge Master account (Authentik SSO). PyBM's calls to the Barge Master
API (the RAO database) are made with the signed-in user's own access token.

## Requirements

- Node.js and [pnpm](https://pnpm.io/) (or npm)
- Python with the **PyBM** package installed (private package index, Barge Master access needed)
- Docker Desktop, if you want to run it in containers

## Run locally

Backend (from the `backend/` folder):

```
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000
```

Frontend (from the project root):

```
pnpm install
pnpm dev
```

Open <http://localhost:8443>. The dev server proxies `/api`, `/plots`, `/study-files` and
`/callback` to the backend, so the browser only sees one origin.

## Run in Docker

```
docker-up.cmd
```

Needs Docker Desktop and PyBM importable with `python` on the building machine (it is copied
into the image). Then open <http://localhost:8090> (set `APP_PORT` to use another port).

See [backend/README.md](backend/README.md) for sign-in, roles (reviewers and admins), hosting on
a server and the other configuration options.

## Input templates

Metocean data can be supplied in two formats; templates are in the project root:

- [HindcastTimeSeries_template.csv](HindcastTimeSeries_template.csv) — hourly time series
  (`Date`, `Hs`, `Tp`)
- [HindcastScatterTable_template.xlsx](HindcastScatterTable_template.xlsx) — Hs/Tp scatter table

The two `BM_OPXXXX_VESSEL_NAME_Workability_*_Rev0.py` scripts are the standalone PyBM templates
for lifting and transfer studies.

## Notes

- Large binary files (`.xlsx`, `.docx`, images, ...) are stored with Git LFS; install
  [Git LFS](https://git-lfs.com/) before cloning.
- Third-party licences are listed in [NOTICE](NOTICE).

## Licence

Copyright (c) Barge Master B.V. Internal use.
