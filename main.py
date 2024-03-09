# Copyright (c) 2019, Bosch Engineering Center Cluj and BFMC orginazers
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
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# ===================================== GENERAL IMPORTS ==================================
import sys

sys.path.append(".")
from multiprocessing import Queue, Event
import logging
import time


# ===================================== PROCESS IMPORTS ==================================
from src.gateway.processGateway import processGateway
from src.hardware.camera.processCamera import processCamera
from src.hardware.serialhandler.processSerialHandler import processSerialHandler
from src.utils.PCcommunicationDemo.processPCcommunication import (
    processPCCommunicationDemo,
)
from src.utils.PCcommunicationDashBoard.processPCcommunication import (
    processPCCommunicationDashBoard,
)
from src.regulation.pid import processPid

from src.utils.messages.allMessages import (
    lineInformation,
    SteerMotor,                
    SignalRunning,
    EngineRun,
    SpeedMotor,
    Record,
    Brake
)

from src.data.CarsAndSemaphores.processCarsAndSemaphores import processCarsAndSemaphores
from src.data.TrafficCommunication.processTrafficCommunication import (
    processTrafficCommunication,
)

# ======================================== SETTING UP ====================================
allProcesses = list()
queueList = {
    "Critical": Queue(),
    "Warning": Queue(),
    "General": Queue(),
    "Config": Queue(),
}

logging = logging.getLogger()

TrafficCommunication = False
Camera = False
PCCommunicationDemo = False
CarsAndSemaphores = False
SerialHandler = True
PID = False
# ===================================== SETUP PROCESSES ==================================

# Initializing gateway
processGateway = processGateway(queueList, logging, debugging=False)
allProcesses.append(processGateway)

# Initializing camera
if Camera:
    processCamera = processCamera(queueList, logging)
    allProcesses.append(processCamera)

# Initializing interface
if PCCommunicationDemo:
    processPCCommunication = processPCCommunicationDemo(queueList, logging)
    allProcesses.append(processPCCommunication)
else:
    processPCCommunicationDashBoard = processPCCommunicationDashBoard(
        queueList, logging
    )
    allProcesses.append(processPCCommunicationDashBoard)

# Initializing cars&sems
if CarsAndSemaphores:
    processCarsAndSemaphores = processCarsAndSemaphores(queueList)
    allProcesses.append(processCarsAndSemaphores)

# Initializing GPS
if TrafficCommunication:
    processTrafficCommunication = processTrafficCommunication(queueList, logging, 3)
    allProcesses.append(processTrafficCommunication)

# Initializing serial connection NUCLEO - > PI
if SerialHandler:
    processSerialHandler = processSerialHandler(queueList, logging, example=False)
    allProcesses.append(processSerialHandler)
    
# Initializing camera
if PID:
    processPid = processPid(queueList, logging)
    allProcesses.append(processPid)

# ===================================== START PROCESSES ==================================
for process in allProcesses:
    process.daemon = True
    process.start()


# time.sleep(2)

# queueList[EngineRun.Queue.value].put(
#     {
#         "Owner": EngineRun.Owner.value,
#         "msgID": EngineRun.msgID.value,
#         "msgType": EngineRun.msgType.value,
#         "msgValue": True 
#     }
# )

# queueList[SpeedMotor.Queue.value].put(
#     {
#         "Owner": SpeedMotor.Owner.value,
#         "msgID": SpeedMotor.msgID.value,
#         "msgType": SpeedMotor.msgType.value,
#         "msgValue": 7.0
#     }
# )

# queueList[SteerMotor.Queue.value].put(
#     {
#         "Owner": SteerMotor.Owner.value,
#         "msgID": SteerMotor.msgID.value,
#         "msgType": SteerMotor.msgType.value,
#         "msgValue": 0.0
#     }
# )

                 
# time.sleep(10)

# queueList[Brake.Queue.value].put(
#     {
#         "Owner": Brake.Owner.value,
#         "msgID": Brake.msgID.value,
#         "msgType": Brake.msgType.value,
#         "msgValue": 0.0
#     }
# )
                 
 

# queueList[Record.Queue.value].put(
#     {
#         "Owner": Record.Owner.value,
#         "msgID": Record.msgID.value,
#         "msgType": Record.msgType.value,
#         "msgValue":True
#     }
# )

# out_line_message = {
#         "length"      : 10,
#         "angle" : 1.57,
#         "right_line"   : True
# }

# queueList[lineInformation.Queue.value].put(
#     {
#         "Owner": lineInformation.Owner.value,
#         "msgID": lineInformation.msgID.value,
#         "msgType": lineInformation.msgType.value,
#         "msgValue": out_line_message,
#     }
# )

# time.sleep(10)

# out_line_message = {
#         "length"      : 400,
#         "angle" : 1,
#         "right_line"   : True
# }

# queueList[lineInformation.Queue.value].put(
#     {
#         "Owner": lineInformation.Owner.value,
#         "msgID": lineInformation.msgID.value,
#         "msgType": lineInformation.msgType.value,
#         "msgValue": out_line_message,
#     }
# )

# for i in range(10):
# queueList[EngineRun.Queue.value].put(
#         {
#             "Owner": EngineRun.Owner.value,
#             "msgID": EngineRun.msgID.value,
#             "msgType": EngineRun.msgType.value,
#             # "msgValue": "Type": "action": "2", "value": 12.0,
#             "msgValue": True #{
#             #     "action":"Run",
#             #     "value" : True
#             # }
#         }
#     )

# queueList[SteerMotor.Queue.value].put(
#         {
#             "Owner": SteerMotor.Owner.value,
#             "msgID": SteerMotor.msgID.value,
#             "msgType": SteerMotor.msgType.value,
#             # "msgValue": "Type": "action": "2", "value": 12.0,
#             "msgValue": 15.0 #{
#             #     "action":"steer", 
#             #     "value": 15.0
#             # }
#         }
#     )

# queueList[SpeedMotor.Queue.value].put(
#         {
#             "Owner": SpeedMotor.Owner.value,
#             "msgID": SpeedMotor.msgID.value,
#             "msgType": SpeedMotor.msgType.value,
#             # "msgValue": "Type": "action": "2", "value": 12.0,
#             "msgValue": 20.0 #{
#             #     "action":"steer", 
#             #     "value": 15.0
#             # }
#         }
#     )


#print("Msgs sent!")

# ===================================== STAYING ALIVE ====================================
blocker = Event()
try:
    blocker.wait()
except KeyboardInterrupt:
    print("\nCatching a KeyboardInterruption exception! Shutdown all processes.\n")
    for proc in allProcesses:
        print("Process stopped", proc)
        proc.stop()
        proc.join()
