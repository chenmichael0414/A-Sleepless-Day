import pygame

class Screen:
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

        self.frozen = False

        self.loading   = True
        self.loadTime  = 20
        self.loadFrame = self.loadTime  # the frame in which we started the loading screen

        self.rooms = {
            'MAIN': {
                'path': 'default.jpeg',
                'pos': None
            },
            'TEST': {
                'path': 'test.jpeg',
                'pos': (40, 40)
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

        if player:
            player.resetPosition(self.rooms[room]['pos'])

    def load(self):
        self.loading   = True
        self.loadFrame = self.frame

    # Clears the screen and iterates the clock and current frame
    def tick(self, x, y):
        self.display.fill((0, 0, 0))

        if self.frame - self.loadFrame >= self.loadTime:    # if it has been 50 or more frames since we started the loading screen
            self.loading = False

        if not self.loading:
            self.display.blit(self.bg, (x, y))

        self.clock.tick(self.fps)
        self.frame += 1


    