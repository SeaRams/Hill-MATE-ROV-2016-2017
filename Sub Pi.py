#Sub Pi is the server
import socket
import pygame

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '0.0.0.0'

port = 9000
sock.bind((host, port))
sock.listen(5)
print "server is ready"

c, addr = sock.accept()
print('Got connection from', addr)

#Setup
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class TextPrint:
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 20)

    def printInfo(self, screen, textString):
        textBitmap = self.font.render(textString, True, BLACK)
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

pygame.init()
size = [500, 700]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Joystick from: " + str(addr))
done = False 
clock = pygame.time.Clock()
pygame.joystick.init()
textPrint = textPrint()

while done == False:
    


c.send('thank you for connecting')
print(c.recv(10)) #ensures that the client "closes" first, or the server port will be stuck on TIME_WAIT
print(c.recv(20))
c.close()
