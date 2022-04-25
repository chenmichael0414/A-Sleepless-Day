import math
import random
import pygame

class Monkey:
    def __init__(self, screen, battle, textbox):
        self.screen  = screen
        self.battle  = battle
        self.textbox = textbox

        self.currentFrame = 0
        self.scale = 3.5

        self.sheet  = pygame.image.load('./enemies/bosses/monkey.png').convert_alpha()

        # The width and height of each individual sprite in the sheet
        self.SHEET_WIDTH  = 250
        self.SHEET_HEIGHT = 300

        self.sprite = None
        self.loadSprite()

        self.attacks = [
            [ pygame.image.load('./attacks/punch.png').convert_alpha(), self.punch ],
            [ pygame.image.load('./attacks/kick.png').convert_alpha(), self.kick ]
        ]
        self.currentAttack = 1

        self.minions = [

        ]

        self.spawnDelay = 40    # Number of frames until the next minion is spawned

        # This is so when you touch a minion, you don't take damage multiple times from the same one
        self.lastCollisionFrame = 0

    def loadSprite(self):
        # extract the current sprite
        rect = pygame.Rect(
            (self.currentFrame % 2) * self.SHEET_WIDTH,           # % 2 because there are 2 sprites per row in spritesheet
            ((self.currentFrame // 2) % 2) * self.SHEET_HEIGHT,   # // 2 % 2 to get the current column (2 columns)
            self.SHEET_WIDTH,
            self.SHEET_HEIGHT
        )

        self.sprite = pygame.Surface(rect.size, pygame.SRCALPHA).convert_alpha()
        self.sprite.blit(self.sheet, (0, 0), rect)

        # upscale the sprite
        self.sprite = pygame.transform.scale(self.sprite, (self.scale * self.screen.PIXEL_SIZE, self.scale * self.screen.PIXEL_SIZE))

        print(self.sprite)

    def tick(self):
        if not self.sprite:
            return

        self.screen.drawSprite(
            self.sprite, 
            (
                (self.screen.SCREEN_WIDTH - self.sprite.get_width()) / 2,
                0
            )
        )

        if self.textbox.drawIfIncomplete(['oohoohooh aahahahah', 'i am going to defeat you!!!'], 'monkey 1'): return

        for minion in self.minions:
            self.screen.drawSprite(
                self.attacks[self.currentAttack][0],
                (
                    minion['x'],
                    minion['y']
                ),
            )

            if minion['x'] > self.screen.SCREEN_WIDTH or minion['y'] > self.screen.SCREEN_HEIGHT:
                self.minions.remove(minion)

            minionW, minionH = self.attacks[self.currentAttack][0].get_size()

            playerRect = pygame.Rect(
                self.battle.PLAYER_OFFSET_X + self.battle.playerX, 
                self.battle.PLAYER_OFFSET_Y - self.battle.playerY, 
                self.battle.playerSize, 
                self.battle.playerSize
            )

            enemyRect = pygame.Rect(minion['x'], minion['y'], minionW, minionH)

            if pygame.Rect.colliderect(playerRect, enemyRect):
                # 50 is an arbitrary number for a delay between damage, can be tweaked
                if self.screen.frame - self.lastCollisionFrame > 50:
                    print('dead!')

                self.lastCollisionFrame = self.screen.frame

        self.attacks[self.currentAttack][1]()

    def punch(self):
        for minion in self.minions:
            xSpeed = 6
            ySpeed = 0

            minion['x'] += xSpeed
            minion['y'] += ySpeed

        # If it is the current frame to draw a minion or there are no minions on the screen (meaning we want one ASAP)
        if (len(self.minions) < 4 and self.screen.frame % self.spawnDelay == 0) or len(self.minions) == 0:
            self.minions.append({
                'x': 0,
                'y': random.randint(self.battle.PLAYER_OFFSET_Y - 100, self.battle.PLAYER_OFFSET_Y)
            })

    def kick(self):
        for minion in self.minions:
            xSpeed = 3 * minion['dir']
            ySpeed = 3

            minion['x'] += xSpeed
            minion['y'] += ySpeed

        # If it is the current frame to draw a minion or there are no minions on the screen (meaning we want one ASAP)
        if (len(self.minions) < 10 and self.screen.frame % self.spawnDelay == 0) or len(self.minions) == 0:
            coinflip = random.randint(0, 1)

            self.minions.append({
                'x': random.randint(0, 150) if coinflip == 0 else random.randint(self.screen.SCREEN_WIDTH - 150, self.screen.SCREEN_WIDTH),
                'y': random.randint((self.screen.SCREEN_HEIGHT / 2) - 200, (self.screen.SCREEN_HEIGHT / 2) - 50),
                'dir': 1 if coinflip == 0 else -1
            })



        


        

        
