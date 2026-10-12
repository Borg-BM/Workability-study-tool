<!-- Source: https://docs.app.barge-master.com/autoapi/PyBM/marine/workability/workability_limits/index.html -->

# PyBM.marine.workability.workability_limits

## Attributes

|                                                                                                              |     |
|--------------------------------------------------------------------------------------------------------------|-----|
| [`cmap`](#PyBM.marine.workability.workability_limits.cmap "PyBM.marine.workability.workability_limits.cmap") |     |

## Classes

|                                                                                                                                                              |     |
|--------------------------------------------------------------------------------------------------------------------------------------------------------------|-----|
| [`workability_accessor`](#PyBM.marine.workability.workability_limits.workability_accessor "PyBM.marine.workability.workability_limits.workability_accessor") |     |

## Functions

|                                                                                                                                                                                                                         |                                                                            |
|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------|
| [`directional_workability`](#PyBM.marine.workability.workability_limits.directional_workability "PyBM.marine.workability.workability_limits.directional_workability")(→ xarray.DataArray)                               | Compute the workability of the machine for the given wave directions.      |
| [`directional_workability_timetrace`](#PyBM.marine.workability.workability_limits.directional_workability_timetrace "PyBM.marine.workability.workability_limits.directional_workability_timetrace")(→ xarray.DataArray) | Compute the workability of the machine using the time trace supplied (MCG) |
| [`_polar_plotter`](#PyBM.marine.workability.workability_limits._polar_plotter "PyBM.marine.workability.workability_limits._polar_plotter")(plot_method, workability_result\[, ...\])                                    |                                                                            |
| [`multicolored_line`](#PyBM.marine.workability.workability_limits.multicolored_line "PyBM.marine.workability.workability_limits.multicolored_line")(ax, Tp_result)                                                      |                                                                            |
| [`multiple_lines`](#PyBM.marine.workability.workability_limits.multiple_lines "PyBM.marine.workability.workability_limits.multiple_lines")(ax, Tp_result)                                                               |                                                                            |
| [`set_polar_plot_params`](#PyBM.marine.workability.workability_limits.set_polar_plot_params "PyBM.marine.workability.workability_limits.set_polar_plot_params")(ax, max_y, Tp)                                          |                                                                            |
| [`plot_ship`](#PyBM.marine.workability.workability_limits.plot_ship "PyBM.marine.workability.workability_limits.plot_ship")(ax\[, plot_diameter\])                                                                      | Plot a ship contour on the given axis.                                     |
| [`_make_legend_proxies`](#PyBM.marine.workability.workability_limits._make_legend_proxies "PyBM.marine.workability.workability_limits._make_legend_proxies")(cmap, \*\*kwargs)                                          |                                                                            |

## Module Contents

PyBM.marine.workability.workability_limits.cmap[](../../../../../../source-code/PyBM/marine/workability/workability_limits.py)  

&nbsp;

*class *PyBM.marine.workability.workability_limits.workability_accessor(*obj*)[](../../../../../../source-code/PyBM/marine/workability/workability_limits.py)  
\_obj[](../../../../../../source-code/PyBM/marine/workability/workability_limits.py)  

table(*Hs*, *Hsrange*)[](../../../../../../source-code/PyBM/marine/workability/workability_limits.py)  

byscatter(*scatter*)[](../../../../../../source-code/PyBM/marine/workability/workability_limits.py)  

plot_detailed_workability(*max_hs=None*, *fig=None*)[](../../../../../../source-code/PyBM/marine/workability/workability_limits.py)  
Plot workability for each system limit.

Parameters:  
- **workability_result** (*xr.DataArray*) – \_description\_

- **max_hs** (*\_type\_,* *optional*) – \_description\_, defaults to None

- **fig** (*\_type\_,* *optional*) – \_description\_, defaults to None

plot_combined_workability(*max_hs=None*, *fig=None*)[](../../../../../../source-code/PyBM/marine/workability/workability_limits.py)  
Plot the result of the workability in polar plots

Parameters:  
- **workability_result** – \[m\] Array of limiting Hs for each wave peak period, direction and machine limit.

- **max_hs** – \[m\] maximum Hs on the polar plot, defaults to None

- **fig** – figure to plot on, defaults to None

&nbsp;

PyBM.marine.workability.workability_limits.directional_workability(*rao: [PyBM.marine.MotionRAO](../../index.md#PyBM.marine.MotionRAO "PyBM.marine.MotionRAO")*, *wave: [PyBM.marine.WaveSpectrum](../../index.md#PyBM.marine.WaveSpectrum "PyBM.marine.WaveSpectrum")*, *machine: [PyBM.marine.machines.Machine_Linear](../../machines/index.md#PyBM.marine.machines.Machine_Linear "PyBM.marine.machines.Machine_Linear")*, *\*\*kwargs*) → xarray.DataArray[](../../../../../../source-code/PyBM/marine/workability/workability_limits.py)  
Compute the workability of the machine for the given wave directions.

Returns:  
\[m\] Array of limiting Hs for each wave peak period, direction and machine limit.

&nbsp;

PyBM.marine.workability.workability_limits.directional_workability_timetrace(*trace: xarray.DataArray*, *machine: PyBM.marine.machines.MCG30.MCG30_Nonlinear*, *\*\*kwargs*) → xarray.DataArray[](../../../../../../source-code/PyBM/marine/workability/workability_limits.py)  
Compute the workability of the machine using the time trace supplied (MCG)

Returns:  
\[m\] Array of limiting Hs for each wave peak period, direction and machine limit.

&nbsp;

PyBM.marine.workability.workability_limits.\_polar_plotter(*plot_method*, *workability_result: xarray.DataArray*, *max_hs=None*, *fig: matplotlib.figure.Figure = None*)[](../../../../../../source-code/PyBM/marine/workability/workability_limits.py)  

&nbsp;

PyBM.marine.workability.workability_limits.multicolored_line(*ax: matplotlib.pyplot.Axes*, *Tp_result*)[](../../../../../../source-code/PyBM/marine/workability/workability_limits.py)  

&nbsp;

PyBM.marine.workability.workability_limits.multiple_lines(*ax: matplotlib.pyplot.Axes*, *Tp_result*)[](../../../../../../source-code/PyBM/marine/workability/workability_limits.py)  

&nbsp;

PyBM.marine.workability.workability_limits.set_polar_plot_params(*ax: matplotlib.pyplot.Axes*, *max_y*, *Tp*)[](../../../../../../source-code/PyBM/marine/workability/workability_limits.py)  

&nbsp;

PyBM.marine.workability.workability_limits.plot_ship(*ax: matplotlib.pyplot.Axes*, *plot_diameter=1.0*)[](../../../../../../source-code/PyBM/marine/workability/workability_limits.py)  
Plot a ship contour on the given axis.

Parameters:  
- **axs** – Axes to plot on.

- **plot_diameter** – diameter of vessel contour, defaults to 1.0

&nbsp;

PyBM.marine.workability.workability_limits.\_make_legend_proxies(*cmap*, *\*\*kwargs*)[](../../../../../../source-code/PyBM/marine/workability/workability_limits.py)  
