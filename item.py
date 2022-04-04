import pygame
import json

class Item:
    def __init__(self, screen, textbox):
        self.screen  = screen
        self.textbox = textbox

        self.imagePaths = json.load(open('./items/items.json'))

        self.scale = 2

        self.active = []

    def addItem(self, name, x=50, y=50):
        self.active.append({
            'name': name,
            'startX': x,
            'startY': y,
            'x': x,
            'y': y,
            'sprite': None,
            'event': lambda: self.textbox.draw(['FUFUFUFUFUFU...', 'FUFUFUFUFUFU!!!!!!']),
            'triggered': False
        })

    # basically makes it so we only have to load image sprites once
    def loadSprite(self, item):
        img = pygame.image.load('./items/{}'.format(self.imagePaths[item['name']])).convert_alpha()
        img = pygame.transform.scale(img, (self.scale * self.screen.PIXEL_SIZE, self.scale * self.screen.PIXEL_SIZE))

        item['sprite'] = img

        return img

    def tick(self):
        for item in self.active:
            if item['x'] >= 0 and item['x'] <= self.screen.SCREEN_WIDTH:
                if item['y'] >= 0 and item['y'] <= self.screen.SCREEN_HEIGHT:
                    # load the image based on the corresponding path from the json file
                    # scale the image down
                    # display it on the screen if it hasn't been picked up

                    if not item['triggered']:
                        img = item['sprite'] or self.loadSprite(item)
                        self.screen.display.blit(img, (item['x'], item['y']))

    # basically makes it so each item stays in a fixed position as the camera scrolls
    def updatePositions(self, dx, dy):
        for item in self.active:
            item['x'] += dx
            item['y'] += dy

    def runEvent(self, item):
        item['event']()
        
        self.textbox.drawAppend(['{} has been added to your inventory.'.format(item['name'])])

        item['triggered'] = True


    
