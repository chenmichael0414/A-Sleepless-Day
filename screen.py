import pygame
import json
from colliders import ImageCollider

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

        self.borderCollider = ImageCollider(
            (self.BG_OFFSET_X - self.OFFSET_X, self.BG_OFFSET_Y - self.OFFSET_Y),
            None,
            self.BACKGROUND_WIDTH, 
            self.BACKGROUND_HEIGHT
        )
        
        self.doors = []

        self.currentRoom = None

    def removeItem(self, item):
        if 'items' in self.rooms[self.currentRoom] and item in self.rooms[self.currentRoom]['items']:
            self.rooms[self.currentRoom]['items'].remove(item)

    def setRoom(self, room, player=None, item=None, load=True):
        if not room in self.rooms or self.frozen:
            return

        if load:
            self.load()

        self.currentRoom = room

        self.bg = pygame.image.load('./rooms/{}'.format(self.rooms[room]['path'])).convert_alpha()
        self.bg = pygame.transform.scale(self.bg, (self.BACKGROUND_WIDTH, self.BACKGROUND_HEIGHT))

        self.border = None

        if 'borderPath' in self.rooms[room]:
            self.border = pygame.image.load('./rooms/{}'.format(self.rooms[room]['borderPath'])).convert_alpha()
            self.border = pygame.transform.scale(self.border, (self.BACKGROUND_WIDTH, self.BACKGROUND_HEIGHT))

        self.borderCollider.updateImage(self.border)

        self.doors = []

        if 'doors' in self.rooms[room]:
            for door in self.rooms[room]['doors']:
                sprite = pygame.image.load('./rooms/{}'.format(door['path'])).convert_alpha()

                # We always just create a new ImageCollider here because rooms can have different amounts (not just 1)
                self.doors.append({
                    'sprite': sprite,
                    'newRoom': door['newRoom'],
                    'collider': ImageCollider(
                        (self.BG_OFFSET_X - self.OFFSET_X, self.BG_OFFSET_Y - self.OFFSET_Y),
                        sprite,
                        self.BACKGROUND_WIDTH, 
                        self.BACKGROUND_HEIGHT
                    )
                })

        self.cameraMode = self.rooms[room]['mode']

        if player:
            player.resetPosition(self.rooms[room].get('pos'))

        if item:
            item.setItems(self.rooms[room].get('items')) 

        # If the camera is in scroll mode, update the item positions according to the starting room position
        if self.cameraMode == "SCROLL" and item and self.rooms[room].get('pos') is not None:
            for i in item.active:
                i['x'] += self.rooms[room]['pos'][0] / 2
                i['y'] -= self.rooms[room]['pos'][1] / 2

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
                if self.border:
                    self.display.blit(self.border, (x + self.BG_OFFSET_X, y + self.BG_OFFSET_Y))

                if self.doors:
                    for door in self.doors:
                        self.display.blit(door['sprite'], (x + self.BG_OFFSET_X, y + self.BG_OFFSET_Y))

                self.display.blit(self.bg, (x + self.BG_OFFSET_X, y + self.BG_OFFSET_Y))
            elif self.cameraMode == "FIXED":
                if self.border:
                    self.display.blit(self.border, (self.BG_OFFSET_X, self.BG_OFFSET_Y))

                if self.doors:
                    for door in self.doors:
                        self.display.blit(door['sprite'], (self.BG_OFFSET_X, self.BG_OFFSET_Y))

                self.display.blit(self.bg, (self.BG_OFFSET_X, self.BG_OFFSET_Y))                      

        # covers screen with black rectangles so it appears to be the actual screen width and screen height (i.e 800x600)
        self.drawBorder()

        self.clock.tick_busy_loop(self.fps)
        self.frame += 1