import pygame

class TitleScreen:
    def __init__(self, screen):
        self.screen = screen

        self.open = True
        
        self.startKey = pygame.K_RETURN

        # TODO: change this to our cover art
        self.coverArt = [
            pygame.image.load('./sprites/title1.png').convert_alpha(),
            pygame.image.load('./sprites/title2.png').convert_alpha()
        ]

        self.animationRate = 40

        self.drawingFrame = 0

    def tick(self):
        self.screen.display.fill((0, 0, 0))
        self.screen.drawSprite(self.coverArt[self.drawingFrame], (0, 0))

        if self.screen.frame % self.animationRate == 0:
            self.drawingFrame += 1

            if self.drawingFrame >= len(self.coverArt):
                self.drawingFrame = 0
        
        self.screen.clock.tick_busy_loop(self.screen.fps)
        self.screen.frame += 1
        pygame.display.update()

        if pygame.key.get_pressed()[self.startKey] and self.open:
            self.screen.load()
            self.open = False