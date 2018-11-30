import face_recognition
import pickle
import cv2
import imutils
import serial.tools.list_ports


plist = list(serial.tools.list_ports.comports())
ser = serial.Serial('COM4', 9600)

print("[INFO] loading encodings...")
data = pickle.loads(open('encodings.pickle', "rb").read())

vs = cv2.VideoCapture(0)
# vs.open('http://[2401:ec00:9:4f92:de55:83ff:fe2b:e185]:8080/video')

while True:
    ret, frame = vs.read()
    if not ret:
        break

    print("[INFO] recognizing faces...")
    frame = imutils.resize(frame, width=750)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    boxes = face_recognition.face_locations(rgb, model='hog')
    for box in boxes:
        (top, right, bottom, left) = box
        if abs(top - bottom) <= 50 or abs(right - left) <= 50:
            boxes.remove(box)
    encodings = face_recognition.face_encodings(rgb, boxes)

    names = []
    stop = 0

    for encoding in encodings:
        # attempt to match each face in the input image to our known encodings
        matches = face_recognition.compare_faces(data['encodings'], encoding)
        name = "Unknown"

        # check to see if we have found a match
        if True in matches:
            # find the indexes of all matched faces then initialize a dictionary
            # to count the total number of times each face was matched
            matchedIdxs = []
            matchedIdxs = [i for (i, b) in enumerate(matches) if b]
            counts = {}

            # loop over the matched indexes and maintain a count for
            # each recognized face face
            for i in matchedIdxs:
                name = data["names"][i]
                counts[name] = counts.get(name, 0) + 1

            # determine the recognized face with the largest number of
            # votes (note: in the event of an unlikely tie Python will
            # select first entry in the dictionary)
            if max(counts.values()) >= 35:
                name = max(counts, key=counts.get)
                if name == 'BJT':   # GO!
                    ser.write('f'.encode())
                else:
                    ser.write('s'.encode())
        else:
            ser.write('s'.encode())

        names.append(name)

    for ((top, right, bottom, left), name) in zip(boxes, names):
        # draw the predicted face name on the image
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        y = top - 15 if top - 15 > 15 else top + 15
        cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

    cv2.imshow('monitor', frame)

    # waitKey()不断刷新图像，频率时间为delay，单位为ms。
    key = cv2.waitKey(1) & 0xFF
    if key == 27:
        break

ser.write('s'.encode())
cv2.destroyAllWindows()
