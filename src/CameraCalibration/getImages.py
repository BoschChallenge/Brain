<<<<<<< HEAD
import cv2
from picamera2 import Picamera2


camera = Picamera2()

config = camera.create_preview_configuration(
    buffer_count=1,
    queue=False,
    main={"format": "XBGR8888", "size": (280, 160)}, #(2048, 1080)},
    lores={"size": (280, 160)},
    encode="lores",
)
camera.configure(config)
camera.start()


num = 0

while True:

    img = camera.capture_array("main") 

    #succes, img = camera.read()
    img = cv2.flip(img, 1)

    k = cv2.waitKey(1)

    if k == 27:
        break
    elif k == ord('s'): # wait for 's' key to save and exit
        cv2.imwrite('/home/hugo/brain/src/CameraCalibration/images/img' + str(num) + '.png', img)
        print("image saved!")
        num += 1

    cv2.imshow('Img',img)

# Release and destroy all windows before termination
camera.release()

=======
import cv2
from picamera2 import Picamera2


camera = Picamera2()

config = camera.create_preview_configuration(
    buffer_count=1,
    queue=False,
    main={"format": "XBGR8888", "size": (280, 160)}, #(2048, 1080)},
    lores={"size": (280, 160)},
    encode="lores",
)
camera.configure(config)
camera.start()


num = 0

while True:

    img = camera.capture_array("main") 

    #succes, img = camera.read()
    img = cv2.flip(img, 1)

    k = cv2.waitKey(1)

    if k == 27:
        break
    elif k == ord('s'): # wait for 's' key to save and exit
        cv2.imwrite('/home/hugo/brain/src/CameraCalibration/images/img' + str(num) + '.png', img)
        print("image saved!")
        num += 1

    cv2.imshow('Img',img)

# Release and destroy all windows before termination
camera.release()

>>>>>>> d9215ae9894be337320fa1b49a08f05bd527d91d
cv2.destroyAllWindows()