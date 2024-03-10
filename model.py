from matrix import Matrix
from agents.agent import Agent
from agents.agent_types.grazers import Grazer
from agents.agent_types.slowboys import SlowBoy
from agents.agent_types.flower import Flower
from food import Food
import numpy as np

N_AGENTS = 0
N_GRAZERS = 2
N_SLOWBOYS = 0
N_FOOD = 0
N_FLOWERS = 2


class Model:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.matrix = Matrix()

        self.init_nodes()

    def init_nodes(self):
        nodes = [
            *[Agent.create_random_node(self) for _ in range(N_AGENTS)],
            *[Grazer.create_random_node(self) for _ in range(N_GRAZERS)],
            *[SlowBoy.create_random_node(self) for _ in range(N_SLOWBOYS)],
            *[Food.create_random_node(self) for _ in range(N_FOOD)],
            *[Flower.create_random_node(self) for _ in range(N_FLOWERS)]
        ]

        for node in nodes:
            self.matrix.add_node(node)

    def update(self):
        for node_type in list(self.matrix.nodes):
            for node in self.matrix.nodes[node_type]:
                node.update()

        # TODO: This resolve interactions should be part of the previous loop
        self.resolve_interactions()
        self.matrix.update()

    def resolve_interactions(self):
        # TODO: Fix duplicate interactions

        for agent in self.matrix.get_nodes_by_type(Agent):
            other_nodes = self.matrix.get_nodes_by_position(agent.x, agent.y)
            for other in other_nodes:
                if agent == other:
                    continue
                agent.interact(other)
                other.interact(agent)

    def __str__(self):
        return str(self.matrix)

    def __repr__(self):
        return repr(self.matrix)