from node import Node
from pheromone import Pheromone
from agents.agent import Agent
from food import Food
from collections import defaultdict
from util.subclasses import get_all_subclasses


class Matrix:
    def __init__(self):
        self.nodes_by_type: defaultdict = defaultdict(list)
        self.nodes_by_position: defaultdict = defaultdict(list)

    def add_node(self, obj: Node):
        self.nodes_by_type[obj.__class__].append(obj)
        self.nodes_by_position[obj.pos_str].append(obj)

    def remove_node(self, obj: Node):
        try:
            self.nodes_by_type[obj.__class__].remove(obj)
            self.nodes_by_position[obj.pos_str].remove(obj)
        except ValueError:
            pass

    def get_nodes_by_position(self, x, y):
        return self.nodes_by_position[Node.position_to_pos_str(x, y)]

    def get_nodes_by_type(self, node_type):
        subclass_types = get_all_subclasses(node_type)
        subclass_types.add(node_type)

        nodes = []
        for subclass_type in subclass_types:
            nodes.extend(self.nodes_by_type[subclass_type])
        return nodes

    def __getitem__(self, key):
        return self.get_nodes_by_type(key)

    def is_empty_for_type(self, x, y, node_type):
        nodes_in_position = self.get_nodes_by_position(x, y)
        return len(nodes_in_position) == 0 or all(
            not isinstance(node, node_type) for node in nodes_in_position
        )

    def __print__(self):
        for node_type in self.nodes_by_type:
            print(f"{node_type}:")
            for node in self.nodes_by_type[node_type]:
                print(f"  {node}")

    def update(self):
        for node_type in self.nodes_by_type:
            for node in self.nodes_by_type[node_type]:
                node.update()
