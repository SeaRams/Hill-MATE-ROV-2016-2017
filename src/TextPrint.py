import pygame

class TextPrint:

    def __init__(self):
        self.BLACK    = (   0,   0,   0)
        self.WHITE    = ( 255, 255, 255)
        self.reset()
        self.font = pygame.font.Font(None, 20)

    def printInfo(self, screen, textString):
        textBitmap = self.font.render(textString, True, self.BLACK)
        screen.blit(textBitmap, [self.x, self.y])
        self.y += self.line_height
        
    def reset(self):
        
        self.x = 10
        self.y = 10
        self.line_height = 15
        
    def indent(self):
        self.x += 10
        
    def unindent(self):
        self.x -= 10
