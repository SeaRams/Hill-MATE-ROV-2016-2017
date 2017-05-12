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
cycle = 60 #cycle value. servos are best at 60, but motors are best at something hundreds. 60 was the value from last year
pwm = PWM(0x40)
pwm.setPWMFreq(cycle)

def usToBit(usVal):
    tick = (1000000 / cycle) / 4096
    return usVal/tick

#Active values. Only thrusters for now. TO CHANGE WHEN ARM GETS MADE
#"Left" "Right" when looking at the ROV from behind. (Camera is "front")
motorLeft = 0
motorRight = 0
motorBackVertical = 0
motorLeftVertical = 0
motorRightVertical = 0
camVal = 0
clawVal = 0

counter = 1
joystickInput = surface.recv(24)
while joystickInput != "ENDENDENDENDENDENDEND":
    #print(joystickInput)
    motorLeft = joystickInput[0:3]
    motorRight = joystickInput[3:6]
    motorBackVertical = joystickInput[6:9]
    motorLeftVertical = joystickInput[9:12]
    motorRightVertical = joystickInput[12:15]
    camVal = joystickInput[15:18]
    clawVal = joystickInput[18:21]
    
    pwm.setPWM(4, 0, int(motorLeft))
    pwm.setPWM(5, 0, int(motorRight))
    pwm.setPWM(8, 0, int(motorBackVertical))
    pwm.setPWM(9, 0, int(motorLeftVertical))
    pwm.setPWM(10, 0, int(motorRightVertical))
    pwm.setPWM(0, 0, int(camVal)) #DEBUGGING: port 1 is arm movement, port 2 is claw open/close
    pwm.setPWM(2, 0, int(clawVal))
    
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
    textPrint.printInfo(screen, "clawVal value: {}".format(clawVal))
    counter+=1
    textPrint.printInfo(screen, str(counter)) #tick rate
    pygame.display.flip()
    surface.send("Confirmation")

    joystickInput = surface.recv(21)
    
pygame.quit()
print(surface.recv(21)) #ensures that the client "closes" first, or the server port will be stuck on TIME_WAIT
surface.close()
