from matrix import Matrix
from agents.agent import Agent
from agents.agent_types.grazers import Grazer
from agents.agent_types.slowboys import SlowBoy
from food import Food
import numpy as np

N_AGENTS = 0
N_GRAZERS = 1
N_SLOWBOYS = 5
N_FOOD = 0


class Model(object):
    def __init__(self, width, height):
        self.matrix = Matrix(width, height)
        self.init_agents()
        self.init_food()

    def init_agents(self):
        self.agents = [
            *[Agent.create_random_agent(self) for _ in range(N_AGENTS)],
            *[Grazer.create_random_agent(self) for _ in range(N_GRAZERS)],
            *[SlowBoy.create_random_agent(self) for _ in range(N_SLOWBOYS)],
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
