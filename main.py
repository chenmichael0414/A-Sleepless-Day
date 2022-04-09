import pygame
import sys

from player import Player
from screen import Screen
from textbox import Textbox
from item import Item
from inventory import Inventory
from key import Key
from intro import cutscene

if __name__ == '__main__':
    pygame.init()

    started = False

    screen    = Screen()
    textbox   = Textbox(screen)
    inventory = Inventory(screen)
    item      = Item(screen, textbox, inventory)
    player    = Player(screen, item)

    block1 = item.addItem('block')
    block2 = item.addItem('block', x=200, y=200,)

    for i in range(5):
        inventory.addToInventory(item.active[0])

    Key.addKey(inventory.displayKey)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.tick(player.x, player.y)

        if not screen.loading:
            player.tick()
            item.tick()
            textbox.tick()
            inventory.tick()
            
            Key.tick()

        if not started and pygame.key.get_pressed()[pygame.K_TAB]:
            cutscene(screen, textbox, player, item)
            started = True

        if pygame.key.get_pressed()[pygame.K_z]: 
            textbox.draw([
                'hello! welcome to our game. here, you will learn everything you need to know. press enter to continue.',
                'wow, see? you\'re already learning! you\'re amazing <3'
            ])

        if pygame.key.get_pressed()[pygame.K_x]: 
            screen.setRoom('TEST', player, item)

        if pygame.key.get_pressed()[pygame.K_c]: 
            screen.setRoom('MAIN', player, item)

        pygame.display.update()