import random
import pygame
from boss_battles.base import Boss
from colliders import ImageCollider


class Monkey(Boss):
    def __init__(self, screen, battle, textbox):
        super().__init__(
            screen, 
            battle, 
            textbox, 
            './enemies/bosses/monkey.png',
            250,
            [
                self.punch,
                self.kick,
                self.punchAndKick
            ],
            {
                'punch': ImageCollider((0, 0), pygame.image.load('./attacks/punch.png').convert_alpha()),
                'kick': ImageCollider((0, 0), pygame.image.load('./attacks/kick.png').convert_alpha()),
            }
        )

    def tick(self):
        if not self.sprite:
            return

        self.drawBoss()

        if self.textbox.drawIfIncomplete(['oohoohooh aahahahah', 'i am going to defeat you!!!'], 'monkey intro'): 
            return

        for minion in self.minions:
            self.drawMinion(minion)
            self.collision(minion)

        self.attacks[self.currentAttack]()

    def reset(self):
        super().reset()

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
            self.loadSprite(1)

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
            self.loadSprite(2)

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
            self.loadSprite(0)
            
            if self.textbox.drawIfIncomplete(['hey u win congrats!'], 'monkey final win'): return

            # self.defeatedMinions = 0
            # self.currentAttack += 1
        


        

        
