
import pygame

class Textbox:
    def __init__(self, screen):
        self.screen = screen

        self.TEXTBOX_HEIGHT = 120
        self.LINE_WIDTH     = 3
        
        pygame.font.init()
        self.font = pygame.font.Font('./fonts/retro.ttf', 25)
        self.textRate = 2   # larger is slower, can only be integer

        self.arrowSheet  = pygame.image.load('./sprites/next.png').convert_alpha()
        self.arrowSprite = None
        self.arrowScale  = 2

        self.arrowRate         = 8
        self.currentArrowFrame = 0

        self.endCutscene = False

        self.isActive = False

        self.finishedTexts = []
        self.finishedFlag  = None

        self.progressButton = pygame.K_RETURN

        self.clean()

    # sets current text to blank and prepares for new text
    def clean(self, isActive=False, currentText=0):
        self.current       = ['']           # current text being written
        self.currentI      = 0              # current index of character that should be written
        self.currentRow    = 0              # current row of text that we are writing (think of currentI as current column)
        self.totalProgress = 0              # how many characters we have written
        self.currentText   = currentText    # which textbox in the array we are currently writing to

        self.isActive = isActive

        self.arrowSprite = None

        self.currentArrowFrame = 0

        # print(self.screen.frozen)

    def parse(self, text):
        # Return the indicies in which we need to go to a new line
        res = []

        words = text.split(' ')
        pastWords = ''

        for word in words:
            # If the width of the string of text is less than our screen width
            # Divide by constant just to give some padding
            if self.font.size(pastWords + word)[0] < self.screen.SCREEN_WIDTH / 1.2:
                pastWords += word + ' '
            else:
                # Store the index in which we need to go to a new line and reset pastWords
                res.append(pastWords)
                pastWords = word + ' '

        res.append(pastWords)

        return res

    # The flag allows us to store when text dialogues are completed
    # Each flag is stored in an array once the text is finished
    # If that flag is in the array, we know that we can proceed in a cutscene/battle/etc.
    def draw(self, text, textRate=None, endCutscene=False, flag=None):
        if self.isActive:
            return

        self.target = text

        if textRate: 
            self.textRate = textRate

        self.endCutscene  = endCutscene
        self.finishedFlag = flag

        self.clean(isActive=True)

    # same as draw, but if another text event is currently happening, this will simply be added to the end
    def drawAppend(self, text, textRate=None):
        for line in text:
            self.target.append(line)

        if textRate: 
            self.textRate = textRate

        self.clean(isActive=True)

    def isFinished(self, flag):
        return flag in self.finishedTexts

    def resetFlag(self, flag):
        if flag in self.finishedTexts:
            self.finishedTexts.remove(flag)

    def drawIfIncomplete(self, text, flag):
        if not self.isFinished(flag):
            self.draw(text, flag=flag)

            return True

        return False

    def getArrow(self):
        # extract the current arrow sprite
        rect = pygame.Rect(
            (self.currentArrowFrame % 3) * self.screen.PIXEL_SIZE,          # % 3 because there are 3 arrows per row in spritesheet
            ((self.currentArrowFrame // 3) % 2) * self.screen.PIXEL_SIZE,   # // 3 % 2 to get the current column (2 columns)
            self.screen.PIXEL_SIZE, 
            self.screen.PIXEL_SIZE
        )

        self.arrowSprite = pygame.Surface(rect.size, pygame.SRCALPHA).convert_alpha()
        self.arrowSprite.blit(self.arrowSheet, (0, 0), rect)

        # upscale the sprite
        self.arrowSprite = pygame.transform.scale(self.arrowSprite, (self.arrowScale * self.screen.PIXEL_SIZE, self.arrowScale * self.screen.PIXEL_SIZE))

    def tick(self):
        # if there is nothing to write, just return
        if not self.isActive:
            return 1

        # Main white box
        self.screen.drawRect(
            (255, 255, 255), # white
            (0, self.screen.SCREEN_HEIGHT, self.screen.SCREEN_WIDTH, self.TEXTBOX_HEIGHT)
        )
        
        # Black border
        self.screen.drawRect(
            (0, 0, 0), # black
            (-self.LINE_WIDTH, self.screen.SCREEN_HEIGHT, self.screen.SCREEN_WIDTH + (self.LINE_WIDTH * 2), self.TEXTBOX_HEIGHT), 
            self.LINE_WIDTH
        )
        
        # Writing the text
        message = self.target[self.currentText]
        rows    = self.parse(message)
        height  = self.font.size(message)[1]

        # If it is a frame in which we should animate and there is still more text to write
        if self.screen.frame % self.textRate == 0 and self.totalProgress < len(message):
            if self.currentI < len(rows[self.currentRow]):
                # Push the current character to the rendered text
                self.current[self.currentRow] += rows[self.currentRow][self.currentI].upper()
                self.currentI += 1
                self.totalProgress += 1
            else:
                # Go on to the next row of text
                self.currentI = 0
                self.currentRow += 1
                self.current.append('')

        # If it is a frame in which we should animate and the arrow has already been grabbed for the first time
        if self.screen.frame % self.arrowRate == 0 and self.arrowSprite:
            self.currentArrowFrame += 1
        
        # Render each row
        for (i, row) in enumerate(self.current):
            textsurface = self.font.render(row, False, (0, 0, 0))
            self.screen.drawSprite(textsurface, (8, self.screen.SCREEN_HEIGHT + 3 + (height * i)))

        # If we have written all characters out, display the next arrow
        if self.totalProgress >= len(message):
            self.getArrow() # updates self.arrowSprite

            # self.next = self.font.render('v', False, (0, 0, 0))
            self.screen.drawSprite(
                self.arrowSprite, 
                (
                    self.screen.SCREEN_WIDTH - self.arrowSprite.get_width(), 
                    self.screen.SCREEN_HEIGHT + self.TEXTBOX_HEIGHT - self.arrowSprite.get_height()
                )
            )

            if pygame.key.get_pressed()[self.progressButton]:
                # If there is another textbox to write
                if self.currentText < len(self.target) - 1:
                    self.currentText += 1
                    self.clean(isActive=True, currentText=self.currentText)
                else:
                    if self.endCutscene:
                        self.endCutscene     = False
                        self.screen.cutscene = False

                    if self.finishedFlag is not None:
                        self.finishedTexts.append(self.finishedFlag)
                        self.finishedFlag = None
                        
                    self.clean()
