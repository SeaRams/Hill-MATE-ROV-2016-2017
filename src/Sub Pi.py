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
pwm = PWM(0x40)
pwm.setPWMFreq(60)

#IMPORTANT: THESE ARE VALUES FROM LAST YEAR, HAVE NOT BEEN CONFIRMED, DO NOT USE WITHOUT TESTING
#Servo default pulse lengths. 
wrist_mid   = 430
claw_mid    = 335
arm_mid     = 410
cam_mid   = 365

#Constant thruster pulse lengths. 
THRUSTER_MID = 410

#Active values. Only thrusters for now. TO CHANGE WHEN ARM GETS MADE
#"Left" "Right" when looking at the ROV from behind. (Camera is "front")
motorLeft = THRUSTER_MID
motorRight = THRUSTER_MID
motorBackVertical = THRUSTER_MID
motorLeftVertical = THRUSTER_MID
motorRightVertical = THRUSTER_MID


joystickInput = surface.recv(15)
while joystickInput != "END":
    motorLeft = joystickInput[0:3]
    motorRight = joystickInput[3:6]
    motorBackVertical = joystickInput[6:9]
    motorLeftVertical = joystickInput[9:12]
    motorRightVertical = joystickInput[12:15]

    pwm.setPWM(4, 0, motorLeft)
    pwm.setPWM(5, 0, motorRight)
    pwm.setPWM(8, 0, motorBackVertical)
    pwm.setPWM(9, 0, motorLeftVertical)
    pwm.setPWM(10, 0, motorRightVertical)

    textPrint.reset()
    textPrint.printInfo(screen,"Motor Values:")
    textPrint.indent()
    textPrint.printInfo(screen, "motorLeft value: {}".format(motorLeft))
    textPrint.printInfo(screen, "motorRight value: {}".format(motorRight))
    textPrint.printInfo(screen, "motorbackVertical value: {}".format(motorBackVertical))
    textPrint.printInfo(screen, "motorLeftVertical value: {}".format(motorLeftVertical))
    textPrint.printInfo(screen, "motorRightVertical value: {}".format(motorRightVertical))
    pygame.display.flip()

    time.sleep(0.05)
    joystickInput = surface.recv(15)
    
pygame.quit()
print(c.recv(21)) #ensures that the client "closes" first, or the server port will be stuck on TIME_WAIT
c.close()