import cv2
import numpy as np
import time
from ControlDrone import ControlDrone
from ControlDroneSim import ControlDroneSim
import cflib
from matplotlib import pyplot as plt
import time,random
from cflib.crazyflie import Crazyflie
import time
from collections import deque
start = time.time()
cam = cv2.VideoCapture(1)
cam.set(cv2.cv.CV_CAP_PROP_FPS, 120)
kernel = np.ones((5,5),np.uint8)
DistanzaConosciuta = 230
DimensioneConosciuta = 10
focalLength = 0
primo = 0
distance = 0
inizio = 0;
max_angle = 100
# Initialize the low-level drivers (don't list the debug drivers)
cflib.crtp.init_drivers(enable_debug_driver=False)
# Scan for Crazyflies and use the first one found
print('Scanning interfaces for Crazyflies...')
available = cflib.crtp.scan_interfaces()
print('Crazyflies found:')
for i in available:
    print(i[0])
if len(available) > 0:
    controlDrone = ControlDrone(available[0][0])
    controlDrone._inizialize_drone()
    while True:
            inizio = inizio + 1
            ret,frame=cam.read()
            rangomin = np.array([68, 147, 215], dtype=np.uint8)
            rangomax = np.array([179,255,255], dtype=np.uint8)
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            mascara = cv2.inRange(hsv,rangomin,rangomax)
            res = cv2.bitwise_and(frame,frame, mask = mascara)
            opening = cv2.morphologyEx(mascara,cv2.MORPH_OPEN,kernel)
            contours, hierarchy = cv2.findContours(opening.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            if len(contours) > 0 :
                cnt = contours[0]
                x,y,w,h=cv2.boundingRect(cnt)
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
                cv2.circle(frame,(int(x+w/2),int(y+h/2)),5,(0,0,255),-1)
                lato = h
                if lato != 0 :
                    if primo < 20:
                        primo += 1
                        focalLength = (lato * DistanzaConosciuta / DimensioneConosciuta)
                    distance = (DimensioneConosciuta * focalLength) / lato
                font = cv2.FONT_HERSHEY_SIMPLEX
                distance = distance / 10
                distance = round(distance, 3)
                cv2.putText(frame, str(distance)+"cm"+str(x+w/2)+"x"+str(y+h/2)+"y", (int(x+w/2),int(y+h/2)), font, 1, (255, 255, 255), 2)
                roll, pitch=controlDrone._control_drone(x+w/2,y+h/2)
            else:
                #print("fuori visione")
                #drone vero
                controlDrone._cut_motor()
            cv2.imshow('camera',frame)
            #cv2.imshow('mask', mascara)
            k=cv2.waitKey(1) & 0xFF
            if k== ord("q"):
                controlDrone._cut_motor()
                break


