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

        # TODO: change this to include all key fragments
        self.keyFragments = [
            'key fragment #1',
            'key fragment #2',
            'key fragment #3',
            'key fragment #4',
            'key fragment #5'
        ]

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
        self.screen.removeItem(item['name'])

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
        # We only want to draw items if all bosses in the current room have been defeated
        if self.screen.bosses is None:
            for item in self.active:
                self.screen.drawSprite(item['sprite'], (item['x'], item['y']))

    # basically makes it so each item stays in a fixed position as the camera scrolls
    def updatePositions(self, dx, dy):
        for item in self.active:
            item['x'] += dx
            item['y'] += dy

    def runEvent(self, item):
        if self.inventory.isFull():
            self.textbox.draw(['sorry, your inventory is full.'])
            return

        if item.get('event') is not None:
            item['event']()

        self.inventory.addToInventory(item)
        self.textbox.drawAppend(['{} has been added to your inventory.'.format(item['name'])])

        self.removeItem(item)

    def getItemByName(self, name):
        for n in self.itemData:
            if n == name:
                return {
                    'name': name,
                    'x': 0,
                    'y': 0,
                    'sprite': self.loadSprite(name),
                    'event': None,
                    'boosts': self.itemData[name].get('boosts')
                }

    def rewardItem(self, name, flag):
        # Only reward the item if the inventory is empty
        if self.inventory.isFull():
            self.textbox.draw(['sorry, your inventory is full.'])
            return

        item = self.getItemByName(name)

        # We assume that the user will only have one copy of this rewarded item
        if not self.hasItem(name):
            self.inventory.addToInventory(item)

        if self.textbox.drawIfIncomplete(['congratulations!', '{} has been added to your inventory.'.format(item['name'])], flag): return True

        if self.hasAllKeyFragments():
            if self.textbox.drawIfIncomplete(['...........', 'congratulations!', 'you have all key fragments!', 'you have crafted the cypher key!'], 'craft cypher key'): return True
            self.craftKey()

        return False

    def hasItem(self, name):
        return self.inventory.hasItem(name)

    def hasAllKeyFragments(self):
        for name in self.keyFragments:
            if not self.hasItem(name):
                return False

        return True

    def craftKey(self):
        # Since we already checked if we have all the fragments in self.hasAllKeyFragments(), we don't have to check again
        for name in self.keyFragments:
            self.inventory.removeFromInventory(name)

        self.inventory.addToInventory(self.getItemByName('key'))

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

    def getPlayerSize(self):
        # Arbitrary initial size
        size = None

        for item in self.inventory.items:
            if item.get('boosts') is not None:
                newSize = item['boosts'].get('size')

                if newSize is not None and (size is None or newSize < size):
                    size = newSize
                
        return size