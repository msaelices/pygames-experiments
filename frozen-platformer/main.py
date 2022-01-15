import pygame
import sys

from config import SCREEN_WIDTH, SCREEN_HEIGHT
from levels import Level


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

level = Level(0, screen)

def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill('black')
        level.run()

        pygame.display.update()
        clock.tick(60)



if __name__ == '__main__':
    main()
