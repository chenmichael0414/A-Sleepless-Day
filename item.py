import pygame
import json

class Item:
    def __init__(self, screen, textbox, inventory):
        self.screen    = screen
        self.textbox   = textbox
        self.inventory = inventory

        self.imagePaths = json.load(open('./items/items.json'))

        self.scale = 2

        self.triggerKey = pygame.K_SPACE

        self.active = []

    def addItem(self, name, x=50, y=50, text=None):
        self.active.append({
            'name': name,
            'startX': x,
            'startY': y,
            'x': x,
            'y': y,
            'sprite': self.loadSprite(name),
            'event': (lambda: self.textbox.draw(['you found a new item!']) if text == None else self.textbox.draw(text)),
        })

    def removeItem(self, loc):
        self.active.pop(loc)
        self.screen.itemRemove(loc)

    def clearItems(self):
        self.active = []

    # basically makes it so we only have to load image sprites once
    def loadSprite(self, name):
        img = pygame.image.load('./items/{}'.format(self.imagePaths[name])).convert_alpha()
        img = pygame.transform.scale(img, (self.scale * self.screen.PIXEL_SIZE, self.scale * self.screen.PIXEL_SIZE))

        return img

    def tick(self):
        for item in self.active:
            self.screen.drawSprite(item['sprite'], (item['x'], item['y']))

    # basically makes it so each item stays in a fixed position as the camera scrolls
    def updatePositions(self, dx, dy):
        for item in self.active:
            item['x'] += dx
            item['y'] += dy

    def runEvent(self, item):
        item['event']()

        self.inventory.addToInventory(item)
        self.textbox.drawAppend(['{} has been added to your inventory.'.format(item['name'])])
        self.screen.itemRemove(self.active.index(item))
        self.active.remove(item)
