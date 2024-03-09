if __name__ == "__main__":
    import sys

    sys.path.insert(0, "../..")

import torch
import pathlib
import cv2
import logging
#from src.detection.model_needed.Distance import SignDistance
path = 'src/detection/yolov5'
model_path = 'src/detection/model_needed/best.pt'
model = torch.hub.load(path, 'custom', path=model_path,source='local')  # local model

#Class for calculating sign distance
#signDistance = SignDistance()

logging.getLogger("utils.general").setLevel(logging.WARNING)

class SignDetect:
    def __init__(self) -> None:
        pass
    # Inference
    def sign_detect(self, frame):
        window_title = "CSI Camera"
        # To flip the image, modify the flip_method parameter (0 and 2 are the most common)
        # print(gstreamer_pipeline(flip_method=0))        
        try:
            #cv2.imshow(window_title, frame)
            #cv2.waitKey(1)
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
                #distance = signDistance.calculate_distance(width)
                #print(f"Distance: {distance}\n")

            return sign_class, confidence, 0 #distance
        except Exception as e:
            print(e)

        return 0, 0, 0
