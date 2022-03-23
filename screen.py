import pygame

class Screen:
    def __init__(self, width=800, height=600, fps=60):
        self.PIXEL_SIZE       = 32
        self.PLAYER_SCALE     = 2.25
        self.BACKGROUND_SCALE = 15
        self.BACKGROUND_SIZE  = self.PIXEL_SIZE * self.PLAYER_SCALE * self.BACKGROUND_SCALE * 2

        self.SCREEN_WIDTH  = width
        self.SCREEN_HEIGHT = height
        self.display = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        self.clock = pygame.time.Clock()
        self.fps = fps

        self.bg = pygame.image.load("background.jpeg")
        self.bg = pygame.transform.scale(self.bg, (self.BACKGROUND_SIZE, self.BACKGROUND_SIZE))

        self.frame = 0

    def tick(self, x, y):
        self.display.fill((0, 0, 0))
        self.display.blit(self.bg, (x, y))
        self.clock.tick(self.fps)

        self.frame += 1


    