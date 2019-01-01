import numpy as np
import cv2
import matplotlib.pyplot as plt
 
# cap = cv2.VideoCapture(0)

# cap = cv2.VideoCapture('http://10.48.187.76:8888/mjpegfeed')
cap = cv2.VideoCapture('http://192.168.3.11:8888/mjpegfeed')
 
while(True):
	# read every frame
    ret, frame = cap.read()
    if False == ret:
       break
    # resize
    frame = cv2.resize(frame, (500, 500))
    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
	
cap.release()
cv2.destroyAllWindows()