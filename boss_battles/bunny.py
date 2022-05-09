'''
Project: Choose Your Own Adventure Game
Team Members: Michael Chen, Kevin Guan, Preston Meek
Due Date: 5/9/2022
Task Description: Design a school-appropriate program that will let users move through rooms based on user input 
and get descriptions of each room.
'''

import random
import math
import pygame
from boss_battles.base import Boss
from colliders import ImageCollider

class Bunny(Boss):
    def __init__(self, screen, battle, textbox):
        super().__init__(
            screen, 
            battle, 
            textbox, 
            'bunny',
            [
                self.soundwave,
                self.carrot,
                self.soundwaveAndCarrot
            ],
            {
                'soundwave': ImageCollider((0, 0), pygame.image.load('./attacks/soundwave.png').convert_alpha()),
                'carrot': ImageCollider((0, 0), pygame.image.load('./attacks/carrot.png').convert_alpha()),
            }
        )

    def tick(self):
        if not self.sprite:
            return

        self.drawBoss()

        if self.textbox.drawIfIncomplete(['Yo, DJ Bunny\'s about to show you what\'s up.', 'Give yourself to the rhythm.'], 'bunny intro'): return

        for minion in self.minions:
            self.drawMinion(minion)
            self.collision(minion)

        self.attacks[self.currentAttack]()

    def reset(self):
        super().reset()

        self.textbox.resetFlag('bunny intro')
        self.textbox.resetFlag('bunny soundwave win')
        self.textbox.resetFlag('bunny carrot win')
        self.textbox.resetFlag('bunny final win')
        self.textbox.resetFlag('bunny reward item')

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
            self.loadSprite(2)

            if self.textbox.drawIfIncomplete(['I hear carrots are good for your eyes.'], 'bunny soundwave win'): return

            self.defeatedMinions = 0
            self.currentAttack += 1

    def carrot(self):
        for minion in self.minions:
            minion['ySpeed'] *= minion['yAccel']
            minion['y']      += minion['ySpeed']

        if self.defeatedMinions < 30:
            # If it is the current frame to draw a minion
            if len(self.minions) < 6 and self.screen.frame % 40 == 0:
                leftBoxCorner  = (self.screen.SCREEN_WIDTH - self.battle.boxWidth) / 2
                rightBoxCorner = (self.screen.SCREEN_WIDTH + self.battle.boxWidth) / 2

                self.minions.append({
                    'x': random.randint(leftBoxCorner, rightBoxCorner - 50),    # - 50 to roughly account for the width of the carrot
                    'y': 0,
                    'ySpeed': 1,
                    'yAccel': random.uniform(1.015, 1.03),
                    'dir': 1,
                    'sprite': pygame.image.load('./attacks/carrot.png').convert_alpha(),
                    'type': 'carrot'
                })
        # If we have defeated enough minions to proceed and all of the minions have despawned, proceed
        elif len(self.minions) == 0:
            self.loadSprite(3)

            # Change the mode to free move for the next phase
            self.battle.mode = "FREE MOVE"

            if self.textbox.drawIfIncomplete(['I could do this all day.'], 'bunny carrot win'): return

            self.defeatedMinions = 0
            self.currentAttack += 1

    def soundwaveAndCarrot(self):
        for minion in self.minions:
            if minion['type'] == 'soundwave':
                xSpeed = 3
                ySpeed = 3 * math.sin(self.screen.frame)

                minion['x'] += xSpeed
                minion['y'] += ySpeed
            elif minion['type'] == 'carrot':
                minion['ySpeed'] *= minion['yAccel']
                minion['y']      += minion['ySpeed']

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
                        'x': random.randint(leftBoxCorner, rightBoxCorner - 50),    # - 50 to roughly account for the width of the carrot
                        'y': 0,
                        'ySpeed': 1,
                        'yAccel': random.uniform(1.015, 1.03),
                        'dir': 1,
                        'sprite': pygame.image.load('./attacks/carrot.png').convert_alpha(),
                        'type': 'carrot'
                    })
        elif len(self.minions) == 0:
            self.loadSprite(0)
            if self.textbox.drawIfIncomplete(['You\'re killing my vibe, man.'], 'bunny final win'): return

            self.loadSprite(None)
            if self.item.rewardItem('key fragment #2', 'bunny reward item'): return

            self.battle.end()