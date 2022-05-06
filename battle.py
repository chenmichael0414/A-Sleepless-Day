import pygame
import math
import random
from key import Key
import os
from boss_battles.monkey import Monkey
from boss_battles.bunny import Bunny
from boss_battles.cat import Cat
from boss_battles.mole import Mole
from boss_battles.elephant import Elephant

class Battle:
    def __init__(self, screen, textbox, item):
        self.screen  = screen
        self.textbox = textbox
        self.item    = item

        self.mode = "GRAVITY"
        
        self.boxWidth  = 400
        self.boxHeight = 350
        self.boxLine  = 3    # box line width

        # Player data
        self.initialSize = 18
        self.playerSize  = 18
        self.playerColor = (255, 0, 0) # red
        
        self.playerX = (self.boxWidth - self.playerSize) / 2
        self.playerY = 0

        self.PLAYER_OFFSET_X = (self.screen.SCREEN_WIDTH - self.boxWidth)   / 2 + self.boxLine
        self.PLAYER_OFFSET_Y = (self.screen.SCREEN_HEIGHT + self.boxHeight) / 2 - self.boxLine - self.playerSize

        self.initialMoveVel = 3
        self.playerMoveVel  = 3

        self.playerYVel   = 0
        self.playerYAccel = .4

        self.initialJumpHeight = 8
        self.playerJumpHeight  = 8

        self.playerHealth = 10
        self.extraHealth  = 0

        # Amount of invulnerable frames the player has after being hit
        # 20 is an arbitrary number for a delay between damage, can be tweaked
        self.invulnerability = 20

        self.heartSheet      = pygame.image.load('./sprites/hearts.png').convert_alpha()
        self.extraHeartSheet = pygame.image.load('./sprites/golden_hearts.png').convert_alpha()

        self.HEART_WIDTH  = 168
        self.HEART_HEIGHT = 32
        self.EXTRA_HEART_WIDTH = 66

        self.heartSprite = None
        self.loadHeartSprite()

        self.extraHeartSprite = None

        self.bosses = {
            'monkey': Monkey(screen, self, textbox),
            'bunny': Bunny(screen, self, textbox),
            'cat': Cat(screen, self, textbox),
            'mole': Mole(screen, self, textbox),
            'elephant': Elephant(screen, self, textbox)
        }
        self.currentBoss = None

    def init(self, boss):
        if boss not in self.bosses:
            return

        self.currentBoss = boss

        self.screen.battling = True
        self.screen.load()

        self.reset()

    def end(self):
        self.screen.battling = False
        self.screen.load()

        self.reset()

    def tick(self):
        if pygame.key.get_pressed()[pygame.K_b]:
            self.init('mole')

        # If the screen is loaded and we are in a battle
        if not self.screen.loading and self.screen.battling:
            self.engine()

    def engine(self):
        # Battle box
        self.screen.drawRect(
            (255, 255, 255), # white
            (
                (self.screen.SCREEN_WIDTH - self.boxWidth) / 2, 
                (self.screen.SCREEN_HEIGHT - self.boxHeight) / 2, 
                self.boxWidth, 
                self.boxHeight
            ),
            self.boxLine
        )

        # Player
        self.playerEngine()

        # Enemies
        self.enemiesEngine()

    def loadHeartSprite(self):
        # extract the current sprite
        rect = pygame.Rect(
            0,
            (10 - self.playerHealth) * self.HEART_HEIGHT,
            self.HEART_WIDTH,
            self.HEART_HEIGHT
        )

        self.heartSprite = pygame.Surface(rect.size, pygame.SRCALPHA).convert_alpha()
        self.heartSprite.blit(self.heartSheet, (0, 0), rect)

    def loadExtraHeartSprite(self):
        # extract the current sprite
        rect = pygame.Rect(
            0,
            (4 - self.extraHealth) * self.HEART_HEIGHT,
            self.EXTRA_HEART_WIDTH,
            self.HEART_HEIGHT
        )

        self.extraHeartSprite = pygame.Surface(rect.size, pygame.SRCALPHA).convert_alpha()
        self.extraHeartSprite.blit(self.extraHeartSheet, (0, 0), rect)

    def playerEngine(self):
        # Player
        self.screen.drawRect(
            self.playerColor,
            (
                self.PLAYER_OFFSET_X + self.playerX, 
                self.PLAYER_OFFSET_Y - self.playerY, 
                self.playerSize, 
                self.playerSize
            ),
        )

        # Player hearts
        self.screen.drawSprite(
            self.heartSprite, 
            (
                0,
                0
            )
        )

        # Extra player hearts
        if self.extraHeartSprite is not None:    
            self.screen.drawSprite(
                self.extraHeartSprite, 
                (
                    0,
                    0
                )
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
        elif self.mode == "FREE MOVE":
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

    def takeDamage(self, damage=1):
        if self.extraHealth > 0:
            self.extraHealth -= damage

            # Only load the extra heart sprite if there is one to load (there isn't one for 0 extra hearts, only 1/2)
            if self.extraHealth > 0:
                self.loadExtraHeartSprite()
            else:
                # Subtract from the player health how far negative we went in extra hearts
                # For example, if our extraHealth is -1, playerHealth will become 10 + (-1) = 10 - 1 = 9
                self.playerHealth += self.extraHealth
                self.extraHeartSprite = None
        else:
            self.playerHealth -= damage

        # Only load the heart sprite if there is one to load
        if self.playerHealth < 0:
            self.playerHealth = 0
        
        self.loadHeartSprite()

        self.albertPain()

        self.playerColor = (155, 0, 0)

        # TODO: actually something when u die besides resetting the battle

        if self.playerHealth <= 0:
            self.reset()

    def albertPain(self):
        soundList = os.listdir("./sounds")
        pygame.mixer.Sound.play(pygame.mixer.Sound(os.path.join("sounds", soundList[random.randint(0,6)])))


    def reset(self):
        # Get the player size
        self.playerSize = self.item.getPlayerSize() or self.initialSize

        self.playerX = (self.boxWidth - self.playerSize) / 2
        self.playerY = 0

        # Reset the player offset Y since it relies on the player size
        self.PLAYER_OFFSET_Y = (self.screen.SCREEN_HEIGHT + self.boxHeight) / 2 - self.boxLine - self.playerSize

        self.playerHealth = 10
        self.loadHeartSprite()

        # Get the extra health based on inventory items
        self.extraHealth = self.item.getExtraHealth()

        if self.extraHealth > 0:
            self.loadExtraHeartSprite()

        # Get any speed or jump multipliers
        self.playerMoveVel    = self.initialMoveVel    * self.item.getBoostMultipliers('speed')
        self.playerJumpHeight = self.initialJumpHeight * self.item.getBoostMultipliers('jump')

        self.bosses[self.currentBoss].reset()

    def enemiesEngine(self):
        self.bosses[self.currentBoss].tick()