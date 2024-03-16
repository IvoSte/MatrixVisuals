from typing import Any
from uuid import uuid4
from node import Node

import numpy as np


class Pheromone(Node):
    def __init__(
        self,
        model,
        x,
        y,
        owner,
        color: tuple,
        fade_rate: float = 1.0,
        fade_threshold: int = 10,
    ):
        super().__init__(model, x, y, color)

        self._color = np.array(color)
        self.id = uuid4()
        self.owner = owner
        self.fade_rate = fade_rate
        self.value = 100
        self.fade_threshold = fade_threshold

        self.update_on_cycle = 5 # Don't execute the update on every cycle, but every 5 cycles


    @property
    def color(self) -> tuple:
        return tuple(self._color)

    @color.setter
    def color(self, value):
        self._color = value

    def fade(self):
        self._color = self._color - self.fade_rate
        self.value = self.value - self.fade_rate
        
        # Check if any value is lower than 0, then set it to 0
        self._color = np.maximum(self._color, 0)

    def is_faded(self):
        return self.value <= self.fade_threshold

    def is_owner(self, agent):
        return self.owner == agent.id

    def __eq__(self, other: Any):
        if not isinstance(other, Pheromone):
            return False
        return self.id == other.id

    def update(self):
        if self.count_cycle % self.update_on_cycle == 0:
            self.fade()
            if self.is_faded():
                self.model.matrix.remove_node(self)
                # TODO: Check if it self deletes actually
            self.count_cycle = 0
        else:
            self.count_cycle += 1
