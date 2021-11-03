import cv2
import matplotlib.pyplot as plt
import numpy as np
import time
from serialWrite import Serial_cmd

vid = cv2.VideoCapture(0)
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
cv2.startWindowThread()

Obj = Serial_cmd()
time.sleep(2)
print('serial connected?')

if not vid.isOpened() or vid == None:
    raise IOError("Cannot open webcam")

while(True):
    #get frame
    ret, frame = vid.read()
    # frame = cv2.imread("InitialVisionTest\\test_img.jpg")

    frame_resized = cv2.resize(frame, (640, 480))
    # using a greyscale picture, also for faster detection
    gray = cv2.cvtColor(frame_resized, cv2.COLOR_RGB2GRAY)

    # detect people in the image
    # returns the bounding boxes for the detected objects
    boxes, weights = hog.detectMultiScale(frame_resized, winStride=(8,8) )

    #find the largest box
    max_box = np.array([])
    for box in boxes:
        if len(max_box) == 0 or box[2] * box[3] > max_box[2]*max_box[3]:
            max_box = box
    
    #if there is a largest box
    if len(max_box) != 0:
        max_box_center_x = max_box[0] + (max_box[2]/2)
        offset_x = ((frame.shape[1]/2) - (max_box_center_x))
        offset_string = 'e' + str(offset_x)
        # print(offset_string)
        Obj.write_data_to_arduino(offset_string)

        max_box = [max_box[0], max_box[1], max_box[0] + max_box[2], max_box[1] + max_box[3]]
        xA, yA, xB, yB = max_box
        # display the detected largest box in the colour picture
        cv2.rectangle(frame_resized, (xA, yA), (xB, yB),
                            (0, 255, 0), 2)
           
    cv2.imshow('frame', frame_resized)
    #q to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
  
vid.release()
cv2.destroyAllWindows()