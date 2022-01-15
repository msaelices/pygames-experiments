import pygame

from config import FPS, SCREEN_WIDTH, SCREEN_HEIGHT
from levels import Level

# controls
PAUSE = pygame.K_p
LEFT = pygame.K_LEFT
RIGHT = pygame.K_RIGHT
JUMP = pygame.K_SPACE

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
        self.status = self.STARTED

    def loop(self):
        while not self.is_done:
            self.handle_events()
            self.update()
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
        keys = pygame.key.get_pressed()
        if self.is_started:
            if keys[LEFT]:
                self.level.player.move_left()
            elif keys[RIGHT]:
                self.level.player.move_right()
            elif keys[JUMP]:
                self.level.player.jump()
            else:
                self.level.player.stop()

    def toggle_pause(self):
        self.status = self.STARTED if self.is_paused else self.PAUSED

    def update(self):
        self.level.update()

    def draw(self):
        self.screen.fill('black')
        self.level.draw()
        pygame.display.update()
