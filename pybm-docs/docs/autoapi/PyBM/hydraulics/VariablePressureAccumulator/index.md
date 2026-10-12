<!-- Source: https://docs.app.barge-master.com/autoapi/PyBM/hydraulics/VariablePressureAccumulator/index.html -->

# PyBM.hydraulics.VariablePressureAccumulator

## Attributes

|                                                                                                                                                    |     |
|----------------------------------------------------------------------------------------------------------------------------------------------------|-----|
| [`normal_symbols`](#PyBM.hydraulics.VariablePressureAccumulator.normal_symbols "PyBM.hydraulics.VariablePressureAccumulator.normal_symbols")       |     |
| [`positive_symbols`](#PyBM.hydraulics.VariablePressureAccumulator.positive_symbols "PyBM.hydraulics.VariablePressureAccumulator.positive_symbols") |     |
| [`syms`](../index.md#PyBM.hydraulics.VariablePressureAccumulator.syms "PyBM.hydraulics.VariablePressureAccumulator.syms")                          |     |
| [`d_accu_T700`](#PyBM.hydraulics.VariablePressureAccumulator.d_accu_T700 "PyBM.hydraulics.VariablePressureAccumulator.d_accu_T700")                |     |
| [`V_accu_T700`](#PyBM.hydraulics.VariablePressureAccumulator.V_accu_T700 "PyBM.hydraulics.VariablePressureAccumulator.V_accu_T700")                |     |
| [`V_nitro_T700`](#PyBM.hydraulics.VariablePressureAccumulator.V_nitro_T700 "PyBM.hydraulics.VariablePressureAccumulator.V_nitro_T700")             |     |

## Classes

|                                                                                                                                                                                     |              |
|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------|
| [`VariablePressureAccumulator`](#PyBM.hydraulics.VariablePressureAccumulator.VariablePressureAccumulator "PyBM.hydraulics.VariablePressureAccumulator.VariablePressureAccumulator") | All symbols: |

## Functions

|                                                                                                                                  |     |
|----------------------------------------------------------------------------------------------------------------------------------|-----|
| [`guesser`](#PyBM.hydraulics.VariablePressureAccumulator.guesser "PyBM.hydraulics.VariablePressureAccumulator.guesser")(symbols) |     |

## Module Contents

PyBM.hydraulics.VariablePressureAccumulator.normal_symbols* = ()*[](../../../../../source-code/PyBM/hydraulics/VariablePressureAccumulator.py)  

&nbsp;

PyBM.hydraulics.VariablePressureAccumulator.positive_symbols* = ()*[](../../../../../source-code/PyBM/hydraulics/VariablePressureAccumulator.py)  

&nbsp;

PyBM.hydraulics.VariablePressureAccumulator.syms[](../../../../../source-code/PyBM/hydraulics/VariablePressureAccumulator.py)  

&nbsp;

PyBM.hydraulics.VariablePressureAccumulator.d_accu_T700* = 0.36*[](../../../../../source-code/PyBM/hydraulics/VariablePressureAccumulator.py)  

&nbsp;

PyBM.hydraulics.VariablePressureAccumulator.V_accu_T700* = 0.25*[](../../../../../source-code/PyBM/hydraulics/VariablePressureAccumulator.py)  

&nbsp;

PyBM.hydraulics.VariablePressureAccumulator.V_nitro_T700* = 4.0*[](../../../../../source-code/PyBM/hydraulics/VariablePressureAccumulator.py)  

&nbsp;

PyBM.hydraulics.VariablePressureAccumulator.guesser(*symbols: list*)[](../../../../../source-code/PyBM/hydraulics/VariablePressureAccumulator.py)  

&nbsp;

*class *PyBM.hydraulics.VariablePressureAccumulator.VariablePressureAccumulator(*\*extra_eq1*, *Ploss_iso=200000.0*, *Ploss_accu=200000.0*, *Ploss_valve=300000.0*, *Ploss_tank=500000.0*, *Floss_ex=0*, *num_solve=False*, *guesses=False*, *\*\*kwargs*)[](../../../../../source-code/PyBM/hydraulics/VariablePressureAccumulator.py)  
All symbols: Pnitro - Nitrogen pressure in the accumulator at midpoint Fact - Max active cylinder force c_f - Contingency factor of required active force, meant for control delay, or pumping pressure loss/gain in the VPA. Usually 1.2 Fdyn - Dynamic forces on cylinder, as required active force. Floss - Extra active force required to overcome losses in the VPA r_acc - Nitrogen pressure loss/gain (ratio) over full stroke of accu (+/-) Fmax - Maximum force of the active + passive cylinder Fmin - Minimum force of the active + passive cylinder Apass - Area of the passive cylinder/chamber P1_loss - Pressure loss in V1 of the VPA P2_loss - Pressure loss in V2 of the VPA P3_loss - Pressure loss in V3 of the VPA P4_loss - Pressure loss in V4 of the VPA Ppas_max - Maximum passive pressure A1 - Area of the tandem cylinder in V1 and V4 in the VPA A2 - Area of the tandem cylinder in V2 and V3 in the VPA

\_syms[](../../../../../source-code/PyBM/hydraulics/VariablePressureAccumulator.py)  

all_eqs[](../../../../../source-code/PyBM/hydraulics/VariablePressureAccumulator.py)  

properties[](../../../../../source-code/PyBM/hydraulics/VariablePressureAccumulator.py)  

*static *syms(*k*)[](../../../../../source-code/PyBM/hydraulics/VariablePressureAccumulator.py)  

prop_dict()[](../../../../../source-code/PyBM/hydraulics/VariablePressureAccumulator.py)  

*static *calc_accu_volume(*A1*, *A2*, *stroke_vpa*, *n_pumps=3*)[](../../../../../source-code/PyBM/hydraulics/VariablePressureAccumulator.py)  

*static *calc_nitro_loss(*A1*, *A2*, *stroke_vpa*, *V_nitro=V_nitro_T700*, *n_pumps=3*)[](../../../../../source-code/PyBM/hydraulics/VariablePressureAccumulator.py)  

*static *calc_accu_stroke(*A1*, *A2*, *stroke_vpa*, *d_accu=d_accu_T700*, *n_pumps=3*, *temp_range=\[273.15, 293.15\]*, *r_accu_fill_inaccuracy=0.04*)[](../../../../../source-code/PyBM/hydraulics/VariablePressureAccumulator.py)  

get_passive_force_steps()[](../../../../../source-code/PyBM/hydraulics/VariablePressureAccumulator.py)  
