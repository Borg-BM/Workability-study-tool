"""
Heavy feeder capacity check example

Author: CBR
Date: 30-03-2023
"""

from PyBM.machines.heavy_feeder import unity_checks_tower
from PyBM.utils import HorizontalStack, Tower, VerticalStack

# Define tower sections
bottom_split = Tower(h=40, m=700e3, D=9, h_cog=20)
mid_split = Tower(h=60, m=600e3, D=9, h_cog=30)
top_split = Tower(h=60, m=500e3, D=8, h_cog=30)

# Check unity checks for each tower section
for tower in [bottom_split, mid_split, top_split]:
    print(unity_checks_tower(tower))


# Stack 2 sections vertically
bottom_mid = VerticalStack([bottom_split, mid_split])

# Check unity checks for the stack
print(unity_checks_tower(bottom_mid))

# Salt & Pepper setup
s_p = HorizontalStack([bottom_split, mid_split], spacing=10)
print(unity_checks_tower(s_p))
