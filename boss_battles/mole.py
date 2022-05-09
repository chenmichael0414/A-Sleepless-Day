'''
Project: Choose Your Own Adventure Game
Team Members: Michael Chen, Kevin Guan, Preston Meek
Due Date: 5/9/2022
Task Description: Design a school-appropriate program that will let users move through rooms based on user input 
and get descriptions of each room.
'''

import random
import pygame
from boss_battles.base import Boss
from colliders import ImageCollider

class Mole(Boss):
    def __init__(self, screen, battle, textbox):
        # Used to alter between vertical and diagnol lightning bolts
        self.count = 0
        # Used to change tornado y speed at certain intervals
        self.change = 0
        # Used to remember the current ySpeed when the tornado speed is not changing
        self.yMemory = 0

        super().__init__(
            screen, 
            battle, 
            textbox, 
            'mole',
            [
                self.tornado,
                self.bolts,
                self.tornadoBolts
            ],
            {
                'bolt1': ImageCollider((0, 0), pygame.image.load('./attacks/bolt1.png').convert_alpha()),
                'bolt2': ImageCollider((0, 0), pygame.image.load('./attacks/bolt2.png').convert_alpha()),
                'bolt3': ImageCollider((0, 0), pygame.image.load('./attacks/bolt3.png').convert_alpha()),
                'tornado': ImageCollider((0, 0), pygame.image.load('./attacks/tornado.png').convert_alpha())
            }
        )

    def tick(self):
        if not self.sprite:
            return

        self.drawBoss()

        if self.textbox.drawIfIncomplete(['I am the fastest mole alive!', 'Feel the wind beneath my feet!'], 'mole intro'): 
            # Change the mode to free move for the entire phase
            self.battle.mode = "FREE MOVE"
            return

        for minion in self.minions:
            self.drawMinion(minion)
            self.collision(minion)

        self.attacks[self.currentAttack]()

    # This resets all the important flags for the boss
    # This is for text dialogue purposes
    def reset(self):
        super().reset()

        self.textbox.resetFlag('mole intro')
        self.textbox.resetFlag('mole tornado win')
        self.textbox.resetFlag('mole bolt win')
        self.textbox.resetFlag('mole final win')
        self.textbox.resetFlag('mole reward item')

    # First attack
    def tornado(self):
        # Move the minions based on their random speed
        for minion in self.minions:
            xSpeed = random.randint(0,4)
            # Speed can only be a factor of 3, making it much more jittery in it's movements
            xSpeed*=3
            # Only changes every 60 frames to a random ySpeed
            if self.change%60==0:
                ySpeed = random.randint(-5,5)
                self.yMemory = ySpeed
            # Uses the previous ySpeed
            else:
                ySpeed = self.yMemory

            self.change+=1

            minion['x'] += xSpeed
            minion['y'] += ySpeed
            

        if self.defeatedMinions < 30:
            topQuarter    = (2*self.screen.SCREEN_HEIGHT - self.battle.boxHeight) / 4
            bottomQuarter = (2*self.screen.SCREEN_HEIGHT + self.battle.boxHeight) / 4
            # If it is the current frame to draw a minion
            if len(self.minions) < 10 and self.screen.frame % 35 == 0:
                self.minions.append({
                        'x': 0,
                        'y': random.randint(int(topQuarter), int(bottomQuarter)),
                        'dir': 1,
                        'sprite': pygame.image.load('./attacks/tornado.png').convert_alpha(),
                        'type': 'tornado'
                })
        # If we have defeated enough minions to proceed and all of the minions have despawned, proceed
        elif len(self.minions) == 0:
            self.loadSprite(1)

            if self.textbox.drawIfIncomplete(['Now face the wrath of my lightning!!'], 'mole tornado win'): return

            self.defeatedMinions = 0
            self.currentAttack += 1

    # Second attack
    def bolts(self):
        # Move the minions based on their type
        # bolts for left diagnol, right diagnol, and vertical
        for minion in self.minions:
            if minion['type'] == 'bolt1':
                xSpeed = -4
                ySpeed = 4

                minion['x'] += xSpeed
                minion['y'] += ySpeed
            elif minion['type'] == 'bolt2':
                xSpeed = 0
                ySpeed = 7

                minion['x'] += xSpeed
                minion['y'] += ySpeed
            elif minion['type'] == 'bolt3':
                xSpeed = 4
                ySpeed = 4

                minion['x'] += xSpeed
                minion['y'] += ySpeed

        if self.defeatedMinions < 30:
            # If it is the current frame to draw a minion
            if len(self.minions) < 10 and self.screen.frame % 45 == 0:
                # Alternates between 2 downward bolts and 2 diagnol bolts
                self.count+=1
                if self.count%2 == 0:
                    topBoxCorner    = (self.screen.SCREEN_HEIGHT - self.battle.boxHeight) / 2
                    leftBoxCorner  = (self.screen.SCREEN_WIDTH - self.battle.boxWidth) / 2
                    yValue = random.randint(topBoxCorner, 2*topBoxCorner)
                    self.minions.append({
                        'x': leftBoxCorner,
                        'y': yValue,
                        'dir': 1,
                        'sprite': pygame.image.load('./attacks/bolt3.png').convert_alpha(),
                        'type': 'bolt3'
                    })
                    rightBoxCorner = (self.screen.SCREEN_WIDTH + self.battle.boxWidth) / 2
                    self.minions.append({
                        'x': rightBoxCorner - 50,
                        'y': yValue,
                        'dir': 1,
                        'sprite': pygame.image.load('./attacks/bolt1.png').convert_alpha(),
                        'type': 'bolt1'
                    })
                else:
                    leftBoxCorner  = (self.screen.SCREEN_WIDTH - self.battle.boxWidth) / 2
                    rightBoxCorner = (self.screen.SCREEN_WIDTH + self.battle.boxWidth) / 2
                    self.minions.append({
                        'x': random.randint(leftBoxCorner, rightBoxCorner - 50),
                        'y': 0,
                        'dir': 1,
                        'sprite': pygame.image.load('./attacks/bolt2.png').convert_alpha(),
                        'type': 'bolt2'
                    })
                    self.minions.append({
                        'x': random.randint(leftBoxCorner, rightBoxCorner - 50),
                        'y': 0,
                        'dir': 1,
                        'sprite': pygame.image.load('./attacks/bolt2.png').convert_alpha(),
                        'type': 'bolt2'
                    })
        # If we have defeated enough minions to proceed and all of the minions have despawned, proceed
        elif len(self.minions) == 0:
            self.loadSprite(2)

            if self.textbox.drawIfIncomplete(['Now I\'m angry!'], 'mole bolt win'): return

            self.defeatedMinions = 0
            self.currentAttack += 1
                    
    # Final attack
    def tornadoBolts(self):
        # Move the minions based on their type
        for minion in self.minions:
            if minion['type'] == 'bolt1':
                xSpeed = -4
                ySpeed = 4

                minion['x'] += xSpeed
                minion['y'] += ySpeed
            elif minion['type'] == 'bolt2':
                xSpeed = 0
                ySpeed = 7

                minion['x'] += xSpeed
                minion['y'] += ySpeed
            elif minion['type'] == 'bolt3':
                xSpeed = 4
                ySpeed = 4

                minion['x'] += xSpeed
                minion['y'] += ySpeed
            elif minion['type'] == 'tornado':
                xSpeed = random.randint(0,4)
                xSpeed*=3
                if self.change%30==0:
                    ySpeed = random.randint(-5,5)
                    self.yMemory = ySpeed
                else:
                    ySpeed = self.yMemory

                self.change+=1
                minion['x'] += xSpeed
                minion['y'] += ySpeed
        # Randomly uses diagnol bolts, vertical bolts, or tornados
        rng = random.randint(0,4)
        if self.defeatedMinions < 45:
            # If it is the current frame to draw a minion
            if len(self.minions) < 10 and self.screen.frame % 35 == 0:
                # 2/5 chance to use diagnol bolts
                if rng < 2:
                    topBoxCorner   = (self.screen.SCREEN_HEIGHT - self.battle.boxHeight) / 2
                    leftBoxCorner  = (self.screen.SCREEN_WIDTH - self.battle.boxWidth) / 2
                    yValue = random.randint(topBoxCorner, 2*topBoxCorner)
                    self.minions.append({
                        'x': leftBoxCorner,
                        'y': yValue,
                        'dir': 1,
                        'sprite': pygame.image.load('./attacks/bolt3.png').convert_alpha(),
                        'type': 'bolt3'
                    })
                    rightBoxCorner = (self.screen.SCREEN_WIDTH + self.battle.boxWidth) / 2
                    self.minions.append({
                        'x': rightBoxCorner - 50,
                        'y': yValue,
                        'dir': 1,
                        'sprite': pygame.image.load('./attacks/bolt1.png').convert_alpha(),
                        'type': 'bolt1'
                    })
                # 2/5 chance to use vertical bolts
                elif rng < 4:
                    leftBoxCorner  = (self.screen.SCREEN_WIDTH - self.battle.boxWidth) / 2
                    rightBoxCorner = (self.screen.SCREEN_WIDTH + self.battle.boxWidth) / 2
                    self.minions.append({
                        'x': random.randint(leftBoxCorner, rightBoxCorner - 50),
                        'y': 0,
                        'dir': 1,
                        'sprite': pygame.image.load('./attacks/bolt2.png').convert_alpha(),
                        'type': 'bolt2'
                    })
                    self.minions.append({
                        'x': random.randint(leftBoxCorner, rightBoxCorner - 50),
                        'y': 0,
                        'dir': 1,
                        'sprite': pygame.image.load('./attacks/bolt2.png').convert_alpha(),
                        'type': 'bolt2'
                    })
                # 1/5 chance to use tornado
                else:
                    topQuarter    = (2*self.screen.SCREEN_HEIGHT - self.battle.boxHeight) / 4
                    bottomQuarter = (2*self.screen.SCREEN_HEIGHT + self.battle.boxHeight) / 4
                    # If it is the current frame to draw a minion
                    if len(self.minions) < 10 and self.screen.frame % 35 == 0:
                        self.minions.append({
                                'x': 0,
                                'y': random.randint(int(topQuarter), int(bottomQuarter)),
                                'dir': 1,
                                'sprite': pygame.image.load('./attacks/tornado.png').convert_alpha(),
                                'type': 'tornado'
                        })
                    


        elif len(self.minions) == 0:
            self.loadSprite(0)
            if self.textbox.drawIfIncomplete(['there\'s...', '...something in the way...'], 'mole final win'): return

            self.loadSprite(None)
            if self.item.rewardItem('key fragment #4', 'mole reward item'): return

            self.battle.end()


        
