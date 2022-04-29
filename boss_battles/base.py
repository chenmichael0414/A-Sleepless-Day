import pygame

from colliders import PlayerCollider

class Boss:
    def __init__(self, screen, battle, textbox, sheetPath, sheetWidth, attacks, minionColliders):
        self.screen = screen
        self.battle = battle
        self.textbox = textbox

        self.scale = 3.5

        self.sheet = pygame.image.load(sheetPath).convert_alpha()

        # The width and height of each individual sprite in the sheet
        # The height is always 300, but the width is variable
        self.SHEET_WIDTH  = sheetWidth
        self.SHEET_HEIGHT = 300

        self.sprite = None
        self.loadSprite(0)

        self.attacks = attacks
        self.currentAttack = 0

        self.minions = []
        self.defeatedMinions = 0

        # Create empty colliders to prepare for collision later
        # These positions will be updated later
        self.playerCollider  = PlayerCollider((0, 0), self.battle.playerSize)
        self.minionColliders = minionColliders

        # This is so when you touch a minion, you don't take damage multiple times from the same one
        self.lastCollisionFrame = 0

        # Reset the battle mode
        self.battle.mode = "GRAVITY"

    # This gets overriden in the child class
    def tick(self):
        pass

    def drawBoss(self):
        self.screen.drawSprite(
            self.sprite, 
            (
                (self.screen.SCREEN_WIDTH - self.sprite.get_width()) / 2,
                0
            )
        )

    def drawMinion(self, minion):
        self.screen.drawSprite(
            minion['sprite'],
            (
                minion['x'],
                minion['y']
            ),
        )

        # If the minion goes off screen (therefore it is defeated)
        if minion['x'] < 0 or minion['x'] > self.screen.SCREEN_WIDTH or minion['y'] > self.screen.SCREEN_HEIGHT:
            self.minions.remove(minion)
            self.defeatedMinions += 1

    def collision(self, minion):
        # Update the colliders of the player and the minion of the right type
        self.playerCollider.setRect((self.battle.PLAYER_OFFSET_X + self.battle.playerX, self.battle.PLAYER_OFFSET_Y - self.battle.playerY))
        self.minionColliders[minion['type']].setRect((minion['x'], minion['y']))

        # Check if the sprites are touching
        if pygame.sprite.collide_mask(self.playerCollider, self.minionColliders[minion['type']]):
            if self.screen.frame - self.lastCollisionFrame > self.battle.invulnerability:
                self.battle.takeDamage()

            self.lastCollisionFrame = self.screen.frame

        # Remove the damaged player color if enough time has passed
        if self.screen.frame - self.lastCollisionFrame > self.battle.invulnerability:
            self.battle.playerColor = (255, 0, 0)

    def reset(self):
        self.loadSprite(0)

        self.currentAttack = 0
        self.minions = []
        self.defeatedMinions = 0
        self.lastCollisionFrame = 0

        self.battle.playerColor = (255, 0, 0)

        self.battle.mode = "GRAVITY"

    def loadSprite(self, frame):
        # extract the current sprite
        rect = pygame.Rect(
            (frame % 2) * self.SHEET_WIDTH,           # % 2 because there are 2 sprites per row in spritesheet
            ((frame // 2) % 2) * self.SHEET_HEIGHT,   # // 2 % 2 to get the current column (2 columns)
            self.SHEET_WIDTH,
            self.SHEET_HEIGHT
        )

        self.sprite = pygame.Surface(rect.size, pygame.SRCALPHA).convert_alpha()
        self.sprite.blit(self.sheet, (0, 0), rect)

        # upscale the sprite
        self.sprite = pygame.transform.scale(self.sprite, (self.scale * self.screen.PIXEL_SIZE, self.scale * self.screen.PIXEL_SIZE))