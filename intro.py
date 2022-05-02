import pygame
import sys
from screen import Screen
import player
from item import Item

def cutscene(screen, textbox, player, item):
    screen.cutscene = True
    item.setItems(None)
    backgrounds = ['SUNRISE1', 'SUNRISE2', 'SUNRISE3', 'BEDROOM']
    
    def tick(currScene):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        if currScene == 0:
            sprite = 2
            for i in range(len(backgrounds)):
                screen.setRoom(backgrounds[i], player, item, load=(True if i == 0 else False))
                if i == 3:
                    player.resetPosition(pos=[screen.SCREEN_WIDTH*4/5, screen.SCREEN_HEIGHT*63/100])
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
        elif currScene == 1:
            sprite = 2
            incomplete = textbox.drawIfIncomplete(['*Yawn.* I finally finished my post lab. Time for me to hit the hay.'], 'cutscene1') 
            if incomplete:
                screen.tick(player.x, player.y)
                textbox.tick()
                player.tick(drawingNumber=sprite)
                pygame.display.update()
                return(currScene)
            else:
                currScene += 1
        elif currScene == 2:
                sprite = 4
                screen.tick(player.x, player.y)
                player.tick(drawingNumber=sprite)
                pygame.display.update()
                screen.cutscene = False
        return currScene
    
    currScene = 0
    while screen.cutscene:
        currScene = tick(currScene)
