<!-- Source: https://docs.app.barge-master.com/autoapi/PyBM/machines/standard_feeder/tower_check/index.html -->

# PyBM.machines.standard_feeder.tower_check

Date: 06-05-2024 Author: CVE Check: XXX

Refs:  
\[1\] TWD-NL-2021-501-C-010-REV-2 - LCD \[2\] TWD-NL-2021-501-R-00-REV-1 - BoD \[3\] TBB_280_6KN_Opt_T1T2_acc \[4\] BM-PR305-EN-2002 LCO Operational BM Standard feeder \[5\] TWD-NL-2021-397-C-110, Standard feeder cylinder limits \[6\] M:EngineeringR&D Projects# PyBMEngineeringSF Tower Check Operational AccelerationsMM400_Op_Accelerations_Rev0.py

## Attributes

|                                                                                                                                                               |     |
|---------------------------------------------------------------------------------------------------------------------------------------------------------------|-----|
| [`design_loads`](#PyBM.machines.standard_feeder.tower_check.design_loads "PyBM.machines.standard_feeder.tower_check.design_loads")                            |     |
| [`Hs_design_transit`](#PyBM.machines.standard_feeder.tower_check.Hs_design_transit "PyBM.machines.standard_feeder.tower_check.Hs_design_transit")             |     |
| [`Hs_design_operational`](#PyBM.machines.standard_feeder.tower_check.Hs_design_operational "PyBM.machines.standard_feeder.tower_check.Hs_design_operational") |     |
| [`t700`](#PyBM.machines.standard_feeder.tower_check.t700 "PyBM.machines.standard_feeder.tower_check.t700")                                                    |     |
| [`t700_cyl_push_max`](#PyBM.machines.standard_feeder.tower_check.t700_cyl_push_max "PyBM.machines.standard_feeder.tower_check.t700_cyl_push_max")             |     |
| [`t700_cyl_pull_max`](#PyBM.machines.standard_feeder.tower_check.t700_cyl_pull_max "PyBM.machines.standard_feeder.tower_check.t700_cyl_pull_max")             |     |
| [`t700_cyl_pass_max`](#PyBM.machines.standard_feeder.tower_check.t700_cyl_pass_max "PyBM.machines.standard_feeder.tower_check.t700_cyl_pass_max")             |     |
| [`t700_cyl_pull_max_act`](#PyBM.machines.standard_feeder.tower_check.t700_cyl_pull_max_act "PyBM.machines.standard_feeder.tower_check.t700_cyl_pull_max_act") |     |
| [`t700_cyl_push_max_act`](#PyBM.machines.standard_feeder.tower_check.t700_cyl_push_max_act "PyBM.machines.standard_feeder.tower_check.t700_cyl_push_max_act") |     |

## Functions

|                                                                                                                                                                     |     |
|---------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----|
| [`unity_checks_tower`](#PyBM.machines.standard_feeder.tower_check.unity_checks_tower "PyBM.machines.standard_feeder.tower_check.unity_checks_tower")(→ numpy.array) |     |

## Module Contents

PyBM.machines.standard_feeder.tower_check.design_loads[](../../../../../../source-code/PyBM/machines/standard_feeder/tower_check.py)  

&nbsp;

PyBM.machines.standard_feeder.tower_check.Hs_design_transit* = 2.5*[](../../../../../../source-code/PyBM/machines/standard_feeder/tower_check.py)  

&nbsp;

PyBM.machines.standard_feeder.tower_check.Hs_design_operational* = 2.0*[](../../../../../../source-code/PyBM/machines/standard_feeder/tower_check.py)  

&nbsp;

PyBM.machines.standard_feeder.tower_check.t700[](../../../../../../source-code/PyBM/machines/standard_feeder/tower_check.py)  

&nbsp;

PyBM.machines.standard_feeder.tower_check.t700_cyl_push_max[](../../../../../../source-code/PyBM/machines/standard_feeder/tower_check.py)  

&nbsp;

PyBM.machines.standard_feeder.tower_check.t700_cyl_pull_max[](../../../../../../source-code/PyBM/machines/standard_feeder/tower_check.py)  

&nbsp;

PyBM.machines.standard_feeder.tower_check.t700_cyl_pass_max[](../../../../../../source-code/PyBM/machines/standard_feeder/tower_check.py)  

&nbsp;

PyBM.machines.standard_feeder.tower_check.t700_cyl_pull_max_act* = 1431000.0*[](../../../../../../source-code/PyBM/machines/standard_feeder/tower_check.py)  

&nbsp;

PyBM.machines.standard_feeder.tower_check.t700_cyl_push_max_act* = 1431000.0*[](../../../../../../source-code/PyBM/machines/standard_feeder/tower_check.py)  

&nbsp;

PyBM.machines.standard_feeder.tower_check.unity_checks_tower(*tower: [PyBM.utils.mass_items.massItem](../../../utils/mass_items/index.md#PyBM.utils.mass_items.massItem "PyBM.utils.mass_items.massItem")*, *tbic: [PyBM.utils.mass_items.massItem](../../../utils/mass_items/index.md#PyBM.utils.mass_items.massItem "PyBM.utils.mass_items.massItem") = None*, *lifting_tool: [PyBM.utils.mass_items.massItem](../../../utils/mass_items/index.md#PyBM.utils.mass_items.massItem "PyBM.utils.mass_items.massItem") = None*, *Hs_transit: float = None*, *Hs_operational: float = None*, *debug=False*) → numpy.array[](../../../../../../source-code/PyBM/machines/standard_feeder/tower_check.py)  
