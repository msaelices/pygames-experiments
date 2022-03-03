from os import path

BASE_DIR: str = path.dirname(path.abspath(__file__))
FPS: int = 60
TILE_SIZE: int = 64
SCREEN_WIDTH: int = TILE_SIZE * 12
SCREEN_HEIGHT: int = TILE_SIZE * 10
SPEED: int = 5
JUMP_SPEED: int = 30
BULLET_SPEED: int = 5
OVERLAP_THRESHOLD: int = 40
