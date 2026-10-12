"""DOCX -> PDF conversion (docx-editor's own PDF export is a paid add-on).

Uses Microsoft Word when it's installed -- as on every Barge Master PC, so nothing extra to
install -- and falls back to headless LibreOffice on a machine without Word (e.g. a Linux server).
"""

import os
import shutil
import subprocess
import sys
import tempfile
import threading
from pathlib import Path

# One conversion at a time: both Word automation and a LibreOffice profile are single-user.
_LOCK = threading.Lock()
_TIMEOUT_S = 120


class PdfConversionError(Exception):
    pass


# ---- Microsoft Word, driven over COM from PowerShell (built into Windows: no extra package) ----

# Opens the document read-only in a hidden Word of its own and quits that Word afterwards.
# New-Object always starts a separate, invisible Word for automation -- never the one the user
# has open -- so it has to be quit even while the user's Word is running, or it stays behind.
# The one exception: a document the user opened meanwhile can land in that Word, so it's left
# running when anything but ours is still open in it.
_WORD_SCRIPT = r"""
$ErrorActionPreference = 'Stop'
$word = New-Object -ComObject Word.Application
try {
  $word.DisplayAlerts = 0
  $m = [Type]::Missing
  $doc = $word.Documents.Open($env:WST_DOCX, $false, $true, $false, $m, $m, $false, $m, $m, $m, $m, $false)
  try { $doc.ExportAsFixedFormat($env:WST_PDF, 17) } finally { $doc.Close(0) }
} finally {
  if ($word.Documents.Count -eq 0) { $word.Quit() }
  [void][Runtime.InteropServices.Marshal]::ReleaseComObject($word)
}
"""


def word_installed() -> bool:
    if sys.platform != "win32":
        return False
    import winreg

    try:
        winreg.CloseKey(winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, r"Word.Application\CLSID"))
        return True
    except OSError:
        return False


def _convert_with_word(source: Path, output: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["powershell.exe", "-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass", "-Command", _WORD_SCRIPT],
        env={**os.environ, "WST_DOCX": str(source), "WST_PDF": str(output)},
        capture_output=True,
        timeout=_TIMEOUT_S,
    )


# ---- LibreOffice (fallback) ----

_SOFFICE_CANDIDATES = (
    r"C:\Program Files\LibreOffice\program\soffice.exe",
    r"C:\Program Files (x86)\LibreOffice\program\soffice.exe",
    "/usr/bin/soffice",
    "/usr/lib/libreoffice/program/soffice",
    "/Applications/LibreOffice.app/Contents/MacOS/soffice",
)

# A private profile so conversions never collide with a LibreOffice window the user has open.
_PROFILE_DIR = Path(tempfile.gettempdir()) / "workability-study-tool-libreoffice"

# With update checks on, a launch can instead download and apply a LibreOffice update, then exit
# without converting (the updater relaunches the command later) -- so they're forced off.
_PROFILE_SETTINGS = """<?xml version="1.0" encoding="UTF-8"?>
<oor:items xmlns:oor="http://openoffice.org/2001/registry" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
<item oor:path="/org.openoffice.Office.Update/Update"><prop oor:name="Enabled" oor:op="fuse"><value>false</value></prop></item>
<item oor:path="/org.openoffice.Office.Jobs/Jobs/org.openoffice.Office.Jobs:Job['UpdateCheck']/Arguments"><prop oor:name="AutoCheckEnabled" oor:op="fuse"><value>false</value></prop></item>
</oor:items>
"""


def find_soffice() -> str | None:
    configured = os.environ.get("SOFFICE_PATH")
    if configured:
        return configured if Path(configured).exists() else None
    return shutil.which("soffice") or shutil.which("libreoffice") or next((c for c in _SOFFICE_CANDIDATES if Path(c).exists()), None)


def _convert_with_libreoffice(soffice: str, source: Path) -> subprocess.CompletedProcess:
    settings = _PROFILE_DIR / "user" / "registrymodifications.xcu"
    settings.parent.mkdir(parents=True, exist_ok=True)
    settings.write_text(_PROFILE_SETTINGS, encoding="utf-8")
    command = [
        soffice,
        f"-env:UserInstallation={_PROFILE_DIR.as_uri()}",
        "--headless",
        "--norestore",
        "--convert-to",
        "pdf",
        "--outdir",
        str(source.parent),
        str(source),
    ]
    return subprocess.run(command, capture_output=True, timeout=_TIMEOUT_S)


def docx_to_pdf(docx_bytes: bytes) -> bytes:
    """The PDF of a .docx, made by Word when it's installed, else LibreOffice. Blocking (up to
    _TIMEOUT_S, one conversion at a time) -- call it from a worker thread. Raises
    PdfConversionError when neither is available or the conversion fails."""
    use_word = word_installed()
    soffice = None if use_word else find_soffice()
    if not use_word and soffice is None:
        raise PdfConversionError(
            "PDF export needs Microsoft Word or LibreOffice on the machine running the backend "
            "(for LibreOffice outside its standard install location, set SOFFICE_PATH)."
        )
    converter = "Word" if use_word else "LibreOffice"
    with _LOCK, tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp).resolve()  # long path: Windows' temp dir can be an 8.3 short name
        source = work / "report.docx"
        output = work / "report.pdf"
        source.write_bytes(docx_bytes)
        try:
            proc = _convert_with_word(source, output) if use_word else _convert_with_libreoffice(soffice, source)
        except subprocess.TimeoutExpired as exc:
            raise PdfConversionError(f"{converter} didn't finish converting within {_TIMEOUT_S}s.") from exc
        if not output.exists():
            details = (proc.stderr or proc.stdout).decode(errors="replace").strip()[-500:]
            raise PdfConversionError(f"{converter} couldn't convert the document{': ' + details if details else '.'}")
        return output.read_bytes()
