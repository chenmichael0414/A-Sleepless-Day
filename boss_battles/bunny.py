import random
import math
import pygame
from boss_battles.base import Boss

class Bunny(Boss):
    def __init__(self, screen, battle, textbox):
        super().__init__(
            screen, 
            battle, 
            textbox, 
            './enemies/bosses/bunny.png',
            308,
            [
                self.soundwave,
                self.carrot,
                self.soundwaveAndCarrot
            ]
        )

    def tick(self):
        if not self.sprite:
            return

        self.drawBoss()

        if self.textbox.drawIfIncomplete(['ahaahahah im a bunny or something', 'nom nom'], 'bunny intro'): return

        for minion in self.minions:
            self.drawMinion(minion)
            self.collision(minion)

        self.attacks[self.currentAttack]()

    def reset(self):
        super().reset()

        self.textbox.resetFlag('bunny intro')

    def soundwave(self):
        for minion in self.minions:
            xSpeed = 6
            ySpeed = 3 * math.sin(self.screen.frame)

            minion['x'] += xSpeed
            minion['y'] += ySpeed

        if self.defeatedMinions < 20:
            # If it is the current frame to draw a minion
            if len(self.minions) < 4 and self.screen.frame % 40 == 0:
                self.minions.append({
                    'x': 0,
                    'y': random.randint(self.battle.PLAYER_OFFSET_Y - 100, self.battle.PLAYER_OFFSET_Y),
                    'dir': 1,
                    'sprite': pygame.image.load('./attacks/soundwave.png').convert_alpha(),
                    'type': 'soundwave'
                })
        # If we have defeated enough minions to proceed and all of the minions have despawned, proceed
        elif len(self.minions) == 0:
            if self.textbox.drawIfIncomplete(['well, i like sound...', '......', '...but i love carrots!!!'], 'bunny soundwave win'): return

            self.defeatedMinions = 0
            self.currentAttack += 1

    def carrot(self):
        for minion in self.minions:
            xSpeed = 0
            ySpeed = random.randint(2, 7)

            minion['x'] += xSpeed
            minion['y'] += ySpeed

        if self.defeatedMinions < 30:
            # If it is the current frame to draw a minion
            if len(self.minions) < 6 and self.screen.frame % 40 == 0:
                leftBoxCorner  = (self.screen.SCREEN_WIDTH - self.battle.boxWidth) / 2
                rightBoxCorner = (self.screen.SCREEN_WIDTH + self.battle.boxWidth) / 2

                self.minions.append({
                    'x': random.randint(leftBoxCorner, rightBoxCorner),
                    'y': 0,
                    'dir': 1,
                    'sprite': pygame.image.load('./attacks/carrot.png').convert_alpha(),
                    'type': 'carrot'
                })
        # If we have defeated enough minions to proceed and all of the minions have despawned, proceed
        elif len(self.minions) == 0:
            if self.textbox.drawIfIncomplete(['NOW IM MAD!!!!!!!!'], 'bunny carrot win'): return

            self.defeatedMinions = 0
            self.currentAttack += 1

    def soundwaveAndCarrot(self):
        # Change the mode to free move
        self.battle.mode = "FREE MOVE"

        for minion in self.minions:
            if minion['type'] == 'soundwave':
                xSpeed = 3
                ySpeed = 3 * math.sin(self.screen.frame)

                minion['x'] += xSpeed
                minion['y'] += ySpeed
            elif minion['type'] == 'carrot':
                xSpeed = 0
                ySpeed = random.randint(2, 5)

                minion['x'] += xSpeed
                minion['y'] += ySpeed

        # 0 is soundwave, 1 is carrot (50/50)
        rng = random.randint(0, 1)

        if self.defeatedMinions < 40:
            # If it is the current frame to draw a minion
            if len(self.minions) < 10 and self.screen.frame % 30 == 0:
                topBoxCorner    = (self.screen.SCREEN_HEIGHT - self.battle.boxHeight) / 2
                bottomBoxCorner = (self.screen.SCREEN_HEIGHT + self.battle.boxHeight) / 2

                if rng == 0:
                    self.minions.append({
                    'x': 0,
                    'y': random.randint(topBoxCorner, bottomBoxCorner),
                    'dir': 1,
                    'sprite': pygame.image.load('./attacks/soundwave.png').convert_alpha(),
                    'type': 'soundwave'
                })
                else:
                    leftBoxCorner  = (self.screen.SCREEN_WIDTH - self.battle.boxWidth) / 2
                    rightBoxCorner = (self.screen.SCREEN_WIDTH + self.battle.boxWidth) / 2

                    self.minions.append({
                        'x': random.randint(leftBoxCorner, rightBoxCorner),
                        'y': 0,
                        'dir': 1,
                        'sprite': pygame.image.load('./attacks/carrot.png').convert_alpha(),
                        'type': 'carrot'
                    })
        elif len(self.minions) == 0:
            if self.textbox.drawIfIncomplete(['hey u win congrats!'], 'bunny final win'): return