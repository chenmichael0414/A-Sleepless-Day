import pygame
import json

from player import BorderCollider

class Screen:
    def __init__(self, width=800, height=600, fps=60):
        self.PIXEL_SIZE       = 32
        self.PLAYER_SCALE     = 2
        self.BACKGROUND_SCALE = 6

        # self.BACKGROUND_HEIGHT = self.PIXEL_SIZE * self.PLAYER_SCALE * self.BACKGROUND_SCALE * 2
        # self.BACKGROUND_WIDTH  = self.BACKGROUND_HEIGHT * width / height
        self.BACKGROUND_WIDTH  = width
        self.BACKGROUND_HEIGHT = height

        self.SCREEN_WIDTH  = width
        self.SCREEN_HEIGHT = height
        #self.display = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

        self.ACTUAL_WIDTH, self.ACTUAL_HEIGHT = self.display.get_size()

        self.OFFSET_X = (self.ACTUAL_WIDTH  - self.SCREEN_WIDTH)  / 2
        self.OFFSET_Y = (self.ACTUAL_HEIGHT - self.SCREEN_HEIGHT) / 2

        self.BG_OFFSET_X = (self.ACTUAL_WIDTH  - self.BACKGROUND_WIDTH)  / 2
        self.BG_OFFSET_Y = (self.ACTUAL_HEIGHT - self.BACKGROUND_HEIGHT) / 2

        self.clock = pygame.time.Clock()
        self.fps = fps
        self.frame = 0

        self.cameraMode = "SCROLL"

        self.frozen = False

        self.battling = False

        self.cutscene = False

        self.loading   = True
        self.loadTime  = 20
        self.loadFrame = self.loadTime  # the frame in which we started the loading screen

        self.rooms = json.load(open('./rooms/rooms.json'))

        self.setRoom('CHEM')

        self.currScene = "CHEM"
        self.items = {
            "CHEM": [
                ['block'],
                ['block', 200, 200], 
                ['arrow', 300, 100, True, lambda: self.setRoom('TEST')]
            ],
            "GYM":[

            ],
            "MATH":[

            ],
            "CSE":[

            ]
        }

    def addSceneItems(self, scene, item):
        for i in self.items[scene]:
            if len(i) ==  1:
                item.addItem(i[0])
            elif len(i) == 3:
                item.addItem(i[0], x=i[1], y=i[2])
            else:
                item.addItem(i[0], i[1], i[2], i[3], i[4])

        self.currScene = scene

    def itemRemove(self, i):
        self.items[self.currScene].pop(i)

    def setRoom(self, room, player=None, item=None, load=True):
        if not room in self.rooms or self.frozen:
            return
        if load:
            self.load()

        self.current = room
        self.bg      = pygame.image.load('./rooms/{}'.format(self.rooms[room]['path'])).convert_alpha()
        self.bg      = pygame.transform.scale(self.bg, (self.BACKGROUND_WIDTH, self.BACKGROUND_HEIGHT))

        if 'borderPath' in self.rooms[room]:
            self.border = pygame.image.load('./rooms/{}'.format(self.rooms[room]['borderPath'])).convert_alpha()
            self.border = pygame.transform.scale(self.border, (self.BACKGROUND_WIDTH, self.BACKGROUND_HEIGHT))

        self.cameraMode = self.rooms[room]['mode']

        if player:
            player.resetPosition(self.rooms[room]['pos'])

        if item and player:
            for i in item.active:
                if self.cameraMode == "SCROLL":
                    i['x'] = i['startX'] + self.rooms[room]['pos'][0]
                    i['y'] = i['startY'] + self.rooms[room]['pos'][1]
                elif self.cameraMode == "FIXED":
                    i['x'] = i['startX'] 
                    i['y'] = i['startY']

        if item:
            self.addSceneItems(room, item)

    def load(self):
        self.loading   = True
        self.loadFrame = self.frame

    def drawSprite(self, sprite, xy):
        x, y = xy

        self.display.blit(sprite, (x + self.OFFSET_X, y + self.OFFSET_Y))

    def drawRect(self, color, xywh, lineWidth=0):
        x, y, w, h = xywh

        pygame.draw.rect(
            self.display,
            color,
            (x + self.OFFSET_X, y + self.OFFSET_Y, w, h),
            lineWidth
        )

    # covers screen with black rectangles so it appears to be the actual screen width and screen height (i.e 800x600)
    def drawBorder(self):
        # makes the height the target height
        pygame.draw.rect(
            self.display, 
            (0, 0, 0), # black
            (0, 0, self.ACTUAL_WIDTH, self.OFFSET_Y),
            0
        )

        pygame.draw.rect(
            self.display, 
            (0, 0, 0), # black
            (0, self.OFFSET_Y + self.SCREEN_HEIGHT, self.ACTUAL_WIDTH, self.OFFSET_Y),
            0
        )

        # makes the width the target width
        pygame.draw.rect(
            self.display, 
            (0, 0, 0), # black
            (0, 0, self.OFFSET_X, self.ACTUAL_HEIGHT),
            0
        )

        pygame.draw.rect(
            self.display, 
            (0, 0, 0), # black
            (self.OFFSET_X + self.SCREEN_WIDTH, 0, self.OFFSET_X, self.ACTUAL_HEIGHT),
            0
        )


    # Clears the screen and iterates the clock and current frame
    def tick(self, x, y):
        self.display.fill((0, 0, 0))

        if self.frame - self.loadFrame >= self.loadTime:    # if it has been 50 or more frames since we started the loading screen
            self.loading = False

        # Draw the background
        if not self.loading and not self.battling:
            if self.cameraMode == "SCROLL":
                self.display.blit(self.bg, (x + self.BG_OFFSET_X, y + self.BG_OFFSET_Y))
            elif self.cameraMode == "FIXED":
                if self.border:
                    self.display.blit(self.border, (self.BG_OFFSET_X, self.BG_OFFSET_Y))

                self.display.blit(self.bg, (self.BG_OFFSET_X, self.BG_OFFSET_Y))                      

        # covers screen with black rectangles so it appears to be the actual screen width and screen height (i.e 800x600)
        self.drawBorder()

        self.clock.tick_busy_loop(self.fps)
        self.frame += 1