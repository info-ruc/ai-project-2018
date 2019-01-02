# AI-Car
An AI-Car based on deep learning and Arduino
# Project 1 - Random Walker

[AI-Car/Project1](https://github.com/jaingmengmeng/AI-Car/tree/master/Project1)

# Project 2 - Sensored Walker

[AI-Car/Project2](https://github.com/jaingmengmeng/AI-Car/tree/master/Project2)

# Project 3 - DeepAI Walker

<p align="center">
    <img src="Media\video\第三次展示视频定稿.gif" alter="第三次展示视频gif">
</p>


## 1. Communication between PC and AI-Car

### (i) Get video stream from phone's camera

**Mobile end**: Install an APP called `DroidCam X Pro`

<p align="center">
    <img src="Media\imgs\Droidcam.jpg" alter="Droidcam" height="400px">
</p>

**PC end**: Get video stream by accessing the server port OR get video stream with `Opencv` library.

<p align="center">
    <img src="Media\imgs\client.png" alter="Client" height="400px">
</p>

```python
import numpy as np
import cv2
import matplotlib.pyplot as plt
 
# cap = cv2.VideoCapture(0)
# 监听PC端的的默认摄像头

# cap = cv2.VideoCapture('http://10.48.187.76:8888/mjpegfeed')
cap = cv2.VideoCapture('http://192.168.3.11:8888/mjpegfeed')
# 监听服务端IP地址和端口号
 
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
```



## 2. Traffic sign detection and identification
## 3. Chinese speech recognition
## 4. Isolated word Chinese speech recognition

# Developer

- <strong>Jiang Liuyang</strong>  
- Long Yanbing  
- Cao Chen  
- Deng Chao

# References

[Recognising Traffic Signs With 98% Accuracy Using Deep Learning](https://towardsdatascience.com/recognizing-traffic-signs-with-over-98-accuracy-using-deep-learning-86737aedc2ab?spm=a2c4e.11153940.blogcont195729.23.79379e37wkqkeC)