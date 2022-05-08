import pygame

class PlayerCollider(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()

        self.size = size

        self.rect = pygame.Rect(pos + (self.size, self.size))
        self.mask = pygame.mask.Mask((self.size, self.size), True)

    def setRect(self, pos):
        self.rect = pygame.Rect(pos + (self.size, self.size))

class ImageCollider(pygame.sprite.Sprite):
    def __init__(self, pos, sprite, width=64, height=64):
        super().__init__()

        self.pos = pos

        self.width  = width
        self.height = height

        self.image = pygame.Surface((width, height), pygame.SRCALPHA).convert_alpha()

        if sprite is not None:
            self.image.blit(sprite, (0, 0))

        self.rect = self.image.get_rect(topleft=pos)
        self.mask = pygame.mask.from_surface(self.image)

    def setRect(self, pos):
        self.pos  = pos
        self.rect = self.image.get_rect(topleft=pos)

    def updateImage(self, sprite, width=None, height=None):
        # If there is no width/height passed in, use self.width/self.height instead
        self.image = pygame.Surface((width or self.width, height or self.height), pygame.SRCALPHA).convert_alpha()

        if sprite is not None:
            self.image.blit(sprite, (0, 0))

        self.rect = self.image.get_rect(topleft=self.pos)
        self.mask = pygame.mask.from_surface(self.image)