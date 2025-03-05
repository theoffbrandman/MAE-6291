import RPi.GPIO as GPIO
import time
import smtplib
import yagmail
from gpiozero import LED, Button, Buzzer

# GPIO Pin Assignments
TRIG_PIN = 23  # Ultrasonic sensor trigger pin
ECHO_PIN = 22  # Ultrasonic sensor echo pin
BUTTON_PIN = 27  # Verification button
GAS_SENSOR_PIN = 20  # MQ2 Gas sensor digital output
RELAY_PIN = 21  # Controls external device
ALARM_PIN = 18  # Warning LED and Buzzer (combined output)

# Distance threshold in cm
DISTANCE_THRESHOLD = 10

# Email Setup
EMAIL_SENDER = "ehunterp17@gmail.com"
EMAIL_PASSWORD = "magk bxdg nzuh fvlh"
EMAIL_RECEIVER = "eliothunter03@gmail.com"

yag = yagmail.SMTP(EMAIL_SENDER, EMAIL_PASSWORD)

# Initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(GAS_SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(RELAY_PIN, GPIO.OUT)
GPIO.setup(ALARM_PIN, GPIO.OUT)

alarm = LED(ALARM_PIN)

# Function to Send Email Notification
def send_email(subject, message):
    yag.send(to=EMAIL_RECEIVER, subject=subject, contents=message)

# Function to Measure Distance Using Ultrasonic Sensor
def distance():
    GPIO.output(TRIG_PIN, 0)
    time.sleep(0.000002)
    GPIO.output(TRIG_PIN, 1)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, 0)
    
    while GPIO.input(ECHO_PIN) == 0:
        time1 = time.time()
        
    while GPIO.input(ECHO_PIN) == 1:
        time2 = time.time()

    during = time2 - time1
    distance = during * 340 / 2 * 100 #distance in cm
    return distance

# Function to Verify User via Button Press
def verify_user():
    ctr = 5
    print("Press button to verify identity.")
    while ctr > 0:
        if GPIO.input(BUTTON_PIN) == GPIO.HIGH:
            time.sleep(0.1)
            print("User verified.")
            send_email("User Verified", "The user has been recognized.")
            return True
        elif ctr > 0:
            print(ctr)
            ctr = ctr - 1
            time.sleep(1)
        elif ctr == 0:
            return False

# Function to Trigger Alarm
def trigger_alarm():
    alarm.blink(on_time=0.25, off_time=0.25, n=10, background=True)
    time.sleep(5)
    GPIO.output(RELAY_PIN, GPIO.HIGH)
    time.sleep(0.1)
    GPIO.output(RELAY_PIN, GPIO.LOW)

# Main Loop
try:
    while True:
        dist = distance()
        if dist < DISTANCE_THRESHOLD:
            time.sleep(0.5)
            if verify_user():
                print("User recognized. No action required.")
                time.sleep(10)
            else:
                print("Unauthorized access detected!")
                trigger_alarm()
        
         #Gas Sensor Monitoring
        if GPIO.input(GAS_SENSOR_PIN) == GPIO.LOW:
            print("Gas levels too high! Triggering safety mechanism.")
            send_email("Gas Alert", "Harmful gas levels detected!")
            #trigger_alarm()
            time.sleep(10)
        
        time.sleep(1)

except KeyboardInterrupt:
    print("Exiting...")
    GPIO.cleanup()