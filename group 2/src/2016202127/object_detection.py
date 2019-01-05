# -*- coding: utf-8 -*-
"""
Created on Thu Dec 27 12:45:42 2018

@author: 啊花花
"""

import numpy as np
#import argparse
import cv2
import time
import schedule
import serial
from PIL import ImageGrab


def screen():
    im = ImageGrab.grab((20,120,620,560))#截图
    #im.show()
    img = im.rotate(-90)
    #img = cv2.flip(im,90)
    #img.show()
    img.save('D:\Image\image4/'+str(c)+'.jpg','JPEG')#图片存储
    
def Rotate(self,beta):               #旋转
        #beta>0表示逆时针旋转；beta<0表示顺时针旋转
        self.transform=np.array([[math.cos(beta),-math.sin(beta),0],
                                 [math.sin(beta), math.cos(beta),0],
                                 [    0,              0,         1]])


def object_detection(Imagepath, prototxt,model,confidence):
    
    CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
	"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
	"dog", "horse", "motorbike", "person", "pottedplant", "sheep",
	"sofa", "train", "tvmonitor"]
    COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))
    net = cv2.dnn.readNetFromCaffe(prototxt,model)
    
    image = cv2.imread(Imagepath)
    #rows = im.shape[0]
   # cols = im.shape[1]
    (h,w) = image.shape[:2]
    #img=Img(im,rows,cols,[248,231])
    #img.Rotate(-math.radians(90))
    
    
    blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 0.007843, (300, 300), 127.5)
    #blob = cv2.
    net.setInput(blob)
    detections = net.forward()
    
    for i in np.arange(0, detections.shape[2]):
        conf = detections[0,0,i,2]
        
        if conf > confidence:
            idx = int(detections[0,0,i,1])
            box = detections[0,0,i,3:7] * np.array([w,h,w,h])
            (startX,startY,endX,endY) = box.astype("int")
            print(idx,box)
            if idx == 15:
                if startY < h / 2 and endY > h / 2:
                    print("person")
                    return 'b'
            if idx == 5:
                if startY < h / 2 and endY > h / 2:
                    print("bottle")
                    return 'a'
            label = "{}: {:.2f}%".format(CLASSES[idx], conf * 100)
            cv2.rectangle(image, (startX, startY), (endX, endY),
			COLORS[idx], 2)
            y = startY - 15 if startY - 15 > 15 else startY + 15
            cv2.putText(image, label, (startX, y),
			cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)
        
    #cv2.imshow("Output", image)
    cv2.waitKey(0)
    return 'b';
            
if __name__ == '__main__':
    ser = serial.Serial("COM5", 9600, timeout=0.5)
    print (ser.name)
    print (ser.port)
    c = 0
    schedule.every(1).seconds.do(screen)
    while True:
    #c = input()
    #print(c)
        schedule.run_pending()
        d = object_detection('D:\Image\image4/'+str(c)+'.jpg',"MobileNetSSD_deploy.prototxt.txt","MobileNetSSD_deploy.caffemodel",0.5)
        ser.write(d.encode())
        ser.readline()
        c += 1
        if c>4:
            d = 0
            ser.write(d.encode())
            ser.readline()
            break   
        time.sleep(0.5)

