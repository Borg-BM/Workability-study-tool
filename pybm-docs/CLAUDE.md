# PyBM documentation — offline copy (read this first)

This folder is a complete offline snapshot of **https://docs.app.barge-master.com/** — the internal
documentation for **PyBM 6.7.2**, Barge Master's Python package of engineering tools (vessel motion
analysis, workability of BM machines, wave hindcast analysis, hydraulics sizing, IIR filters, tower checks).

The live site sits behind Authentik SSO, so you (an agent in a sandbox) cannot reach it. Everything that was
on it is here instead. **Do not try to fetch the live site; use these files.** Snapshot taken 2026-09-28.

## Folder layout

| Path | What it is | When to use it |
|---|---|---|
| `CLAUDE.md` | This orientation guide | Start here |
| `API_MAP.md` | One-page map of every PyBM module, class, method and function (generated from the code) | Find *where* something lives |
| `docs/` | Every page of the site converted to Markdown, same paths as the site (`docs/usage/hindcast.md` = `/usage/hindcast.html`) | Read guides, theory, templates, API docs |
| `docs/autoapi/PyBM/...` | Auto-generated API reference (signatures, parameters, docstrings) per module | Exact call signatures |
| `source-code/PyBM/...` | **Full Python source** of the PyBM modules, recovered from the site's "[source]" pages | Ground truth for behaviour — check here when docs are vague |
| `examples/` | The downloadable example/template scripts from the Templates page | Starting points for new scripts |
| `rst-sources/` | Original reStructuredText sources of every page | Only if Markdown conversion looks garbled |

## Most important pages

- `docs/conventions.md` — **READ AND FOLLOW.** The docs say conventions are "the main source of errors".
- `docs/installation.md` — pip registry setup, venvs, requirements.txt.
- `docs/templates.md` — worked examples for every feature (same code as `examples/`).
- `docs/theory.md` — wave spectra (PM, JONSWAP, Torsethaugen), spreading, frequency/time-domain response, MPE, RAO translation.
- `docs/usage/workability.md`, `docs/usage/hindcast.md`, `docs/usage/workability_percentages.md`,
  `docs/usage/importing_rao_tool.md`, `docs/usage/venv.md` — user guides.

## Key facts (summarised from the docs)

**Conventions**
- All inputs/outputs in **SI units**.
- RAOs: frequency in **Hz**; directions in **degrees**; translational RAOs [X, Y, Z] in **m/m**; rotational [Rx, Ry, Rz] in **deg/m**.
- RAO origin is stored w.r.t. **APP / CL / Keel** (aft perpendicular, centreline, keel). Points of interest (POI) are given w.r.t. the RAO origin — e.g. `pos_wrt_trace = pos - trace.origin`.
- Use `PyBM.marine.motion_analysis.RAO.modify_conventions()` to convert foreign RAOs to PyBM conventions.
- The coordinate-system figure (`conventions.png`) is **not available** (see "Known gaps"). Direction enums
  (`SurgeDir`, `SwayDir`, `HeaveDir`, `RollDir`, `PitchDir`, `YawDir`, `WaveOrigin`, `RotationUnit`) are in
  `source-code/PyBM/marine/motion_analysis/RAO.py` — read those for the exact definitions.
- MCG slewing angle: 90° = port side, 270° = starboard side (from the example scripts).

**Installation**
- PyBM installs from BM's private PyPI (`pypi.app.barge-master.com`) configured in `C:\Users\<user>\pip\pip.ini` — see `docs/installation.md`.
- `pip install PyBM` (or `PyBM==x.y.z`). Semantic versioning — major bump = breaking change. Pin with `pip freeze > requirements.txt`.

**Main entry points** (most are re-exported from `PyBM.marine`)
- RAOs: `MotionRAO.from_api(vessel_name, loading_condition)` loads from the BM RAO database (MongoDB via API; triggers an auth flow). The old `MotionRAO.default_rao_path` / `load_rao` is being deprecated.
- Wave spectra: `Jonswap(Hs, Tp, WaveDir, spreading=...)`, `PiersonMoskowitz`, `Torsethaugen`. Parameters can be arrays and broadcast (xarray-based).
- Frequency domain: `compute_response(wave, rao, poi=...)`, `compute_mpe(wave, rao, poi=..., storm_duration=...)` → xarray with e.g. `mpe["POS"].sel(DOF="Z")`.
- Time domain: `TimeDomain`, `TimeDomain.load_all_default_time_traces(vessel, revision)`.
- Machines (workability limits): `MCG30*_Linear` / `MCG30*_Nonlinear` (variants L/M × TRANSFER / TIPLADDER / HIGHLOAD / LOWLOAD), `T700`, `HeavyFeeder`, `HeavyFeederSurgeSway`. Base classes `Machine_Linear` / `Machine_Nonlinear` in `marine/machines/machine_interface.py`.
- Workability: `PyBM.marine.workability` (e.g. `directional_workability_timetrace`), `.workability` xarray accessor (`plot_detailed_workability`).
- Hindcast: loaders (`ExcelTimeSeriesLoader`, `ExcelScatterLoader`, `CopernicusLoader`, `NDBCLoader`, `DNVLoader`) → `Hindcast(loader)` factory → `HindcastTimeSeries` / `HindcastScatterTable` (stats, Hs–Tp occurrence, workability %).
- Other: `PyBM.utils` (`VesselDimensions`, mass items, plot template), `PyBM.hydraulics` (accumulators, cylinders, buckling), `PyBM.signal` (IIR filters), `PyBM.machines.*.tower_check`, `PyBM.constants` (`g = 9.81`, `rho = 1025`).

## How to work with this

1. Look up the module in `API_MAP.md`.
2. Read the matching `docs/autoapi/.../index.md` for signatures and docstrings.
3. If behaviour matters, read the actual code in `source-code/`.
4. Copy the closest script from `examples/` as a starting point, and check it against `docs/conventions.md`.
5. The code here is **version 6.7.2**. If the project pins another PyBM version (check `requirements.txt`), APIs may differ. The installed package in the venv (`site-packages/PyBM`) is then the better reference.

## Known gaps — don't go looking for these

- **Images:** all 19 figures on the live site are broken (served as Git LFS pointer files, not real PNGs). They are marked `[image: … not available …]` in the Markdown. The originals are only in the PyBM Git repo (`git lfs pull`).
- **Downloadable files** that are not reproduced inline on the site are missing: `HindcastTimeSeries_template.csv`, `HindcastScatterTable_template.xlsx`, `RAO_combined.xlsx`, `rao_csv.csv`, `rao_txt.txt`, `rao_lis.LIS`. Links to them in `docs/` are dead. (`examples/install_setup.ps1` came from the user's own Downloads folder, not from this snapshot.)
- **Source code** covers only modules that have documented objects (49 files). Package `__init__.py` files, `conf.py`, tests and the `templates/` folder of the repo are not included. `source-code/PyBM/marine/machines/MCG30.py` is really the `MCG30` package's `__init__`.
- **Redaction:** one hard-coded Copernicus Marine password in `HindcastLoader.py` was replaced with `<REDACTED>`. Don't hard-code credentials. Use `copernicusmarine login` or environment variables.
