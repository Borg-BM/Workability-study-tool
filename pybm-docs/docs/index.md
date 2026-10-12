<!-- Source: https://docs.app.barge-master.com/index.html -->

# PyBM Documentation

This is the Python Documentation for PyBM, a Python package containing the Barge Master engineering tools.

# Installation

This package should be installed using PIP, cloning is only required when developing the package. Installation steps and how to use it is detailed in the [Installation](installation.md#installation) page.

# User guides and training material

User guides and training material can be found under the [User Guides](usage.md#user-guides) page. Currently, there is documentation for the trainings:

- [Virtual Environments](usage/venv.md#virtual-environments)

- [Importing RAOs with the RAO Import Tool](usage/importing_rao_tool.md#rao-import-tool)

- [PyBM Workability Training](usage/workability.md#pybm-workability-training)

- [Hindcast Analysis](usage/hindcast.md#hindcast)

# Conventions

The conventions used in PyBM are described in the [Conventions](conventions.md#conventions) page. Please READ AND FOLLOW them, they are the main source of errors when working with RAO and vessel motions.

# Features

The following features are available in PyBM, more information is available in the [User Guides](usage.md#user-guides) or the [Templates](templates.md#templates) page.

- [Motion Analysis](theory.md#motion-analysis): Compute frequency and time domain vessel motions. See templates [here](templates.md#motion-analysis).

- [Workability](usage/workability.md#pybm-workability-training): Compute workability of Barge Master machines on a given vessel. See templates [here](templates.md#workability).

- [Hindcast Analysis](usage/hindcast.md#hindcast): Load and analyze historical wave data from multiple sources (Copernicus, NOAA NDBC, DNV, Excel). Allows combining with workability studies to obtain workability percentages. See templates [here](templates.md#hindcast).

- Mass Item tools: Simplified “stacking” of masses for CoG and inertia calculations. For now, the use of this tool is limited to “Heavy Feeder Tower check” analysis (see item below). Further features are still in a development branch and will be released in future versions.

- [Heavy Feeder Tower check](templates.md#heavy-feeder-tower-check): Check HF performance for different towers and configurations.

- [IIR Filter design](templates.md#iir-filters): Tools for designing and plotting IIR filters for the BM machines.

- Hydraulic / Mechanic design: Tools for sizing and optimization of hydraulic systems.
