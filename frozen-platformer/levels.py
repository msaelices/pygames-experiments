from typing import Generator

import pygame
from pygame.surface import Surface

from config import SPEED, TILE_SIZE
from sprites import BaseSprite, Enemy, Player, SnowFlake, Tile

levels_layout: list[list[str]] = [
    [
        '   P                     ',
        '   XXXX         XXXX     ',
        '          E              ',
        '         XXX             ',
        '                 XXXX    ',
        'X                        ',
        'X     XX                 ',
        'X  X      E        XXXX  ',
        'X  X     XX  X    XX     ',
        'XXXXXX         XXXXX  XXX',
    ],
    [
        '     E                   ',
        'XXXXXXX         XXXX   XX',
        '                         ',
        '         XXX             ',
        '                  XXX    ',
        'X                        ',
        'X                        ',
        'XX                 X     ',
        'XXXX     XX       XX     ',
        'XXXX             XXXXXXXX',
    ],
]


class Level:

    def __init__(self, number: int, surface: Surface):
        self.offset = 0
        self.surface = surface
        level_layout = levels_layout[number]
        self.setup(level_layout)

    def setup(self, layout: list[str]) -> None:
        self.enemies = pygame.sprite.Group()
        self.tiles = pygame.sprite.Group()
        self.snow_flakes = pygame.sprite.Group()

        for y, row in enumerate(layout):
            for x, cell in enumerate(row):
                cell_pos = (x * TILE_SIZE, y * TILE_SIZE)
                if cell == 'X':
                    tile = Tile(TILE_SIZE, cell_pos)
                    self.tiles.add(tile)
                elif cell == 'P':
                    self.player = Player(cell_pos)
                elif cell == 'E':
                    enemy = Enemy(cell_pos)
                    self.enemies.add(enemy)

        for _ in range(20):
            self.snow_flakes.add(SnowFlake())

    def get_all_sprites(self) -> Generator[BaseSprite, None, None]:
        yield self.player
        yield from self.tiles.sprites()  # type: ignore
        yield from self.enemies.sprites()  # type: ignore
        yield from self.snow_flakes.sprites()  # type: ignore

    def draw(self) -> None:
        for sprite in self.get_all_sprites():
            sprite.draw(self.surface, self.offset)

    def update(self) -> None:
        self.player.update(level=self)
        self.snow_flakes.update(level=self)
        self.enemies.update(level=self)
        # Move camera offset according to the player position
        min_offset, max_offset = 100, 400
        assert self.player.rect
        player_posx = self.player.rect.centerx
        player_offset = abs(player_posx - self.offset)
        if player_offset > max_offset or player_offset < min_offset:
            offset_vel = SPEED if player_offset > max_offset else -SPEED
            self.offset += offset_vel
        self.offset = max(self.offset, 0)
