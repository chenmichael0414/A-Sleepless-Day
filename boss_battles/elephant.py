import random
import pygame
from boss_battles.base import Boss
from colliders import ImageCollider

class Elephant(Boss):
    def __init__(self, screen, battle, textbox):
        # List containing full batstache animation frames
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
                self.words,
                self.batstache,
                self.wordsBatstache
            ],
            {
                'batstache1': ImageCollider((0, 0), pygame.image.load('./attacks/batstache1.png').convert_alpha()),
                'batstache2': ImageCollider((0, 0), pygame.image.load('./attacks/batstache2.png').convert_alpha()),
                'batstache3': ImageCollider((0, 0), pygame.image.load('./attacks/batstache3.png').convert_alpha()),
                'batstache4': ImageCollider((0, 0), pygame.image.load('./attacks/batstache4.png').convert_alpha()),
                'word1': ImageCollider((0, 0), pygame.image.load('./attacks/word1.png').convert_alpha()),
                'word2': ImageCollider((0, 0), pygame.image.load('./attacks/word2.png').convert_alpha())
            }
        )

    def tick(self):
        if not self.sprite:
            return

        self.drawBoss()

        if self.textbox.drawIfIncomplete(['Face my expansive vocabulary!'], 'elephant intro'): 
            return


        for minion in self.minions:
            self.drawMinion(minion)
            self.collision(minion)

        self.attacks[self.currentAttack]()

    def reset(self):
        super().reset()

        self.textbox.resetFlag('elephant intro')
        self.textbox.resetFlag('elephant words win')
        self.textbox.resetFlag('elephant batstache win')
        self.textbox.resetFlag('elephant final win')
        self.textbox.resetFlag('elephant reward item')

    def words(self):
        for minion in self.minions:
            # This word will come from the left slowly, before speeding to the right
            if minion['type']=='word1':
                if self.screen.frame % 20 == 0:
                    if minion['dir']==1:
                        minion['speed'][0] = 1
                        minion['speed'][1] = 0
                        minion['dir']+=1
                    elif minion['dir']==2:
                        minion['speed'][0] = 0
                        minion['speed'][1] = 0
                        minion['dir']+=1
                    else:
                        minion['speed'][0] = 25
                        minion['speed'][1] = 0
            # This word will come from the top slowly, before speeding to the bottom
            else:
                if self.screen.frame % 50 == 0:
                    if minion['dir']==1:
                        minion['speed'][0] = 0
                        minion['speed'][1] = 1
                        minion['dir']+=1
                    elif minion['dir']==2:
                        minion['speed'][0] = 0
                        minion['speed'][1] = 0
                        minion['dir']+=1
                    else:
                        minion['speed'][0] = 0
                        minion['speed'][1] = 25

            minion['x'] += minion['speed'][0]
            minion['y'] += minion['speed'][1]
        if self.defeatedMinions < 30:
            #  1st word
            #  If it is the current frame to draw a minion
            if len(self.minions) < 10 and self.screen.frame % 60 == 0:
                bottomBoxCorner = (self.screen.SCREEN_HEIGHT + self.battle.boxHeight) / 2
                self.minions.append({
                        'x': 0,
                        'y': bottomBoxCorner-32,
                        'dir': 1,
                        'sprite': pygame.image.load('./attacks/word1.png').convert_alpha(),
                        'type': 'word1',
                        'animation': 0,
                        'speed': [random.randint(1,4),random.randint(-2,0)]
                })
            #  2nd word
            if len(self.minions) < 10 and self.screen.frame % 150 == 0:
                leftBoxCorner  = (self.screen.SCREEN_WIDTH - self.battle.boxWidth) / 2
                rightBoxCorner = (self.screen.SCREEN_WIDTH + self.battle.boxWidth) / 2
                self.minions.append({
                        'x': random.randint(leftBoxCorner, rightBoxCorner-200),
                        'y': 0,
                        'dir': 1,
                        'sprite': pygame.image.load('./attacks/word2.png').convert_alpha(),
                        'type': 'word2',
                        'animation': 0,
                        'speed': [random.randint(-1,1),0]
                })

        # If we have defeated enough minions to proceed and all of the minions have despawned, proceed
        elif len(self.minions) == 0:
            self.loadSprite(1)

            if self.textbox.drawIfIncomplete(['Words may not hurt you, but my hoard of batstaches will!'], 'elephant words win'): 
                # Change the mode to free move for the next phase
                self.battle.mode = "FREE MOVE"
                return

            self.defeatedMinions = 0
            self.currentAttack += 1


    def batstache(self):
        for minion in self.minions:
            
            # The batstache will alternate between moving randomly and pausing
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
            # Cycles through the batstache sprites every 4 frames
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
        # If we have defeated enough minions to proceed and all of the minions have despawned, proceed
        elif len(self.minions) == 0:
            self.loadSprite(2)

            if self.textbox.drawIfIncomplete(['That\'s it, you sir are done for now!'], 'elephant mustache win'): return

            self.defeatedMinions = 0
            self.currentAttack += 1

    def wordsBatstache(self):
        for minion in self.minions:
            # these if statements decide how the minion will move depending on what sprite it is
            if minion['type']=='word1':
                if self.screen.frame % 20 == 0:
                    if minion['dir']==1:
                        minion['speed'][0] = 1
                        minion['speed'][1] = 0
                        minion['dir']+=1
                    elif minion['dir']==2:
                        minion['speed'][0] = 0
                        minion['speed'][1] = 0
                        minion['dir']+=1
                    else:
                        minion['speed'][0] = 25
                        minion['speed'][1] = 0
            elif minion['type']=='word2':
                if self.screen.frame % 50 == 0:
                    if minion['dir']==1:
                        minion['speed'][0] = 0
                        minion['speed'][1] = 1
                        minion['dir']+=1
                    elif minion['dir']==2:
                        minion['speed'][0] = 0
                        minion['speed'][1] = 0
                        minion['dir']+=1
                    else:
                        minion['speed'][0] = 0
                        minion['speed'][1] = 25
            else:
                if self.screen.frame % 30 == 0:
                    if minion['dir']==1:
                        minion['speed'][0] = random.randint(1,4)
                        minion['speed'][1] = random.randint(-5,5)
                        minion['dir']=0
                    else:
                        minion['speed'][0] = 0
                        minion['speed'][1] = 0
                        minion['dir']=1
                if self.screen.frame % 4 == 0:
                    minion['sprite'] = self.batstacheDict[minion['animation']][1]
                    minion['type'] = self.batstacheDict[minion['animation']][0]
                    minion['animation']+=1
                    if minion['animation']>8:
                        minion['animation']=0
            minion['x'] += minion['speed'][0]
            minion['y'] += minion['speed'][1]

        if self.defeatedMinions < 45:
            # Multiple if statements used to individually track each type of minion
            # If it is the current frame to draw a minion
            if len(self.minions) < 20 and self.screen.frame % 60 == 0:
                bottomBoxCorner = (self.screen.SCREEN_HEIGHT + self.battle.boxHeight) / 2
                topBoxCorner    = (self.screen.SCREEN_HEIGHT - self.battle.boxHeight) / 2
                self.minions.append({
                        'x': 0,
                        'y': random.randint(topBoxCorner, bottomBoxCorner-32),
                        'dir': 1,
                        'sprite': pygame.image.load('./attacks/word1.png').convert_alpha(),
                        'type': 'word1',
                        'animation': 0,
                        'speed': [random.randint(1,4),0]
                })
            if len(self.minions) < 20 and self.screen.frame % 150 == 0:
                leftBoxCorner  = (self.screen.SCREEN_WIDTH - self.battle.boxWidth) / 2
                rightBoxCorner = (self.screen.SCREEN_WIDTH + self.battle.boxWidth) / 2
                self.minions.append({
                        'x': random.randint(leftBoxCorner, rightBoxCorner-200),
                        'y': 0,
                        'dir': 1,
                        'sprite': pygame.image.load('./attacks/word2.png').convert_alpha(),
                        'type': 'word2',
                        'animation': 0,
                        'speed': [random.randint(-1,1),0]
                })
            if len(self.minions) < 15 and self.screen.frame % 30 == 0:
                self.minions.append({
                        'x': 0,
                        'y': self.screen.SCREEN_HEIGHT/2,
                        'dir': 1,
                        'sprite': pygame.image.load('./attacks/batstache1.png').convert_alpha(),
                        'type': 'batstache1',
                        'animation': 0,
                        'speed': [random.randint(1,4),random.randint(-5,5)]
                })
        # If we have defeated enough minions to proceed and all of the minions have despawned, proceed
        elif len(self.minions) == 0:
            self.loadSprite(0)
            if self.textbox.drawIfIncomplete(['perhaps it\'s time to retire...'], 'elephant final win'): return

            self.loadSprite(None)
            if self.item.rewardItem('key fragment #5', 'elephant reward item'): return

            self.battle.end()

        
