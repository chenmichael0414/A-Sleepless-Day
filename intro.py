import pygame
from screen import Screen
import player
from item import Item

def cutscene(screen, textbox, player, item):
    # clear items
    item.clearItems()
    item.tick()
    # sunrise to bedroom
    backgrounds = ['SUNRISE1', 'SUNRISE2', 'SUNRISE3', 'BEDROOM']
    for i in range(len(backgrounds)):
        screen.setRoom(backgrounds[i], load=(True if i == 0 else False))
        screen.tick(player.x, player.y)
        pygame.display.update()
        last = pygame.time.get_ticks()
        while pygame.time.get_ticks() <= last + 1000:
            screen.tick(player.x, player.y)
            pygame.display.update()

    textbox.draw([
                'hello! welcome to our game. here, you will learn everything you need to know. press enter to continue.',
                'wow, see? you\'re already learning! you\'re amazing <3'
            ])
    
    while True:
        textTick = textbox.tick()
        screen.tick(player.x, player.y)
        pygame.display.update()
        if textTick == 1:
            break
