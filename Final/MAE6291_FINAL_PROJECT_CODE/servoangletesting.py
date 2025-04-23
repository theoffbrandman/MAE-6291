# ANGLE TESING CODE

import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)

servo = GPIO.PWM(11, 50)  
servo.start(0)

def setAngle(angle):
    duty = angle / 18 + 3
    GPIO.output(11,True)
    servo.ChangeDutyCycle(duty)
    sleep(1)
    GPIO.output(11,False)
    servo.ChangeDutyCycle(duty)
    
# INIT Code
setAngle(90)
print("CENTER")

# FACE TRACKING CODE
    