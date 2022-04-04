from tkinter import SCROLL
import pygame

class Screen:
    SCROLL = 0
    FIXED  = 1

    def __init__(self, width=800, height=600, fps=60):
        self.PIXEL_SIZE       = 32
        self.PLAYER_SCALE     = 2
        self.BACKGROUND_SCALE = 15
        self.BACKGROUND_SIZE  = self.PIXEL_SIZE * self.PLAYER_SCALE * self.BACKGROUND_SCALE * 2

        self.SCREEN_WIDTH  = width
        self.SCREEN_HEIGHT = height
        self.display = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        self.clock = pygame.time.Clock()
        self.fps = fps
        self.frame = 0

        self.cameraMode = Screen.SCROLL

        self.frozen = False

        self.loading   = True
        self.loadTime  = 20
        self.loadFrame = self.loadTime  # the frame in which we started the loading screen

        self.rooms = {
            'MAIN': {
                'path': 'default.jpeg',
                'pos': None,
                'mode': Screen.FIXED
            },
            'TEST': {
                'path': 'test.jpeg',
                'pos': (40, 40),
                'mode': Screen.SCROLL
            }
        }

        self.setRoom('MAIN')

    def setRoom(self, room, player=None):
        if not room in self.rooms or self.frozen:
            return

        self.load()

        self.current = room
        self.bg      = pygame.image.load('./img/backgrounds/{}'.format(self.rooms[room]['path']))
        self.bg      = pygame.transform.scale(self.bg, (self.BACKGROUND_SIZE, self.BACKGROUND_SIZE))

        self.cameraMode = self.rooms[room]['mode']

        if player:
            player.resetPosition(self.rooms[room]['pos'] if self.cameraMode == Screen.SCROLL else None)

    def load(self):
        self.loading   = True
        self.loadFrame = self.frame

    # Clears the screen and iterates the clock and current frame
    def tick(self, x, y):
        self.display.fill((0, 0, 0))

        if self.frame - self.loadFrame >= self.loadTime:    # if it has been 50 or more frames since we started the loading screen
            self.loading = False

        if not self.loading:
            if self.cameraMode == Screen.SCROLL:
                self.display.blit(self.bg, (x, y))
            elif self.cameraMode == Screen.FIXED:
                self.display.blit(self.bg, (self.BACKGROUND_SIZE / -2, self.BACKGROUND_SIZE / -2))

            

        self.clock.tick(self.fps)
        self.frame += 1


    