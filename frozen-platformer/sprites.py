from pygame import Surface
from pygame.sprite import Sprite

from config import GRAVITY, TERMINAL_VELOCITY

class Tile(Sprite):

    def __init__(self, size: int, pos: tuple):
        super().__init__()
        self.image = Surface((size, size))
        self.image.fill('grey')
        self.rect = self.image.get_rect(topleft=pos)

    def update(self, x_shift: int):
        self.rect.x += x_shift


class Entity(Sprite):

    def __init__(self, pos: tuple):
        super().__init__()
        # TODO: show real sprites
        self.image = Surface((30, 60))
        self.image.fill(self.color)
        self.rect = self.image.get_rect(topleft=pos)
        self.vel_x = 0
        self.vel_y = 0


class Enemy(Entity):
    color = 'red'


class Player(Entity):
    color = 'green'
