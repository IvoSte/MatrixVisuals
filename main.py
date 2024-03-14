from model import Model
from display import GridDisplay
from controller import Controller
import pygame
from config import load_config

# DISPLAY_WIDTH = 800
# DISPLAY_HEIGHT = 800
# NODES_X = 100
# NODES_Y = 100


def main():
    pygame.init()

    config = load_config("config.toml")

    model = Model(config["model"], config["agents"])

    display = GridDisplay(
        config["display"]["DISPLAY_WIDTH"],
        config["display"]["DISPLAY_HEIGHT"],
        config["display"]["DISPLAY_WIDTH"] / model.width,
        config["display"]["DISPLAY_HEIGHT"] / model.height,
        config["colors"]["BACKGROUND_COLOR"],
    )
    display.connect_model(model)
    controller = Controller(model, display, config["display"]["FPS"])

    controller.run()


if __name__ == "__main__":
    main()
