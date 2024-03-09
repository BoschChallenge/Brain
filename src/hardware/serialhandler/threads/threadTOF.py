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
import binascii
import serial

from multiprocessing import Pipe
from src.utils.messages.allMessages import (
    EngineRun,
    SpeedMotor,
    Brake
)
from src.templates.threadwithstop import ThreadWithStop
import time
from src.hardware.serialhandler.threads.threadWrite import Speeds

class threadTOF(ThreadWithStop):
    """Thread which will handle camera functionalities.\n
    Args:
        pipeRecv (multiprocessing.queues.Pipe): A pipe where we can receive configs for camera. We will read from this pipe.
        pipeSend (multiprocessing.queues.Pipe): A pipe where we can write configs for camera. Process Gateway will write on this pipe.
        queuesList (dictionar of multiprocessing.queues.Queue): Dictionar of queues where the ID is the type of messages.
        logger (logging object): Made for debugging.
        debugger (bool): A flag for debugging.
    """

    # ================================ INIT ===============================================
    def __init__(self, port, queuesList):
        self.queuesList = queuesList

        self.slow_distance = 500 # mm
        self.stop_distance = 300 # mm
        self.detected = [0, 0, 0]
        
        self.serial_handler = serial.Serial(port, baudrate=115200)
        if self.serial_handler.isOpen():
            print("Serial connection opened successfully")
        else:
            print("Failed to open serial connection")

        super(threadTOF, self).__init__()

    # =============================== STOP ================================================
    def stop(self):
        print("STOPING TOF")
        print("STOPING TOF")

        print("STOPING TOF")

        print("STOPING TOF")

        print("STOPING TOF")

        print("STOPING TOF")

        # if self.serial_handler.isOpen():
        #     self.serial_handler.close()
        #     print("Serial connection closed")

        super(threadTOF, self).stop()

    def cl(self, a):
        dat1 = a[0:1]

        if dat1 == 'a':
            dat1 = 10
        elif dat1 == 'b':
            dat1 = 11
        elif dat1 == 'c':
            dat1 = 12
        elif dat1 == 'd':
            dat1 = 13
        elif dat1 == 'e':
            dat1 = 14
        elif dat1 == 'f':
            dat1 = 15
            
        return dat1

    # ================================ RUN ================================================
    def run(self):
        while self._running:
            if self.serial_handler.inWaiting(): 
                num = self.serial_handler.inWaiting()
                try:   
                    data = str(binascii.b2a_hex(self.serial_handler.read(num)))
                    print("Received data: ", data)

                    if len(data) > 8:
                        dat1 = data[6:7]
                        dat2 = data[7:8]
                        dat3 = data[8:9]
                        dat4 = data[9:10]
                        jl = (((int(self.cl(dat1)) * 16) + int(self.cl(dat2))) * 256) + ((int(self.cl(dat3)) * 16) + int(self.cl(dat4)))
                        

                        if jl <= self.slow_distance:
                            print("SLOWING DOWN")
                            self.set_desired_speed(Speeds.SLOW.value)
                            self.detected.pop(0)
                            self.detected.insert(0, 1)
                        elif jl <= self.stop_distance:
                            print("STOPPING")
                            self.set_brake()
                            self.detected.pop(0)
                            self.detected.insert(0, 1)
                        else:
                            self.detected.pop(0)
                            self.detected.insert(0, 0)

                        if sum(self.detected) == 0:
                            self.set_desired_speed(Speeds.NORMAL.value)

                except Exception as e:
                    print("Error reading data:", e)

            time.sleep(0.1)

    def set_brake(self):
        self.queuesList[Brake.Queue.value].put(
            {
                "Owner": Brake.Owner.value,
                "msgID": Brake.msgID.value,
                "msgType": Brake.msgType.value,
                "msgValue": True
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
        super(threadTOF, self).start()

