'''
Project: Choose Your Own Adventure Game
Team Members: Michael Chen, Kevin Guan, Preston Meek
Due Date: 5/9/2022
Task Description: Design a school-appropriate program that will let users move through rooms based on user input 
and get descriptions of each room.
'''

import pygame
import sys

from title import TitleScreen
from player import Player
from screen import Screen
from textbox import Textbox
from item import Item
from inventory import Inventory
from battle import Battle
from key import Key
from intro import cutscene
from outro import ending

if __name__ == '__main__':
    pygame.init()
    pygame.mixer.init()
    
    pygame.mouse.set_visible(False)

    started = False

    screen    = Screen()
    title     = TitleScreen(screen)
    textbox   = Textbox(screen)
    inventory = Inventory(screen)
    item      = Item(screen, textbox, inventory)
    battle    = Battle(screen, textbox, item)
    player    = Player(screen, item, battle, textbox)

    Key.addKey(inventory.displayKey)
    Key.addKey(pygame.K_b)

    screen.setRoom('HALLWAY', player, item)

    # to test full inventory
    # for i in range(0, 16):
        # inventory.addToInventory({
            # 'name': 'block',
            # 'sprite': item.loadSprite('block')
       # })

    # item.rewardItem('flashlight', 'ajsidfosdaif')

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        # If the title screen is open, we restart the loop so nothing else renders
        if title.open:
            title.tick()
            continue

        # Runs the cutscene once the title screen is closed
        if not started:
            cutscene(screen, textbox, player, item, inventory)
            started = True
            sprite = 0
            player.tick(drawingNumber=sprite)
            textbox.draw([
                'Is that a cowboy cat??',
                'I must be hallucinating due to my poor time management skills.',
                'If I can just make it home and take a nap, everything will go back to normal.',
            ]) 

        screen.tick(player.x, player.y)
        battle.tick()

        if not screen.loading: 
            if not screen.battling:
                player.tick()

                if not screen.isEvent:
                    item.tick()

                if not textbox.isActive:
                    inventory.tick()

                    # TODO: find a better way to do this incase we need toggling elsewhere
                    # this is because we don't want the player to be able to turn inventory on while text is running
                    Key.tick()  

        # covers screen with black rectangles so it appears to be the actual screen width and screen height (i.e 800x600)
        # this is done after everything else is drawn EXCEPT textbox so this is the top layer (besides textbox)
        # this is because the textbox is drawn on top of the border at the bottom of the screen
        screen.drawBorder()

        if not screen.loading:
            if not inventory.isActive:
                textbox.tick()

            # If a room is too dark, trigger the dark event
            if screen.dark and not item.hasItem('flashlight'): 
                screen.triggerEvent(textbox, player, item, ['this room is too dark to see in.', 'please come back with a light source.', '(hint: bottom left!)'])
            
        # Freeze the screen if a textbox is open or if the inventory is open
        screen.frozen = textbox.isActive or inventory.isActive

        if screen.currentRoom == "FINALE":
            ending(screen, textbox, player, item, inventory)
            screen.setRoom('HALLWAY', player, item)
            title.open = True
            started = False
            continue

        '''
        if not started and pygame.key.get_pressed()[pygame.K_TAB]:
            cutscene(screen, textbox, player, item)
            started = True

        if pygame.key.get_pressed()[pygame.K_z]: 
            textbox.draw([
                'hello! welcome to our game. here, you will learn everything you need to know. press enter to continue.',
                'wow, see? you\'re already learning! you\'re amazing <3'
            ])

         if pygame.key.get_pressed()[pygame.K_c]:
            screen.setRoom('CHEM', player, item)

        if pygame.key.get_pressed()[pygame.K_i]:
            screen.setRoom('CSE', player, item)

        if pygame.key.get_pressed()[pygame.K_o]:
            screen.setRoom('MATH', player, item)

        if pygame.key.get_pressed()[pygame.K_p]:
            screen.setRoom('GYM', player, item)

        if pygame.key.get_pressed()[pygame.K_u]:
            screen.setRoom('HALLWAY', player, item)
        '''

        pygame.display.update()