from adafruit_servokit import ServoKit
# if __name__ == "__main__":
import sys
sys.path.append("..")

import data
import time
import RPi.GPIO as GPIO
from enum import Enum

MIN_IMP = [1000]
MAX_IMP = [2000]
MIN_ANG = [0]
MAX_ANG = [180]


class Pins(Enum):
    MOTOR = 12
    SERVO = 18

class Speeeeds(Enum):
    SLOW = 88
    NORMAL = 78
    FAST = 70
    STOP = 90


class Control:

    def __init__(self):

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        self.pca = ServoKit(channels=16)
        self.pca.servo[0].set_pulse_width_range(MIN_IMP[0], MAX_IMP[0])
        self.pca.servo[1].set_pulse_width_range(MIN_IMP[0], MAX_IMP[0])

        print("Start PWM with 0%")
        
        self.servo(0)  # Initialization
        self.set_x_drive_mode(Speeeeds.STOP)

        time.sleep(0.2)

    def set_x_drive_mode(self, speed: Speeeeds):

        self.pca.servo[1].angle = (speed.value)
        print(f"Speed: {speed.value}")

    def servo(self, x):
        print(f"Angle: {self.translate(x, -25, 25, 0, 180)}")
        self.pca.servo[0].angle = self.translate(x, -25, 25, 0, 180)

    def translate(self, value, leftMin, leftMax, rightMin, rightMax):
        # Figure out how 'wide' each range is
        leftSpan = leftMax - leftMin
        rightSpan = rightMax - rightMin

        # Convert the left range into a 0-1 range (float)
        valueScaled = float(value - leftMin) / float(leftSpan)

        # Convert the 0-1 range into a value in the right range.
        return rightMin + (valueScaled * rightSpan)

    def stop(self):

        self.set_x_drive_mode(Speeeeds.STOP)

        if self.debug:
            print("Stopping bldc")



if __name__ == '__main__':
    bldc = Control()

    try:
        
        bldc.servo(0)
        time.sleep(1)


        bldc.servo(20)
        bldc.set_x_drive_mode(Speeeeds.FAST)


    except KeyboardInterrupt:
        bldc.stop()
