#Sub Pi is the server
import socket
import pygame
from TextPrint import TextPrint


def setUpSocket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '0.0.0.0'
    port = 9000
    sock.bind((host, port))
    sock.listen(5)
    print "server is ready"
    surface, addr = sock.accept()
    print('Got connection from', addr)
    surface.send('Thank you for connecting')

def setUpScreen():
    pygame.init()
    textPrint = TextPrint()
    size = [500, 500]
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Joystick Info from: " + str(addr))
    clock = pygame.time.Clock()

setUpSocket()
setUpScreen()


joystickInput = surface.recv(24)
while joystickInput != "END":
    textPrint.reset()
    
    #print joystickInput
    joystickInput = surface.recv(24)

    textPrint.printInfo(screen,"Joystick axis:")
    textPrint.indent()

    for i in range(4):
        textPrint.printInfo(screen,"Axis {} value: {}".format(i, joystickInput[i * 6:i * 6 + 6]))
    pygame.display.flip()
    
pygame.quit()
print(c.recv(21)) #ensures that the client "closes" first, or the server port will be stuck on TIME_WAIT
c.close()

