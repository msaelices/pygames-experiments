import pygame

from config import TILE_SIZE
from sprites import Enemy, Player, Tile

levels_layout = [
    [
        '                    ',
        '   XXXX         XXXX',
        '          E         ',
        '         XXX        ',
        '                    ',
        'X       E           ',
        'XP                  ',
        'XX                 X',
        'XXXX     XX      EXX',
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

    def setup(self, layout: list[str]):
        self.enemies = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.tiles = pygame.sprite.Group()
        for y, row in enumerate(layout):
            for x, cell in enumerate(row):
                cell_pos = (x * TILE_SIZE, y * TILE_SIZE)
                if cell == 'X':
                    tile = Tile(TILE_SIZE, cell_pos)
                    self.tiles.add(tile)
                elif cell == 'P':
                    player = Player(cell_pos)
                    self.player.add(player)
                elif cell == 'E':
                    enemy = Enemy(cell_pos)
                    self.enemies.add(enemy)


    def draw(self):
        self.tiles.draw(self.surface)
        self.player.draw(self.surface)
        self.enemies.draw(self.surface)

    def move_x(self, x):
        self.tiles.update(x)
