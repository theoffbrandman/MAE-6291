# TESTING FOR SERVO MOTORS

import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)

servo = GPIO.PWM(11, 50)  
servo.start(0)

servo.ChangeDutyCycle(2)
sleep(1)
servo.ChangeDutyCycle(7)
sleep(1)
servo.ChangeDutyCycle(12)
sleep(1)

servo.ChangeDutyCycle(12)
sleep(1)




servo.stop()
GPIO.cleanup()

    