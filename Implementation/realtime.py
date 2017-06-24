import cv2
import numpy as np
cap = cv2.VideoCapture(1)
def nothing(x):
    pass
# Creating a window for later use
cv2.namedWindow('result')
# Starting with 100's to prevent error while masking
h,s,v = 100,100,100
# Creating track bar
cv2.createTrackbar('h', 'result',0,179,nothing)
cv2.createTrackbar('s', 'result',0,255,nothing)
cv2.createTrackbar('v', 'result',0,255,nothing)
cv2.createTrackbar('q', 'result',0,179,nothing)
cv2.createTrackbar('w', 'result',0,255,nothing)
cv2.createTrackbar('e', 'result',0,255,nothing)
while(1):
    _, frame = cap.read()
    #converting to HSV
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    # get info from track bar and appy to result
    h = cv2.getTrackbarPos('h','result')
    s = cv2.getTrackbarPos('s','result')
    v = cv2.getTrackbarPos('v','result')
    q = cv2.getTrackbarPos('q', 'result')
    w = cv2.getTrackbarPos('w', 'result')
    e = cv2.getTrackbarPos('e', 'result')
    # Normal masking algorithm
    lower_blue = np.array([h,s,v])
    upper_blue = np.array([q,w,e])
    mask = cv2.inRange(hsv,lower_blue, upper_blue)
    result = cv2.bitwise_and(frame,frame,mask = mask)
    cv2.imshow('result',result)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
cap.release()
cv2.destroyAllWindows()