from dataclasses import dataclass
import numpy as np
from typing import Any

@dataclass
class Node:
    model: Any # Should be of type Model, but gives circular import error (how to fix my god I always get this just for trying to make things nice)
    x: int
    y: int
    color: tuple[int, int, int] = (4, 2, 0)

    def set_random_color(self):
        self.color = tuple(np.random.choice(range(256), size=3))

    def set_color(self, color: tuple):
        self.color = color

    def update(self):
        pass

    def __str__(self):
        return f"Node({self.x}, {self.y}, {self.color})"
    
    def __repr__(self):
        return f"Node({self.x}, {self.y}, {self.color})"
