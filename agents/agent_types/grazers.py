import numpy as np
from turbocolor import turbo_colormap_data as turbo
from agents.agent import Agent

class Grazer(Agent):
    def __init__(
        self, model, x=None, y=None, color=(255, 255, 255), chromosome: list = None
    ):
        super().__init__(model, x, y, color)
        self.chromosome = (
            chromosome
            if chromosome is not None
            else [np.random.rand() for _ in range(6)]
        )
        self.move_probabilities = self.chromosome_to_move_probabilities()
        self.energy = np.random.randint(255)
        self.set_position(x, y)
        self.color = self.energy_to_color()
        self.fade_rate = 1

    @classmethod
    def create_random_node(cls, model):
        x = np.random.randint(model.width)
        y = np.random.randint(model.height)
        color = tuple(np.random.randint(256, size=3))
        ag = cls(model, x, y, color)
        return ag

    def set_position(self, x=None, y=None):
        self.x = x if x is not None else np.random.randint(self.matrix.x)
        self.y = y if y is not None else np.random.randint(self.matrix.y)

    def chromosome_to_move_probabilities(self):
        return [
            np.array(self.chromosome[:3]) / sum(self.chromosome[:3]),
            np.array(self.chromosome[3:]) / sum(self.chromosome[3:]),
        ]

    def move(self, dx=None, dy=None):
        if dx is None:
            dx = np.random.choice([-1, 0, 1], p=self.move_probabilities[0])
        if dy is None:
            dy = np.random.choice([-1, 0, 1], p=self.move_probabilities[1])
        super().move(dx, dy)

    def update(self):
        self.move()
        if self.energy > 255:
            self.energy = 255
        if self.energy < 0:
            self.energy = 0
        self.energy -= 0.5
        self.color = self.energy_to_color()
        self.drop_pheromone()

    def chromosome_to_color(self):
        color = [int(turbo[int(self.energy)] * 255) for turbo in self.chromosome]
        return tuple(color)

    def energy_to_color(self):
        rgb_color = [int(srgb_color * 255) for srgb_color in turbo[int(self.energy)]]
        return tuple(rgb_color)

    def hgt_send(self):
        return self.chromosome

    def hgt_receive(self, chromosome):
        self.chromosome = chromosome
        self.move_probabilities = self.chromosome_to_move_probabilities()
        self.color = self.energy_to_color()

    def interact(self, other):
        if isinstance(other, Grazer):
            if self.energy >= other.energy:
                other.hgt_receive(self.hgt_send())
                # self.energy -= other.energy # interesting for dynamics #note
        elif other.__class__.__name__ == 'Food':
            self.eat(other)
        elif other.__class__.__name__ == 'Flower':
            self.eat(other)

    def eat(self, food):
        if self.x == food.x and self.y == food.y:
            self.energy += 150
            return True
        return False
