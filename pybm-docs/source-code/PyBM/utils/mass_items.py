import copy
from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass

class massItem:
    """Represents a mass item with height, mass, and center of gravity properties."""

    h: float

    """[m] height"""

    m: float

    """[kg] mass"""

    h_cog: float = 0

    """[m] Height of CoG"""

    x_cog: float = 0

    """[m] Longitudinal offset of CoG"""

    y_cog: float = 0

    """[m] transverse offset of CoG"""

    I: float = 0

    """Inertia around CoG [kg.m2]"""

    def get_I(self) -> float:
        """[kg.m2] Get the inertia around the center of gravity."""
        return self._I

    def set_I(self, value: float):
        """[kg.m2] Set the inertia around the center of gravity."""
        self._I = value

    def I_shifted(self, offset):
        """Get the inertia around an offset point.

        :param offset: [m] distance from stack CoG
        :return: Inertia around offset point [kg.m2]
        """
        return self.I + self.m * offset**2

massItem.I = property(massItem.get_I, massItem.set_I)

@dataclass

class Tower(massItem):
    """Represents a tower mass item."""

    D: float = 0

    """[m] Diameter of Tower"""

    @property

    def I(self):
        """Get the inertia around the center of gravity of the tower."""
        return self.m / 12 * (6 * (self.D**2) / 4 + self.h**2)

    @I.setter
    def I(self, value):
        """Set the inertia around the center of gravity of the tower."""
        pass

class Stack(ABC):
    """Abstract base class for a stack of mass items."""

    def __init__(self, items) -> None:
        """Initialize the stack with a list of mass items."""

        self.items = copy.deepcopy(items)

    @property

    def m(self):
        """Get the total mass of the stack.

        :return: The total mass of the stack in units of meters [kg].
        :rtype: float
        """
        return sum(item.m for item in self.items)

    @abstractmethod

    def h(self):
        """[m] Abstract method to get the height of the stack."""
        pass

    @property

    def h_cog(self):
        """[m] Get the height of the center of gravity of the stack."""
        return sum(item.m * item.h_cog_stacked for item in self.items) / self.m

    @property

    def x_cog(self):
        """[m] Get the longitudinal offset of the center of gravity of the stack."""
        return sum(item.m * item.x_cog_stacked for item in self.items) / self.m

    @property

    def y_cog(self):
        """[m] Get the transverse offset of the center of gravity of the stack."""
        return sum(item.m * item.y_cog_stacked for item in self.items) / self.m

    @property

    def I(self):
        """Get the inertia around the center of gravity of the stack.

        :return: Inertia around the center of gravity [kg.m2]
        """
        return sum(
            item.I + item.m * ((self.h_cog - item.h_cog_stacked) ** 2 + (self.x_cog - item.x_cog_stacked) ** 2)
            for item in self.items
        )

    def I_shifted(self, offset):
        """Get the inertia around an offset point.

        :param offset: [m] distance from stack CoG
        :return: Inertia around offset point [kg.m2]
        """
        return self.I + self.m * offset**2

    def __str__(self) -> str:
        """Get a string representation of the stack."""
        temp = f"Stack: m={self.m/1e3:.0f}t, H={self.h:.2f}m, CoG={self.h_cog:.2f}m\n  "
        return temp + "\n  ".join(map(str, self.items))

class VerticalStack(Stack):
    """Represents a vertical stack of mass items."""

    def __init__(self, items, cog_factor=1.0) -> None:
        """
        Initialize the vertical stack.

        :param items: [kg] A list of mass items.
        :type items: list
        :param cog_factor: [-] The center of gravity factor, defaults to 1.0.
        :type cog_factor: float, optional
        """
        super().__init__(items)
        h = 0
        for item in self.items:
            item.h_cog_stacked = h + item.h_cog * cog_factor
            item.x_cog_stacked = item.x_cog
            item.y_cog_stacked = item.y_cog
            h = h + item.h

    @property

    def h(self):
        """[m] Get the height of the vertical stack."""
        return sum(item.h for item in self.items)

class HorizontalStack(Stack):
    """Represents a horizontal stack of mass items."""

    def __init__(self, items, spacing, cog_factor=1.0) -> None:
        """
        Initialize the horizontal stack.

        :param items: [kg] A list of mass items to be stacked horizontally.
        :type items: list
        :param spacing: [m] The spacing between each item in the stack.
        :type spacing: float
        :param cog_factor: [-] The center of gravity factor, defaults to 1.0.
        :type cog_factor: float, optional
        """
        super().__init__(items)
        n_items = len(items)

        for i, item in enumerate(self.items):
            item.h_cog_stacked = item.h_cog * cog_factor
            item.x_cog_stacked = (i - (n_items - 1) / 2) * spacing + item.x_cog
            item.y_cog_stacked = item.y_cog

    @property

    def h(self):
        """[m] Get the height of the horizontal stack."""
        return max(item.h for item in self.items)

    def __str__(self) -> str:
        """Get a string representation of the horizontal stack."""
        return (
            super().__str__()
            + f"\n Horizontal CoG:{self.x_cog:.2f} -> CoG Positions: "
            + ", ".join(map(str, [item.x_cog_stacked for item in self.items]))
        )
