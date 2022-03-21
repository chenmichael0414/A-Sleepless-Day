import pygame

class Player:
    def __init__(self, screen):
        self.screen = screen
        self.bgWidth, self.bgHeight = self.screen.bg.get_size()

        self.x = self.bgWidth / -2
        self.y = self.bgHeight / -2

        # keys used for movement and their directions (x, y)
        self.moveKeys = {
            pygame.K_LEFT: (1, 0),
            pygame.K_RIGHT: (-1, 0),
            pygame.K_UP: (0, 1),
            pygame.K_DOWN: (0, -1)
        }

        self.scale = 3.5
        
        self.sheet = pygame.image.load('./albert.png').convert()
        self.sprite = None
        self.pixel_size = 32

        # coordinates of the spritesheet (for animations)
        self.coords = [
            (0, 32),
            (32, 0),
            (0, 32),
            (32, 32)
        ]

        self.currentFrame  = 0 # current frame of animation
        self.animationRate = 10 # after how many frames do we switch costumes

    def tick(self):
        self.draw()
        self.move()

    def load_sprite(self):
        # extract the image from the spritesheet
        # cycles through the self.coords array for different animations
        # this is calculated through modulating with the animation rate
        rect = pygame.Rect(self.coords[self.currentFrame % len(self.coords)] + (self.pixel_size, self.pixel_size))

        self.sprite = pygame.Surface(rect.size).convert_alpha()
        self.sprite.blit(self.sheet, (0, 0), rect)

        # upscale the spritesheet
        self.sprite = pygame.transform.scale(self.sprite, (self.scale * self.pixel_size, self.scale * self.pixel_size))

    def draw(self):
        self.load_sprite()
        w, h = self.sprite.get_size()

        self.screen.display.blit(self.sprite, (self.screen.SCREEN_WIDTH/2 - w/2, self.screen.SCREEN_HEIGHT/2 - h/2))

    def move(self):
        pressed = pygame.key.get_pressed()

        size = self.sprite.get_width()

        moveFactor = (size / 2)

        isMoving = False

        for key, dir in self.moveKeys.items():
            if pressed[key]:
                isMoving = True

                # if we are currently on a frame in which we should move
                if self.screen.frame % self.animationRate == 0:
                    # multiply the move factor by the direction
                    self.x += moveFactor * dir[0]
                    self.y += moveFactor * dir[1]

                    self.currentFrame += 1

                break # so we can't move diagonally
        
        # basically fake border checks
        # instead of checking for border collisions, we just overrwite them before we re-render the screen
        # TODO: this!
        
        # if we are not moving, make sure the character is still
        if not isMoving:
            self.currentFrame = 0

        