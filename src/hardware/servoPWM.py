
import RPi.GPIO as GPIO 
from enum import Enum


class Speeeeds(Enum):
    SLOW = 6.8
    NORMAL = 6.65
    FAST = 6.5


class Controls:
    def __init__(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(12, GPIO.OUT)
        GPIO.setup(18, GPIO.OUT)

        frequency = 25000
 
        self.pwm_steering = GPIO.PWM(18, frequency)
        self.pwm_drive = GPIO.PWM(12, frequency)

        self.pwm_steering.start(7.5)
        self.pwm_drive.start(7)

        
    def servo(self, status):
        self.pwm_steering.ChangeDutyCycle(status/12 + 7.5)
        print(f"DC: {status/18 + 7.5}")

    def set_x_drive_mode(self, speed: Speeeeds):

        self.pwm_drive.ChangeDutyCycle(speed)
        print(f"DC: {status/36 + 7.5}")


if __name__ == "__main__":
    actuators = Controls()
    try:
        while True:

                status = int(input(f"Input angle:: "))
                actuators.servo(status)
            
    except KeyboardInterrupt:
        print("EXIT")