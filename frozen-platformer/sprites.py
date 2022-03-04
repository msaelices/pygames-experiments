from __future__ import annotations

from collections import defaultdict
from enum import Enum
from os import path, walk
from random import randint
from typing import Any, cast

import pygame
from pygame.rect import Rect
from pygame.sprite import Sprite, Group
from pygame.surface import Surface

from config import (
    BASE_DIR, BULLET_SPEED, JUMP_SPEED, OVERLAP_THRESHOLD,
    SCREEN_HEIGHT, SCREEN_WIDTH, SPEED, TILE_SIZE,
)

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from levels import Level


def _draw_sprite(image: Surface | None, rect: Rect | None, surface: Surface | None, offset: int = 0) -> None:
    if image and surface and rect:
        rect = rect.copy()
        rect.x -= offset
        surface.blit(image, rect)


class Direction(Enum):
    LEFT = 1
    RIGHT = 2


class BaseSprite(Sprite):

    def draw(self, surface: Surface, offset: int = 0) -> None:
        _draw_sprite(self.image, self.rect, surface, offset)


class Tile(BaseSprite):

    def __init__(self, size: int, pos: tuple[int, int]):
        super().__init__()
        self.image = Surface((size, size))
        self.image.fill('grey')
        self.rect = self.image.get_rect(topleft=pos)

    def update(self, *args: Any, **kwargs: Any) -> None:
        x_shift = kwargs.pop('x_shift', None)
        if self.rect:
            self.rect.x += x_shift


class AnimatedSprite(BaseSprite):
    animations: defaultdict[str, list[Surface | None]]
    sprites_dir: str
    size: tuple[int, int]

    @property
    def animation(self) -> list[Surface | None]:
        return self.animations[self.status]

    @property
    def image(self) -> Surface | None:  # type: ignore
        """Get current animated image based on its status"""
        return cast(Surface, self.animation[self.frame_idx])

    def __init__(self, pos: tuple[int, int]):
        super().__init__()
        self.status = 'idle'
        self.steps = 0
        self.init_animations()
        self.rect = self.image and self.image.get_rect(topleft=pos) or None

    def init_animations(self) -> None:
        self.frame_idx = 0
        self.animations = defaultdict(list)
        sprites_path = path.join(
            BASE_DIR, 'graphics', 'sprites', self.sprites_dir,
        )
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

    def animate(self) -> None:
        # heuristics to know if change the animated frame for the entity
        self.steps = (self.steps + 1) % (SPEED * 3)
        if self.steps == 0:
            self.shift_frame()

    def shift_frame(self) -> None:
        self.frame_idx = (self.frame_idx + 1) % len(self.animation)

    def update(self, *args: Any, **kwargs: Any) -> None:
        super().update(args, kwargs)
        self.animate()


class Entity(AnimatedSprite):
    gravity = 2  # default gravity speed
    terminal_velocity = 5  # default terminal velocity
    direction: Direction = Direction.RIGHT

    def __init__(self, pos: tuple[int, int]):
        super().__init__(pos=pos)
        self.vel_x = 0
        self.vel_y = 0
        self.in_ground = False

    def check_in_ground(self, level: Level) -> bool:
        if self.rect:
            rect_below = self.rect.copy()
            rect_below.y += 1  # check if a rect just below the player is colliding
            for tile in level.tiles:
                if tile.rect and rect_below.colliderect(tile.rect):
                    return True
        return False

    def apply_gravity(self, level: Level) -> None:
        self.in_ground = self.check_in_ground(level)
        if not self.in_ground:
            self.vel_y = min(self.vel_y + self.gravity, self.terminal_velocity)

    def update(self, *args: Any, **kwargs: Any) -> None:
        super().update()

        assert self.rect

        level = kwargs.pop('level')
        self.apply_gravity(level)
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        # make sure the player is not passing through obstacles
        tiles_hit = pygame.sprite.spritecollide(self, level.tiles, False)
        for tile in tiles_hit:
            rect = self.rect
            t_rect = tile.rect
            assert t_rect
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

    def draw(self, surface: Surface, offset: int = 0) -> None:
        image = self.image
        if image and self.direction == Direction.LEFT:
            image = pygame.transform.flip(image, True, False)
        _draw_sprite(image, self.rect, surface, offset)


class SnowFlake(Entity):
    sprites_dir = 'snowflake'
    size = (10, 10)
    gravity = 1
    terminal_velocity = 2

    def __init__(self) -> None:
        super().__init__(self.get_random_pos(initial=True))

    def get_random_pos(self, initial: bool=False) -> tuple[int, int]:
        x = randint(0, SCREEN_WIDTH - 1)
        y = randint(0, SCREEN_HEIGHT - 1) if initial else 0
        return (x, y)

    def check_in_ground(self, level: Level) -> bool:
        return False  # never touch ground so it's always falling

    def update(self, *args: Any, **kwargs: Any) -> None:
        level = kwargs.pop('level')
        assert self.rect
        self.animate()
        self.apply_gravity(level)
        self.rect.y += self.vel_y
        if self.rect.y >= level.surface.get_height():
            self.rect.topleft = self.get_random_pos()

    def draw(self, surface: Surface, offset: int = 0) -> None:
        if self.rect and self.rect.x < offset:
            # Make sure the snowflake does not disappear from screen
            self.rect.x += SCREEN_WIDTH
        super().draw(surface, offset)


class Bullet(AnimatedSprite):
    sprites_dir = 'snowflake'
    size = (10, 10)

    def __init__(self, pos: tuple[int, int], direction: Direction):
        super().__init__(pos=pos)
        self.direction = direction

    @property
    def vel_x(self) -> int:
        return BULLET_SPEED if self.direction == Direction.RIGHT else -BULLET_SPEED

    def update(self, *args: Any, **kwargs: Any) -> None:
        assert self.rect
        self.rect.x += self.vel_x


class Enemy(Entity):
    sprites_dir = 'enemy'
    size = (TILE_SIZE // 2, TILE_SIZE)


class Player(Entity):
    sprites_dir = 'player'
    size = (TILE_SIZE // 2, TILE_SIZE)
    bullets: Group = Group()

    def move_left(self) -> None:
        self.vel_x = -SPEED
        self.direction = Direction.LEFT

    def move_right(self) -> None:
        self.vel_x = SPEED
        self.direction = Direction.RIGHT

    def jump(self) -> None:
        if self.in_ground:
            self.vel_y = -JUMP_SPEED
            self.in_ground = False

    def stop(self) -> None:
        self.vel_x = 0

    def shoot(self) -> None:
        assert self.rect
        self.bullets.add(
            Bullet(pos=self.rect.center, direction=self.direction)
        )

    def update(self, *args: Any, **kwargs: Any) -> None:
        level = kwargs.pop('level')
        super().update(level=level)
        self.bullets.update()

    def draw(self, surface: Surface, offset: int = 0) -> None:
        super().draw(surface, offset)

        rect = surface.get_rect().copy()
        rect.x += offset
        for bullet in self.bullets.sprites():
            if bullet.rect and bullet.rect in rect:
                cast(Bullet, bullet).draw(surface, offset=offset)
            else:
                self.bullets.remove(bullet)
