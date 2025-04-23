from flask import Flask, render_template, Response, stream_with_context, request
import cv2
from picamera2 import Picamera2
import RPi.GPIO as GPIO
import time

# Flask setup
app = Flask(__name__)

# GPIO setup
GPIO.setmode(GPIO.BOARD)
servo_pin_x = 11  
servo_pin_y = 13 

GPIO.setup(servo_pin_x, GPIO.OUT)
GPIO.setup(servo_pin_y, GPIO.OUT)

servo_x = GPIO.PWM(servo_pin_x, 50)
servo_y = GPIO.PWM(servo_pin_y, 50)

servo_x.start(0)
servo_y.start(0)

angle_x = 120
angle_y = 60

def set_angle(servo, angle):
    angle = max(0, min(180, angle))
    duty = angle / 18 + 3
    servo.ChangeDutyCycle(duty)
    time.sleep(0.2)
    servo.ChangeDutyCycle(0)

# Start servos at neutral position
set_angle(servo_x, angle_x)
set_angle(servo_y, angle_y)
time.sleep(1)

frame_center_x = 320
frame_center_y = 240

def video_stream():
    face_detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    assert not face_detector.empty()
    cv2.startWindowThread()

    picam2 = Picamera2()
    picam2.configure(picam2.create_preview_configuration(main={
        "format": 'XRGB8888',
        "size": (640, 480)
    }))
    picam2.start()


    global angle_x, angle_y

    while True:
        frame = picam2.capture_array()
        grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(grey, 1.1, 5)

        if len(faces) > 0:
            (x, y, w, h) = max(faces, key=lambda b: b[2]*b[3])
            face_center_x = x + w // 2
            face_center_y = y + h // 2

            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.circle(frame, (face_center_x, face_center_y), 4, (0, 0, 255), -1)

            offset_x = face_center_x - frame_center_x
            offset_y = face_center_y - frame_center_y

            # Update servo angles
            if abs(offset_x) > 20:
                angle_x -= offset_x / 25
                angle_x = max(0, min(180, angle_x))
                set_angle(servo_x, angle_x)

            if abs(offset_y) > 20:
                angle_y += offset_y / 25
                angle_y = max(0, min(180, angle_y))
                set_angle(servo_y, angle_y)

        ret, buffer = cv2.imencode('.jpeg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def camera():
    return render_template('camera.html')

@app.route('/video_feed')

def video_feed():
    return Response(video_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')
    
if __name__ == '__main__':
    try:
        print("\n=============================================")
        print("IoT Face Tracking Flask Server is Running!")
        print("Access stream at: http://<RaspberryPi_IP>:5000")
        print("=============================================\n")

        app.run(host='0.0.0.0', port=5000, debug=True)

    except KeyboardInterrupt:
        print("Interrupted by user")

    finally:
        servo_x.stop()
        servo_y.stop()
        GPIO.cleanup()
        cv2.destroyAllWindows()
