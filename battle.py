import pygame
from key import Key

class Battle:
    def __init__(self, screen):
        self.screen = screen

        self.boxWidth  = 400
        self.boxHeight = 350
        self.boxLine  = 3    # box line width

        self.playerX = 0
        self.playerY = 0

        self.playerMoveVel    = 3
        self.playerYVel       = 0
        self.playerYAccel     = .4
        self.playerJumpHeight = 8

        self.mode = "GRAVITY"

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
                (self.screen.SCREEN_WIDTH - self.boxWidth) / 2, 
                self.screen.SCREEN_HEIGHT - self.boxHeight, 
                self.boxWidth, 
                self.boxHeight
            ),
            self.boxLine
        )

        # Player
        self.screen.drawRect(
            (255, 0, 0), # red
            (
                (self.screen.SCREEN_WIDTH - self.boxWidth) / 2 + self.playerX + self.boxLine, 
                self.screen.SCREEN_HEIGHT - self.boxLine - self.playerSize - self.playerY, 
                self.playerSize, 
                self.playerSize
            ),
        )

        if pygame.key.get_pressed()[pygame.K_d]:
            self.playerX += self.playerMoveVel

        if pygame.key.get_pressed()[pygame.K_a]:
            self.playerX -= self.playerMoveVel

        rightBound = self.boxWidth - self.playerSize - (self.boxLine * 2)
        leftBound = 0

        if self.playerX > rightBound:
            self.playerX = rightBound

        if self.playerX < leftBound:
            self.playerX = leftBound

        if self.mode == "GRAVITY":
            if pygame.key.get_pressed()[pygame.K_w] and self.playerY == 0:
                self.playerYVel = self.playerJumpHeight

            self.playerY += self.playerYVel
            self.playerYVel -= self.playerYAccel
        elif self.mode == "NORMAL":
            if pygame.key.get_pressed()[pygame.K_w]:
                self.playerY += self.playerMoveVel

            if pygame.key.get_pressed()[pygame.K_s]:
                self.playerY -= self.playerMoveVel

        topBound    = self.boxHeight - self.playerSize - (self.boxLine * 2)
        bottomBound = 0

        if self.playerY > topBound:
            self.playerY = topBound

        if self.playerY < bottomBound:
            self.playerY    = bottomBound
            self.playerYVel = 0