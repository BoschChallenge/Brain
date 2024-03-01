from ultralytics import YOLO
from ultralytics.models.yolo.detect import DetectionValidator
import cv2
import numpy
from Distance import SignDistance

model = YOLO("best.pt")
SD = SignDistance()

cap = cv2.VideoCapture("full_hd14.264")
i = 0
try:
    while True:
        # Read a frame from the camera
        ret, frame = cap.read()

        if not ret:
            print("Error reading frame")
            break

        # Run the prediction on the frame
        results = model(source=frame,show=False, verbose=False, conf=0.5)

        for result in results:
            detection_count = result.boxes.shape[0]
            for i in range(detection_count):
                cls = int(result.boxes.cls[i].item())
                name = result.names[cls]
                
                print("\nName: ", name)
                array = (result.boxes.xywh.numpy()).reshape(4)
                distance = SD.calculate_distance(array[2])
                print("Distance:",distance)

        # Break the loop if 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    # Release the video capture object and close the OpenCV windows
    cap.release()
    cv2.destroyAllWindows()