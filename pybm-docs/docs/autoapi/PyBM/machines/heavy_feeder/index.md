<!-- Source: https://docs.app.barge-master.com/autoapi/PyBM/machines/heavy_feeder/index.html -->

# PyBM.machines.heavy_feeder

## Submodules

- [PyBM.machines.heavy_feeder.tower_check](tower_check/index.md)

## Attributes

|                                                                                                      |     |
|------------------------------------------------------------------------------------------------------|-----|
| [`design_loads`](#PyBM.machines.heavy_feeder.design_loads "PyBM.machines.heavy_feeder.design_loads") |     |
| [`Hs_design`](#PyBM.machines.heavy_feeder.Hs_design "PyBM.machines.heavy_feeder.Hs_design")          |     |
| [`g`](#PyBM.machines.heavy_feeder.g "PyBM.machines.heavy_feeder.g")                                  |     |
| [`rho`](#PyBM.machines.heavy_feeder.rho "PyBM.machines.heavy_feeder.rho")                            |     |

## Classes

|                                                                                                         |                                                                             |
|---------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------|
| [`Tower`](#PyBM.machines.heavy_feeder.Tower "PyBM.machines.heavy_feeder.Tower")                         | Represents a tower mass item.                                               |
| [`VerticalStack`](#PyBM.machines.heavy_feeder.VerticalStack "PyBM.machines.heavy_feeder.VerticalStack") | Represents a vertical stack of mass items.                                  |
| [`massItem`](#PyBM.machines.heavy_feeder.massItem "PyBM.machines.heavy_feeder.massItem")                | Represents a mass item with height, mass, and center of gravity properties. |

## Functions

|                                                                                                                                       |                                                                                        |
|---------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------|
| [`unity_checks_tower`](#PyBM.machines.heavy_feeder.unity_checks_tower "PyBM.machines.heavy_feeder.unity_checks_tower")(→ numpy.array) | Calculate unity checks of a different tower w.r.t. the heavy feeder design conditions. |

## Package Contents

*class *PyBM.machines.heavy_feeder.Tower[](../../../../../source-code/PyBM/utils/mass_items.py)  
Bases: [`massItem`](#PyBM.machines.heavy_feeder.massItem "PyBM.machines.heavy_feeder.massItem")

Represents a tower mass item.

D*: float = 0*  
\[m\] Diameter of Tower

*property *I  
Get the inertia around the center of gravity of the tower.

&nbsp;

*class *PyBM.machines.heavy_feeder.VerticalStack(*items*, *cog_factor=1.0*)[](../../../../../source-code/PyBM/utils/mass_items.py)  
Bases: `Stack`

Represents a vertical stack of mass items.

*property *h  
\[m\] Get the height of the vertical stack.

&nbsp;

*class *PyBM.machines.heavy_feeder.massItem[](../../../../../source-code/PyBM/utils/mass_items.py)  
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

get_I() → float[](../../../../../source-code/PyBM/utils/mass_items.py)  
\[kg.m2\] Get the inertia around the center of gravity.

set_I(*value: float*)[](../../../../../source-code/PyBM/utils/mass_items.py)  
\[kg.m2\] Set the inertia around the center of gravity.

I_shifted(*offset*)[](../../../../../source-code/PyBM/utils/mass_items.py)  
Get the inertia around an offset point.

Parameters:  
**offset** – \[m\] distance from stack CoG

Returns:  
Inertia around offset point \[kg.m2\]

&nbsp;

PyBM.machines.heavy_feeder.design_loads[](../../../../../source-code/PyBM/machines/heavy_feeder/tower_check.py)  

&nbsp;

PyBM.machines.heavy_feeder.Hs_design* = 2.5*[](../../../../../source-code/PyBM/machines/heavy_feeder/tower_check.py)  

&nbsp;

PyBM.machines.heavy_feeder.unity_checks_tower(*tower: [PyBM.utils.mass_items.massItem](../../utils/mass_items/index.md#PyBM.utils.mass_items.massItem "PyBM.utils.mass_items.massItem")*, *tbic: [PyBM.utils.mass_items.massItem](../../utils/mass_items/index.md#PyBM.utils.mass_items.massItem "PyBM.utils.mass_items.massItem") = None*, *lifting_tool: [PyBM.utils.mass_items.massItem](../../utils/mass_items/index.md#PyBM.utils.mass_items.massItem "PyBM.utils.mass_items.massItem") = None*, *Hs: float = None*) → numpy.array[](../../../../../source-code/PyBM/machines/heavy_feeder/tower_check.py)  
Calculate unity checks of a different tower w.r.t. the heavy feeder design conditions.

Parameters:  
- **tower** ([*massItem*](#PyBM.machines.heavy_feeder.massItem "PyBM.machines.heavy_feeder.massItem")) – Tower properties

- **tbic** ([*massItem*](#PyBM.machines.heavy_feeder.massItem "PyBM.machines.heavy_feeder.massItem")) – TBIC properties, by default the vinyard TBIC will be used.

- **lifting_tool** ([*massItem*](#PyBM.machines.heavy_feeder.massItem "PyBM.machines.heavy_feeder.massItem")) – Lifting tool properties, by default the vinyard tool will be used.

- **Hs** (*float*) – \[m\] Significant Waave height used for acceleration scaling, defaults to 2.5m

Returns:  
list of unity checks \[Fz, Mx, My\]

Return type:  
np.array

&nbsp;

PyBM.machines.heavy_feeder.g* = 9.81*[](../../../../../source-code/PyBM/constants.py)  

&nbsp;

PyBM.machines.heavy_feeder.rho* = 1025*[](../../../../../source-code/PyBM/constants.py)  
