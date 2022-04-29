import random
import pygame
from boss_battles.base import Boss

class Mole(Boss):
    def __init__(self, screen, battle, textbox):
        super().__init__(
            screen, 
            battle, 
            textbox, 
            './enemies/bosses/mole.png',
            250,    # fix this value
            [
                self.attack1
            ],
            {
                # load attack collision classes heres
            }
        )

    def tick(self):
        if not self.sprite:
            return

        self.drawBoss()

        if self.textbox.drawIfIncomplete(['change this text'], 'mole intro'): return

        for minion in self.minions:
            self.drawMinion(minion)
            self.collision(minion)

        self.attacks[self.currentAttack]()

    def reset(self):
        super().reset()

        self.textbox.resetFlag('mole intro')

    def attack1(self):
        pass


        

        
