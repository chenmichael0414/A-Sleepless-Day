import pygame
from screen import Screen
import math

class Player:
    def __init__(self, screen, item):
        self.screen = screen
        self.item = item

        self.sheet = pygame.image.load('./sprites/albert.png').convert_alpha()
        self.sprite = None
        self.size   = (15, 20)    # actual size of the pixel art
        self.offset = (8, 7)      # offset for selecting each sprite from the spritesheet

        # keys used for movement and their directions (x, y)
        self.moveKeys = {
            pygame.K_a: (1, 0),
            pygame.K_d: (-1, 0),
            pygame.K_w: (0, 1),
            pygame.K_s: (0, -1)
        }
        self.currentKey = pygame.K_a

        self.pixel_size = screen.PIXEL_SIZE
        self.scale = screen.PLAYER_SCALE

        # coordinates of the spritesheet (for animations)
        self.coords = {
            pygame.K_s: 0,
            pygame.K_a: 1,
            pygame.K_d: 2,
            pygame.K_w: 3
        }

        self.currentFrame  = 0 # current frame of animation
        self.animationRate = 6 # after how many frames do we switch costumes
        self.cutscene = False

        self.resetPosition()

    def resetPosition(self, pos=None):
        if pos:
            self.x = pos[0]
            self.y = pos[1]
        else:
            if self.screen.cameraMode == "SCROLL":
                self.x = (self.screen.ACTUAL_WIDTH - self.screen.BACKGROUND_WIDTH)   / -2
                self.y = (self.screen.ACTUAL_HEIGHT - self.screen.BACKGROUND_HEIGHT) / -2
            elif self.screen.cameraMode == "FIXED":
                self.load_sprite()
                w, h = self.sprite.get_size()

                self.x = self.screen.SCREEN_WIDTH  / 2 - w / 2
                self.y = self.screen.SCREEN_HEIGHT / 2 - h / 2


    def tick(self, drawingNumber=None):
        if drawingNumber != None:
            self.currentFrame = drawingNumber
            self.draw(drawingNumber)
        else:
            self.draw()

        if not self.screen.frozen:
            if not self.cutscene:
                self.move()

            w, h = self.sprite.get_size()
            scrollRect = pygame.Rect(self.screen.SCREEN_WIDTH / 2 - w / 2, self.screen.SCREEN_HEIGHT / 2 - h / 2, w, h)
            fixedRect  = pygame.Rect(self.x, self.y, w, h)

            # checks for item collisions
            # if we are touching an item and press the space key, pick it up and trigger the event
            for item in self.item.active:
                if item['sprite'] is None:
                    return

                itemRect = pygame.Rect((item['x'], item['y']) + item['sprite'].get_size())

                collision1 = self.screen.cameraMode == "SCROLL" and pygame.Rect.colliderect(scrollRect, itemRect)
                collision2 = self.screen.cameraMode == "FIXED" and pygame.Rect.colliderect(fixedRect, itemRect)
    
                if (collision1 or collision2) and pygame.key.get_pressed()[self.item.triggerKey]:
                    print(self.item.active)
                    print(item["loc"])
                    self.item.runEvent(item)
                    print(self.item.active)

    def load_sprite(self, drawingNumber = None):
        # extract the image from the spritesheet
        # cycles through the self.coords array for different animations
        # this is calculated through modulating with the animation rate
        # extracts current sprite coords from object
        currentSprite = (self.pixel_size * (self.currentFrame % 4), self.pixel_size * (int(drawingNumber/4) if drawingNumber != None else self.coords[self.currentKey]))

        newCoords = tuple(map(sum, zip(currentSprite, self.offset))) # adds the tuples together
        rect = pygame.Rect(newCoords + self.size)

        self.sprite = pygame.Surface(rect.size, pygame.SRCALPHA).convert_alpha()

        self.sprite.blit(self.sheet, (0, 0), rect)
        print(self.currentFrame)

        # upscale the sprite
        self.sprite = pygame.transform.scale(self.sprite, (self.scale * self.pixel_size, self.scale * self.pixel_size))

    def draw(self, drawingNumber=None):
        if drawingNumber != None:
            self.load_sprite(drawingNumber)
        else:
            self.load_sprite()
        w, h = self.sprite.get_size()

        if self.screen.cameraMode == "SCROLL":
            self.screen.drawSprite(self.sprite, (self.screen.SCREEN_WIDTH / 2 - w / 2, self.screen.SCREEN_HEIGHT / 2 - h / 2))
        elif self.screen.cameraMode == "FIXED":
            self.screen.drawSprite(self.sprite, (self.x, self.y))

    def move(self):
        pressed = pygame.key.get_pressed()

        moveFactor = self.size[0] * 3 # multiply the actual width of the sprite by a factor

        isMoving = False

        for key, dir in self.moveKeys.items():
            if pressed[key]:
                self.currentKey = key
                isMoving = True

                # if we are currently on a frame in which we should move
                if self.screen.frame % self.animationRate == 0:
                    # if we are in fixed screen, reverse all movement
                    if self.screen.cameraMode == "SCROLL":
                        cameraDir = 1
                    elif self.screen.cameraMode == "FIXED":
                        cameraDir = -1

                    # multiply the move factor by the direction
                    self.x += moveFactor * dir[0] * cameraDir
                    self.y += moveFactor * dir[1] * cameraDir

                    #spriteRect = self.sprite.get_ + self.size

                    # if the player would go out of the background, just undo the movement
                    # since this is all done before a render, it basically looks like the player is stuck at the wall
                    if self.collision(moveFactor):
                        self.x -= moveFactor * dir[0] * cameraDir
                        self.y -= moveFactor * dir[1] * cameraDir
                    else:
                        if self.screen.cameraMode == "SCROLL":
                            self.item.updatePositions(moveFactor * dir[0] * cameraDir, moveFactor * dir[1] * cameraDir)

                    self.currentFrame += 1

                break # so we can't move diagonally
        
        # if we are not moving, make sure the character is still
        if not isMoving:
            self.currentFrame = 0

    def collision(self, moveFactor):
        if self.screen.cameraMode == "SCROLL":
            if self.x > self.screen.BACKGROUND_WIDTH / 2:  return True
            if self.x < self.screen.BACKGROUND_WIDTH / -2: return True

            if self.y > self.screen.BACKGROUND_HEIGHT / 2 + moveFactor:  return True
            if self.y < self.screen.BACKGROUND_HEIGHT / -2: return True

        if self.screen.cameraMode == "FIXED":
            # should technically be width of player / 2 instead but doesnt make much of a difference
            if self.x > self.screen.SCREEN_WIDTH - moveFactor: return True
            if self.x < -moveFactor: return True

            if self.y > self.screen.SCREEN_HEIGHT - moveFactor * 2: return True
            if self.y < -moveFactor: return True