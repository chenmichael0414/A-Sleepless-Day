import pygame
import sys

from player import Player
from screen import Screen

if __name__ == '__main__':
    pygame.init()

    screen = Screen()
    player = Player(screen)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.tick(player.x, player.y)
        player.tick()

        pygame.display.update()