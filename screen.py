import pygame
import json
from colliders import ImageCollider

class Screen:
    def __init__(self, width=800, height=600, fps=60):
        self.PIXEL_SIZE       = 32
        self.PLAYER_SCALE     = 2
        self.BACKGROUND_SCALE = 6

        self.defaultWidth  = width
        self.defaultHeight = height

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

        # The last frame in which the "room is too dark" or "room is locked" event was triggered
        # This is stored for unique textbox flag purposes
        self.eventFrame = 0

        self.cameraMode = "SCROLL"

        self.frozen = False

        self.battling = False

        self.cutscene = False

        self.loading   = True
        self.loadTime  = 20
        self.loadFrame = self.loadTime  # the frame in which we started the loading screen

        self.rooms    = json.load(open('./rooms/rooms.json'))
        self.bossData = json.load(open('./boss_battles/bosses.json'))

        self.borderCollider = ImageCollider(
            (self.BG_OFFSET_X - self.OFFSET_X, self.BG_OFFSET_Y - self.OFFSET_Y),
            None,
            self.BACKGROUND_WIDTH, 
            self.BACKGROUND_HEIGHT
        )
        
        self.doors = []

        self.dark    = False
        self.locked  = False
        self.isEvent = False

        self.boss = None
        self.bossScale = .35

        self.previousRoom = None
        self.currentRoom  = None

        self.previousPos    = None
        self.previousCamera = None

    # NOTE: do not call this alone, call it from item.removeItem()
    def removeItem(self, name):
        item = self.getItemByName(name)

        if 'items' in self.rooms[self.currentRoom] and item in self.rooms[self.currentRoom]['items']:
            self.rooms[self.currentRoom]['items'].remove(item)

    def getItemByName(self, name):
        if 'items' in self.rooms[self.currentRoom]:
            for item in self.rooms[self.currentRoom]['items']:
                if name == item['name']:
                    return item

        return None

    def setRoom(self, room, player, item, pos=None, load=True):
        if not room in self.rooms or self.frozen:
            return

        if load:
            self.load()

        # This is because the setRoom() function is sometimes triggered a few times when the room key is pressed
        # (although the room keys will be removed once we fix all doors, they are just for debugging)
        if room != self.currentRoom:
            self.previousRoom = self.currentRoom

        self.currentRoom  = room

        # If a room has a specified width/height, use that
        # Otherwise, use the default
        if self.rooms[room].get('size'):
            self.BACKGROUND_WIDTH  = self.rooms[room]['size'][0]
            self.BACKGROUND_HEIGHT = self.rooms[room]['size'][1]
        else:
            self.BACKGROUND_WIDTH  = self.defaultWidth
            self.BACKGROUND_HEIGHT = self.defaultHeight

        # Recalculate background offset
        self.BG_OFFSET_X = (self.ACTUAL_WIDTH  - self.BACKGROUND_WIDTH)  / 2
        self.BG_OFFSET_Y = (self.ACTUAL_HEIGHT - self.BACKGROUND_HEIGHT) / 2

        # Set a room to be dark if it is specified in rooms.json AND the player does not have a dark-preventing item (i.e flashlight)
        self.dark = True if self.rooms[room].get('dark') is not None and not item.hasDarkItem() else False

        # Set a room to be locked if it is specified in rooms.json AND the player does not have the key
        self.locked = True if self.rooms[room].get('locked') is not None and not item.hasItem('key') else False

        # If a room is dark or locked, make the background completely dark
        if self.dark or self.locked:
            self.bg = pygame.Surface((self.BACKGROUND_WIDTH, self.BACKGROUND_HEIGHT))

            self.isEvent = True
        else:
            self.bg = pygame.image.load('./rooms/{}'.format(self.rooms[room]['path'])).convert_alpha()
            self.bg = pygame.transform.scale(self.bg, (self.BACKGROUND_WIDTH, self.BACKGROUND_HEIGHT))

            self.isEvent = False

        self.border = None

        if 'borderPath' in self.rooms[room]:
            self.border = pygame.image.load('./rooms/{}'.format(self.rooms[room]['borderPath'])).convert_alpha()
            self.border = pygame.transform.scale(self.border, (self.BACKGROUND_WIDTH, self.BACKGROUND_HEIGHT))

        self.borderCollider.updateImage(self.border, self.BACKGROUND_WIDTH, self.BACKGROUND_HEIGHT)

        self.doors = []

        if 'doors' in self.rooms[room]:
            for door in self.rooms[room]['doors']:
                sprite = pygame.image.load('./rooms/{}'.format(door['path'])).convert_alpha()
                sprite = pygame.transform.scale(sprite, (self.BACKGROUND_WIDTH, self.BACKGROUND_HEIGHT))

                # We always just create a new ImageCollider here because rooms can have different amounts (not just 1)
                self.doors.append({
                    'sprite': sprite,
                    'newRoom': door['newRoom'],
                    'newPos': door.get('newPos'),
                    'collider': ImageCollider(
                        (self.BG_OFFSET_X - self.OFFSET_X, self.BG_OFFSET_Y - self.OFFSET_Y),
                        sprite,
                        self.BACKGROUND_WIDTH, 
                        self.BACKGROUND_HEIGHT
                    )
                })

        self.boss = None

        if 'boss' in self.rooms[room]:
            bossName = self.rooms[room]['boss']['name']
            bossPos  = self.rooms[room]['boss']['pos']

            # This object gives the boss data for the SPECIFIC boss, not all bosses (that is what self.bossData is)
            bossData = self.bossData[bossName]

            # Get the first sprite from the boss spritesheet
            bossSheet = pygame.image.load('./enemies/bosses/{}'.format(bossData['path'])).convert_alpha()

            rect = pygame.Rect(
                0,
                0,
                bossData['sheetWidth'],         # This is extracted from the bossData object created above since it IS unique to the boss
                self.bossData['sheetHeight']    # This is extracted from self.bossData since the sheetHeight is NOT unique to the boss
            )

            bossSprite = pygame.Surface(rect.size, pygame.SRCALPHA).convert_alpha()
            bossSprite.blit(bossSheet, (0, 0), rect)

            # Downscale the sprite
            bossSprite = pygame.transform.scale(bossSprite, (self.bossScale * bossData['sheetWidth'], self.bossScale * self.bossData['sheetHeight']))

            self.boss = {
                'name': bossName,
                'sprite': bossSprite,
                'x': bossPos[0],
                'y': bossPos[1]
            }

        self.previousCamera = self.cameraMode
        self.cameraMode     = self.rooms[room]['mode']

        if player:
            # Set the previous position (which is used if the triggerEvent() function is called)
            if self.previousCamera == "SCROLL":
                # We have to multiply by -2 here because the player starting position is divided by -2 in scroll mode
                # See player.resetPosition() for more info
                self.previousPos = (player.x * -2, player.y * -2)
            elif self.previousCamera == "FIXED":
                self.previousPos = (player.x, player.y)

            # If an event is triggered, we want to just spawn the player in the middle of the screen
            if self.isEvent:
                player.resetPosition()
            else:
                player.resetPosition(pos or self.rooms[room].get('pos'))

        if item:
            item.setItems(self.rooms[room].get('items')) 

        # If the camera is in scroll mode, update the item and boss positions according to the starting room position
        if self.cameraMode == "SCROLL" and (pos is not None or self.rooms[room].get('pos') is not None):
            p = pos or self.rooms[room].get('pos')

            if item:
                for i in item.active:
                    pass
                    i['x'] -= p[0] / 2
                    i['y'] -= p[1] / 2

            if self.boss:
                self.boss['x'] -= p[0] / 2
                self.boss['y'] -= p[1] / 2

    def removeBoss(self, battle):
        name = self.boss['name']

        self.boss = None
        self.rooms[self.currentRoom].pop('boss')

        battle.init(name)

    def load(self):
        self.loading   = True
        self.loadFrame = self.frame

    def triggerEvent(self, textbox, player, item, alert):
        if self.eventFrame == 0:
            self.eventFrame = self.frame

        if textbox.drawIfIncomplete(alert, 'event ' + str(self.eventFrame)): return

        self.eventFrame = 0
        self.frozen     = False

        if self.previousRoom:
            self.setRoom(self.previousRoom, player, item, pos=self.previousPos)
        else:
            self.setRoom('CHEM', player, item)

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

            # draw an overworld boss that triggers the battle
            if self.boss and not self.isEvent:
                self.drawSprite(self.boss['sprite'], (self.boss['x'], self.boss['y']))                

        self.clock.tick_busy_loop(self.fps)
        self.frame += 1