import numpy as np
import cv2
import time
from src.detection.LineDetection import LineDetect
#from src.detection.model import SignDetect
from multiprocessing import Process

class ProcessDetection:
    def __init__(self):
        self.LD = LineDetect()  
        #self.SD = SignDetect()
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

        self.process = Process(target=self.detect)
        self.running_flag = False

    def start(self):
        self.running_flag = True
        self.process.start()

    def stop(self):
        self.running_flag = False
        self.process.join()

    def detect(self):
        start_time = time.time()
        while self.running_flag:
            seconds = time.time() - start_time
            if seconds > 15:
                self.running_flag = False
            ret,frame = self.cap.read()
            self.LD.detectLines(frame)
            #self.SD.sign_detect(frame)