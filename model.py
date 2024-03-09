from matrix import Matrix
from node import Node
from agent import Agent
from agent import Grazer
from food import Food
import numpy as np

N_AGENTS = 0
N_GRAZERS = 5
N_FOOD = 0


class Model(object):
    def __init__(self, width, height):
        self.matrix = Matrix(width, height)
        self.init_agents()
        self.init_grazers()
        self.agents = self.grazers
        self.init_food()

    def init_agents(self):
        self.agents = [
            *[
                Agent(
                    self,
                    *tuple(np.random.choice(range(self.matrix.x), size=2)),
                    color=(0, 255, 0),
                )
                for _ in range(N_AGENTS)
            ],
            *[
                Agent(
                    self,
                    *tuple(np.random.choice(range(self.matrix.x), size=2)),
                    color=(255, 0, 0),
                )
                for _ in range(N_AGENTS)
            ],
            *[
                Agent(
                    self,
                    *tuple(np.random.choice(range(self.matrix.x), size=2)),
                    color=(0, 0, 255),
                )
                for _ in range(N_AGENTS)
            ],
        ]

    def init_grazers(self):
        self.grazers = [
            Grazer(
                self,
            )
            for _ in range(N_GRAZERS)
        ]

    def init_food(self):
        self.food = []
        for _ in range(N_FOOD):
            self.generate_food()

    def generate_food(self):
        food_item = Food(
            x=np.random.randint(self.matrix.x),
            y=np.random.randint(self.matrix.y),
            color=(0, np.random.randint(255), 0),
        )
        self.food.append(food_item)
        self.matrix.add_food(food_item)

    def __str__(self):
        return str(self.matrix)

    def __repr__(self):
        return repr(self.matrix)

    def update(self):
        for agent in self.agents:
            agent.update()
            self.matrix.move_agent(agent)
            self.matrix.set_node_color(agent.x, agent.y, agent.color)
        for food in self.food:
            self.matrix.set_node_color(food.x, food.y, food.color)
        # self.resolve_interactions()
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
                            self.food.remove(food_item)
                            # print(f"food interaction: {agent} eats {food_item}")
                        for other in agents[idx:]:
                            if agent != other:
                                agent.interact(other)
                                other.interact(agent)
                            # print(f"agent interaction: {agent} interacts with {other}")

    def update_food(self):
        if len(self.food) < N_FOOD:
            self.generate_food()
