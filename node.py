import numpy as np
from uuid import uuid4

class Node:
    def __init__(self, model, x, y, color=(4, 2, 0)):
        self.model = model
        self.id = uuid4()
        self.x = x
        self.y = y
        self.color = color

    def set_random_color(self):
        self.color = tuple(np.random.choice(range(256), size=3))

    def set_color(self, color: tuple):
        self.color = color

    def update(self):
        pass

    @classmethod
    def create_random_node(cls, model):
        x = np.random.randint(model.width)
        y = np.random.randint(model.height)
        color = tuple(np.random.randint(256, size=3))
        ag = cls(model, x, y, color)
        return ag

    @classmethod
    def _create_pos_str(cls, x, y):
        return f"({x}, {y})"

    @property
    def pos_str(self):
        return self._create_pos_str(self.x, self.y)

    @classmethod
    def position_to_pos_str(cls, x, y):
        return cls._create_pos_str(x, y)

    def __str__(self):
        return f"{self.__class__.__name__}({self.x}, {self.y}, {self.color}) -- {self.id}"
    
    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def interact(self, other):
        pass
