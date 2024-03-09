import numpy as np
from pheromone import Pheromone
from agents.agent import Agent

class SlowBoy(Agent):
    def __init__(self, model, x=None, y=None, color=(255, 255, 255)):
        super().__init__(model, x, y, color)
        self.fade_rate = 2

    def move(self, dx=None, dy=None):
        if dx is None:
            dx = np.random.choice([-1, 0, 1], p=[0.015,0.98,0.005])
        if dy is None:
            dy = np.random.choice([-1, 0, 1], p=[0.005,0.98,0.015])
        super().move(dx, dy)

    def drop_pheromone(self):
        # Add a new pheromone to the matrix in Von Neumann neighborhood
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if abs(dx) + abs(dy) == 1 or (dx == 0 and dy == 0):
                    self.model.matrix.add_node(
                        Pheromone(
                            (self.x + dx) % self.matrix.x,
                            (self.y + dy) % self.matrix.y,
                            self.id,
                            self.color,
                            self.fade_rate,
                        )
                    )

    def update(self):
        self.move()
        self.drop_pheromone()