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
            self.punch,
            self.kick,
            self.punchAndKick
        ]
        self.currentAttack = 0

        self.minions = []
        self.defeatedMinions = 0

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

        if self.textbox.drawIfIncomplete(['oohoohooh aahahahah', 'i am going to defeat you!!!'], 'monkey intro'): return

        for minion in self.minions:
            self.screen.drawSprite(
                minion['sprite'],
                (
                    minion['x'],
                    minion['y']
                ),
            )

            # If the minion goes off screen (therefore it is defeated)
            if minion['x'] > self.screen.SCREEN_WIDTH or minion['y'] > self.screen.SCREEN_HEIGHT:
                self.minions.remove(minion)
                self.defeatedMinions += 1

            minionW, minionH = minion['sprite'].get_size()

            playerRect = pygame.Rect(
                self.battle.PLAYER_OFFSET_X + self.battle.playerX, 
                self.battle.PLAYER_OFFSET_Y - self.battle.playerY, 
                self.battle.playerSize, 
                self.battle.playerSize
            )

            enemyRect = pygame.Rect(minion['x'], minion['y'], minionW, minionH)

            if pygame.Rect.colliderect(playerRect, enemyRect):
                # 20 is an arbitrary number for a delay between damage, can be tweaked
                if self.screen.frame - self.lastCollisionFrame > 20:
                    self.battle.takeDamage()

                self.lastCollisionFrame = self.screen.frame

        self.attacks[self.currentAttack]()

    def reset(self):
        self.loadSprite()

        self.currentAttack = 0
        self.minions = []
        self.defeatedMinions = 0
        self.lastCollisionFrame = 0

        self.textbox.resetFlag('monkey intro')
        self.textbox.resetFlag('monkey punch win')
        self.textbox.resetFlag('monkey kick win')
        self.textbox.resetFlag('monkey final win')

    def punch(self):
        for minion in self.minions:
            xSpeed = 6
            ySpeed = 0

            minion['x'] += xSpeed
            minion['y'] += ySpeed

        if self.defeatedMinions < 20:
            # If it is the current frame to draw a minion
            if len(self.minions) < 4 and self.screen.frame % 40 == 0:
                self.minions.append({
                    'x': 0,
                    'y': random.randint(self.battle.PLAYER_OFFSET_Y - 100, self.battle.PLAYER_OFFSET_Y),
                    'dir': 1,
                    'sprite': pygame.image.load('./attacks/punch.png').convert_alpha(),
                    'type': 'punch'
                })
        # If we have defeated enough minions to proceed and all of the minions have despawned, proceed
        elif len(self.minions) == 0:
            if self.textbox.drawIfIncomplete(['uhhh good job i guess...'], 'monkey punch win'): return

            self.defeatedMinions = 0
            self.currentAttack += 1

    def kick(self):
        for minion in self.minions:
            xSpeed = 4 * minion['dir']
            ySpeed = 4

            minion['x'] += xSpeed
            minion['y'] += ySpeed

        if self.defeatedMinions < 40:
            # If it is the current frame to draw a minion
            if len(self.minions) < 8 and self.screen.frame % 20 == 0:
                coinflip = random.randint(0, 1)
                kick     = pygame.image.load('./attacks/kick.png').convert_alpha()

                # Basically just generates some nice random position data
                # Conflip determines if the kick comes from the left or right
                self.minions.append({
                    'x': random.randint(0, 150) if coinflip == 0 else random.randint(self.screen.SCREEN_WIDTH - 150, self.screen.SCREEN_WIDTH),
                    'y': random.randint((self.screen.SCREEN_HEIGHT / 2) - 200, (self.screen.SCREEN_HEIGHT / 2) - 60),
                    'dir': 1 if coinflip == 0 else -1,
                    'sprite': pygame.transform.flip(kick, True, False) if coinflip == 0 else kick,
                    'type': 'kick'
                })
        elif len(self.minions) == 0:
            if self.textbox.drawIfIncomplete(['*really agitated monkey noises*'], 'monkey kick win'): return

            self.defeatedMinions = 0
            self.currentAttack += 1

    def punchAndKick(self):
        for minion in self.minions:
            if minion['type'] == 'punch':
                xSpeed = 6
                ySpeed = 0

                minion['x'] += xSpeed
                minion['y'] += ySpeed
            elif minion['type'] == 'kick':
                xSpeed = 4 * minion['dir']
                ySpeed = 4

                minion['x'] += xSpeed
                minion['y'] += ySpeed

        # 0-2 is punch, 3-4 is kick
        rng = random.randint(0, 4)

        if self.defeatedMinions < 40:
            # If it is the current frame to draw a minion
            if len(self.minions) < 10 and self.screen.frame % 30 == 0:
                if rng <= 2:
                    self.minions.append({
                        'x': 0,
                        'y': random.randint(self.battle.PLAYER_OFFSET_Y - 100, self.battle.PLAYER_OFFSET_Y - 50),
                        'dir': 1,
                        'sprite': pygame.image.load('./attacks/punch.png').convert_alpha(),
                        'type': 'punch'
                    })
                else:
                    coinflip = random.randint(0, 1)
                    kick     = pygame.image.load('./attacks/kick.png').convert_alpha()

                    # Basically just generates some nice random position data
                    # Conflip determines if the kick comes from the left or right
                    self.minions.append({
                        'x': random.randint(0, 150) if coinflip == 0 else random.randint(self.screen.SCREEN_WIDTH - 150, self.screen.SCREEN_WIDTH),
                        'y': random.randint((self.screen.SCREEN_HEIGHT / 2) - 200, (self.screen.SCREEN_HEIGHT / 2) - 50),
                        'dir': 1 if coinflip == 0 else -1,
                        'sprite': pygame.transform.flip(kick, True, False) if coinflip == 0 else kick,
                        'type': 'kick'
                    })
        elif len(self.minions) == 0:
            if self.textbox.drawIfIncomplete(['hey u win congrats!'], 'monkey final win'): return

            # self.defeatedMinions = 0
            # self.currentAttack += 1



        


        

        
