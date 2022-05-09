import pygame
from pygame.locals import *
import sys
from screen import Screen
import player
from item import Item

def ending(screen, textbox, player, item, inventory):
    screen.cutscene = True
    item.setItems(None)
    screen.setRoom('FINALE', player, item, load=True)
    last = pygame.time.get_ticks()
    while pygame.time.get_ticks() <= last + 20:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
    sprite=16
    player.resetPosition(pos=[screen.SCREEN_WIDTH*3/5, screen.SCREEN_HEIGHT*63/100])
    player.tick(drawingNumber=sprite)
    screen.tick(player.x, player.y)
    pygame.display.update()
    last = pygame.time.get_ticks()
    while pygame.time.get_ticks() <= last + 3000:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.tick(player.x, player.y)
        player.tick(drawingNumber=sprite)
        pygame.display.update()
    def tick():
        # exit game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        incomplete = textbox.drawIfIncomplete(['Sweet dreams...'], 'outro1') 
        if incomplete:
            screen.tick(player.x, player.y)
            textbox.tick()
            player.tick(drawingNumber=sprite)
            pygame.display.update()
            return
        screen.cutscene = False
        return
    while screen.cutscene:
        tick()