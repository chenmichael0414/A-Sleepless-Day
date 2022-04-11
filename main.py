import pygame
import sys

from player import Player
from screen import Screen
from textbox import Textbox
from item import Item
from inventory import Inventory
from battle import Battle
from key import Key
from intro import cutscene

if __name__ == '__main__':
    pygame.init()

    started = False

    screen    = Screen()
    textbox   = Textbox(screen)
    inventory = Inventory(screen)
    item      = Item(screen, textbox, inventory)
    battle    = Battle(screen)
    player    = Player(screen, item)

    item.addItem('block')
    item.addItem('block', x=200, y=200)

    for i in range(5):
        inventory.addToInventory(item.active[0])

    Key.addKey(inventory.displayKey)
    Key.addKey(pygame.K_b)

    screen.setRoom('MAIN', player, item)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.tick(player.x, player.y)
        battle.tick()

        if not screen.loading and not screen.battling:
            player.tick()
            item.tick()
            textbox.tick()
            inventory.tick()
            Key.tick()

        if textbox.isActive or inventory.isActive:
            screen.frozen = True
        else:
            screen.frozen = False

        if not started and pygame.key.get_pressed()[pygame.K_SPACE]:
            cutscene(screen)
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