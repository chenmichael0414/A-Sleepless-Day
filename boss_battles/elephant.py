import random
import pygame
from boss_battles.base import Boss
from colliders import ImageCollider

class Elephant(Boss):
    def __init__(self, screen, battle, textbox):
        self.batstacheDict = [
            ['batstache1', pygame.image.load('./attacks/batstache1.png').convert_alpha()],
            ['batstache1', pygame.image.load('./attacks/batstache1.png').convert_alpha()],
            ['batstache2', pygame.image.load('./attacks/batstache2.png').convert_alpha()],
            ['batstache3', pygame.image.load('./attacks/batstache3.png').convert_alpha()],
            ['batstache4', pygame.image.load('./attacks/batstache4.png').convert_alpha()],
            ['batstache4', pygame.image.load('./attacks/batstache4.png').convert_alpha()],
            ['batstache3', pygame.image.load('./attacks/batstache3.png').convert_alpha()],
            ['batstache2', pygame.image.load('./attacks/batstache2.png').convert_alpha()],
            ['batstache1', pygame.image.load('./attacks/batstache1.png').convert_alpha()]
        ]
        super().__init__(
            screen, 
            battle, 
            textbox, 
            'elephant',
            [
                self.batstache
            ],
            {
                'batstache1': ImageCollider((0, 0), pygame.image.load('./attacks/batstache1.png').convert_alpha()),
                'batstache2': ImageCollider((0, 0), pygame.image.load('./attacks/batstache2.png').convert_alpha()),
                'batstache3': ImageCollider((0, 0), pygame.image.load('./attacks/batstache3.png').convert_alpha()),
                'batstache4': ImageCollider((0, 0), pygame.image.load('./attacks/batstache4.png').convert_alpha())
            }
        )

    def tick(self):
        if not self.sprite:
            return

        self.drawBoss()

        if self.textbox.drawIfIncomplete(['Face my hoard of bat-staches!'], 'elephant intro'): 
            self.battle.mode = "FREE MOVE"
            return


        for minion in self.minions:
            self.drawMinion(minion)
            self.collision(minion)

        self.attacks[self.currentAttack]()

    def reset(self):
        super().reset()

        self.textbox.resetFlag('elephant intro')

    def batstache(self):
        for minion in self.minions:

            if self.screen.frame % 30 == 0:
                if minion['dir']==1:
                    minion['speed'][0] = random.randint(1,4)
                    minion['speed'][1] = random.randint(-5,5)
                    minion['dir']=0
                else:
                    minion['speed'][0] = 0
                    minion['speed'][1] = 0
                    minion['dir']=1


            minion['x'] += minion['speed'][0]
            minion['y'] += minion['speed'][1]
            if self.screen.frame % 4 == 0:
                minion['sprite'] = self.batstacheDict[minion['animation']][1]
                minion['type'] = self.batstacheDict[minion['animation']][0]
                minion['animation']+=1
                if minion['animation']>8:
                    minion['animation']=0

                


        if self.defeatedMinions < 30:
            # If it is the current frame to draw a minion
            if len(self.minions) < 20 and self.screen.frame % 30 == 0:
                self.minions.append({
                        'x': 0,
                        'y': self.screen.SCREEN_HEIGHT/2,
                        'dir': 1,
                        'sprite': pygame.image.load('./attacks/batstache1.png').convert_alpha(),
                        'type': 'batstache1',
                        'animation': 0,
                        'speed': [random.randint(1,4),random.randint(-5,5)]
                })

            elif len(self.minions) == 0:
                self.loadSprite(2)

                if self.textbox.drawIfIncomplete(['Now I\'m angry!'], 'mole bolt win'): return

                self.defeatedMinions = 0
                self.currentAttack += 1

        

        
