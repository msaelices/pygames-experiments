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
        self.in_ground = False

    def check_in_ground(self, level):
        rect_below = self.rect.copy()
        rect_below.y += 1  # check if a rect just below the player is colliding
        for tile in level.tiles:
            if rect_below.colliderect(tile.rect):
                return True
        return False

    def apply_gravity(self, level):
        self.in_ground = self.check_in_ground(level)
        if not self.in_ground:
            self.vel_y = min(self.vel_y + GRAVITY, TERMINAL_VELOCITY)

    def update_pos(self, level):
        self.apply_gravity(level)
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        tiles_hit = pygame.sprite.spritecollide(self, level.tiles, False)
        for tile in tiles_hit:
            if self.vel_x > 0:
                self.rect.right = tile.rect.left
                self.vel_x = 0
            elif self.vel_x < 0:
                self.rect.left = tile.rect.right
                self.vel_x = 0
            if self.vel_y > 0:
                self.rect.bottom = tile.rect.top
                self.vel_y = 0
                self.in_ground = True
            elif self.vel_y < 0:
                self.rect.top = tile.rect.bottom
                self.vel_y = 0

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
        if self.in_ground:
            self.vel_y = -JUMP_SPEED
            self.in_ground = False

    def stop(self):
        self.vel_x = 0