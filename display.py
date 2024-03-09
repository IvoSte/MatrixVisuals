import pygame
from node import Node
from matrix import Matrix
from model import Model


class GridDisplay:
    def __init__(
        self,
        _display_width: int,
        _display_height: int,
        _node_width: int,
        _node_height: int,
    ):
        self.display_width = _display_width
        self.display_height = _display_height
        self.node_width = _node_width
        self.node_height = _node_height

        assert (
            self.node_width == self.node_height
        ), "Node width and height must be equal."
        assert (
            self.display_width % self.node_width == 0
        ), "Display width must be a multiple of node width."
        assert (
            self.display_height % self.node_height == 0
        ), "Display height must be a multiple of node height."

        self.grid_display = pygame.display.set_mode(
            (self.display_width, self.display_height)
        )
        pygame.display.get_surface().fill((255, 255, 255))  # background

    def connect_model(self, _model: Model):
        self.model = _model

    def _draw_square(self, x, y, color):
        pygame.draw.rect(
            self.grid_display,
            # pygame.Color(*color, a=100), --> Need other layer type to change alpha.
            color,
            [
                x * self.node_width,
                y * self.node_height,
                self.node_width,
                self.node_height,
            ],
        )

    def _draw_circle(self, x, y, color):
        pygame.draw.circle(
            self.grid_display,
            color,
            (
                x * self.node_width + self.node_width // 2,
                y * self.node_height + self.node_height // 2,
            ),
            self.node_width // 2,
        )

    def _draw_grid(self, matrix: Matrix):
        for row in matrix:
            for item in row:
                self._draw_square(item.x, item.y, item.color)
                # self._draw_circle(item.x, item.y, item.color)

    def reset(self):
        pygame.display.get_surface().fill((255, 255, 255))
        pygame.display.update()

    def update(self):
        self._draw_grid(self.model.matrix)
        pygame.display.update()
