import pygame
from key import Key

class Battle:
    def __init__(self, screen):
        self.screen = screen

        self.boxSize = 150  # box width and height
        self.boxLine = 3    # box line width

        self.playerX = 0
        self.playerY = 0

        self.playerSize = 18

    def tick(self):
        if pygame.key.get_pressed()[pygame.K_b]:
            self.screen.battling = True
            self.screen.load()

        # If the screen is loaded and we are in a battle
        if not self.screen.loading and self.screen.battling:
            self.engine()

    def engine(self):
        # Battle box
        self.screen.drawRect(
            (255, 255, 255), # white
            (
                (self.screen.SCREEN_WIDTH - self.boxSize) / 2, 
                self.screen.SCREEN_HEIGHT - self.boxSize, 
                self.boxSize, 
                self.boxSize
            ),
            self.boxLine
        )

        self.screen.drawRect(
            (255, 0, 0), # red
            (
                (self.screen.SCREEN_WIDTH - self.boxSize) / 2 + self.playerX + self.boxLine, 
                self.screen.SCREEN_HEIGHT - self.boxLine - self.playerSize - self.playerY, 
                self.playerSize, 
                self.playerSize
            ),
        )

        if pygame.key.get_pressed()[pygame.K_d]:
            pass