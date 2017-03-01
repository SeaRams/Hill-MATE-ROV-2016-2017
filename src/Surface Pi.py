#Surface Pi is the client

import socket
import pygame
import time
from TextPrint import TextPrint
   
sub = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '169.254.209.5' #eth0 "inet addr" of Sub Pi
port = 9000 #Arbitrary port above 5000 - must be same for sub Pi
sub.connect((host, port))
print "Connected"
print(sub.recv(1024))

pygame.init()
pygame.joystick.init()
clock = pygame.time.Clock()
running = True

cycle = 60 #Current cycle for the motors. If slow response time, raise.

def usToBit(usVal):
    tick = (1000000 / cycle) / 4096
    return usVal / tick

#IMPORTANT: THESE ARE VALUES FROM LAST YEAR, HAVE NOT BEEN CONFIRMED, DO NOT USE WITHOUT TESTING
#Servo default pulse lengths.

#Generally, mid should be usToBit(1500), +90 should be usToBit(2000) and -90 should be usToBit(1000)
#But these servos are not accurate, so they can only be found by testing
#Make sure to use usToBit(NUMBER) instead of just a number.
ARM_RIGHT = usToBit(2000)
ARM_MID = usToBit(1500)
ARM_LEFT = usToBit(1000)

CLAW_CLOSE = usToBit(1000)
CLAW_MID = usToBit(1500)
#CLAW_OPEN = usToBit(2000) THIS MAY NOT BE NECESSARY - we might want to Claw to be open fully at all times when it is not closed.
#There may be a few problems:
#1) Closing on the object may force the claw to be more open than "CLAW_CLOSE", which may strain the motor
#2) The motor may not be strong enough, which is the problem we had last year
#3) The screws may come loose, which was the problem last year

CAM_BACKWARD = usToBit(2000)
CAM_MID = usToBit(1500)
CAM_FORWARD = usToBit(1000)

#Constant thruster pulse lengths.
THRUSTER_MAX = usToBit(1900) #1900 us is full forward, raise if not fast enough.
THRUSTER_MID = usToBit(1500)
THRUSTER_MIN = usToBit(1100)
'''
Old values
THRUSTER_MAX = 600 
THRUSTER_MID = 410
THRUSTER_MIN = 220
'''

#Active values. Only thrusters for now. TO CHANGE WHEN ARM GETS MADE
#"Left" "Right" when looking at the ROV from behind. (Camera is "front")
motorLeft = THRUSTER_MID
motorRight = THRUSTER_MID
motorBackVertical = THRUSTER_MID
motorLeftVertical = THRUSTER_MID
motorRightVertical = THRUSTER_MID
camVal = CAM_MID
armVal = ARM_MID
clawVal = CLAW_OPEN


def changeInterval(x, in_min, in_max, out_min, out_max):     #x is a value between in_min and in_max. It is "re-mapped" to between out_min and out_max.
    return int( (x-in_min) * (out_max-out_min) // (in_max-in_min) + out_min )

def processForwardBackward(joystickValue): #remember that moving the joystick forward results in a negative value.
    global motorLeft, motorRight
    motorLeft = changeInterval(-joystickValue, -1, 1, THRUSTER_MAX, THRUSTER_MIN) 
    motorRight = changeInterval(-joystickValue, -1, 1, THRUSTER_MIN, THRUSTER_MAX)
    #DEBUGGING: If the robot moves forward when joystick is forward, delete the above and switch to:
    # motorLeft = changeInterval(-joystickValue, -1, 1, THRUSTER_MIN, THRUSTER_MAX) 
    # motorRight = changeInterval(-joystickValue, -1, 1, THRUSTER_MAX, THRUSTER_MIN)
    #Otherwise, just delete this block comment. The reason is that the motors are mis-matched to resist torque.

def processYaw(joystickValue):
    global motorLeft, motorRight
    motorLeft = changeInterval(joystickValue, -1, 1, THRUSTER_MIN, THRUSTER_MAX)
    motorRight = changeInterval(joystickValue, -1, 1, THRUSTER_MIN, THRUSTER_MAX)
    #DEBUGGING: If the robot is yawing the wrong way, switch to this code:
    # motorLeft = changeInterval(joystickValue, 1, -1, THRUSTER_MIN, THRUSTER_MAX)
    # motorRight = changeInterval(joystickValue, 1, -1, THRUSTER_MIN, THRUSTER_MAX)
    #if works as intended, delete the comment.

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

def processClaw(joystick1): #if claw doesn't work, skype me
    global clawVal
    if(joystick1.get_button(0)):
        if(clawVal > CLAW_CLOSE): #close as you hold the trigger button
            clawVal = clawVal - 5
    else: #go back to open if nothing is pressed
        clawVal = CLAW_MID

def processHat(joystick1):
    global camVal, armVal, clawVal
    joystickHatInput = str(joystick1.get_hat(0))
    if(joystickHatInput == "(0, 1)"):
        if(camVal > CAM_FORWARD):
            camVal = camVal - 5
    elif(joystickHatInput == "(0, -1)"):
        if(camVal < CAM_BACKWARD):
            camVal = camVal + 5
    elif(joystickHatInput = "(1, 0)"): #DEBUGGING: if the arm is moving left when the hat is directed right, replace (1, 0) with (-1, 0) and (-1, 0) with (1, 0).
        if(armVal < ARM_RIGHT):
            armVal = armVal + 5
    elif(joystickHatInput = "(-1, 0)"):
        if(armVal > ARM_LEFT):
            armVal = armVal - 5
    

def processJoystick():
    joystick = pygame.joystick.Joystick(0) #Was in main while loop, does this work? *NOT TESTED
    joystick.init()
    for event in pygame.event.get(): # User did something
        if event.type == pygame.JOYBUTTONDOWN:
            if(joystick.get_button(10) == 1 && joystick.getbutton(11) == 1): #press button 11 and 12 at the same time to kill
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
    processHat(joystick)
    processClaw(joystick)
        
def packageInformation():
    toSend = str(motorLeft) + str(motorRight) + str(motorBackVertical) + str(motorLeftVertical) + str(motorRightVertical) + str(camVal) + str(armVal) + str(clawVal)
    return toSend

while running == True:
    processJoystick()
    if(running):
        temp = packageInformation()
        sub.send(temp)
        sub.recv(12)
    else:
        sub.send("ENDENDENDENDENDENDENDEND")

pygame.quit()
sub.send("Thank you for serving")
sub.close()
#Surface Pi is the client
