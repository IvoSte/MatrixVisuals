import numpy as np
from agents.agent import Agent


class Automaton(Agent):

    def __init__(self, model, x=None, y=None, color=(255, 255, 255)):
        super().__init__(model, x, y, color)
        self.neighbourhood_type = "moore"  # or "von_neumann"
        self.neighbour_coordinates = []

    def function(self):
        pass

    def get_neighbour_coordinates(self):
        if self.neighbourhood_type == "moore":
            return [
                (self.x + dx, self.y + dy)
                for dx in [-1, 0, 1]
                for dy in [-1, 0, 1]
                if (dx != 0 or dy != 0)
            ]
        elif self.neighbourhood_type == "von_neumann":
            return [
                (self.x + dx, self.y + dy)
                for dx in [-1, 0, 1]
                for dy in [-1, 0, 1]
                if (dx == 0 or dy == 0) and (dx != 0 or dy != 0)
            ]

    def update(self):
        self.function()

    def interact(self, other):
        pass
