import pygame
import sys

from player import Player
from screen import Screen
from textbox import Textbox

if __name__ == '__main__':
    pygame.init()

    screen = Screen()
    player = Player(screen)
    textbox = Textbox(screen)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.tick(player.x, player.y)
        player.tick()
        textbox.tick()

        if pygame.key.get_pressed()[pygame.K_a]: 
            textbox.draw([
                'hello! welcome to our game. here, you will learn everything you need to know. press enter to continue.',
                'wow, see? you\'re already learning! you\'re amazing <3'
            ]) 

        pygame.display.update()