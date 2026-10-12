<!-- Source: https://docs.app.barge-master.com/autoapi/PyBM/utils/mass_items/index.html -->

# PyBM.utils.mass_items

## Classes

|                                                                                                     |                                                                             |
|-----------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------|
| [`massItem`](#PyBM.utils.mass_items.massItem "PyBM.utils.mass_items.massItem")                      | Represents a mass item with height, mass, and center of gravity properties. |
| [`Tower`](#PyBM.utils.mass_items.Tower "PyBM.utils.mass_items.Tower")                               | Represents a tower mass item.                                               |
| [`Stack`](#PyBM.utils.mass_items.Stack "PyBM.utils.mass_items.Stack")                               | Abstract base class for a stack of mass items.                              |
| [`VerticalStack`](#PyBM.utils.mass_items.VerticalStack "PyBM.utils.mass_items.VerticalStack")       | Represents a vertical stack of mass items.                                  |
| [`HorizontalStack`](#PyBM.utils.mass_items.HorizontalStack "PyBM.utils.mass_items.HorizontalStack") | Represents a horizontal stack of mass items.                                |

## Module Contents

*class *PyBM.utils.mass_items.massItem[](../../../../../source-code/PyBM/utils/mass_items.py)  
Represents a mass item with height, mass, and center of gravity properties.

h*: float*[](../../../../../source-code/PyBM/utils/mass_items.py)  
\[m\] height

m*: float*[](../../../../../source-code/PyBM/utils/mass_items.py)  
\[kg\] mass

h_cog*: float = 0*[](../../../../../source-code/PyBM/utils/mass_items.py)  
\[m\] Height of CoG

x_cog*: float = 0*[](../../../../../source-code/PyBM/utils/mass_items.py)  
\[m\] Longitudinal offset of CoG

y_cog*: float = 0*[](../../../../../source-code/PyBM/utils/mass_items.py)  
\[m\] transverse offset of CoG

I*: float = 0*[](../../../../../source-code/PyBM/utils/mass_items.py)  
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

*class *PyBM.utils.mass_items.Tower[](../../../../../source-code/PyBM/utils/mass_items.py)  
Bases: [`massItem`](#PyBM.utils.mass_items.massItem "PyBM.utils.mass_items.massItem")

Represents a tower mass item.

D*: float = 0*[](../../../../../source-code/PyBM/utils/mass_items.py)  
\[m\] Diameter of Tower

*property *I[](../../../../../source-code/PyBM/utils/mass_items.py)  
Get the inertia around the center of gravity of the tower.

&nbsp;

*class *PyBM.utils.mass_items.Stack(*items*)[](../../../../../source-code/PyBM/utils/mass_items.py)  
Bases: `abc.ABC`

Abstract base class for a stack of mass items.

items[](../../../../../source-code/PyBM/utils/mass_items.py)  

*property *m[](../../../../../source-code/PyBM/utils/mass_items.py)  
Get the total mass of the stack.

Returns:  
The total mass of the stack in units of meters \[kg\].

Return type:  
float

*abstractmethod *h()[](../../../../../source-code/PyBM/utils/mass_items.py)  
\[m\] Abstract method to get the height of the stack.

*property *h_cog[](../../../../../source-code/PyBM/utils/mass_items.py)  
\[m\] Get the height of the center of gravity of the stack.

*property *x_cog[](../../../../../source-code/PyBM/utils/mass_items.py)  
\[m\] Get the longitudinal offset of the center of gravity of the stack.

*property *y_cog[](../../../../../source-code/PyBM/utils/mass_items.py)  
\[m\] Get the transverse offset of the center of gravity of the stack.

*property *I[](../../../../../source-code/PyBM/utils/mass_items.py)  
Get the inertia around the center of gravity of the stack.

Returns:  
Inertia around the center of gravity \[kg.m2\]

I_shifted(*offset*)[](../../../../../source-code/PyBM/utils/mass_items.py)  
Get the inertia around an offset point.

Parameters:  
**offset** – \[m\] distance from stack CoG

Returns:  
Inertia around offset point \[kg.m2\]

\_\_str\_\_() → str[](../../../../../source-code/PyBM/utils/mass_items.py)  
Get a string representation of the stack.

&nbsp;

*class *PyBM.utils.mass_items.VerticalStack(*items*, *cog_factor=1.0*)[](../../../../../source-code/PyBM/utils/mass_items.py)  
Bases: [`Stack`](#PyBM.utils.mass_items.Stack "PyBM.utils.mass_items.Stack")

Represents a vertical stack of mass items.

*property *h[](../../../../../source-code/PyBM/utils/mass_items.py)  
\[m\] Get the height of the vertical stack.

&nbsp;

*class *PyBM.utils.mass_items.HorizontalStack(*items*, *spacing*, *cog_factor=1.0*)[](../../../../../source-code/PyBM/utils/mass_items.py)  
Bases: [`Stack`](#PyBM.utils.mass_items.Stack "PyBM.utils.mass_items.Stack")

Represents a horizontal stack of mass items.

*property *h[](../../../../../source-code/PyBM/utils/mass_items.py)  
\[m\] Get the height of the horizontal stack.

\_\_str\_\_() → str[](../../../../../source-code/PyBM/utils/mass_items.py)  
Get a string representation of the horizontal stack.
