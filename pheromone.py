
from typing import Any
from uuid import uuid4
from node import Node

FADE_THRESHOLD = 10

class Pheromone(Node):
    def __init__(self, model, x, y, owner, color: tuple, fade_rate: float = 1):
        super().__init__(model, x, y, color)

        self._color = color
        self.id = uuid4()
        self.owner = owner
        self.fade_rate = fade_rate
        self.value = 100

    @property
    def color(self):
        return tuple([x * (self.value / 100) for x in self._color])

    @color.setter
    def color(self, value):
        self._color = value

    def fade(self):
        self.value = max(0, self.value - self.fade_rate)

    def is_faded(self):
        return self.value <= FADE_THRESHOLD

    def is_owner(self, agent):
        return self.owner == agent.id
    
    def __eq__(self, other: Any):
        if not isinstance(other, Pheromone):
            return False
        return self.id == other.id

    def update(self):
        self.fade()
        if self.is_faded():
            self.model.matrix.nodes[Pheromone].remove(self)
    
