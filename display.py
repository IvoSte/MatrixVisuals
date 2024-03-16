import pygame
from matrix import Matrix
from model import Model
import numpy as np
from node import Node

from functools import lru_cache

# BACKGROUND_COLOR = (0, 0, 0)
# BACKGROUND_COLOR = (255,255,255)


class GridDisplay:
    def __init__(
        self,
        _display_width: int,
        _display_height: int,
        _node_width: int,
        _node_height: int,
        background_color: tuple = (0, 0, 0),
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
        self.font = pygame.font.SysFont("Arial", 18, bold=True)

        self.set_background_color(background_color)

        pygame.display.get_surface().fill(self.background_color)  # background
        self.transparent_screen = pygame.Surface(
            (self.display_width, self.display_height), pygame.SRCALPHA
        )
        self.ui_screen = pygame.Surface(
            (self.display_width, self.display_height), pygame.SRCALPHA
        )

    def connect_model(self, _model: Model):
        self.model = _model

    @lru_cache(maxsize=256)
    def cached_screen_position(self, x, y):
        return (x * self.node_width, y * self.node_height)

    def _draw_square(self, x, y, color, opacity=255):
        pygame.draw.rect(
            self.transparent_screen,
            (*color, opacity),
            [
                *self.cached_screen_position(x, y),
                self.node_width,
                self.node_height,
            ],
        )

    def _draw_circle(self, x, y, color, opacity=255):
        pygame.draw.circle(
            self.transparent_screen,
            (*color, opacity),
            (
                x * self.node_width + self.node_width // 2,
                y * self.node_height + self.node_height // 2,
            ),
            self.node_width // 1,
        )

    def set_background_color(self, background_color):
        self.background_color = background_color

    def _draw_nodes(self, matrix: Matrix):
        for node in matrix.get_nodes_by_type(Node):
            # TODO: This is just very slow
            # if isinstance(obj, Pheromone):
            #     all_pheromones_on_tile = [
            #         x
            #         for x in matrix.get_nodes_by_position(obj.x, obj.y)
            #         if isinstance(x, Pheromone)
            #     ]
            #     if len(all_pheromones_on_tile) > 1:
            #         # Interpolate the color
            #         colors = [x.color for x in all_pheromones_on_tile]
            #         color = tuple([sum(x) // len(x) for x in zip(*colors)])
            #         opacity = max(
            #             all_pheromones_on_tile,
            #             key=lambda x: x.opacity,
            #         ).opacity
            #         self._draw_square(obj.x, obj.y, color, opacity)
            #         continue
            self._draw_square(node.x, node.y, node.color, node.opacity)


    def _draw_grid(self):
        for x in range(0, int(self.display_width), int(self.node_width)):
            pygame.draw.line(
                self.grid_display, (40, 40, 40), (x, 0), (x, self.display_height)
            )
        for y in range(0, int(self.display_height), int(self.node_height)):
            pygame.draw.line(
                self.grid_display, (40, 40, 40), (0, y), (self.display_width, y)
            )

    def _draw_background(self):
        self.grid_display.fill(self.background_color)

    def set_fps_counter(self, fps):
        self.fps = fps

    def _draw_fps_counter(self):
        if self.fps:
            fps_text = self.font.render(f"FPS: {self.fps:.2f}", True, (255, 255, 255))
            self.ui_screen.blit(fps_text, (10, 10))

    def reset(self):
        pygame.display.get_surface().fill(self.background_color)
        pygame.display.update()

    def clear_screen(self):
        self._draw_background()
        self.transparent_screen.fill(pygame.Color(0, 0, 0, 0))
        self.ui_screen.fill(pygame.Color(0, 0, 0, 0))

    def update(self):
        self.clear_screen()
        self._draw_grid()
        self._draw_nodes(self.model.matrix)
        self._draw_fps_counter()
        self.grid_display.blit(self.transparent_screen, (0, 0))
        self.grid_display.blit(self.ui_screen, (0, 0))
        pygame.display.update()
