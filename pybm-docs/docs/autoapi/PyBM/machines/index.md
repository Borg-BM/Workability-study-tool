<!-- Source: https://docs.app.barge-master.com/autoapi/PyBM/machines/index.html -->

# PyBM.machines

## Submodules

- [PyBM.machines.heavy_feeder](heavy_feeder/index.md)
- [PyBM.machines.standard_feeder](standard_feeder/index.md)

## Attributes

|                                                                                                       |     |
|-------------------------------------------------------------------------------------------------------|-----|
| [`design_loads`](#id15 "PyBM.machines.design_loads")                                                  |     |
| [`Hs_design`](#PyBM.machines.Hs_design "PyBM.machines.Hs_design")                                     |     |
| [`g`](#id17 "PyBM.machines.g")                                                                        |     |
| [`rho`](#id18 "PyBM.machines.rho")                                                                    |     |
| [`design_loads`](#id15 "PyBM.machines.design_loads")                                                  |     |
| [`Hs_design_transit`](#PyBM.machines.Hs_design_transit "PyBM.machines.Hs_design_transit")             |     |
| [`Hs_design_operational`](#PyBM.machines.Hs_design_operational "PyBM.machines.Hs_design_operational") |     |
| [`t700`](#PyBM.machines.t700 "PyBM.machines.t700")                                                    |     |
| [`t700_cyl_push_max`](#PyBM.machines.t700_cyl_push_max "PyBM.machines.t700_cyl_push_max")             |     |
| [`t700_cyl_pull_max`](#PyBM.machines.t700_cyl_pull_max "PyBM.machines.t700_cyl_pull_max")             |     |
| [`t700_cyl_pass_max`](#PyBM.machines.t700_cyl_pass_max "PyBM.machines.t700_cyl_pass_max")             |     |
| [`t700_cyl_pull_max_act`](#PyBM.machines.t700_cyl_pull_max_act "PyBM.machines.t700_cyl_pull_max_act") |     |
| [`t700_cyl_push_max_act`](#PyBM.machines.t700_cyl_push_max_act "PyBM.machines.t700_cyl_push_max_act") |     |
| [`g`](#id17 "PyBM.machines.g")                                                                        |     |
| [`rho`](#id18 "PyBM.machines.rho")                                                                    |     |

## Classes

|                                                       |                                                                             |
|-------------------------------------------------------|-----------------------------------------------------------------------------|
| [`Tower`](#id0 "PyBM.machines.Tower")                 | Represents a tower mass item.                                               |
| [`VerticalStack`](#id3 "PyBM.machines.VerticalStack") | Represents a vertical stack of mass items.                                  |
| [`massItem`](#id5 "PyBM.machines.massItem")           | Represents a mass item with height, mass, and center of gravity properties. |
| [`T700`](#PyBM.machines.T700 "PyBM.machines.T700")    | Helper class that provides a standard way to create an ABC using            |
| [`Tower`](#id0 "PyBM.machines.Tower")                 | Represents a tower mass item.                                               |
| [`VerticalStack`](#id3 "PyBM.machines.VerticalStack") | Represents a vertical stack of mass items.                                  |
| [`massItem`](#id5 "PyBM.machines.massItem")           | Represents a mass item with height, mass, and center of gravity properties. |

## Functions

|                                                                                 |     |
|---------------------------------------------------------------------------------|-----|
| [`unity_checks_tower`](#id16 "PyBM.machines.unity_checks_tower")(→ numpy.array) |     |
| [`unity_checks_tower`](#id16 "PyBM.machines.unity_checks_tower")(→ numpy.array) |     |

## Package Contents

*class *PyBM.machines.Tower[](../../../../source-code/PyBM/utils/mass_items.py)  
Bases: [`massItem`](#id5 "PyBM.machines.massItem")

Represents a tower mass item.

D*: float = 0*  
\[m\] Diameter of Tower

*property *I  
Get the inertia around the center of gravity of the tower.

&nbsp;

*class *PyBM.machines.VerticalStack(*items*, *cog_factor=1.0*)[](../../../../source-code/PyBM/utils/mass_items.py)  
Bases: `Stack`

Represents a vertical stack of mass items.

*property *h  
\[m\] Get the height of the vertical stack.

&nbsp;

*class *PyBM.machines.massItem[](../../../../source-code/PyBM/utils/mass_items.py)  
Represents a mass item with height, mass, and center of gravity properties.

h*: float*  
\[m\] height

m*: float*  
\[kg\] mass

h_cog*: float = 0*  
\[m\] Height of CoG

x_cog*: float = 0*  
\[m\] Longitudinal offset of CoG

y_cog*: float = 0*  
\[m\] transverse offset of CoG

I*: float = 0*  
Inertia around CoG \[kg.m2\]

get_I() → float[](../../../../source-code/PyBM/utils/mass_items.py)  
\[kg.m2\] Get the inertia around the center of gravity.

set_I(*value: float*)[](../../../../source-code/PyBM/utils/mass_items.py)  
\[kg.m2\] Set the inertia around the center of gravity.

I_shifted(*offset*)[](../../../../source-code/PyBM/utils/mass_items.py)  
Get the inertia around an offset point.

Parameters:  
**offset** – \[m\] distance from stack CoG

Returns:  
Inertia around offset point \[kg.m2\]

&nbsp;

PyBM.machines.design_loads[](../../../../source-code/PyBM/machines/standard_feeder/tower_check.py)  

&nbsp;

PyBM.machines.Hs_design* = 2.5*[](../../../../source-code/PyBM/machines/heavy_feeder/tower_check.py)  

&nbsp;

PyBM.machines.unity_checks_tower(*tower: [PyBM.utils.mass_items.massItem](../utils/mass_items/index.md#PyBM.utils.mass_items.massItem "PyBM.utils.mass_items.massItem")*, *tbic: [PyBM.utils.mass_items.massItem](../utils/mass_items/index.md#PyBM.utils.mass_items.massItem "PyBM.utils.mass_items.massItem") = None*, *lifting_tool: [PyBM.utils.mass_items.massItem](../utils/mass_items/index.md#PyBM.utils.mass_items.massItem "PyBM.utils.mass_items.massItem") = None*, *Hs: float = None*) → numpy.array[](../../../../source-code/PyBM/machines/standard_feeder/tower_check.py)  
Calculate unity checks of a different tower w.r.t. the heavy feeder design conditions.

Parameters:  
- **tower** ([*massItem*](#id5 "PyBM.machines.massItem")) – Tower properties

- **tbic** ([*massItem*](#id5 "PyBM.machines.massItem")) – TBIC properties, by default the vinyard TBIC will be used.

- **lifting_tool** ([*massItem*](#id5 "PyBM.machines.massItem")) – Lifting tool properties, by default the vinyard tool will be used.

- **Hs** (*float*) – \[m\] Significant Waave height used for acceleration scaling, defaults to 2.5m

Returns:  
list of unity checks \[Fz, Mx, My\]

Return type:  
np.array

&nbsp;

PyBM.machines.g* = 9.81*[](../../../../source-code/PyBM/constants.py)  

&nbsp;

PyBM.machines.rho* = 1025*[](../../../../source-code/PyBM/constants.py)  

&nbsp;

*class *PyBM.machines.T700(*position*, *orientation*, *P_passive=35000000.0*)[](../../../../source-code/PyBM/marine/machines/T700.py)  
Bases: [`PyBM.marine.machines.machine_interface.Machine_Linear`](../marine/machines/machine_interface/index.md#PyBM.marine.machines.machine_interface.Machine_Linear "PyBM.marine.machines.machine_interface.Machine_Linear")

Helper class that provides a standard way to create an ABC using inheritance.

cd* = 13.8*  

vmax* = 0.736*  

vmax_center* = 0.44*  

stroke* = 2.2*  

max_flow* = 0.044*  

bore* = 0.42*  

rod* = 0.33*  

rod_center* = 0.26*  

cylinder  

CYLINDER_NAMES* = \['c1', 'c2', 'c3'\]*  

N_CYLINDERS* = 3*  

POI_NAMES* = \['center', 'c1', 'c2', 'c3'\]*  

*property *h  

*property *c1  

*property *c2  

*property *c3  

P_passive* = 35000000.0*  

cylinder_coordinates  

workability_checks  

get_POI()[](../../../../source-code/PyBM/marine/machines/T700.py)  
Return cylinder positions w.r.t. RAO definitions.

check_stroke_limit(*motion_at_poi*)[](../../../../source-code/PyBM/marine/machines/T700.py)  

check_cylinder_velocity_limit(*motion_at_poi*)[](../../../../source-code/PyBM/marine/machines/T700.py)  

check_platform_velocity_limit(*motion_at_poi*)[](../../../../source-code/PyBM/marine/machines/T700.py)  

compute_cylinder_forces(*Fz*, *Mx*, *My*)[](../../../../source-code/PyBM/marine/machines/T700.py)  

plot(*axs: matplotlib.axes.Axes = None*)[](../../../../source-code/PyBM/marine/machines/T700.py)  

&nbsp;

*class *PyBM.machines.Tower[](../../../../source-code/PyBM/utils/mass_items.py)  
Bases: [`massItem`](#id5 "PyBM.machines.massItem")

Represents a tower mass item.

D*: float = 0*  
\[m\] Diameter of Tower

*property *I  
Get the inertia around the center of gravity of the tower.

&nbsp;

*class *PyBM.machines.VerticalStack(*items*, *cog_factor=1.0*)[](../../../../source-code/PyBM/utils/mass_items.py)  
Bases: `Stack`

Represents a vertical stack of mass items.

*property *h  
\[m\] Get the height of the vertical stack.

&nbsp;

*class *PyBM.machines.massItem[](../../../../source-code/PyBM/utils/mass_items.py)  
Represents a mass item with height, mass, and center of gravity properties.

h*: float*  
\[m\] height

m*: float*  
\[kg\] mass

h_cog*: float = 0*  
\[m\] Height of CoG

x_cog*: float = 0*  
\[m\] Longitudinal offset of CoG

y_cog*: float = 0*  
\[m\] transverse offset of CoG

I*: float = 0*  
Inertia around CoG \[kg.m2\]

get_I() → float[](../../../../source-code/PyBM/utils/mass_items.py)  
\[kg.m2\] Get the inertia around the center of gravity.

set_I(*value: float*)[](../../../../source-code/PyBM/utils/mass_items.py)  
\[kg.m2\] Set the inertia around the center of gravity.

I_shifted(*offset*)[](../../../../source-code/PyBM/utils/mass_items.py)  
Get the inertia around an offset point.

Parameters:  
**offset** – \[m\] distance from stack CoG

Returns:  
Inertia around offset point \[kg.m2\]

&nbsp;

PyBM.machines.design_loads[](../../../../source-code/PyBM/machines/standard_feeder/tower_check.py)  

&nbsp;

PyBM.machines.Hs_design_transit* = 2.5*[](../../../../source-code/PyBM/machines/standard_feeder/tower_check.py)  

&nbsp;

PyBM.machines.Hs_design_operational* = 2.0*[](../../../../source-code/PyBM/machines/standard_feeder/tower_check.py)  

&nbsp;

PyBM.machines.t700[](../../../../source-code/PyBM/machines/standard_feeder/tower_check.py)  

&nbsp;

PyBM.machines.t700_cyl_push_max[](../../../../source-code/PyBM/machines/standard_feeder/tower_check.py)  

&nbsp;

PyBM.machines.t700_cyl_pull_max[](../../../../source-code/PyBM/machines/standard_feeder/tower_check.py)  

&nbsp;

PyBM.machines.t700_cyl_pass_max[](../../../../source-code/PyBM/machines/standard_feeder/tower_check.py)  

&nbsp;

PyBM.machines.t700_cyl_pull_max_act* = 1431000.0*[](../../../../source-code/PyBM/machines/standard_feeder/tower_check.py)  

&nbsp;

PyBM.machines.t700_cyl_push_max_act* = 1431000.0*[](../../../../source-code/PyBM/machines/standard_feeder/tower_check.py)  

&nbsp;

PyBM.machines.unity_checks_tower(*tower: [PyBM.utils.mass_items.massItem](../utils/mass_items/index.md#PyBM.utils.mass_items.massItem "PyBM.utils.mass_items.massItem")*, *tbic: [PyBM.utils.mass_items.massItem](../utils/mass_items/index.md#PyBM.utils.mass_items.massItem "PyBM.utils.mass_items.massItem") = None*, *lifting_tool: [PyBM.utils.mass_items.massItem](../utils/mass_items/index.md#PyBM.utils.mass_items.massItem "PyBM.utils.mass_items.massItem") = None*, *Hs_transit: float = None*, *Hs_operational: float = None*, *debug=False*) → numpy.array[](../../../../source-code/PyBM/machines/standard_feeder/tower_check.py)  

&nbsp;

PyBM.machines.g* = 9.81*[](../../../../source-code/PyBM/constants.py)  

&nbsp;

PyBM.machines.rho* = 1025*[](../../../../source-code/PyBM/constants.py)  
