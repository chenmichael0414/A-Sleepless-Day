import pygame
import json

class Item:
    def __init__(self, screen, textbox, inventory):
        self.screen    = screen
        self.textbox   = textbox
        self.inventory = inventory

        self.itemData = json.load(open('./items/items.json'))

        self.scale = 2

        self.triggerKey = pygame.K_SPACE

        self.darkItem = 'pie'   # TODO: change this to a flashlight

        self.active = []

    def addItem(self, name, x=50, y=50, text=None):
        self.active.append({
            'name': name,
            'x': x,
            'y': y,
            'sprite': self.loadSprite(name),
            'event': (lambda: self.textbox.draw(['you found a new item!']) if text == None else self.textbox.draw(text)),
            'boosts': self.itemData[name].get('boosts')
        })

    def removeItem(self, item):
        self.active.remove(item)

        # We build the item to not have any miscellaneous data (sprite, event)
        # This way, it matches exactly how the items object is constructed in rooms.json
        temp = {
            'name': item.get('name'),
            'x': item.get('x'),
            'y': item.get('y'),
            'text': item.get('text')
        }

        # This removes any key-value pairs in which the value is None
        # This way, if x, y, and text are None, they are simply removed
        # https://stackoverflow.com/questions/33797126/proper-way-to-remove-keys-in-dictionary-with-none-values-in-python
        self.screen.removeItem({k: v for k, v in temp.items() if v is not None})

    def setItems(self, items):
        self.active = []

        if items is not None:
            for item in items:
                self.addItem(item.get('name'), item.get('x'), item.get('y'), item.get('text'))

    # basically makes it so we only have to load image sprites once
    def loadSprite(self, name):
        img = pygame.image.load('./items/{}'.format(self.itemData[name]['path'])).convert_alpha()
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

        self.removeItem(item)

    def hasItem(self, name):
        return self.inventory.hasItem(name)

    def hasDarkItem(self):
        return self.inventory.hasItem(self.darkItem)

    # Basically, we search through each item in our inventory, seeing if they give any extra health
    # If they do, add it to the total amount of extra health and return that value once all have been added
    def getExtraHealth(self):
        totalExtraHealth = 0

        for item in self.inventory.items:
            if item.get('boosts') is not None:
                extraHealth = item['boosts'].get('health')

                if extraHealth is not None:
                    totalExtraHealth += extraHealth

        return totalExtraHealth

    # Same idea as the above function, but with multipliers
    # We multiply all of them to an initial value of 1 and return that
    def getBoostMultipliers(self, type):
        totalBoost = 1

        for item in self.inventory.items:
            if item.get('boosts') is not None:
                boost = item['boosts'].get(type)

                if boost is not None:
                    totalBoost *= boost

        return totalBoost

