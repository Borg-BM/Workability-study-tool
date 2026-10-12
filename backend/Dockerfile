# syntax=docker/dockerfile:1
# Backend image: FastAPI + PyBM + LibreOffice (PDF export -- there's no Word in a Linux
# container, so docx_pdf.py falls back to headless LibreOffice).
#
# PyBM comes from the `pybm` build context (the PyBM package folder installed on the machine
# doing the build, see docker-compose.yml / docker-up.cmd), so the build needs no credentials
# for Barge Master's private package index.
FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONPATH=/opt/pybm

# Carlito and Liberation are metric-compatible stand-ins for the report's Calibri and Arial,
# so LibreOffice's PDF keeps the same line and page breaks as the .docx.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libreoffice-writer-nogui \
        fonts-crosextra-carlito \
        fonts-liberation \
        fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# PyBM's runtime dependencies plus the backend's own, pinned to the versions the native
# setup runs (docker-constraints.txt) so a calculation gives the same numbers in both.
COPY requirements.txt docker-constraints.txt ./
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt -c docker-constraints.txt \
        numpy matplotlib xarray dask scipy netCDF4 h5netcdf openpyxl sympy geopy xlrd requests pandas

COPY --from=pybm . /opt/pybm/PyBM
COPY app ./app

EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/api/health', timeout=4)"

# Only nginx can reach this port, so its X-Forwarded-Proto is trusted -- that's how the
# sign-in redirect knows it's behind https on a server.
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--forwarded-allow-ips", "*"]
