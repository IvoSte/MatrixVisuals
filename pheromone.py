from typing import Any
from uuid import uuid4
from node import Node


class Pheromone(Node):
    def __init__(
        self,
        model,
        x,
        y,
        owner,
        color: tuple,
        fade_rate: float = 1,
        fade_threshold: int = 10,
    ):
        super().__init__(model, x, y, color)

        self._color = color
        self.id = uuid4()
        self.owner = owner
        self.fade_rate = fade_rate
        self.value = 100
        self.fade_threshold = fade_threshold

    @property
    def color(self):
        return tuple([x * (self.value / 100) for x in self._color])

    @color.setter
    def color(self, value):
        self._color = value

    def fade(self):
        self.value = max(0, self.value - self.fade_rate)

    def is_faded(self):
        return self.value <= self.fade_threshold

    def is_owner(self, agent):
        return self.owner == agent.id

    def __eq__(self, other: Any):
        if not isinstance(other, Pheromone):
            return False
        return self.id == other.id

    def update(self):
        self.fade()
        if self.is_faded():
            self.model.matrix.remove_node(self)
            # TODO: Check if it self deletes actually
