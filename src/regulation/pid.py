if __name__ == "__main__":
    import sys
    print(sys.path)
    sys.path.insert(0, "../..")

from src.hardware.serialhandler.processSerialHandler import processSerialHandler
from src.templates.workerprocess import WorkerProcess
from src.regulation.threads.threadPid import threadPid
from src.utils.messages.allMessages import lineInformation


from multiprocessing import Queue, Pipe
import logging
import time

class processPid(WorkerProcess):

    def __init__(self, queueList, logging, debugging=False):
        self.queuesList = queueList
        self.logging = logging
        pipeRecv, pipeSend = Pipe(duplex=False)
        self.pipeRecv = pipeRecv
        self.pipeSend = pipeSend
        self.debugging = debugging
        super(processPid, self).__init__(self.queuesList)
        
    def stop(self):
        """Function for stopping threads and the process."""
        for thread in self.threads:
            thread.stop()
            thread.join()
        super(processPid, self).stop()

    # ===================================== RUN ==========================================
    def run(self):
        """Apply the initializing methods and start the threads."""
        super(processPid, self).run()

    # ===================================== INIT TH ======================================
    def _init_threads(self):
        """Create the Camera Publisher thread and add to the list of threads."""
        pidTh = threadPid(
            self.pipeRecv, self.pipeSend, self.queuesList, self.logging, self.debugging
        )
        self.threads.append(pidTh)


if __name__ == "__main__":
    
    from multiprocessing import Queue, Event
    import time
    import logging
    import cv2
    import base64
    import numpy as np

    allProcesses = list()

    debugg = True

    queueList = {
        "Critical": Queue(),
        "Warning": Queue(),
        "General": Queue(),
        "Config": Queue(),
    }

    logger = logging.getLogger()

    process = processPid(queueList, logger, debugg)

    process.daemon = True

    time.sleep(4)

    try:
        process.start()
        time.sleep(5)
        out_line_message = {
            "length"      : 10,
            "angle" : 1.57,
            "right_line"   : True
        }

    
        queueList[lineInformation.Queue.value].put(
            {
                "Owner": lineInformation.Owner.value,
                "msgID": lineInformation.msgID.value,
                "msgType": lineInformation.msgType.value,
                "msgValue": out_line_message,
            }
        )
        
        print("message sent")
        
        while True:
            
            pass
            # if debugg:
            #     logger.warning("getting")
            # img = {"msgValue": 1}
            # while type(img["msgValue"]) != type(":text"):
            #     img = queueList["General"].get()
            # image_data = base64.b64decode(img["msgValue"])
            # img = np.frombuffer(image_data, dtype=np.uint8)
            # image = cv2.imdecode(img, cv2.IMREAD_COLOR)
            # if debugg:
            #     logger.warning("got")
            # cv2.imshow("frame", image)
            # cv2.waitKey(1)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(e)

    process.stop()


    

    
        

    

        
