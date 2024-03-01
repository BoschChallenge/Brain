if __name__ == "__main__":
    import sys
    print(sys.path)
    sys.path.insert(0, "../..")

from src.computer_vision.lineDetection.LineDetection import LineDetect
from src.hardware.serialhandler.processSerialHandler import processSerialHandler

from threading import Thread
from multiprocessing import Queue, Pipe
import logging
import time



class Pid():

    def __init__(self):

        self.frame = None
        self.dist_packet = 0
        
        self.LINE_THREAD = True

        self.DESIRED_DISTANCE = 150
        self.MAX_PID = 22

        self.Kp = 5

        self.linedetector = LineDetect()
        ld_thread = Thread(target=self.start, args=(self.frame))
        ld_thread.start()

    def start(self, frame=None):
        
        while self.LINE_THREAD:
            self.dist_packet = self.linedetector.detect(frame)
            self.calculate_pid()

    def stop(self):
        pass

    def calculate_pid(self):

        actual_distance, actual_angle, actual_line = self.dist_packet

        error = self.DESIRED_DISTANCE - actual_distance

        pid = self.Kp * error 

        if pid >= self.MAX_PID:
            pid = self.MAX_PID

        elif pid <= -self.MAX_PID:
            pid = -self.MAX_PID

        print(f"Steraing angle: {pid}")

        return pid  

    def set_desired_angle(self):

        # def example(self):
        # """This function simulte the movement of the car."""
        # if self.exampleFlag:
        #     self.pipeSendRunningSignal.send({"Type": "Run", "value": True})
        #     self.pipeSendSpeed.send({"Type": "Speed", "value": self.s})
        #     self.pipeSendSteer.send({"Type": "Steer", "value": self.i})
        #     self.i += self.j
        #     if self.i >= 21.0:
        #         self.i = 21.0
        #         self.s = self.i / 7
        #         self.j *= -1
        #     if self.i <= -21.0:
        #         self.i = -21.0
        #         self.s = self.i / 7
        #         self.j *= -1.0
        #     threading.Timer(0.01, self.example).start()

        allProcesses = list()
        debugg = False
        # We have a list of multiprocessing.Queue() which individualy represent a priority for processes.
        queueList = {
            "Critical": Queue(),
            "Warning": Queue(),
            "General": Queue(),
            "Config": Queue(),
        }
        logger = logging.getLogger()
        pipeRecv, pipeSend = Pipe(duplex=False)
        process = processSerialHandler(queueList, logger, debugg, True)
        process.daemon = True
        process.start()
        time.sleep(4)  # modify the value to increase/decrease the time of the example
        process.stop()

    def set_desired_speed(self):
        pass


if __name__ == "__main__":
    import cv2

    cap = cv2.VideoCapture("src\computer_vision\lineDetection\full_hd2.mp4")
    ret,frame = cap.read()

    pid = Pid()

    
        

    

        
