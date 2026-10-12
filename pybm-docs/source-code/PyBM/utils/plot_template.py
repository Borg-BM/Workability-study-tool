import matplotlib as mpl
from cycler import cycler

bm_colors = [
    (29, 97, 152),
    (243, 112, 61),
    (128, 130, 133),
    (0, 40, 98),
    (241, 90, 41),
    (188, 190, 192),
    (58, 71, 101),
    (247, 148, 30),
    (65, 64, 66),
    (142, 216, 248),
]

colors = []

for c in bm_colors:

    c = tuple([x / 255 for x in c])

    colors.append(c)

bm_cycler = cycler(color=colors)

mpl.rcParams["axes.prop_cycle"] = bm_cycler
