import pygame
import math
import random
from key import Key
from boss_battles.monkey import Monkey
from boss_battles.bunny import Bunny
from boss_battles.cat import Cat
from boss_battles.mole import Mole
from boss_battles.elephant import Elephant

class Battle:
    def __init__(self, screen, textbox):
        self.screen  = screen
        self.textbox = textbox

        self.mode = "GRAVITY"
        
        self.boxWidth  = 400
        self.boxHeight = 350
        self.boxLine  = 3    # box line width

        # Player data
        self.playerSize  = 18
        self.playerColor = (255, 0, 0) # red
        
        self.playerX = (self.boxWidth - self.playerSize) / 2
        self.playerY = 0

        self.PLAYER_OFFSET_X = (self.screen.SCREEN_WIDTH - self.boxWidth)   / 2 + self.boxLine
        self.PLAYER_OFFSET_Y = (self.screen.SCREEN_HEIGHT + self.boxHeight) / 2 - self.boxLine - self.playerSize

        self.playerMoveVel    = 3
        self.playerYVel       = 0
        self.playerYAccel     = .4
        self.playerJumpHeight = 8

        self.playerHealth = 10

        # Amount of invulnerable frames the player has after being hit
        # 20 is an arbitrary number for a delay between damage, can be tweaked
        self.invulnerability = 20

        self.heartSheet   = pygame.image.load('./sprites/hearts.png').convert_alpha()
        self.HEART_WIDTH  = 168
        self.HEART_HEIGHT = 32

        self.heartSprite = None
        self.loadHeartSprite()

        # Enemy data
        # This enemy just exists so the enemy loop runs at least once
        # (if enemy array is empty, it won't run)
        self.enemies = [
            {
                'x': self.screen.SCREEN_WIDTH + 1,
                'y': 0,
                'angle': 1.5,
                'speed': 4,
                'size': 18
            }
        ]

        self.bosses = {
            'monkey': Monkey(screen, self, textbox),
            'bunny': Bunny(screen, self, textbox),
            'cat': Cat(screen, self, textbox),
            'mole': Mole(screen, self, textbox),
            'elephant': Elephant(screen, self, textbox)
        }
        self.currentBoss = 'bunny'


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
        self.playerHealth -= damage
        self.loadHeartSprite()

        self.playerColor = (155, 0, 0)

        # TODO: actually something when u die besides resetting the battle

        if self.playerHealth <= 0:
            self.reset()

    def reset(self):
        self.playerX = (self.boxWidth - self.playerSize) / 2
        self.playerY = 0

        self.playerHealth = 10
        self.loadHeartSprite()

        self.bosses[self.currentBoss].reset()

    def enemiesEngine(self):
        self.screen.cutscene = True
        self.bosses[self.currentBoss].tick() 


        '''
        for enemy in self.enemies:
            self.screen.drawRect(
                (0, 0, 255), # blue
                (
                    enemy['x'], 
                    enemy['y'], 
                    enemy['size'], 
                    enemy['size']
                ),
            )

            # self.enemyAttack1(enemy)
            self.enemyAttack2(enemy)

            if enemy['x'] > self.screen.SCREEN_WIDTH or enemy['y'] > self.screen.SCREEN_HEIGHT:
                self.enemies.remove(enemy)

            playerRect = pygame.Rect(self.PLAYER_OFFSET_X + self.playerX, self.PLAYER_OFFSET_Y - self.playerY, self.playerSize, self.playerSize)
            enemyRect  = pygame.Rect(enemy['x'], enemy['y'], enemy['size'], enemy['size'])

            if pygame.Rect.colliderect(playerRect, enemyRect):
                self.reset()
        '''
        

    def enemyAttack1(self, enemy):
        xSpeed = enemy['speed'] * math.cos(enemy['angle'])
        ySpeed = enemy['speed'] * math.sin(enemy['angle'])

        enemy['x'] += xSpeed
        enemy['y'] += ySpeed

        while len(self.enemies) < 7:
            # Angle is kinda random but at the same time pointing towards the center of the player box
            self.enemies.append({
                'x': random.randint(0, 400),
                'y': 0,
                'angle': math.atan2(self.screen.SCREEN_WIDTH / 2, self.screen.SCREEN_HEIGHT / 2) + random.uniform(-.25, .75),
                'speed': random.randint(4, 8),
                'size': 18
            })

    def enemyAttack2(self, enemy):
        enemy['x'] += enemy['speed']
        enemy['y'] += math.sin(enemy['x'] / 20) * 3

        while len(self.enemies) < 5:
            # Angle is kinda random but at the same time pointing towards the center of the player box
            self.enemies.append({
                'x': 0,
                'y': random.randint(self.screen.SCREEN_HEIGHT - 51, self.screen.SCREEN_HEIGHT - 1),
                'angle': 0,
                'speed': random.randint(2, 4),
                'size': 18
            })