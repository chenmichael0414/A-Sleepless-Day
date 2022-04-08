from re import I
import pygame
from key import Key

class Inventory:
    def __init__(self, screen):
        self.screen = screen

        self.displayKey  = pygame.K_e

        self.dimensions = (
            self.screen.SCREEN_WIDTH / 6,
            self.screen.SCREEN_HEIGHT / 8, 
            self.screen.SCREEN_WIDTH * 4 / 6,
            self.screen.SCREEN_HEIGHT * 6 / 8
        )
        self.boxSize = 65
        self.boxGrid = (4, 4)
        self.padding = 10

        self.items = []

    def addToInventory(self, item):
        self.items.append(item)

    def tick(self):
        if Key.isToggled(self.displayKey):
            self.screen.frozen = True
            self.display()
        else:
            self.screen.frozen = False    
        
    def display(self):
        # Main white box
        pygame.draw.rect(
            self.screen.display, 
            (255, 255, 255), # white
            self.dimensions,
            0
        )

        # Black border
        for i in range(4):
            pygame.draw.rect(
                self.screen.display, 
                (0, 0, 0), # black
                (
                    self.dimensions[0] - i,
                    self.dimensions[1] - i,
                    self.dimensions[2],
                    self.dimensions[3]
                ), 
                1
            )

        # we want to generate a grid of tiles that will display each item
        remainingX = self.dimensions[2] - (self.padding * 2)
        columnSize = remainingX / self.boxGrid[0]

        remainingY = self.dimensions[3] - (self.padding * 2)
        rowSize    = remainingY / self.boxGrid[1]

        for i in range(self.boxGrid[1]):
            for j in range(self.boxGrid[0]):
                pygame.draw.rect(
                    self.screen.display, 
                    (0, 0, 0), # black
                    (
                        self.dimensions[0] + self.padding + (columnSize / 2) + (columnSize * j) - (self.boxSize / 2),
                        self.dimensions[1] + self.padding + (rowSize / 2)    + (rowSize * i)    - (self.boxSize / 2),
                        self.boxSize,
                        self.boxSize
                    ), 
                    2
                )

        # next, we want to load items into the tiles
        i = 0
        j = 0
        for item in self.items:
            w, h = item['sprite'].get_size()

            self.screen.display.blit(item['sprite'], (
                self.dimensions[0] + self.padding + (columnSize / 2) + (columnSize * j) - (w / 2),
                self.dimensions[1] + self.padding + (rowSize / 2)    + (rowSize * i)    - (h / 2)
            ))

            # go to the next row if we have filled all the boxes in the current one
            if j != 0 and j % (self.boxGrid[1] - 1) == 0:
                j = 0
                i += 1
            else:
                j += 1