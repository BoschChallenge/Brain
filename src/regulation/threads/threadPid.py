# Copyright (c) 2019, Bosch Engineering Center Cluj and BFMC organizers
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:

# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.

# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.

# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE
import threading

from multiprocessing import Pipe
from src.utils.messages.allMessages import (
    EngineRun,
    SpeedMotor,
    SteerMotor,
    lineInformation,
    Brake,
    Config,
)
from src.templates.threadwithstop import ThreadWithStop
import time
<<<<<<< HEAD
from src.hardware.serialhandler.threads.threadWrite import Speeds
=======
>>>>>>> d9215ae9894be337320fa1b49a08f05bd527d91d


class threadPid(ThreadWithStop):
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
        super(threadPid, self).__init__()
        self.queuesList = queuesList
        self.logger = logger
        self.pipeRecvConfig = pipeRecv
        self.pipeSendConfig = pipeSend
        self.debugger = debugger
        pipeRecvLine, pipeSendLine = Pipe(duplex=False)
        self.pipeRecvLine = pipeRecvLine
        self.pipeSendLine = pipeSendLine
        self.subscribe()
        #self.Queue_Sending()
        self.Configs()
        
        self.DESIRED_DISTANCE = 50
        self.MAX_PID = 20
        self.Kp = 0.5

    def subscribe(self):
        """Subscribe function. In this function we make all the required subscribe to process gateway"""
        self.queuesList["Config"].put(
            {
                "Subscribe/Unsubscribe": "subscribe",
                "Owner": lineInformation.Owner.value,
                "msgID": lineInformation.msgID.value,
                "To": {"receiver": "threadPid", "pipe": self.pipeSendLine},
            }
        )
        # self.queuesList["Config"].put(
        #     {
        #         "Subscribe/Unsubscribe": "subscribe",
        #         "Owner": Config.Owner.value,
        #         "msgID": Config.msgID.value,
        #         "To": {"receiver": "threadCamera", "pipe": self.pipeSendConfig},
        #     }
        # )

    # def Queue_Sending(self):
    #     """Callback function for recording flag."""
    #     self.queueList[EngineRun.Queue.value].put(
    #             {
    #                 "Owner": EngineRun.Owner.value,
    #                 "msgID": EngineRun.msgID.value,
    #                 "msgType": EngineRun.msgType.value,
    #                 "msgValue": True 
    #             }
    #         )

    #     self.queueList[SteerMotor.Queue.value].put(
    #             {
    #                 "Owner": SteerMotor.Owner.value,
    #                 "msgID": SteerMotor.msgID.value,
    #                 "msgType": SteerMotor.msgType.value,
    #                 "msgValue": 15.0 #{
    #             }
    #         )

    #     self.queueList[SpeedMotor.Queue.value].put(
    #             {
    #                 "Owner": SpeedMotor.Owner.value,
    #                 "msgID": SpeedMotor.msgID.value,
    #                 "msgType": SpeedMotor.msgType.value,
    #                 # "msgValue": "Type": "action": "2", "value": 12.0,
    #                 "msgValue": 20.0 #{
    #                 #     "action":"steer", 
    #                 #     "value": 15.0
    #                 # }
    #             }
    #         )
 
    #     # TODO rate
    #     threading.Timer(1, self.Queue_Sending).start()

    # =============================== STOP ================================================
    def stop(self):
        super(threadPid, self).stop()

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
        while self._running:
            if self.pipeRecvLine.poll():
                print("Thread Pid")
                message = self.pipeRecvLine.recv()
                message = message["value"]
                
                actual_distance = message["length"]
                actual_angle = message["angle"]
                actual_line = message["right_line"]
 
                error = self.DESIRED_DISTANCE - actual_distance

                print(f"actual_distance: {actual_distance}, error: {error}")

                pid = self.Kp * error 

                if pid >= self.MAX_PID:
                    pid = self.MAX_PID

                elif pid <= -self.MAX_PID:
                    pid = -self.MAX_PID
                
                print(f"Steering angle: {-pid}")
                
                if first:
                    self.queuesList[EngineRun.Queue.value].put(
                    {
                        "Owner": EngineRun.Owner.value,
                        "msgID": EngineRun.msgID.value,
                        "msgType": EngineRun.msgType.value,
                        "msgValue": True 
                    }
                    )
<<<<<<< HEAD
                    self.set_desired_speed(Speeds.NORMAL.value)
                    first = False
                
                self.set_desired_angle(pid)
                
            time.sleep(0.02)
                #print(f"Time PID: {time.time()}")
=======
                    self.set_desired_speed(7.0)
                    first = False
                
                self.set_desired_angle(-pid)
                time.sleep(0.2)
>>>>>>> d9215ae9894be337320fa1b49a08f05bd527d91d


    def set_brake(self):
        self.queuesList[Brake.Queue.value].put(
            {
                "Owner": Brake.Owner.value,
                "msgID": Brake.msgID.value,
                "msgType": Brake.msgType.value,
                "msgValue": 0.0
            }
        )
                 
    def set_desired_angle(self, angle):
        
        self.queuesList[SteerMotor.Queue.value].put(
            {
                "Owner": SteerMotor.Owner.value,
                "msgID": SteerMotor.msgID.value,
                "msgType": SteerMotor.msgType.value,
                "msgValue": angle
            }
        )


    def set_desired_speed(self, speed):
        self.queuesList[SpeedMotor.Queue.value].put(
            {
                "Owner": SpeedMotor.Owner.value,
                "msgID": SpeedMotor.msgID.value,
                "msgType": SpeedMotor.msgType.value,
                "msgValue": speed 
            }
        )
    # =============================== START ===============================================
    def start(self):
        super(threadPid, self).start()

