import pygame
from key import Key

class Battle:
    def __init__(self, screen):
        self.screen = screen

    def tick(self):
        self.screen.battling = Key.isToggled(pygame.K_b)
        print(self.screen.battling)