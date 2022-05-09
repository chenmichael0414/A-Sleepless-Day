'''
Project: Choose Your Own Adventure Game
Team Members: Michael Chen, Kevin Guan, Preston Meek
Due Date: 5/9/2022
Task Description: Design a school-appropriate program that will let users move through rooms based on user input 
and get descriptions of each room.
'''

import math
import random
import pygame
from boss_battles.base import Boss
from colliders import ImageCollider

class Cat(Boss):
    def __init__(self, screen, battle, textbox):
        super().__init__(
            screen, 
            battle, 
            textbox, 
            'cat',
            [
                self.hat,
                self.fish,
                self.hatAndFish
            ],
            {
                'hat': ImageCollider((0, 0), pygame.image.load('./attacks/hat.png').convert_alpha()),
                'fish': ImageCollider((0, 0), pygame.image.load('./attacks/fish.png').convert_alpha())
            }
        )

    def tick(self):
        if not self.sprite:
            return

        self.drawBoss()

        if self.textbox.drawIfIncomplete(['meooooowwww', 'me..*ooowww* is what you\'re going to say when i defeat you!'], 'cat intro'): return

        for minion in self.minions:
            self.drawMinion(minion)
            self.collision(minion)

        self.attacks[self.currentAttack]()

    def reset(self):
        super().reset()

        self.textbox.resetFlag('cat intro')
        self.textbox.resetFlag('cat hat win')
        self.textbox.resetFlag('cat fish win')
        self.textbox.resetFlag('cat final win')
        self.textbox.resetFlag('cat reward item')

    def hat(self):
        for minion in self.minions:
            xSpeed = 4 * minion['dir']
            ySpeed = 5 * minion['trig'](self.screen.frame / 15)

            minion['x'] += xSpeed
            minion['y'] += ySpeed

        if self.defeatedMinions < 10: #10
            # If it is the current frame to draw a minion
            if len(self.minions) < 6 and self.screen.frame % 60 == 0:
                coinflip  = random.randint(0, 1)
                coinflip2 = random.randint(0, 1)

                self.minions.append({
                    'x': 0 if coinflip == 0 else self.screen.SCREEN_WIDTH,
                    'y': random.randint(self.battle.PLAYER_OFFSET_Y - 100, self.battle.PLAYER_OFFSET_Y),
                    'dir': 1 if coinflip == 0 else -1,
                    'sprite': pygame.image.load('./attacks/hat.png').convert_alpha(),
                    'trig': (lambda x: math.sin(x)) if coinflip2 == 0 else (lambda x: math.cos(x)),  # Changes the trig function for movement
                    'type': 'hat'
                })
        # If we have defeated enough minions to proceed and all of the minions have despawned, proceed
        elif len(self.minions) == 0:
            self.loadSprite(1)

            # Change the mode to free move for the next phase
            self.battle.mode = "FREE MOVE"

            if self.textbox.drawIfIncomplete(['you know, i\'m a little hungry...'], 'cat hat win'): return

            self.defeatedMinions = 0
            self.currentAttack += 1

    def fish(self):
        for minion in self.minions:
            # Parabolic motion
            minion['x'] += minion['xSpeed'] * minion['dir']
            minion['y'] = ((minion['x'] - (self.screen.SCREEN_WIDTH / 2)) ** 2) * .001 + minion['yOffset']

        if self.defeatedMinions < 10: #10
            # If it is the current frame to draw a minion
            if len(self.minions) < 4 and self.screen.frame % 40 == 0:
                coinflip = random.randint(0, 1)
                yOffset  = random.randint(self.screen.SCREEN_HEIGHT / 2 - 200, self.screen.SCREEN_HEIGHT / 2 + 140)

                fish = pygame.image.load('./attacks/fish.png').convert_alpha()

                self.minions.append({
                    'x': 0 if coinflip == 0 else self.screen.SCREEN_WIDTH,
                    'xSpeed': random.randint(3, 5),
                    'yOffset': yOffset,
                    'y': (self.screen.SCREEN_WIDTH / 2) ** 2 * .001 + yOffset,
                    'dir': 1 if coinflip == 0 else -1,
                    'sprite': pygame.transform.flip(fish, True, False) if coinflip == 0 else fish,
                    'type': 'fish'
                })
        # If we have defeated enough minions to proceed and all of the minions have despawned, proceed
        elif len(self.minions) == 0:
            self.loadSprite(3)

            if self.textbox.drawIfIncomplete(['AAAAHHHH!!!! *meow :3*'], 'cat fish win'): return

            self.defeatedMinions = 0
            self.currentAttack += 1

    def hatAndFish(self):
        for minion in self.minions:
            if minion['type'] == 'hat':
                xSpeed = 4 * minion['dir']
                ySpeed = 5 * minion['trig'](self.screen.frame / 15)

                minion['x'] += xSpeed
                minion['y'] += ySpeed
            elif minion['type'] == 'fish':
                # Parabolic motion
                minion['x'] += minion['xSpeed'] * minion['dir']
                minion['y'] = ((minion['x'] - (self.screen.SCREEN_WIDTH / 2)) ** 2) * .001 + minion['yOffset']

        # 0-2 is fish, 3-4 is hat
        rng = random.randint(0, 4)

        if self.defeatedMinions < 40: # 40
            # If it is the current frame to draw a minion
            if len(self.minions) < 7 and self.screen.frame % 25 == 0:
                if rng <= 2:
                    coinflip = random.randint(0, 1)
                    yOffset  = random.randint(self.screen.SCREEN_HEIGHT / 2 - 200, self.screen.SCREEN_HEIGHT / 2 + 140)

                    fish = pygame.image.load('./attacks/fish.png').convert_alpha()

                    self.minions.append({
                        'x': 0 if coinflip == 0 else self.screen.SCREEN_WIDTH,
                        'xSpeed': random.randint(3, 5),
                        'yOffset': yOffset,
                        'y': (self.screen.SCREEN_WIDTH / 2) ** 2 * .001 + yOffset,
                        'dir': 1 if coinflip == 0 else -1,
                        'sprite': pygame.transform.flip(fish, True, False) if coinflip == 0 else fish,
                        'type': 'fish'
                    })
                else:
                    coinflip  = random.randint(0, 1)
                    coinflip2 = random.randint(0, 1)

                    self.minions.append({
                        'x': 0 if coinflip == 0 else self.screen.SCREEN_WIDTH,
                        'y': random.randint(self.battle.PLAYER_OFFSET_Y - 200, self.battle.PLAYER_OFFSET_Y + 100),
                        'dir': 1 if coinflip == 0 else -1,
                        'sprite': pygame.image.load('./attacks/hat.png').convert_alpha(),
                        'trig': (lambda x: math.sin(x)) if coinflip2 == 0 else (lambda x: math.cos(x)),  # Changes the trig function for movement
                        'type': 'hat'
                    })
        elif len(self.minions) == 0:
            self.loadSprite(0)
            if self.textbox.drawIfIncomplete(['well... i guess that\'s it for me...', 'me-owwww...'], 'cat final win'): return

            self.loadSprite(None)
            if self.item.rewardItem('key fragment #1', 'cat reward item'): return

            self.battle.end()
            


        

        
