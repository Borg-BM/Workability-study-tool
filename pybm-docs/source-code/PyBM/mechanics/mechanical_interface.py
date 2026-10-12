from abc import ABC, abstractmethod

class MechanicalInterface(ABC):
    def __init__(self, min_pos, max_pos) -> None:

        self.min_pos = min_pos

        self.max_pos = max_pos

    @abstractmethod

    def L_cylinder(self, effective_disp):
        """Return cylinder length for given compensation length.

        :param effective_disp: [m] Displacement to compensate for.
        """
        pass

    @abstractmethod

    def force_ratio(self, effective_disp):
        """Return ratio of Cylinder Force / External force for a given position.

        :param effective_disp: [m] Displacement to compensate for.
        """
        pass
