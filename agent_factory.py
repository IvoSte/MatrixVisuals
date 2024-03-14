from agents.agent_types import flower, grazers, loopy_grazer, slowboys, walker


from util.subclasses import get_all_subclasses
from agents.agent import Agent


class AgentFactory:
    def __init__(self):
        self.init_agent_types()

    def init_agent_types(self):
        self.agent_types = get_all_subclasses(Agent)

    def build_agents(self, model, agent_config):
        agents = []
        for agent_type in self.agent_types:
            agents.extend(
                [
                    agent_type.create_random_node(model)
                    for _ in range(agent_config[agent_type.__name__.upper()])
                ]
            )
        return agents


if __name__ == "__main__":
    from config import load_config
    from model import Model

    config = load_config("config.toml")

    model = Model(config["model"], config["agents"])
    af = AgentFactory()

    nodes = af.build_agents(model, config["agents"])

    for node in nodes:
        print(node)
