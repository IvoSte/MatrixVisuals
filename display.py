import pygame
from pheromone import Pheromone
from matrix import Matrix
from model import Model

BACKGROUND_COLOR = (0,0,0)
# BACKGROUND_COLOR = (255,255,255)

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
        self.font = pygame.font.SysFont("Arial" , 18 , bold = True)

        pygame.display.get_surface().fill(BACKGROUND_COLOR)  # background

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

    def _draw_nodes(self, matrix: Matrix):
        # TODO: Find all pheromones that are on the same square
        # and interpolate the color
        for object_type in matrix.nodes:
            for obj in matrix.nodes[object_type]:
                if isinstance(obj, Pheromone):
                    all_pheromones_on_tile = [x for x in matrix.get_nodes_by_position(obj.x, obj.y) if isinstance(x, Pheromone)]
                    if len(all_pheromones_on_tile) > 1:
                        # Interpolate the color
                        colors = [x.color for x in all_pheromones_on_tile]
                        color = tuple([sum(x) // len(x) for x in zip(*colors)])
                        self._draw_square(obj.x, obj.y, color)
                        continue
                self._draw_square(obj.x, obj.y, obj.color)
                # self._draw_circle(item.x, item.y, item.color)

    def _draw_grid(self):
        for x in range(0, int(self.display_width), int(self.node_width)):
            pygame.draw.line(self.grid_display, (40, 40, 40), (x, 0), (x, self.display_height))
        for y in range(0, int(self.display_height), int(self.node_height)):
            pygame.draw.line(self.grid_display, (40, 40, 40), (0, y), (self.display_width, y))

    def _draw_background(self):
        self.grid_display.fill(BACKGROUND_COLOR)

    def set_fps_counter(self, fps):
        self.fps = fps

    def _draw_fps_counter(self):
        if self.fps:
            fps_text = self.font.render(f"FPS: {self.fps:.2f}", True, (255, 255, 255))
            self.grid_display.blit(fps_text, (10, 10))

    def reset(self):
        pygame.display.get_surface().fill(BACKGROUND_COLOR)
        pygame.display.update()

    def update(self):
        self._draw_background()
        self._draw_grid()
        self._draw_nodes(self.model.matrix)
        self._draw_fps_counter()
        pygame.display.update()
