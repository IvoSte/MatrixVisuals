from agents.agent_types.grazers import Grazer


class LoopyGrazer(Grazer):
    def __init__(
        self, model, x=None, y=None, color=(255, 255, 255), chromosome: list = None
    ):
        super().__init__(model, x, y, color)

    def move(self, dx=None, dy=None):
        super().move(dx, dy)

    def update(self):
        self.move()
        if self.energy > 255:
            self.energy = 255
        if self.energy < 0:
            self.energy = 255
        self.energy -= 3
        self.color = self.energy_to_color()
        self.drop_pheromone()
