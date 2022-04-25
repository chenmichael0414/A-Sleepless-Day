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

    pygame.mouse.set_visible(False)

    started = False

    screen    = Screen()
    textbox   = Textbox(screen)
    inventory = Inventory(screen)
    item      = Item(screen, textbox, inventory)
    battle    = Battle(screen, textbox)
    player    = Player(screen, item)

    Key.addKey(inventory.displayKey)
    Key.addKey(pygame.K_b)

    screen.setRoom('CHEM', player, item)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.tick(player.x, player.y)
        battle.tick()

        if not screen.loading:
            textbox.tick()

            if not screen.battling:
                player.tick()
                item.tick()
                inventory.tick()
                Key.tick()
            
        # Freeze the screen if a textbox is open or if the inventory is open
        screen.frozen = textbox.isActive or inventory.isActive

        if not started and pygame.key.get_pressed()[pygame.K_TAB]:
            cutscene(screen, textbox, player, item)
            started = True

        if pygame.key.get_pressed()[pygame.K_z]: 
            textbox.draw([
                'hello! welcome to our game. here, you will learn everything you need to know. press enter to continue.',
                'wow, see? you\'re already learning! you\'re amazing <3'
            ])

        if pygame.key.get_pressed()[pygame.K_c]:
            item.clearItems() 
            screen.setRoom('CHEM', player, item)

        pygame.display.update()