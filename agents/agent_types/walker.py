import numpy as np
from agents.agent import Agent


class Walker(Agent):
    def __init__(self, model, x=None, y=None, color=(255, 255, 255)):
        super().__init__(model, x, y, color)

        self.set_position(x, y)
        self.color = color
        self.fade_rate = 0.5

    def move(self, dx=None, dy=None):
        if dx is None:
            dx = np.random.choice([-1, 0, 1])
        if dy is None:
            dy = np.random.choice([-1, 0, 1])

        if True:  # TOROIDAL:
            self.x = (self.x + dx) % self.model.width
            self.y = (self.y + dy) % self.model.height
        else:
            self.x = max(0, min(self.model.width - 1, self.x + dx))
            self.y = max(0, min(self.model.height - 1, self.y + dy))
