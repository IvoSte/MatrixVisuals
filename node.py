from dataclasses import dataclass
import numpy as np
from agents.agent import Agent
from food import Food

@dataclass
class Node:
    x: int
    y: int
    color: tuple[int, int, int] = (4, 2, 0)
    objects: list = None

    def set_random_color(self):
        self.color = tuple(np.random.choice(range(256), size=3))

    def set_color(self, color: tuple):
        self.color = color

    def add_object(self, obj):
        if self.objects is None:
            self.objects = []
        if obj not in self.objects:
            self.objects.append(obj)

    def get_agents(self):
        if self.objects is None:
            return None
        return (obj for obj in self.objects if isinstance(obj, Agent))
    
    def get_food(self):
        if self.objects is None:
            return None
        return (obj for obj in self.objects if isinstance(obj, Food))

    def update(self):
        if self.objects is None:
            return
        for obj in self.objects:
            if obj.x != self.x or obj.y != self.y:
                self.objects.remove(obj)
        # print(self.objects)
