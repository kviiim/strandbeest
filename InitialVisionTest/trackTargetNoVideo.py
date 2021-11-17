import cv2
import matplotlib.pyplot as plt
import numpy as np
import serial
import serial.tools.list_ports as list_ports
import time
from serialWrite import Serial_cmd


vid = cv2.VideoCapture(-1)

#224, 191, 105
#173, 143, 61
light_boundary = (170, 140, 60)
dark_boundary = (255, 200, 110)

ser = Serial_cmd()
time.sleep(2)
print('serial connected?')
              
while(True):
    #get frame
    ret, frame = vid.read()

    mask = cv2.inRange(frame, light_boundary, dark_boundary)

    # detect the contours on the binary image using cv2.CHAIN_APPROX_NONE
    contours, hierarchy = cv2.findContours(image=mask, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
    result = frame.copy()

    if len(contours) > 0:
        c = max(contours, key = cv2.contourArea)

        x,y,w,h = cv2.boundingRect(c)

        center_x = x + (w/2)
        offset_x = ((mask.shape[1]/2) - center_x)
        offset_string = 'e' + str(offset_x) + '\n'
        print(offset_string)
        ser.write_data_to_arduino(offset_string)
        # draw the biggest contour (c) in green
        cv2.rectangle(result,(x,y),(x+w,y+h),(0,255,0),2)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
  
vid.release()
cv2.destroyAllWindows()