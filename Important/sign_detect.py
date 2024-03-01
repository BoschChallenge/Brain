# MIT License
# Copyright (c) 2019-2022 JetsonHacks

# Using a CSI camera (such as the Raspberry Pi Version 2) connected to a
# NVIDIA Jetson Nano Developer Kit using OpenCV
# Drivers for the camera and OpenCV are included in the base image

from ultralytics import YOLO
#from ultralytics.models.yolo.detect import DetectionValidator
import cv2

""" 
gstreamer_pipeline returns a GStreamer pipeline for capturing from the CSI camera
Flip the image by setting the flip_method (most common values: 0 and 2)
display_width and display_height determine the size of each camera pane in the window on the screen
Default 1920x1080 displayd in a 1/4 size window
"""

def gstreamer_pipeline(
    sensor_id=0,
    capture_width=1920,
    capture_height=1080,
    display_width=960,
    display_height=540,
    framerate=30,
    flip_method=0,
):
    return (
        "nvarguscamerasrc sensor-id=%d ! "
        "video/x-raw(memory:NVMM), width=(int)%d, height=(int)%d, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            sensor_id,
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )

def sign_detect():
    window_title = "CSI Camera"
    model = YOLO("best.pt")
    # To flip the image, modify the flip_method parameter (0 and 2 are the most common)
    # print(gstreamer_pipeline(flip_method=0))
    video_capture = cv2.VideoCapture(gstreamer_pipeline(), cv2.CAP_GSTREAMER)
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
                results = model(source=frame, show=True, verbose=False, conf=0.5)

                for result in results:
                    detection_count = result.boxes.shape[0]

                    for i in range(detection_count):
                        cls = int(result.boxes.cls[i].item())
                        name = result.names[cls]
                        print("Name: ", name)

                # Break the loop if 'q' key is pressed
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            # if ret_val:
            #    if cv2.getWindowProperty(window_title, cv2.WND_PROP_AUTOSIZE) >= 0:
            #        cv2.imshow(window_title, frame)
            #    cv2.waitKey(10)
        else:
            print("Error: Unable to open camera")
    except Exception as e:
        print(e)
  
    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    sign_detect()
