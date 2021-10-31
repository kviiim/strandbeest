import cv2
import matplotlib.pyplot as plt
import numpy as np
import serial
import serial.tools.list_ports as list_ports
import time
from graphing import *

vid = cv2.VideoCapture(0)

#224, 191, 105
#173, 143, 61
light_boundary = (170, 140, 60)
dark_boundary = (255, 200, 110)

class Serial_cmd:
    Arduino_IDs = ((0x2341, 0x0043), (0x2341, 0x0001), 
                   (0x2A03, 0x0043), (0x2341, 0x0243), 
                   (0x0403, 0x6001), (0x1A86, 0x7523))
    
    def __init__(self, port=''):
        if port == '':
            self.dev = None
            self.connected = False
            devices = list_ports.comports()
            for device in devices:
                if (device.vid, device.pid) in Serial_cmd.Arduino_IDs:
                    try:
                        self.dev = serial.Serial(device.device, 115200)
                        self.connected = True
                        print('Connected to {!s}...'.format(device.device))
                    except:
                        pass
                if self.connected:
                    break
        else:
            try:
                self.dev = serial.Serial(port, 115200)
                self.connected = True
            except:
                self.edev = None
                self.connected = False
    def write_data_to_arduino(self, string_to_write):
        if self.connected:
            self.write_data(string_to_write)
Obj = Serial_cmd()
              
while(True):
    #get frame
    ret, frame = vid.read()

    mask = cv2.inRange(frame, light_boundary, dark_boundary)

    # detect the contours on the binary image using cv2.CHAIN_APPROX_NONE
    contours, hierarchy = cv2.findContours(image=mask, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
    print(hierarchy)                    
    result = frame.copy()

    if len(contours) > 0:
        c = max(contours, key = cv2.contourArea)

        x,y,w,h = cv2.boundingRect(c)

        center_x = x + (w/2)
        offset_x = -1*((frame.width/2) - center_x)
        offset_string = 's' + str(offset_x)
        Obj.write_data(offset_string)

        # draw the biggest contour (c) in green
        cv2.rectangle(result,(x,y),(x+w,y+h),(0,255,0),2)         
  
    cv2.imshow('frame', result)
    #q to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
  
vid.release()
cv2.destroyAllWindows()