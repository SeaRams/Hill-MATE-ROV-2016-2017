#Sub Pi is the server
import socket
import pygame

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

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '0.0.0.0'

port = 9000
sock.bind((host, port))
sock.listen(5)
print "server is ready"

c, addr = sock.accept()
print('Got connection from', addr)
c.send('thank you for connecting')

#Setup TextPrint
pygame.init()
textPrint = TextPrint()
size = [500, 500]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Joystick Info from: " + str(addr))
clock = pygame.time.Clock()



joystickInput = c.recv(24)

while joystickInput != "END":
    screen.fill(WHITE)
    textPrint.reset()
    
    #print joystickInput
    joystickInput = c.recv(24)

    textPrint.printInfo(screen,"Joystick axis:")
    textPrint.indent()

    for i in range(4):
        textPrint.printInfo(screen,"Axis {} value: {}".format(i, joystickInput[i * 6:i * 6 + 6]))
    pygame.display.flip()
    #clock.tick(20)
pygame.quit()
print(c.recv(21)) #ensures that the client "closes" first, or the server port will be stuck on TIME_WAIT
c.close()
'''
#Setup
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


pygame.init()
size = [500, 700]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Joystick from: " + str(addr))
done = False 
clock = pygame.time.Clock()
pygame.joystick.init()
textPrint = textPrint()

while done == False:

'''
