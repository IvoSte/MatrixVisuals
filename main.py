from model import Model
from display import GridDisplay
from controller import Controller
import pygame

DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 800
NODES_X = 100
NODES_Y = 100


def main():
    pygame.init()

    model = Model(NODES_X, NODES_Y)
    display = GridDisplay(
        DISPLAY_WIDTH,
        DISPLAY_HEIGHT,
        DISPLAY_WIDTH / model.matrix.x,
        DISPLAY_HEIGHT / model.matrix.y,
    )
    display.connect_model(model)
    controller = Controller(model, display)

    controller.run()


if __name__ == "__main__":
    main()
