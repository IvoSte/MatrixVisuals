import numpy as np
from agents.agent import Agent
from node import Node

class Flower(Agent):
    def __init__(self, model, x, y, color=(255, 255, 255)):
        super().__init__(model, x, y, color)
        self.fade_rate = 0
        self.grow_rate = 0.001

    def move(self, dx=None, dy=None):
        pass

    @classmethod
    def create_random_node(cls, model):
        x = np.random.randint(model.width)
        y = np.random.randint(model.height)
        color = tuple(np.random.randint(256, size=3))
        ag = cls(model, x, y, color)
        return ag

    def drop_pheromone(self):
        pass

    def grow(self):
        # Chance to grow to nearby random tile if it's empty
        dx = np.random.choice([-1, 0, 1])
        dy = np.random.choice([-1, 0, 1])

        if np.random.rand() < self.grow_rate:
            if self.model.matrix.is_empty_for_type((self.x + dx) % self.model.width, (self.y + dy) % self.model.height, Flower):
                self.model.matrix.add_node(
                    Flower(self.model, (self.x + dx) % self.model.width, (self.y + dy) % self.model.height, self.color)
                )

    def update(self):
        self.grow()

    def interact(self, other: Node):
        if other.__class__.__name__ == "Grazer":
            self.model.matrix.remove_node(self)