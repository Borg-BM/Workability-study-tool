from dataclasses import dataclass

import numpy as np

@dataclass

class POI:

    x: float = 0.0

    """[m] x postion (length) """

    y: float = 0.0

    """[m] y postion (width) """

    z: float = 0.0

    """[m] z postion (height) """

@dataclass

class VesselDimensions:
    # CoG: np.array = [40, 0, ]
    # """[m] CoG pos from [APP, CL, K]"""

    Length: float = 90.0

    """[m] length of vessel, from APP"""

    Depth: float = 13.0

    """[m] depth of vessel, keel to deck"""

    Draft: float = 7.0

    """[m] draft of vessel"""

    Breadth: float = 20.0

    """[m] Breadth of vessel"""
