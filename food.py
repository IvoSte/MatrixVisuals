from node import Node
import numpy as np

class Food(Node):
    def __init__(self, model, x, y, color=(0, 255, 0)):
        super().__init__(model, x, y, color)

    def get_eaten(self):
        # self.model.matrix.remove_node(self)

        # Get another random position, so as to grow in a new spot
        # Faster than throwing it away and creating a new one
        self.x = np.random.randint(self.model.width)
        self.y = np.random.randint(self.model.height)

    @classmethod
    def create_random_node(cls, model):
        x = np.random.randint(model.width)
        y = np.random.randint(model.height)
        color = (0, 255, 0)
        ag = cls(model, x, y, color)
        return ag


    def interact(self, other: Node):
        if other.__class__.__name__ == "Grazer":
            self.get_eaten()
