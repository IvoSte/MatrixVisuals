import pygame


class Controller:
    def __init__(self, model, display, fps):

        self.model = model
        self.display = display
        self.running = False
        self.fps = fps
        self.clock = pygame.time.Clock()

    def run(self):
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.quit_simulation()
            self.model.update()
            self.display.set_fps_counter(self.clock.get_fps())
            self.display.update()
            self.clock.tick(self.fps)

    def quit_simulation(self):
        pygame.quit()
        quit()
