
from typing import Any
from uuid import uuid4

FADE_THRESHOLD = 10

class Pheromone:
    def __init__(self, x, y, owner, color: tuple, fade_rate: float = 1):
        self.id = uuid4()
        self.owner = owner
        self.x = x
        self.y = y
        self.color = color # (r, g, b)
        self.fade_rate = fade_rate

    def fade(self):
        self.color = tuple(int(max(0, c - self.fade_rate)) for c in self.color)

    def is_faded(self):
        return all(c <= FADE_THRESHOLD for c in self.color)

    def is_owner(self, agent):
        return self.owner == agent

    def __repr__(self):
        return f"Pheromone({self.x}, {self.y}, {self.color})"
    
    def __str__(self):
        return f"Pheromone({self.x}, {self.y}, {self.color})"
    
    def __eq__(self, other: Any):
        if not isinstance(other, Pheromone):
            return False
        return self.id == other.id
    
