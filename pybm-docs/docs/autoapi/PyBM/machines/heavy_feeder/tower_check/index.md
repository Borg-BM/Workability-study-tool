<!-- Source: https://docs.app.barge-master.com/autoapi/PyBM/machines/heavy_feeder/tower_check/index.html -->

# PyBM.machines.heavy_feeder.tower_check

Date: 20-03-2023 Date checked: 12-06-2025 Author: CBR Check: AKO

Refs:  
\[1\] TWD-NL-2021-512-C-010-REV-6 Heavy feeder re-design LCD \[2\] TBB_280_6KN_Opt_T1T2_acc

## Attributes

|                                                                                                                              |     |
|------------------------------------------------------------------------------------------------------------------------------|-----|
| [`design_loads`](#PyBM.machines.heavy_feeder.tower_check.design_loads "PyBM.machines.heavy_feeder.tower_check.design_loads") |     |
| [`Hs_design`](#PyBM.machines.heavy_feeder.tower_check.Hs_design "PyBM.machines.heavy_feeder.tower_check.Hs_design")          |     |

## Functions

|                                                                                                                                                               |                                                                                        |
|---------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------|
| [`unity_checks_tower`](#PyBM.machines.heavy_feeder.tower_check.unity_checks_tower "PyBM.machines.heavy_feeder.tower_check.unity_checks_tower")(→ numpy.array) | Calculate unity checks of a different tower w.r.t. the heavy feeder design conditions. |

## Module Contents

PyBM.machines.heavy_feeder.tower_check.design_loads[](../../../../../../source-code/PyBM/machines/heavy_feeder/tower_check.py)  

&nbsp;

PyBM.machines.heavy_feeder.tower_check.Hs_design* = 2.5*[](../../../../../../source-code/PyBM/machines/heavy_feeder/tower_check.py)  

&nbsp;

PyBM.machines.heavy_feeder.tower_check.unity_checks_tower(*tower: [PyBM.utils.mass_items.massItem](../../../utils/mass_items/index.md#PyBM.utils.mass_items.massItem "PyBM.utils.mass_items.massItem")*, *tbic: [PyBM.utils.mass_items.massItem](../../../utils/mass_items/index.md#PyBM.utils.mass_items.massItem "PyBM.utils.mass_items.massItem") = None*, *lifting_tool: [PyBM.utils.mass_items.massItem](../../../utils/mass_items/index.md#PyBM.utils.mass_items.massItem "PyBM.utils.mass_items.massItem") = None*, *Hs: float = None*) → numpy.array[](../../../../../../source-code/PyBM/machines/heavy_feeder/tower_check.py)  
Calculate unity checks of a different tower w.r.t. the heavy feeder design conditions.

Parameters:  
- **tower** ([*massItem*](../../../index.md#PyBM.massItem "PyBM.massItem")) – Tower properties

- **tbic** ([*massItem*](../../../index.md#PyBM.massItem "PyBM.massItem")) – TBIC properties, by default the vinyard TBIC will be used.

- **lifting_tool** ([*massItem*](../../../index.md#PyBM.massItem "PyBM.massItem")) – Lifting tool properties, by default the vinyard tool will be used.

- **Hs** (*float*) – \[m\] Significant Waave height used for acceleration scaling, defaults to 2.5m

Returns:  
list of unity checks \[Fz, Mx, My\]

Return type:  
np.array
