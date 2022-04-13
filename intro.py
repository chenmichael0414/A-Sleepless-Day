import pygame
from screen import Screen
import player
from item import Item

def cutscene(screen, textbox, player, item):
    screen.cutscene = True
    sprite = 4
    # clear items
    item.clearItems()
    item.tick()
    # sunrise to bedroom
    backgrounds = ['SUNRISE1', 'SUNRISE2', 'SUNRISE3', 'BEDROOM']
    player.resetPosition(pos=[-400, -400])
    for i in range(len(backgrounds)):
        screen.setRoom(backgrounds[i], load=(True if i == 0 else False))
        if i == 3:
            player.resetPosition(pos=[screen.SCREEN_WIDTH*4/5, screen.SCREEN_HEIGHT*63/100])
            sprite = 4
            player.tick(drawingNumber=sprite)
        screen.tick(player.x, player.y)
        pygame.display.update()
        last = pygame.time.get_ticks()
        while pygame.time.get_ticks() <= last + 1000:
            screen.tick(player.x, player.y)
            player.tick(drawingNumber=sprite)
            pygame.display.update()

    screen.cutscene = True
    textbox.draw([
        '*Yawn*. I finally finished my post-lab. Time for me to hit the hay.'
    ], endCutscene=True)
    
    sprite = 8

    while screen.cutscene:
        screen.tick(player.x, player.y)
        textbox.tick()
        player.tick(drawingNumber=sprite)
        pygame.display.update()