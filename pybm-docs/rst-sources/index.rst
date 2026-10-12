.. toctree::
   :hidden:

   PyBM Documentation <self>
   Installation <installation>
   User Guides and Training Material <usage>
   Templates <templates>
   Conventions <conventions>
   Theory <theory>
   Usage <usage/_usage>


PyBM Documentation
******************

This is the Python Documentation for PyBM, a Python package containing the Barge Master engineering tools.


Installation
************

This package should be installed using PIP, cloning is only required when developing the package.
Installation steps and how to use it is detailed in the :ref:`installation:Installation` page.

User guides and training material
*********************************

User guides and training material can be found under the :ref:`usage:User Guides` page. Currently, there is documentation for the trainings:

- :ref:`usage/venv:Virtual Environments`
- :ref:`Importing RAOs with the RAO Import Tool <usage/importing_rao_tool:RAO Import Tool>`
- :ref:`usage/workability:PyBM Workability Training`
- :ref:`Hindcast Analysis <usage/hindcast:Hindcast>`


Conventions
***********

The conventions used in PyBM are described in the :ref:`conventions:Conventions` page. Please READ AND FOLLOW them, they are the main source of errors when working with RAO and vessel motions.


Features
********

The following features are available in PyBM, more information is available in the :ref:`usage:User Guides` or the :ref:`templates:templates` page.

- :ref:`Motion Analysis <theory:Motion Analysis>`: Compute frequency and time domain vessel motions. See templates :ref:`here <templates:Motion Analysis>`.
- :ref:`Workability <usage/workability:PyBM Workability Training>`: Compute workability of Barge Master machines on a given vessel. See templates :ref:`here <templates:Workability>`.
- :ref:`Hindcast Analysis <usage/hindcast:Hindcast>`: Load and analyze historical wave data from multiple sources (Copernicus, NOAA NDBC, DNV, Excel). Allows combining with workability studies to obtain workability percentages. See templates :ref:`here <templates:Hindcast>`.
- Mass Item tools: Simplified "stacking" of masses for CoG and inertia calculations. For now, the use of this tool is limited to "Heavy Feeder Tower check" analysis (see item below). Further features are still in a development branch and will be released in future versions.
- :ref:`Heavy Feeder Tower check <templates:Heavy Feeder Tower check>`: Check HF performance for different towers and configurations.
- :ref:`IIR Filter design <templates:IIR Filters>`: Tools for designing and plotting IIR filters for the BM machines.
- :ref:`Hydraulic / Mechanic design <templates:Hydraulic / Mechanical sizing>`: Tools for sizing and optimization of hydraulic systems.
