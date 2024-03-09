class Food:
    def __init__(self, x, y, color=(0, 255, 0)):
        self.x = x
        self.y = y
        self.color = color

    def get_eaten(self):
        self.x = -1
        self.y = -1

    def __str__(self):
        return f"Food ({self.x}, {self.y}) with color {self.color} --"
