import pygame
from typing import List

from config import TILE_SIZE
from sprites import Tile

levels_layout = [
    [
        '                    ',
        '   XXXX         XXXX',
        '                    ',
        '         XXX        ',
        '                    ',
        'X                   ',
        'X                   ',
        'XX                 X',
        'XXXX     XX       XX',
        'XXXX             XXX',
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
        self.surface = surface
        level_layout = levels_layout[number]
        self.setup(level_layout)

    def setup(self, layout: List[str]):
        self.tiles = pygame.sprite.Group()
        for y, row in enumerate(layout):
            for x, cell in enumerate(row):
                if cell == 'X':
                    tile = Tile(TILE_SIZE, (x * TILE_SIZE, y * TILE_SIZE))
                    self.tiles.add(tile)

    def run(self):
        # TODO: base this scroll on the player's input
        self.tiles.update(-1)
        self.tiles.draw(self.surface)
