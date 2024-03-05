if __name__ == "__main__":
    import sys
    print(sys.path)
    sys.path.insert(0, "../..")

from src.computer_vision.lineDetection.LineDetection import LineDetect
from src.hardware.serialhandler.processSerialHandler import processSerialHandler
from brain.main import queueList

from threading import Thread, Timer
from multiprocessing import Queue, Pipe
import logging
import time

class Pid():

    def __init__(self):

        self.frame = None
        self.dist_packet = 0
        
        self.LINE_THREAD = True

        self.DESIRED_DISTANCE = 400
        self.MAX_PID = 22

        self.Kp = 0.05

        self.linedetector = LineDetect()
        ld_thread = Thread(target=self.start)
        ld_thread.start()

    def start(self):
        cap = cv2.VideoCapture("full_hd2.mp4")
        while self.LINE_THREAD:
            ret, frame = cap.read()
            if not ret:
                break

            current_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0
            # Print the current video time
            print("Current video time: {:.2f} seconds".format(current_time))

            self.dist_packet = self.linedetector.detect_lines(frame)
            self.calculate_pid()

    def stop(self):
        pass

    def calculate_pid(self):

        try:
            actual_distance, actual_angle, actual_line = self.dist_packet

        except Exception as ex:
             print(f"Error distance reading {ex}")


        error = self.DESIRED_DISTANCE - actual_distance

        print(f"actual_distance: {actual_distance}, error: {error}")

        pid = self.Kp * error 

        if pid >= self.MAX_PID:
            pid = self.MAX_PID

        elif pid <= -self.MAX_PID:
            pid = -self.MAX_PID

        print(f"Steraing angle: {pid}")

        return pid  

    def set_desired_angle(self, angle):


        queueList[SteerMotor.Queue.value].put(
        {
            "Owner": SteerMotor.Owner.value,
            "msgID": SteerMotor.msgID.value,
            "msgType": SteerMotor.msgType.value,
            # "msgValue": "Type": "action": "2", "value": 12.0,
            "msgValue": 15.0 #{
            #     "action":"steer", 
            #     "value": 15.0
            # }
        }
    )


    def set_desired_speed(self, speed):
        
        queueList[SpeedMotor.Queue.value].put(
        {
            "Owner": SpeedMotor.Owner.value,
            "msgID": SpeedMotor.msgID.value,
            "msgType": SpeedMotor.msgType.value,
            # "msgValue": "Type": "action": "2", "value": 12.0,
            "msgValue": 20.0 #{
            #     "action":"steer", 
            #     "value": 15.0
            # }
        }
    )
        


    def set_desired_speed(self):
        pass


if __name__ == "__main__":
    import cv2

    try:
        # pid = Pid()

        data = {"Type": "Steer", "value": 20}
        queueList["General"].put(data)


    except KeyboardInterrupt:

        self.LINE_THREAD = False
        # Handle keyboard interrupt gracefully
        print("Keyboard interrupt detected. Exiting...")


    

    
        

    

        
