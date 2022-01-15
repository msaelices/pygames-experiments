import pygame
from pygame import Surface
from pygame.sprite import Sprite

from config import GRAVITY, JUMP_SPEED, SPEED, TERMINAL_VELOCITY

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

    def apply_gravity(self):
        self.vel_y = min(self.vel_y + GRAVITY, TERMINAL_VELOCITY)

    def update_pos(self):
        self.apply_gravity()
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

    def draw(self, surface: Surface):
        surface.blit(self.image, self.rect)


class Enemy(Entity):
    color = 'red'


class Player(Entity):
    color = 'green'

    def move_left(self):
        self.vel_x = -SPEED

    def move_right(self):
        self.vel_x = SPEED

    def jump(self):
        self.vel_y = -JUMP_SPEED

    def stop(self):
        self.vel_x = 0