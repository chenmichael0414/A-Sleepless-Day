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
            [
                self.soundwave
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
            xSpeed = 4
            ySpeed = math.sin(self.screen.frame)

            minion['x'] += xSpeed
            minion['y'] += ySpeed

        if self.defeatedMinions < 20:
            # If it is the current frame to draw a minion
            if len(self.minions) < 3 and self.screen.frame % 40 == 0:
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