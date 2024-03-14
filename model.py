from agents.agent_types.loopy_grazer import LoopyGrazer
from matrix import Matrix
from agents.agent import Agent
from agents.agent_types.grazers import Grazer
from agents.agent_types.slowboys import SlowBoy
from agents.agent_types.flower import Flower
from agents.agent_types.walker import Walker
from food import Food
import numpy as np
from agent_factory import AgentFactory

N_WALKERS = 0
N_GRAZERS = 2
N_SLOWBOYS = 0
N_FOOD = 0
N_FLOWERS = 2


class Model:
    def __init__(self, model_config, agents_config):
        self.width = model_config["NODES_X"]
        self.height = model_config["NODES_Y"]

        self.matrix = Matrix()

        self.init_nodes(agents_config)

    def init_nodes(self, agents_config):
        agent_factory = AgentFactory()
        nodes = agent_factory.build_agents(self, agents_config)

        for node in nodes:
            self.matrix.add_node(node)

    def update(self):
        for node_type in list(self.matrix.nodes_by_type):
            for node in self.matrix.nodes_by_type[node_type]:
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
