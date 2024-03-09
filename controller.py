import pygame

FPS = 144


class Controller:
    def __init__(self, model, display):

        self.model = model
        self.display = display
        self.running = False
        pygame.init()
        self.clock = pygame.time.Clock()

    def run(self):
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    self.quit_simulation()
            self.model.update()
            self.display.update()
            self.clock.tick(FPS)

    def quit_simulation(self):
        pygame.quit()
        quit()
