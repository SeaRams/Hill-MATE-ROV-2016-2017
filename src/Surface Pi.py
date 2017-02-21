#Surface Pi is the client

import socket
import pygame
import time
from TextPrint import TextPrint

sub = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '169.254.122.176' #eth0 "inet addr" of Sub Pi
port = 9001 #Arbitrary port above 5000 - must be same for sub Pi
sub.connect((host, port))
print "Connected"
print(sub.recv(1024))

pygame.init()
pygame.joystick.init()
clock = pygame.time.Clock()
running = True

print(pygame.joystick.get_count())

#IMPORTANT: THESE ARE VALUES FROM LAST YEAR, HAVE NOT BEEN CONFIRMED, DO NOT USE WITHOUT TESTING
#Servo default pulse lengths. 
wrist_minus = 280
wrist_mid   = 430
wrist_plus  = 580
    
claw_minus  = 200
claw_mid    = 335
claw_plus   = 490

arm_minus   = 270
arm_mid     = 410
arm_plus    = 550

cam_mid   = 365

#Constant thruster pulse lengths. 
THRUSTER_MAX = 600
THRUSTER_MID = 410
THRUSTER_MIN = 220


#Active values. Only thrusters for now. TO CHANGE WHEN ARM GETS MADE
#"Left" "Right" when looking at the ROV from behind. (Camera is "front")
motorLeft = THRUSTER_MID
motorRight = THRUSTER_MID
motorBackVertical = THRUSTER_MID
motorLeftVertical = THRUSTER_MID
motorRightVertical = THRUSTER_MID

#Controls how much juice is going to the motors. Ranges from 0% to 100%
throttle = 0;

