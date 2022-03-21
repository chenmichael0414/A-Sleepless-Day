import pygame

class Screen:
    def __init__(self, width=800, height=800, fps=60):
        self.SCREEN_WIDTH  = width
        self.SCREEN_HEIGHT = height
        self.display = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        self.clock = pygame.time.Clock()
        self.fps = fps

        self.bg = pygame.image.load("background.jpeg")
        self.bg = pygame.transform.scale(self.bg, (self.SCREEN_WIDTH * 3, self.SCREEN_HEIGHT * 3))

        self.frame = 0

    def tick(self, x, y):
        self.display.fill((0, 0, 0))
        self.display.blit(self.bg, (x, y))
        self.clock.tick(self.fps)

        self.frame += 1


    