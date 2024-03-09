from matrix import Matrix
from agents.agent import Agent
from agents.agent_types.grazers import Grazer
from agents.agent_types.slowboys import SlowBoy
from food import Food
import numpy as np

N_AGENTS = 0
N_GRAZERS = 3
N_SLOWBOYS = 0
N_FOOD = 200


class Model:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.matrix = Matrix()

        self.init_nodes()
        self.init_agents()
        self.init_food()

    def init_nodes(self):
        self.init_food()
        self.init_agents()

    def init_food(self):
        for _ in range(N_FOOD):
            self.generate_food()

    def init_agents(self):
        agents = [
            *[Agent.create_random_agent(self) for _ in range(N_AGENTS)],
            *[Grazer.create_random_agent(self) for _ in range(N_GRAZERS)],
            *[SlowBoy.create_random_agent(self) for _ in range(N_SLOWBOYS)],
        ]
        

        for agent in agents:
            self.matrix.add_node(agent)

    def generate_food(self):
        food_item = Food(
            self,
            x=np.random.randint(self.width),
            y=np.random.randint(self.height),
            color=(0, np.random.randint(255), 0),
        )
        self.matrix.add_node(food_item)

    def __str__(self):
        return str(self.matrix)

    def __repr__(self):
        return repr(self.matrix)

    def update(self):
        for node_type in list(self.matrix.nodes):
            for node in self.matrix.nodes[node_type]:
                node.update()
        self.resolve_interactions()
        self.update_food()
        self.matrix.update()

    def resolve_interactions(self):
        for agents in self.matrix.get_nodes_by_type(Agent):
            for agent in agents:
                other_nodes = self.matrix.get_nodes_by_position(agent.x, agent.y)
                for other in other_nodes:
                    if agent == other:
                        continue
                    if other.__class__ == Food and callable(getattr(other, "eat", None)):
                        agent.eat(other)
                        other.get_eaten()
                    else:
                        agent.interact(other)
                        other.interact(agent)


    def update_food(self):
        if len(self.matrix.food) < N_FOOD:
            self.generate_food()
