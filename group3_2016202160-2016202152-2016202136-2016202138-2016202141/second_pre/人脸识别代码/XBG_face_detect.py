import cv2
import imutils
import serial.tools.list_ports


plist = list(serial.tools.list_ports.comports())
ser = serial.Serial('COM4', 9600)

writer = None
vs = cv2.VideoCapture(0)
# vs.open('http://172.20.10.8:8080/video')
cascPath = "haarcascade_frontalface_default.xml"

while True:
    ret, frame = vs.read()
    if not ret:
        break

    # Create the haar cascade 人脸特征识别
    frame = imutils.resize(frame, width=750)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faceCascade = cv2.CascadeClassifier(cascPath)

    # Detect faces in the image
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=10,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    if len(faces):
        for (left, top, width, height) in faces:
            cv2.rectangle(frame, (left, top), (left+width, height+top), (0, 255, 0), 2)
            print(left, top, width, height)
            '''if left > 480:    # turn left
                ser.write('l'.encode())
            elif left < 230:    # turn right
                ser.write('r'.encode())
            else:   # keep going
                ser.write('f'.encode())'''
            ser.write('f'.encode())
    else:
        ser.write('s'.encode())

    cv2.imshow('monitor', frame)

    # waitKey()不断刷新图像，频率时间为delay，单位为ms。
    key = cv2.waitKey(2000) & 0xFF
    if key == 27:
        break

ser.write('s'.encode())
cv2.destroyAllWindows()
