import numpy as np
from pheromone import Pheromone
from uuid import uuid4
from node import Node

TOROIDAL = True


class Agent(Node):
    def __init__(self, model, x, y, color=(255, 255, 255)):
        super().__init__(model, x, y, color)

        self.id = uuid4()
        self.model = model
        self.matrix = model.matrix
        self.fade_rate = 25

    def drop_pheromone(self):
        # Make sure each agent can only have one pheromone on each tile
        for node in list(self.model.matrix.get_nodes_by_position(self.x, self.y)):
            if isinstance(node, Pheromone) and node.is_owner(self):
                self.model.matrix.remove_node(node)

        # Add a new pheromone to the matrix
        self.model.matrix.add_node(
            Pheromone(self.model, self.x, self.y, self.id, self.color, self.fade_rate)
        )

    @classmethod
    def create_random_node(cls, model):
        x = np.random.randint(model.width)
        y = np.random.randint(model.height)
        color = tuple(np.random.randint(256, size=3))
        ag = cls(model, x, y, color)
        return ag

    def update(self):
        self.move()
        self.drop_pheromone()

    def move(self, dx=None, dy=None):
        if dx is None:
            dx = np.random.choice([-1, 0, 1])
        if dy is None:
            dy = np.random.choice([-1, 0, 1])

        if TOROIDAL:
            self.x = (self.x + dx) % self.model.width
            self.y = (self.y + dy) % self.model.height
        else:
            self.x = max(0, min(self.model.width - 1, self.x + dx))
            self.y = max(0, min(self.model.height - 1, self.y + dy))

    def __str__(self):
        return f"{type(self)} ({self.x}, {self.y}) with color {self.color} --"
