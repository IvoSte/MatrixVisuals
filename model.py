from matrix import Matrix
from agents.agent import Agent
from agents.agent_types.grazers import Grazer
from agents.agent_types.slowboys import SlowBoy
from food import Food
import numpy as np

N_AGENTS = 0
N_GRAZERS = 1
N_SLOWBOYS = 0
N_FOOD = 1


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
        self.update_food()
        self.matrix.update()

    def resolve_interactions(self):
        # print("resolving interactions...")
        # print(self.matrix.nodes)
        for row in self.matrix.nodes:
            for node in row:
                if node.objects != None and len(node.objects) > 1:
                    agents = [obj for obj in node.objects if isinstance(obj, Agent)]
                    food = [obj for obj in node.objects if isinstance(obj, Food)]

                    for idx, agent in enumerate(agents):
                        for food_item in food:
                            agent.eat(food_item)
                            food_item.get_eaten()
                            # TODO: Check if this actually removes the food item from the matrix
                            self.matrix.food.remove(food_item)
                            # print(f"food interaction: {agent} eats {food_item}")
                        for other in agents[idx:]:
                            if agent != other:
                                agent.interact(other)
                                other.interact(agent)
                            # print(f"agent interaction: {agent} interacts with {other}")

    def update_food(self):
        if len(self.matrix.food) < N_FOOD:
            self.generate_food()
