<!-- Source: https://docs.app.barge-master.com/conventions.html -->

# Conventions

## Units

All units are in [SI units](https://en.wikipedia.org/wiki/International_System_of_Units). Make sure all inputs to PyBM functions are in SI units.

## Coordinate System

The following coordinate_system is used in PyBM:

\[image: \_images/conventions.png — not available, stored as Git LFS pointer on the server\]

When loading RAOs for the first time, make sure to check the conventions of your input data, and if necessary, convert them to the PyBM conventions. [`PyBM.marine.motion_analysis.RAO.modify_conventions()`](autoapi/PyBM/marine/motion_analysis/index.md#id6 "PyBM.marine.motion_analysis.RAO.modify_conventions") can be used to convert RAOs to PyBM conventions.

## RAO Conventions

For RAOs being used in PyBM, the following conventions apply:

- Frequency in Hz

- Directions in degrees (following the PyBM coordinate system shown above)

- Motion RAOs are in m/m for \[X, Y, Z\]

- Motion RAOs are in deg/m for \[Rx, Ry, Rz\]

- RAO origin should be stored w.r.t to the APP/CL/Keel (defined above).

Points of Interest (POI) are given w.r.t. the origin of the RAO.
