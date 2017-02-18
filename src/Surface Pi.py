#Surface Pi is the client

import socket
import pygame
from TextPrint import TextPrint

def setUpSocket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '169.254.122.176' #eth0 "inet addr" of Sub Pi
    port = 9000 #Arbitrary port above 5000 - must be same for sub Pi
    sock.connect((host, port))
    print "Connected"
    print(sock.recv(1024))


done = False

while done == False:
    joystick1 = pygame.joystick.Joystick(0)
    joystick1.init()
    
    for event in pygame.event.get():
        if event.type == pygame.JOYBUTTONDOWN:
            if(joystick1.get_button(11) == 1): #kill command
                sock.send("END")
                done = True
    
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