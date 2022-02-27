from tkinter import W
import pygame

from config import TILE_SIZE
from sprites import Enemy, Player, SnowFlake, Tile

levels_layout = [
    [
        '   P                ',
        '   XXXX         XXXX',
        '          E         ',
        '         XXX        ',
        '                    ',
        'X                   ',
        'X     XX            ',
        'XX        E        X',
        'XXXX     XX  X    XX',
        'XXXXXX         XXXXX',
    ],
    [
        '                    ',
        'XXXXXXX         XXXX',
        '                    ',
        '         XXX        ',
        '                    ',
        'X                   ',
        'X                   ',
        'XX                 X',
        'XXXX     XX       XX',
        'XXXX             XXX',
    ],
]


class Level:

    def __init__(self, number: int, surface: pygame.Surface):
        self.offset = 0
        self.surface = surface
        level_layout = levels_layout[number]
        self.setup(level_layout)

    def setup(self, layout: list[str]):
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

    def get_all_sprites(self):
        yield self.player
        yield from self.tiles.sprites()
        yield from self.enemies.sprites()
        yield from self.snow_flakes.sprites()

    def draw(self):
        for sprite in self.get_all_sprites():
            sprite.draw(self.surface, self.offset)

    def update(self):
        self.player.update(self)
        self.snow_flakes.update(self)
        self.enemies.update(self)
        # Move camera offset according to the player position
        min_offset, max_offset = 100, 400
        player_posx = self.player.rect.centerx
        player_offset = abs(player_posx - self.offset)
        # print(f'Player X: {player_posx} Offset: {self.offset} Player offset: {player_offset}')
        if player_offset > max_offset or player_offset < min_offset:
            offset_vel = 5 if player_offset > max_offset else -5
            self.offset += offset_vel
        self.offset = max(self.offset, 0)

    def scroll_x(self, x):
        self.tiles.update(x)
