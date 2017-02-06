#Surface Pi is the client

import socket
import pygame

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = '169.254.122.176' #eth0 "inet addr" of Sub Pi
port = 9000 #Arbitrary port above 5000 - must be same for sub Pi

sock.connect((host, port))

print "connected"
print(sock.recv(1024))

#sock.send("thank you for serving")
sock.close()

# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)

# This is a simple class that will help us print to the screen
# It has nothing to do with the joysticks, just outputing the
# information.
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
 
# Set the width and height ofont.render(textString, True, BLACK)
# screen.blit(textBif the screen [width,height]
#size = [500, 700]
#screen = pygame.display.set_mode(size)

#pygame.display.set_caption("My Game")

#Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Initialize the joysticks

    
# Get ready to print
#textPrint = TextPrint()

#temp = 0

while done == False:
    joystick1 = pygame.joystick.Joystick(0)
    joystick1.init()
    
    for event in pygame.event.get():
        if event.type == pygame.JOYBUTTONDOWN and (joystick1.get_button(11) == 1 or joystick1.get_button(10) == 1):
            sock.send("END")
            done = True;
    
    toSend = ""
    for i in range(0, 4):
        axis = str(joystick1.get_axis(i))
        toSend += str(axis)[0:6]
        for j in range(0, 6 - len(str(axis))):
            toSend += "0" #just in case "axis" is 1.0 or too short
    #print toSend
    sock.send(toSend)
    clock.tick(20)

sock.send("thank you for serving")
sock.close()