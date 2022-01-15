import pygame

from config import FPS, SCREEN_WIDTH, SCREEN_HEIGHT
from levels import Level

# controls
PAUSE = pygame.K_p

class Game:
    IDLE = 0
    STARTED = 1
    PAUSED = 2
    GAME_OVER = 3

    @property
    def is_done(self):
        return self.status == self.GAME_OVER

    @property
    def is_started(self):
        return self.status == self.STARTED

    @property
    def is_paused(self):
        return self.status == self.PAUSED

    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.level = Level(0, self.screen)
        self.clock = pygame.time.Clock()
        self.done = False
        self.status = self.IDLE

    def loop(self):
        while not self.is_done:
            self.handle_events()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.status = self.GAME_OVER
            elif event.type == pygame.KEYDOWN:
                if event.key == PAUSE:
                    self.toggle_pause()

    def toggle_pause(self):
        self.status = self.STARTED if self.is_paused else self.PAUSED

    def draw(self):
        self.screen.fill('black')
        if not self.is_paused:
            self.level.move_x(-1)
        self.level.draw()
        pygame.display.update()
