import pygame
from screen import Screen

class Player:
    def __init__(self, screen):
        self.screen = screen

        self.sheet = pygame.image.load('./img/albert.png').convert()
        self.sprite = None
        self.size   = (15, 20)    # actual size of the pixel art
        self.offset = (8, 7)    # offset for selecting each sprite from the spritesheet

        # keys used for movement and their directions (x, y)
        self.moveKeys = {
            pygame.K_LEFT: (1, 0),
            pygame.K_RIGHT: (-1, 0),
            pygame.K_UP: (0, 1),
            pygame.K_DOWN: (0, -1)
        }
        self.currentKey = pygame.K_DOWN

        self.pixel_size = screen.PIXEL_SIZE
        self.scale = screen.PLAYER_SCALE

        # coordinates of the spritesheet (for animations)
        self.coords = {
            pygame.K_DOWN: 0,
            pygame.K_LEFT: 1,
            pygame.K_RIGHT: 2,
            pygame.K_UP: 3
        }

        self.currentFrame  = 0 # current frame of animation
        self.animationRate = 10 # after how many frames do we switch costumes

        self.resetPosition()

    def resetPosition(self, pos=None):
        if pos:
            self.x = pos[0]
            self.y = pos[1]
        else:
            if self.screen.cameraMode == Screen.SCROLL:
                self.x = self.screen.BACKGROUND_SIZE / -2
                self.y = self.screen.BACKGROUND_SIZE / -2
            elif self.screen.cameraMode == Screen.FIXED:
                self.load_sprite()
                w, h = self.sprite.get_size()

                self.x = self.screen.SCREEN_WIDTH  / 2 - w / 2
                self.y = self.screen.SCREEN_HEIGHT / 2 - h / 2


    def tick(self):
        self.draw()

        if not self.screen.frozen:
            self.move()

    def load_sprite(self):
        # extract the image from the spritesheet
        # cycles through the self.coords array for different animations
        # this is calculated through modulating with the animation rate
        # extracts current sprite coords from object
        currentSprite = (self.pixel_size * (self.currentFrame % 4), self.pixel_size * self.coords[self.currentKey])

        newCoords = tuple(map(sum, zip(currentSprite, self.offset))) # adds the tuples together
        rect = pygame.Rect(newCoords + self.size)

        self.sprite = pygame.Surface(rect.size).convert_alpha()
        self.sprite.blit(self.sheet, (0, 0), rect)

        # upscale the sprite
        self.sprite = pygame.transform.scale(self.sprite, (self.scale * self.pixel_size, self.scale * self.pixel_size))

    def draw(self):
        self.load_sprite()
        w, h = self.sprite.get_size()

        if self.screen.cameraMode == Screen.SCROLL:
            self.screen.display.blit(self.sprite, (self.screen.SCREEN_WIDTH / 2 - w / 2, self.screen.SCREEN_HEIGHT / 2 - h / 2))
        elif self.screen.cameraMode == Screen.FIXED:
            self.screen.display.blit(self.sprite, (self.x, self.y))

    def move(self):
        pressed = pygame.key.get_pressed()

        moveFactor = self.size[0] * 2 # multiply the actual width of the sprite by a factor

        isMoving = False

        for key, dir in self.moveKeys.items():
            if pressed[key]:
                self.currentKey = key
                isMoving = True

                # if we are currently on a frame in which we should move
                if self.screen.frame % self.animationRate == 0:
                    # if we are in fixed screen, reverse all movement
                    if self.screen.cameraMode == Screen.SCROLL:
                        cameraDir = 1
                    elif self.screen.cameraMode == Screen.FIXED:
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
                    

                    self.currentFrame += 1

                break # so we can't move diagonally
        
        # basically fake border checks
        # instead of checking for border collisions, we just overrwite them before we re-render the screen
        # TODO: this!

        
        # if we are not moving, make sure the character is still
        if not isMoving:
            self.currentFrame = 0

    def collision(self, moveFactor):
        #if self.x > self.startX: return True
        if self.screen.cameraMode == Screen.SCROLL:
            if self.x > self.screen.SCREEN_WIDTH / 2: return True
            if self.x < self.screen.SCREEN_WIDTH / 2 - self.screen.BACKGROUND_SIZE: return True

            if self.y > self.screen.SCREEN_HEIGHT / 2: return True
            if self.y < self.screen.SCREEN_HEIGHT / 2 - self.screen.BACKGROUND_SIZE + moveFactor: return True

        if self.screen.cameraMode == Screen.FIXED:
            if self.x > self.screen.SCREEN_WIDTH - moveFactor: return True
            if self.x < -moveFactor: return True

            if self.y > self.screen.SCREEN_HEIGHT - moveFactor * 2: return True
            if self.y < -moveFactor: return True