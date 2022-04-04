import pygame
import sys

from player import Player
from screen import Screen
from textbox import Textbox
from item import Item

if __name__ == '__main__':
    pygame.init()

    screen  = Screen()
    textbox = Textbox(screen)
    item    = Item(screen, textbox)
    player  = Player(screen, item)

    item.addItem('block')
    item.addItem('block', x=200, y=200)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.tick(player.x, player.y)

        if not screen.loading:
            player.tick()
            item.tick()
            textbox.tick()

        if pygame.key.get_pressed()[pygame.K_a]: 
            textbox.draw([
                'hello! welcome to our game. here, you will learn everything you need to know. press enter to continue.',
                'wow, see? you\'re already learning! you\'re amazing <3'
            ])

        if pygame.key.get_pressed()[pygame.K_b]: 
            screen.setRoom('TEST', player, item)

        if pygame.key.get_pressed()[pygame.K_c]: 
            screen.setRoom('MAIN', player, item)

        pygame.display.update()