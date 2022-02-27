from collections import defaultdict
from os import path, walk
from random import randint

import pygame
from pygame import Surface
from pygame.sprite import Sprite

from config import (
    BASE_DIR, JUMP_SPEED, OVERLAP_THRESHOLD, SCREEN_HEIGHT, SCREEN_WIDTH, SPEED, TILE_SIZE
)

class Tile(Sprite):

    def __init__(self, size: int, pos: tuple):
        super().__init__()
        self.image = Surface((size, size))
        self.image.fill('grey')
        self.rect = self.image.get_rect(topleft=pos)

    def update(self, x_shift: int):
        self.rect.x += x_shift


class AnimatedSprite(Sprite):

    @property
    def animation(self):
        return self.animations[self.status]

    @property
    def image(self):
        """Get current animated image based on its status"""
        return self.animation[self.frame_idx]

    def __init__(self, pos: tuple):
        super().__init__()
        self.status = 'idle'
        self.steps = 0
        self.init_animations()
        self.rect = self.image.get_rect(topleft=pos)

    def init_animations(self):
        self.frame_idx = 0
        self.animations = defaultdict(list)
        sprites_path = path.join(BASE_DIR, 'graphics', 'sprites', self.sprites_dir)
        for _, _, file_names in walk(sprites_path):
            for fname in sorted(file_names):
                fpath = path.join(sprites_path, fname)
                img = pygame.transform.scale(
                    pygame.image.load(fpath).convert_alpha(),
                    self.size,
                )
                name, _ = path.splitext(fname)
                status, _ = name.split('_')
                self.animations[status].append(img)

    def animate(self):
        # heuristics to know if change the animated frame for the entity
        self.steps = (self.steps + 1) % (SPEED * 3)
        if self.steps == 0:
            self.shift_frame()

    def shift_frame(self):
        self.frame_idx = (self.frame_idx + 1) % len(self.animation)

    def update(self):
        super().update()
        self.animate()


class Entity(AnimatedSprite):
    gravity = 2  # default gravity speed
    terminal_velocity = 5  # default terminal velocity

    def __init__(self, pos: tuple):
        super().__init__(pos=pos)
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
            self.vel_y = min(self.vel_y + self.gravity, self.terminal_velocity)

    def update(self, level):
        super().update()

        self.apply_gravity(level)
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        # make sure the player is not passing through obstacles
        tiles_hit = pygame.sprite.spritecollide(self, level.tiles, False)
        for tile in tiles_hit:
            rect = self.rect
            t_rect = tile.rect
            if abs(rect.right - t_rect.left) < OVERLAP_THRESHOLD and self.vel_x > 0:
                self.rect.right = t_rect.left
                self.vel_x = 0
            elif abs(rect.left - t_rect.right) < OVERLAP_THRESHOLD and self.vel_x < 0:
                self.rect.left = t_rect.right
                self.vel_x = 0
            if abs(rect.bottom - t_rect.top) < OVERLAP_THRESHOLD and self.vel_y > 0:
                self.rect.bottom = t_rect.top
                self.vel_y = 0
                self.in_ground = True
            elif abs(rect.top - t_rect.bottom) < OVERLAP_THRESHOLD and self.vel_y < 0:
                self.rect.top = t_rect.bottom
                self.vel_y = 0

    def draw(self, surface: Surface):
        surface.blit(self.image, self.rect)


class SnowFlake(Entity):
    sprites_dir = 'snowflake'
    size = (10, 10)
    gravity = 1
    terminal_velocity = 2

    def __init__(self):
        super().__init__(self.get_random_pos(initial=True))

    def get_random_pos(self, initial=False):
        x = randint(0, SCREEN_WIDTH - 1)
        y = randint(0, SCREEN_HEIGHT - 1) if initial else 0
        return (x, y)

    def check_in_ground(self, level):
        return False  # never touch ground so it's always falling

    def update(self, level):
        self.animate()
        self.apply_gravity(level)
        self.rect.y += self.vel_y
        if self.rect.y >= level.surface.get_height():
            self.rect.topleft = self.get_random_pos()


class Enemy(Entity):
    sprites_dir = 'enemy'
    size = (TILE_SIZE // 2, TILE_SIZE)


class Player(Entity):
    sprites_dir = 'player'
    size = (TILE_SIZE // 2, TILE_SIZE)

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
