import torch
import pathlib
import cv2
import logging
from Distance import SignDistance
temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath

#C:\Users\milos\Documents\BoschChallenge\Modelv5\yolov5
model = torch.hub.load('yolov5', 'custom', path='best.pt',source='local')  # local model

pathlib.PosixPath = temp

#Class for calculating sign distance
signDistance = SignDistance()

#model = torch.hub.load('yolov5\\.','custom',path = 'C:\\Users\\milos\\Documents\\BoschChallenge\\Modelv5\\best.pt',source='local', force_reload=True)

logging.getLogger("utils.general").setLevel(logging.WARNING)

class SignDetect:
    def __init__(self) -> None:
        pass
    # Inference
    def sign_detect(self):
        window_title = "CSI Camera"
        # To flip the image, modify the flip_method parameter (0 and 2 are the most common)
        # print(gstreamer_pipeline(flip_method=0))
        video_capture = cv2.VideoCapture(0)#gstreamer_pipeline(), cv2.CAP_GSTREAMER)
        video_capture.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        
        try:
            if video_capture.isOpened():
                window_handle = cv2.namedWindow(window_title, cv2.WINDOW_AUTOSIZE)
                while True:
                    ret, frame = video_capture.read()

                    if not ret:
                        print("Error reading frame")
                        break

                    cv2.imshow(window_title, frame)
                    results = model(frame)
                    prediction = results.pandas().xyxy[0].values
                    prediction_wh = results.pandas().xywh[0].values
                    for value in prediction:
                        box = value[:4]
                        confidence = value[4]
                        sign_class = value[5]
                        sign_name = value[6]
                        print(f"Box: {box}\nConfidence: {confidence}\nClass: {sign_class}\nName: {sign_name}")
                    for value in prediction_wh:
                        width = value[2]
                        height = value[3]
                        distance = signDistance.calculate_distance(width)
                        print(f"Width: {width}\nHeight: {height}\n")
                        print(f"Distance: {distance}\n")

                    # Break the loop if 'q' key is pressed
                    if cv2.waitKey(10) & 0xFF == ord('q'):
                        break
            else:
                print("Error: Unable to open camera")
        except Exception as e:
            print(e)
    
        video_capture.release()
        cv2.destroyAllWindows()

#Class for sign detection
signDetection = SignDetect()

if __name__ == "__main__":
    signDetection.sign_detect()