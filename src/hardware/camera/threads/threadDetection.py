
import cv2
import threading
import base64
import time
import numpy as np
import pickle

from multiprocessing import Pipe
from src.utils.messages.allMessages import (
    serialCamera,
    lineInformation,
    signInformation,
    Config,
)
from src.detection.model import SignDetect
from src.detection.LineDetection import LineDetect
from src.templates.threadwithstop import ThreadWithStop


class threadDetection(ThreadWithStop):
    """Thread which will handle camera functionalities.\n
    Args:
        pipeRecv (multiprocessing.queues.Pipe): A pipe where we can receive configs for camera. We will read from this pipe.
        pipeSend (multiprocessing.queues.Pipe): A pipe where we can write configs for camera. Process Gateway will write on this pipe.
        queuesList (dictionar of multiprocessing.queues.Queue): Dictionar of queues where the ID is the type of messages.
        logger (logging object): Made for debugging.
        debugger (bool): A flag for debugging.
    """

    # ================================ INIT ===============================================
    def __init__(self, pipeRecv, pipeSend, queuesList, logger, debugger):
        super(threadDetection, self).__init__()
        self.queuesList = queuesList
        self.logger = logger
        self.pipeRecvConfig = pipeRecv
        self.pipeSendConfig = pipeSend
        self.debugger = debugger
        pipeRecvSerialCamera, pipeSendSerialCamera = Pipe(duplex=False)
        self.pipeRecvSerialCamera = pipeRecvSerialCamera
        self.pipeSendSerialCamera = pipeSendSerialCamera
        self.subscribe()
        self.Configs()
        self.signDetect = SignDetect()
        self.lineDetect = LineDetect()

        self.mapx, self.mapy = None, None
        self.roi = None

    def subscribe(self):
        """Subscribe function. In this function we make all the required subscribe to process gateway"""
    
        self.queuesList["Config"].put(
            {
                "Subscribe/Unsubscribe": "subscribe",
                "Owner": serialCamera.Owner.value,
                "msgID": serialCamera.msgID.value,
                "To": {"receiver": "threadDetection", "pipe": self.pipeSendSerialCamera},
            }
        )
        self.queuesList["Config"].put(
            {
                "Subscribe/Unsubscribe": "subscribe",
                "Owner": Config.Owner.value,
                "msgID": Config.msgID.value,
                "To": {"receiver": "threadDetection", "pipe": self.pipeSendConfig},
            }
        )

    # =============================== STOP ================================================
    def stop(self):
        super(threadDetection, self).stop()

    # =============================== CONFIG ==============================================
    def Configs(self):
        """Callback function for receiving configs on the pipe."""
        while self.pipeRecvConfig.poll():
            message = self.pipeRecvConfig.recv()
            message = message["value"]
            print(message)
            # self.camera.set_controls(
            #     {
            #         "AeEnable": False,
            #         "AwbEnable": False,
            #         message["action"]: float(message["value"]),
            #     }
            # )
        threading.Timer(1, self.Configs).start()

    # ================================ RUN ================================================
    def run(self):
        first = True
        """This function will run while the running flag is True. It captures the image from camera and make the required modifies and then it send the data to process gateway."""
        while self._running:
            if self.pipeRecvSerialCamera.poll():

                start_time = time.time()

                print("Thread Detection")
                message = self.pipeRecvSerialCamera.recv()
                message = message["value"]
                
                image_data = base64.b64decode(message)
                img = np.frombuffer(image_data, dtype=np.uint8)
                img = cv2.imdecode(img, cv2.IMREAD_COLOR)

                # if first: 
                #     with open('/home/hugo/brain/src/CameraCalibration/calibration.pkl', 'rb') as file:
                #         # Ucitavanje parametara iz calibration.pkl
                #         loaded_data = pickle.load(file)
                #         cameraMatrix, dist = loaded_data
                #     h = img.shape[0]
                #     w = img.shape[1]
                #     newCameraMatrix, self.roi = cv2.getOptimalNewCameraMatrix(cameraMatrix, dist, (w,h), 1, (w,h))
                #     self.mapx, self.mapy = cv2.initUndistortRectifyMap(cameraMatrix, dist, None, newCameraMatrix, (w,h), 5)
                #     first = False

                # x, y, w, h = self.roi
                # dst = cv2.remap(img, self.mapx, self.mapy, cv2.INTER_LINEAR)

                # calibratedImage = dst[y:y+h, x:x+w]
                length,angle,right_line = self.lineDetect.detectLines(img)#calibratedImage)
                #sign_class, confidence, distance = self.signDetect.sign_detect(image)
                cv2.imshow("frame", img)
                cv2.waitKey(1)
                
                print(length, angle, right_line)
                if length != 0:
                    #length /= 1.792

                    out_line_message = {
                        "length"      : length*0.264583333,
                        "angle" : angle,
                        "right_line"   : right_line
                    }

                    self.queuesList[lineInformation.Queue.value].put(
                        {
                            "Owner": lineInformation.Owner.value,
                            "msgID": lineInformation.msgID.value,
                            "msgType": lineInformation.msgType.value,
                            "msgValue": out_line_message,
                        }
                    )

                #print(f"Detect time: {time.time() - start_time}")
                
                #stime.sleep(0.1)
                # self.queuesList[signInformation.Queue.value].put(
                #     {
                #         "Owner": signInformation.Owner.value,
                #         "msgID": signInformation.msgID.value,
                #         "msgType": signInformation.msgType.value,
                #         "msgValue": out_line_message,
                #     }
                # )

    # =============================== START ===============================================
    def start(self):
        print("Starting thread detection")
        super(threadDetection, self).start()


