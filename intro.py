'''
Project: Choose Your Own Adventure Game
Team Members: Michael Chen, Kevin Guan, Preston Meek
Due Date: 5/9/2022
Task Description: Design a school-appropriate program that will let users move through rooms based on user input 
and get descriptions of each room.
'''

import pygame
from pygame.locals import *
import sys
from screen import Screen
import player
from item import Item

def cutscene(screen, textbox, player, item, inventory):
    screen.cutscene = True
    item.setItems(None)
    backgrounds = ['SUNRISE1', 'SUNRISE2', 'SUNRISE3', 'BEDROOM']
    
    # wait a certain amount of time
    def delay(time):
        last = pygame.time.get_ticks()
        while pygame.time.get_ticks() <= last + time:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

    # make albert move on his own without player input
    def autoMove(key, duration):
        last = pygame.time.get_ticks()

        while pygame.time.get_ticks() <= last + duration:
            player.simulateKey(key)
            screen.tick(player.x, player.y)
            player.tick()
            pygame.display.update()

    def tick(currScene):
        # exit game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        # sunrise
        if currScene == 0:
            sprite = 2
            for i in range(len(backgrounds)):
                screen.setRoom(backgrounds[i], player, item, load=(True if i == 0 else False))

                if i == 3:
                    player.resetPosition(pos=[screen.SCREEN_WIDTH*3/5, screen.SCREEN_HEIGHT*63/100])
                    player.tick(drawingNumber=sprite)

                screen.tick(player.x, player.y)
                pygame.display.update()
                last = pygame.time.get_ticks()

                while pygame.time.get_ticks() <= last + 1000:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            sys.exit()

                    screen.tick(player.x, player.y)

                    if i == 3:
                        player.tick(drawingNumber=sprite)

                    pygame.display.update()
            currScene += 1

        # albert finishes post lab
        elif currScene == 1:
            sprite = 2

            incomplete = textbox.drawIfIncomplete(['*Yawn.* I finally finished my pre-lab. Time for me to hit the hay.'], 'cutscene1') 
            if incomplete:
                screen.tick(player.x, player.y)
                textbox.tick()
                player.tick(drawingNumber=sprite)
                pygame.display.update()
                return(currScene)
                
            else:
                currScene += 1

        # albert notices it's 6:00 am and runs to catch the bus
        elif currScene == 2:
            sprite = 8
            incomplete = textbox.drawIfIncomplete(['OH SHOOT! IT\'S ALREADY 6:00 AM?!?', 'I\'M GONNA BE LATE TO SCHOOL!'], 'cutscene2') 
            
            if incomplete:
                screen.tick(player.x, player.y)
                textbox.tick()
                player.tick(drawingNumber=sprite)
                pygame.display.update()
                return(currScene)

            currScene += 1

        # albert leaves his room
        elif currScene == 3:
            sprite = 8

            last = pygame.time.get_ticks()
            while pygame.time.get_ticks() <= last + 550:
                player.simulateKey(K_d)
                screen.tick(player.x, player.y)
                player.tick()
                pygame.display.update()
            currScene += 1

        # load for bus ride
        elif currScene == 4:
            incomplete = textbox.drawIfIncomplete(['One bus ride later...'], 'cutscene3') 
            if incomplete:
                screen.tick(player.x, player.y)
                textbox.tick()
                pygame.display.update()
                return(currScene)
            currScene += 1

        # albert enters the school  
        elif currScene == 5:
            screen.setRoom('HALLWAY', player, item, load=False)
            autoMove(K_s, 250)
            sprite = 12
            screen.tick(player.x, player.y)
            player.tick(drawingNumber=sprite)
            pygame.display.update()
            delay(500)
            currScene += 1
        # albert notices the lock on the front door
        elif currScene == 6:
            sprite = 12
            incomplete = textbox.drawIfIncomplete(['Why is there a giant lock on the front door?', 'Maybe there\'s a key somewhere around here?'], 'cutscene5') 
            if incomplete:
                screen.tick(player.x, player.y)
                textbox.tick()
                player.tick(drawingNumber=sprite)
                pygame.display.update()
                return(currScene)
            currScene += 1
        # albert goes to chem
        elif currScene == 7:
            autoMove(K_a, 1990)
            autoMove(K_w, 250)
            sprite = 17
            screen.tick(player.x, player.y)
            player.tick(drawingNumber=sprite)
            pygame.display.update()
            currScene += 1

        # give player instructions
        elif currScene == 8:
            #Instructions
            incomplete = textbox.drawIfIncomplete([
                'welcome to albert\'s sleepless day!',
                'controls: wasd to move, {doorKey} to open doors, {itemKey} to pick up items, and {inventoryKey} to open inventory.'.format(doorKey=pygame.key.name(player.doorKey), itemKey=pygame.key.name(item.triggerKey), inventoryKey=pygame.key.name(inventory.displayKey)),
                'defeat the five cypher stickers to craft the cypher key and escape to freedom!',
                'good luck...'
            ], 'cutscene4') 
            if incomplete:
                screen.tick(player.x, player.y)
                textbox.tick()
                pygame.display.update()
                return(currScene)
            screen.cutscene = False
        return currScene
    currScene = 0
    while screen.cutscene:
        currScene = tick(currScene)
    screen.setRoom('CHEM', player, item, load=False)