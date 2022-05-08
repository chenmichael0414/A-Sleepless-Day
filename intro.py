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
    
    def tick(currScene):
        # exit game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        # first scene: sunrise
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
        # second scene: albert finishes post lab
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
        elif currScene == 3:
            sprite = 8
            last = pygame.time.get_ticks()
            while pygame.time.get_ticks() <= last + 550:
                player.simulateKey(K_d)
                screen.tick(player.x, player.y)
                player.tick(drawingNumber=sprite)
                pygame.display.update()
            currScene += 1
        elif currScene == 4:
            incomplete = textbox.drawIfIncomplete(['One bus ride later...'], 'cutscene3') 
            if incomplete:
                screen.tick(player.x, player.y)
                textbox.tick()
                pygame.display.update()
                return(currScene)
            screen.cutscene = False

            # Instructions
            textbox.draw([
                'welcome to albert\'s sleepless day!',
                'controls: wasd to move, {doorKey} to open doors, {itemKey} to pick up items, and {inventoryKey} to open inventory.'.format(doorKey=pygame.key.name(player.doorKey), itemKey=pygame.key.name(item.triggerKey), inventoryKey=pygame.key.name(inventory.displayKey)),
                'defeat the 5 cypher stickers to craft the cypher key and escape to freedom!',
                'good luck...'
            ])
        return currScene
    currScene = 0
    while screen.cutscene:
        currScene = tick(currScene)
    screen.setRoom('CHEM', player, item)
