<!-- Source: https://docs.app.barge-master.com/autoapi/PyBM/marine/machines/HeavyFeederSurgeSway/index.html -->

# PyBM.marine.machines.HeavyFeederSurgeSway

Heavy Feeder class to compensate Surge and Sway motion of a POI

## Classes

|                                                                                                                                                            |                                                                  |
|------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------|
| [`HeavyFeederSurgeSway`](#PyBM.marine.machines.HeavyFeederSurgeSway.HeavyFeederSurgeSway "PyBM.marine.machines.HeavyFeederSurgeSway.HeavyFeederSurgeSway") | Helper class that provides a standard way to create an ABC using |

## Module Contents

*class *PyBM.marine.machines.HeavyFeederSurgeSway.HeavyFeederSurgeSway(*position*, *orientation*, *comp_point=\[0, 0, 0\]*)[](../../../../../../source-code/PyBM/marine/machines/HeavyFeederSurgeSway.py)  
Bases: [`PyBM.marine.machines.HeavyFeeder.HeavyFeeder`](../HeavyFeeder/index.md#PyBM.marine.machines.HeavyFeeder.HeavyFeeder "PyBM.marine.machines.HeavyFeeder.HeavyFeeder")

Helper class that provides a standard way to create an ABC using inheritance.

workability_checks[](../../../../../../source-code/PyBM/marine/machines/HeavyFeederSurgeSway.py)  

get_POI()[](../../../../../../source-code/PyBM/marine/machines/HeavyFeederSurgeSway.py)  
Return cylinder positions w.r.t. RAO definitions.

apply_machine_dofs(*rao*)[](../../../../../../source-code/PyBM/marine/machines/HeavyFeederSurgeSway.py)  

check_stroke_limit(*motion_at_poi*)[](../../../../../../source-code/PyBM/marine/machines/HeavyFeederSurgeSway.py)  
