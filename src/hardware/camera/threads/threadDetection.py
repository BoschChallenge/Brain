import cv2
import threading
import base64
import time
import numpy as np

from multiprocessing import Pipe
from src.utils.messages.allMessages import (
    serialCamera,
    lineInformation,
    signInformation,
    Config,
    SpeedMotor,
    SteerMotor,
    Brake
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
        """This function will run while the running flag is True. It captures the image from camera and make the required modifies and then it send the data to process gateway."""
        while self._running:
            while self.pipeRecvSerialCamera.poll():
                print("Thread Detection")
                message = self.pipeRecvSerialCamera.recv()
                message = message["value"]
                
                image_data = base64.b64decode(message)
                img = np.frombuffer(image_data, dtype=np.uint8)
                image = cv2.imdecode(img, cv2.IMREAD_COLOR)

                length,angle,right_line = self.lineDetect.detectLines(image)

                out_line_message = {
                    "length"     : length,
                    "angle"      : angle,
                    "right_line" : right_line
                }
            
                sign_class, confidence, distance = self.signDetect.sign_detect(image)

                out_sign_message = {
                    "class"      : sign_class,
                    "confidence" : confidence,
                    "distance"   : distance
                }
                # cv2.imshow("frame", image)
                # cv2.waitKey(1)

                match sign_class:
                    case 9:#"Stop"
                        if(distance <= 25):
                            self.queueList[Brake.Queue.value].put(
                                {
                                    "Owner": "Camera",
                                    "msgID": Brake.msgID.value,
                                    "msgType": Brake.msgType.value,
                                    "msgValue": {"action": "speed", "value": 0.0},
                                }
                            )
                    case 6: #"Crosswalk"
                        self.queueList[SpeedMotor.Queue.value].put(
                            {
                                "Owner": "Camera",
                                "msgID": SpeedMotor.msgID.value,
                                "msgType": SpeedMotor.msgType.value,
                                "msgValue": {"action": "speed", "value": 8.0},
                                # The vehicle must visibly slow down on crosswalk
                            }
                        )
                    case 7: #"Priority":
                        pass
                        # self.queueList["General"].put(
                        #     {
                        #         "Owner": "Camera",
                        #         "msgID": 2,
                        #         "msgType": "String",
                        #         "msgValue": "This is a message",
                        #         # The vehicle must go into the intersection without stopping at all
                        #     }
                        # )
                    case 1: #"Highway entry":
                        self.queueList[SpeedMotor.Queue.value].put(
                            {
                                "Owner": "Camera",
                                "msgID": SpeedMotor.msgID.value,
                                "msgType": SpeedMotor.msgType.value,
                                "msgValue": {"action": "speed", "value": 25.0},
                                # The vehicle must visibly increase its speed
                            }
                        )
                    case 2: #"Highway end":
                        self.queueList[SpeedMotor.Queue.value].put(
                            {
                                "Owner": "Camera",
                                "msgID": SpeedMotor.msgID.value,
                                "msgType": SpeedMotor.msgType.value,
                                "msgValue": {"action": "speed", "value": 15.0},
                                # The vehicle must return to normal speed
                            }
                        )
                    case 4: #"One-way":
                        pass
                        # self.queueList["General"].put(
                        #     {
                        #         "Owner": "Camera",
                        #         "msgID": 2,
                        #         "msgType": "String",
                        #         "msgValue": "This is the text2",
                        #         # Signals a one-way road
                        #     }
                        # )
                    case 8: #"roundabout":
                        pass
                        # self.queueList["General"].put(
                        #     {
                        #         "Owner": "Camera",
                        #         "msgID": 2,
                        #         "msgType": "String",
                        #         "msgValue": "This is the text2",
                        #         # Signals a roundabout
                        #     }
                        # )
                    case 3: #"no-entry":
                        pass
                        # self.queueList["General"].put(
                        #     {
                        #         "Owner": "Camera",
                        #         "msgID": 2,
                        #         "msgType": "String",
                        #         "msgValue": "This is the text2",
                        #         # Signals a non-entry road
                        #     }
                        # )
                    case 5: #Parking
                        pass
                        # self.queueList["General"].put(
                        #     {
                        #         "Owner": "Camera",
                        #         "msgID": 2,
                        #         "msgType": "String",
                        #         "msgValue": "This is the text2",
                        #     }
                        # )
            
                self.queuesList[lineInformation.Queue.value].put(
                    {
                        "Owner": lineInformation.Owner.value,
                        "msgID": lineInformation.msgID.value,
                        "msgType": lineInformation.msgType.value,
                        "msgValue": out_line_message,
                    }
                )

                self.queuesList[signInformation.Queue.value].put(
                    {
                        "Owner": signInformation.Owner.value,
                        "msgID": signInformation.msgID.value,
                        "msgType": signInformation.msgType.value,
                        "msgValue": out_sign_message,
                    }
                )

    # =============================== START ===============================================
    def start(self):
        print("Starting thread detection")
        super(threadDetection, self).start()