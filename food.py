from node import Node

class Food(Node):
    def __init__(self, model, x, y, color=(0, 255, 0)):
        super().__init__(model, x, y, color)

    def get_eaten(self):
        self.model.matrix.remove_node(self)

    def __str__(self):
        return f"Food ({self.x}, {self.y}) with color {self.color} --"

    def interact(self, other: Node):
        if other.__class__.__name__ == "Grazer":
            self.get_eaten()
