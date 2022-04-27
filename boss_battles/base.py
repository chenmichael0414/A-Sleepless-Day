import pygame

class Boss:
    def __init__(self, screen, battle, textbox, sheetPath, attacks):
        self.screen = screen
        self.battle = battle
        self.textbox = textbox

        self.currentFrame = 0
        self.scale = 3.5

        self.sheet = pygame.image.load(sheetPath).convert_alpha()

        # The width and height of each individual sprite in the sheet
        self.SHEET_WIDTH  = 250
        self.SHEET_HEIGHT = 300

        self.sprite = None
        self.loadSprite()

        self.attacks = attacks
        self.currentAttack = 0

        self.minions = []
        self.defeatedMinions = 0

        # Create empty colliders to prepare for collision later
        # These positions will be updated later
        self.playerCollider = PlayerBattleCollider((0, 0), self.battle.playerSize)
        self.minionColliders = {
            'punch': MinionCollider((0, 0), pygame.image.load('./attacks/punch.png').convert_alpha()),
            'kick': MinionCollider((0, 0), pygame.image.load('./attacks/kick.png').convert_alpha())
        }

        # This is so when you touch a minion, you don't take damage multiple times from the same one
        self.lastCollisionFrame = 0

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
        if minion['x'] > self.screen.SCREEN_WIDTH or minion['y'] > self.screen.SCREEN_HEIGHT:
            self.minions.remove(minion)
            self.defeatedMinions += 1

    def collision(self, minion):
        # Update the colliders of the player and the minion of the right type
        self.playerCollider.setRect((self.battle.PLAYER_OFFSET_X + self.battle.playerX, self.battle.PLAYER_OFFSET_Y - self.battle.playerY))
        self.minionColliders[minion['type']].setRect((minion['x'], minion['y']))

        # Check if the sprites are touching
        if pygame.sprite.collide_mask(self.playerCollider, self.minionColliders[minion['type']]):
            # 20 is an arbitrary number for a delay between damage, can be tweaked
            if self.screen.frame - self.lastCollisionFrame > 20:
                self.battle.takeDamage()

            self.lastCollisionFrame = self.screen.frame

    def reset(self):
        self.loadSprite()

        self.currentAttack = 0
        self.minions = []
        self.defeatedMinions = 0
        self.lastCollisionFrame = 0

    def loadSprite(self):
        # extract the current sprite
        rect = pygame.Rect(
            (self.currentFrame % 2) * self.SHEET_WIDTH,           # % 2 because there are 2 sprites per row in spritesheet
            ((self.currentFrame // 2) % 2) * self.SHEET_HEIGHT,   # // 2 % 2 to get the current column (2 columns)
            self.SHEET_WIDTH,
            self.SHEET_HEIGHT
        )

        self.sprite = pygame.Surface(rect.size, pygame.SRCALPHA).convert_alpha()
        self.sprite.blit(self.sheet, (0, 0), rect)

        # upscale the sprite
        self.sprite = pygame.transform.scale(self.sprite, (self.scale * self.screen.PIXEL_SIZE, self.scale * self.screen.PIXEL_SIZE))

class PlayerBattleCollider(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()

        self.size = size

        self.rect = pygame.Rect(pos + (size, size))
        self.mask = pygame.mask.Mask((size, size), True)

    def setRect(self, pos):
        self.rect = pygame.Rect(pos + (self.size, self.size))

class MinionCollider(pygame.sprite.Sprite):
    def __init__(self, pos, sprite):
        super().__init__()

        self.image = pygame.Surface((64, 64), pygame.SRCALPHA)
        self.image.blit(sprite, (0, 0))

        self.rect = self.image.get_rect(topleft=pos)
        self.mask = pygame.mask.from_surface(self.image)

    def setRect(self, pos):
        self.rect = self.image.get_rect(topleft=pos)