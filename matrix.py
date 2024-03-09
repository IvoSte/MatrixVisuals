from node import Node


class Matrix:

    def __init__(self, x=4, y=4):
        self.x = x
        self.y = y
        assert self.x == self.y, "Matrix should be square"
        self.nodes = [[Node(i, j) for j in range(y)] for i in range(x)]

    def set_node_color(self, x, y, color):
        self.nodes[x][y].color = color

    @classmethod
    def matrix_with_nodes(nodes: list[list[Node]]):
        matrix = Matrix(len(nodes), len(nodes[0]))
        matrix.nodes = nodes
        return matrix

    def randomize_nodes(self):
        for row in self.nodes:
            for node in row:
                node.set_random_color()

    def __iter__(self):
        return iter(self.nodes)

    def __len__(self):
        return len(self.nodes)

    def __print__(self):
        for row in self.nodes:
            print(row)

    def fade_node(self, node, fade_rate):
        node.color = tuple(int(max(0, c - fade_rate)) for c in node.color)

    def fade_nodes(self, fade_rate):
        for row in self.nodes:
            for node in row:
                self.fade_node(node, fade_rate)

    def move_agent(self, agent):
        self.nodes[agent.x][agent.y].add_object(agent)

    def add_food(self, food):
        self.nodes[food.x][food.y].add_object(food)

    def update(self):
        for row in self.nodes:
            for node in row:
                node.update()
        self.fade_nodes(1)
