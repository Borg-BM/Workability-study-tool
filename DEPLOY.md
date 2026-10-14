# Deploying to Portainer

The stack is `docker-compose.portainer.yml`: the same two containers as `docker-compose.yml`
(nginx frontend + FastAPI backend), built on the Docker host, with PyBM taken from a folder
on that host and the data in a named volume (`workability-data`).

## 1. Authentik (once, by an Authentik admin)

Sign-in, reviewers and admins are described in [backend/README.md](backend/README.md);
the steps for a server:

1. **Redirect URI** — on PyBM's Authentik provider (client id from
   `https://api.app.barge-master.com/.well-known/oauth-config`) add
   `https://<server address>/callback` as an allowed redirect URI (strict match).
   Optionally enable the `offline_access` scope so tokens renew silently.
2. **Groups** — create `workability-reviewers` and `workability-admins`, add members
   (each needs an email address).
3. **Service account + API token** — user `workability-study-tool`, a role with
   *Can view User* and *Can view Group*, and a non-expiring **API** token. Verify it with the
   PowerShell check in backend/README.md before deploying.

## 2. Docker host

- Put the PyBM package folder on the host, e.g. `/opt/pybm-src/PyBM` (copy from a PC with
  `python -c "import os, PyBM; print(os.path.dirname(PyBM.__file__))"`). Re-copy and rebuild
  when PyBM is updated.
- Put HTTPS (existing reverse proxy) in front of the frontend container's port, forwarding
  `X-Forwarded-Proto`. The session cookie is Secure on https.

## 3. Portainer

Stacks → Add stack → *Repository* (`https://github.com/Borg-BM/Workability-study-tool`,
compose path `docker-compose.portainer.yml`; add Git credentials if the repo is private;
Git LFS files are not needed for the build) — or paste the file into the web editor after
cloning the repo to the host. Environment variables:

| Variable | Value |
| --- | --- |
| `PYBM_DIR` | host path to the PyBM folder |
| `PUBLIC_URL` | `https://<server address>` (no trailing slash) |
| `AUTHENTIK_API_TOKEN` | the service account's token key |
| `REVIEWER_GROUP`, `ADMIN_GROUP` | optional, default to the group names above |
| `APP_PORT` | optional, default 8090 |
| `AUTHENTIK_CLIENT_ID`/`_SECRET` | only for a dedicated Authentik application |

Deploy, then check the backend container log: each sign-in logs the token lifetime, and a
failed group lookup logs Authentik's answer. Updating = *Pull and redeploy* with *Re-build
images* on.
