import pygame
from screen import Screen
import player
from item import Item

def cutscene(screen, textbox, player, item):
    player.cutscene = True
    sprite = 0
    # clear items
    item.clearItems()
    item.tick()
    # sunrise to bedroom
    backgrounds = ['SUNRISE1', 'SUNRISE2', 'SUNRISE3', 'BEDROOM']
    player.resetPosition(pos=[-200, -200])
    for i in range(len(backgrounds)):
        screen.setRoom(backgrounds[i], load=(True if i == 0 else False))
        if i == 3:
            player.resetPosition(pos=[screen.SCREEN_WIDTH*4/5, screen.SCREEN_HEIGHT*63/100])
            sprite = 8
            player.tick(drawingNumber = sprite)
        screen.tick(player.x, player.y)
        pygame.display.update()
        last = pygame.time.get_ticks()
        while pygame.time.get_ticks() <= last + 1000:
            screen.tick(player.x, player.y)
            player.tick(drawingNumber = sprite)
            pygame.display.update()

    textbox.draw([
                '*Yawn*. I finally finished my post-lab. Time for me to hit the hay.'
            ])
    
    last = pygame.time.get_ticks()
    while pygame.time.get_ticks() < last + 3000:
        screen.tick(player.x, player.y)
        player.tick(drawingNumber = sprite)
        pygame.display.update()