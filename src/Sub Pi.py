#Sub Pi is the server
import socket
import pygame
import time
from TextPrint import TextPrint
from Adafruit_PWM_Servo_Driver import PWM


#setup socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '0.0.0.0'
port = 9000
sock.bind((host, port))
sock.listen(5)
print "server is ready"
surface, addr = sock.accept()
print('Got connection from', addr)
surface.send('Thank you for connecting')

#setup screen
pygame.init()
textPrint = TextPrint()
size = [500, 500]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Joystick Info from: " + str(addr))
clock = pygame.time.Clock()

# Initialise the PWM device using the default address
cycle = 60
pwm = PWM(0x40)
pwm.setPWMFreq(cycle)

def usToBit(usVal):
    tick = (1000000 / cycle) / 4096
    return usVal/tick

#IMPORTANT: THESE ARE VALUES FROM LAST YEAR, HAVE NOT BEEN CONFIRMED, DO NOT USE WITHOUT TESTING
#Servo default pulse lengths. 
wrist_mid   = 430
claw_mid    = 335
arm_mid     = 410
CAM_MID   = usToBit(1500)

#Constant thruster pulse lengths. 
THRUSTER_MID = 410

#Active values. Only thrusters for now. TO CHANGE WHEN ARM GETS MADE
#"Left" "Right" when looking at the ROV from behind. (Camera is "front")
motorLeft = THRUSTER_MID
motorRight = THRUSTER_MID
motorBackVertical = THRUSTER_MID
motorLeftVertical = THRUSTER_MID
motorRightVertical = THRUSTER_MID
camVal = CAM_MID

counter = 1
joystickInput = surface.recv(18)
while joystickInput != "ENDENDENDENDENDEND":
    #print(joystickInput)
    motorLeft = joystickInput[0:3]
    motorRight = joystickInput[3:6]
    motorBackVertical = joystickInput[6:9]
    motorLeftVertical = joystickInput[9:12]
    motorRightVertical = joystickInput[12:15]
    camVal = joystickInput[15:18]
    
    pwm.setPWM(4, 0, int(motorLeft))
    pwm.setPWM(5, 0, int(motorRight))
    pwm.setPWM(8, 0, int(motorBackVertical))
    pwm.setPWM(9, 0, int(motorLeftVertical))
    pwm.setPWM(10, 0, int(motorRightVertical))
    pwm.setPWM(0, 0, int(camVal))
    
    textPrint.reset()
    screen.fill(( 255, 255, 255))
    textPrint.printInfo(screen,"Motor Values:")
    textPrint.indent()
    textPrint.printInfo(screen, "motorLeft value: {}".format(motorLeft))
    textPrint.printInfo(screen, "motorRight value: {}".format(motorRight))
    textPrint.printInfo(screen, "motorbackVertical value: {}".format(motorBackVertical))
    textPrint.printInfo(screen, "motorLeftVertical value: {}".format(motorLeftVertical))
    textPrint.printInfo(screen, "motorRightVertical value: {}".format(motorRightVertical))
    textPrint.printInfo(screen, "camVal value: {}".format(camVal))
    counter+=1
    textPrint.printInfo(screen, str(counter))
    pygame.display.flip()
    surface.send("Confirmation")

    joystickInput = surface.recv(18)
    
pygame.quit()
print(surface.recv(21)) #ensures that the client "closes" first, or the server port will be stuck on TIME_WAIT
surface.close()
