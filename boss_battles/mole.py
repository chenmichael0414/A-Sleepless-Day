import random
import pygame
from boss_battles.base import Boss
from colliders import ImageCollider

class Mole(Boss):
    def __init__(self, screen, battle, textbox):
        self.count = 0
        super().__init__(
            screen, 
            battle, 
            textbox, 
            './enemies/bosses/mole.png',
            519,
            [
                self.bolts
            ],
            {
                'bolt1': ImageCollider((0, 0), pygame.image.load('./attacks/bolt1.png').convert_alpha()),
                'bolt2': ImageCollider((0, 0), pygame.image.load('./attacks/bolt2.png').convert_alpha()),
                'bolt3': ImageCollider((0, 0), pygame.image.load('./attacks/bolt3.png').convert_alpha()),
                'ballFire': ImageCollider((0, 0), pygame.image.load('./attacks/ballFire.png').convert_alpha())
            }
        )

    def tick(self):
        if not self.sprite:
            return

        self.drawBoss()

        if self.textbox.drawIfIncomplete(['I am the fastest mole alive!', 'prepare to be electrified!'], 'mole intro'): 
            return

        for minion in self.minions:
            self.drawMinion(minion)
            self.collision(minion)

        self.attacks[self.currentAttack]()

    def reset(self):
        super().reset()

        self.textbox.resetFlag('mole intro')

    def bolts(self):
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

        if self.defeatedMinions < 40:
            # If it is the current frame to draw a minion
            if len(self.minions) < 10 and self.screen.frame % 30 == 0:
                self.count+=1
                if self.count%2 == 0:
                    topBoxCorner    = (self.screen.SCREEN_HEIGHT - self.battle.boxHeight) / 2
                    leftBoxCorner  = (self.screen.SCREEN_WIDTH - self.battle.boxWidth) / 2
                    yValue = random.randint(topBoxCorner, 2*topBoxCorner)
                    print(yValue)
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
                    
        elif len(self.minions) == 0:
            self.loadSprite(0)
            
            if self.textbox.drawIfIncomplete(['hey u win congrats!'], 'monkey final win'): return


        