def changeInterval(x, in_min, in_max, out_min, out_max):     #x is a value between in_min and in_max. It is "re-mapped" to between out_min and out_max.
    return int( (x-in_min) * (out_max-out_min) // (in_max-in_min) + out_min )

def processForwardBackward(joystickValue): #remember that moving the joystick forward results in a negative value.
    global motorLeft, motorRight
    newValue = changeInterval(-joystickValue, -1, 1, THRUSTER_MIN, THRUSTER_MAX)
    motorLeft = newValue
    motorRight = newValue

def processYaw(joystickValue):
    global motorLeft, motorRight
    #I think -1 joystick value is counterclockwise and 1 is clockwise. CHECK THIS. If not, replace left with right and right with let.
    motorLeft = changeInterval(joystickValue, -1, 1, THRUSTER_MIN, THRUSTER_MAX)
    motorRight = changeInterval(joystickValue, 1, -1, THRUSTER_MIN, THRUSTER_MAX)

def processVertical(joystick1):
    global motorBackVertical, motorLeftVertical, motorRightVertical
    if(joystick1.get_button(6)): #button labeled "7" is pressed, ROV goes down
        if(motorBackVertical > THRUSTER_MIN): #because there are two front motors and one back, the front ones go half as fast as the back one so the ROV doesn't flip.
            motorBackVertical = motorBackVertical - 2
            motorLeftVertical = motorLeftVertical - 1
            motorRightVertical = motorRightVertical - 1

    elif(joystick1.get_button(7)): #button labeled "8" is pressed, ROV goes up
        if(motorBackVertical < THRUSTER_MAX): #because there are two front motors and one back, the front ones go half as fast as the back one so the ROV doesn't flip.
            motorBackVertical = motorBackVertical + 2
            motorLeftVertical = motorLeftVertical + 1
            motorRightVertical = motorRightVertical + 1

    else: #neither button was pressed, ROV will stop moving vertically
        motorBackVertical = THRUSTER_MID
        motorLeftVertical = THRUSTER_MID
        motorRightVertical = THRUSTER_MID

def processJoystick():
    joystick = pygame.joystick.Joystick(0) #Was in main while loop, does this work? *NOT TESTED
    joystick.init()
    for event in pygame.event.get(): # User did something
        if event.type == pygame.JOYBUTTONDOWN:
            if(joystick.get_button(0) == 1):
                global running
                running = False
    if(abs(joystick.get_axis(1)) > 0.1): #has to be moved at least a little to trigger
        processForwardBackward(joystick.get_axis(1)) #"1" should be the forward-backwards axis. CHECK THIS
    elif(abs(joystick.get_axis(2)) > 0.1):
        processYaw(joystick.get_axis(2)) #"2" should be the twist axis. CHECK THIS
    else:
        global motorLeft, motorRight
        motorLeft = THRUSTER_MID
        motorRight = THRUSTER_MID
    processVertical(joystick)
        
def packageInformation():
    toSend = str(motorLeft) + str(motorRight) + str(motorBackVertical) + str(motorLeftVertical) + str(motorRightVertical)
    return toSend

while running == True:
    processJoystick()
    if(running):
        sub.send(packageInformation())
    else:
        sub.send("END")

    time.sleep(0.05) #every 50 milliseconds
pygame.quit()
sub.send("Thank you for serving")
sub.close()
#Surface Pi is the client

import socket
import pygame
import time
from TextPrint import TextPrint

sub = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '169.254.122.176' #eth0 "inet addr" of Sub Pi
port = 9000 #Arbitrary port above 5000 - must be same for sub Pi
sub.connect((host, port))
print "Connected"
print(sub.recv(1024))

pygame.init()
joystick1 = pygame.joystick.Joystick(0) #Was in main while loop, does this work? *NOT TESTED
joystick1.init()
print("k")
running = True


#IMPORTANT: THESE ARE VALUES FROM LAST YEAR, HAVE NOT BEEN CONFIRMED, DO NOT USE WITHOUT TESTING
#Servo default pulse lengths. 
wrist_minus = 280
wrist_mid   = 430
wrist_plus  = 580
    
claw_minus  = 200
claw_mid    = 335
claw_plus   = 490

arm_minus   = 270
arm_mid     = 410
arm_plus    = 550

cam_mid   = 365

#Constant thruster pulse lengths. 
THRUSTER_MAX = 600
THRUSTER_MID = 410
THRUSTER_MIN = 220


#Active values. Only thrusters for now. TO CHANGE WHEN ARM GETS MADE
#"Left" "Right" when looking at the ROV from behind. (Camera is "front")
motorLeft = THRUSTER_MID
motorRight = THRUSTER_MID
motorBackVertical = THRUSTER_MID
motorLeftVertical = THRUSTER_MID
motorRightVertical = THRUSTER_MID

#Controls how much juice is going to the motors. Ranges from 0% to 100%
throttle = 0;

def changeInterval(x, in_min, in_max, out_min, out_max):     #x is a value between in_min and in_max. It is "re-mapped" to between out_min and out_max.
    return int( (x-in_min) * (out_max-out_min) // (in_max-in_min) + out_min )

def processForwardBackward(joystickValue): #remember that moving the joystick forward results in a negative value.
    newValue = changeInterval(-joystickValue, -1, 1, THRUSTER_MIN, THRUSTER_MAX)
    motorLeft = newValue
    motorRight = newValue

def processYaw(joystickValue):
    #I think -1 joystick value is counterclockwise and 1 is clockwise. CHECK THIS. If not, replace left with right and right with let.
    motorLeft = changeInterval(joystickValue, -1, 1, THRUSTER_MIN, THRUSTER_MAX)
    motorRight = changeInterval(joystickValue, 1, -1, THRUSTER_MIN, THRUSTER_MAX)

def processVertical():
    if(joystick1.get_button(6)): #button labeled "7" is pressed, ROV goes down
        if(motorBackVertical > THRUSTER_MIN): #because there are two front motors and one back, the front ones go half as fast as the back one so the ROV doesn't flip.
            motorBackVertical = motorBackVertical - 2
            motorLeftVertical = motorLeftVertical - 1
            motorRightVertical = motorRightVertical - 1

    elif(joystick1.get_button(7)): #button labeled "8" is pressed, ROV goes up
        if(motorBackVertical < THRUSTER_MAX): #because there are two front motors and one back, the front ones go half as fast as the back one so the ROV doesn't flip.
            motorBackVertical = motorBackVertical + 2
            motorLeftVertical = motorLeftVertical + 1
            motorRightVertical = motorRightVertical + 1

    else: #neither button was pressed, ROV will stop moving vertically
        motorBackVertical = THRUSTER_MID
        motorLeftVertical = THRUSTER_MID
        motorRightVertical = THRUSTER_MID

def processJoystick():
    if(joystick1.get_button(0) == 1): #trigger button ends program
        running = False
    else:
        processForwardBackward(joystick1.get_axis(1)) #"1" should be the forward-backwards axis. CHECK THIS
        processYaw(joystick1.get_axis(2)) #"2" should be the twist axis. CHECK THIS
        processVertical()

def packageInformation():
    toSend = str(motorLeft) + str(motorRight) + str(motorBackVertical) + str(motorLeftVertical) + str(motorRightVertical)
    return toSend

while running:
    processJoystick()
    if(running):
        sub.send(packageInformation())
    else:
        sub.send("END")

    time.sleep(0.05) #every 50 milliseconds
    
sub.send("Thank you for serving")
sub.close()
