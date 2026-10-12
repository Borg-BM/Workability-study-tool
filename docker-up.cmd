@echo off
rem Builds and (re)starts the Workability Study Tool in Docker -- see docker-compose.yml.
rem Hands the backend build the PyBM package installed on this machine (no access to the
rem private package index needed). Extra arguments go to `docker compose up`.
setlocal
cd /d "%~dp0"

for /f "delims=" %%d in ('python -c "import os, PyBM; print(os.path.dirname(PyBM.__file__))"') do set "PYBM_DIR=%%d"
if not defined PYBM_DIR (
  echo PyBM isn't importable with `python` on this machine -- install it first.
  exit /b 1
)

if not defined APP_PORT set "APP_PORT=8090"

docker compose up -d --build %*
if errorlevel 1 exit /b 1
echo.
echo Workability Study Tool: http://localhost:%APP_PORT%
