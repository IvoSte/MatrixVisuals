import numpy as np
from turbocolor import turbo_colormap_data as turbo

TOROIDAL = True


class Agent:
    def __init__(self, model, x, y, color=(255, 255, 255)):
        self.model = model
        self.matrix = model.matrix
        self.x = x
        self.y = y
        self.color = color

    def update(self):
        self.move()

    def move(self, dx=None, dy=None):
        if dx is None:
            dx = np.random.choice([-1, 0, 1])
        if dy is None:
            dy = np.random.choice([-1, 0, 1])

        if TOROIDAL:
            self.x = (self.x + dx) % self.matrix.x
            self.y = (self.y + dy) % self.matrix.y
        else:
            self.x = max(0, min(self.matrix.x - 1, self.x + dx))
            self.y = max(0, min(self.matrix.y - 1, self.y + dy))

    def __str__(self):
        return f"{type(self)} ({self.x}, {self.y}) with color {self.color} --"


class Grazer(Agent):
    def __init__(
        self, matrix, x=None, y=None, color=(255, 255, 255), chromosome: list = None
    ):
        super().__init__(matrix, x, y, color)
        self.chromosome = (
            chromosome
            if chromosome is not None
            else [np.random.rand() for _ in range(6)]
        )
        self.move_probabilities = self.chromosome_to_move_probabilities()
        self.energy = np.random.randint(255)
        self.set_position(x, y)
        self.color = self.energy_to_color()

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
        if self.energy >= 255:
            self.energy -= 1
        if self.energy < 0:
            self.energy = 255
        self.energy -= 1
        self.color = self.energy_to_color()

    def chromosome_to_color(self):
        color = [int(turbo[self.energy] * 255) for turbo in self.chromosome]
        return tuple(color)

    def energy_to_color(self):
        rgb_color = [int(srgb_color * 255) for srgb_color in turbo[self.energy]]
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

    def eat(self, food):
        if self.x == food.x and self.y == food.y:
            self.energy += 1
            return True
        return False
