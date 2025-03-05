import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(21, GPIO.OUT)

try:
    while True:
        GPIO.output(21, GPIO.HIGH)
        print("Relay is ON")
        time.sleep(1)
        GPIO.output(21, GPIO.LOW) # Turn the relay off
        print("Relay is OFF")
        time.sleep(1)
except KeyboardInterrupt:
    GPIO.output(21, GPIO.LOW)
    print("Program interrupted, relay turned off")
finally:
    GPIO.cleanup()