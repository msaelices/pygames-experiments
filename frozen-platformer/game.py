import pygame
import sys

from config import FPS, SCREEN_WIDTH, SCREEN_HEIGHT
from levels import Level

class Game:

    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.level = Level(0, self.screen)
        self.clock = pygame.time.Clock()
        self.done = False

    def start(self):
        while not self.done:
            self.handle_events()
            self.draw()
            self.clock.tick(FPS)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def draw(self):
        self.screen.fill('black')
        self.level.run()
        pygame.display.update()
