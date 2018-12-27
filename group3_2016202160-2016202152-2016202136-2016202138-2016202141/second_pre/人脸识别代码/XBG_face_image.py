import face_recognition
import pickle
import cv2
import serial.tools.list_ports


plist = list(serial.tools.list_ports.comports())

print("[INFO] loading encodings...")
data = pickle.loads(open('codes/wdx.pickle', "rb").read())

i = 0
fp = 0  # 负判断错  94
tp = 0  # 对的正   93
fn = 0  # 错的负   0
tn = 0  # 负判断对  25

for i in range(1, 120):
    path = 'codes/pos/' + str(i) + '.jpg'
    try:
        image = cv2.imread(path)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    except:
        continue

    print("[INFO] recognizing faces...")
    boxes = face_recognition.face_locations(rgb, model='hog')
    for box in boxes:
        (top, right, bottom, left) = box
        if abs(top - bottom) <= 50 or abs(right - left) <= 50:
            boxes.remove(box)
    encodings = face_recognition.face_encodings(rgb, boxes)

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
            if max(counts.values()) >= 50:
                name = max(counts, key=counts.get)
        if name == 'WDX':
            tp += 1
        else:
            fn += 1
    print(tp, fn)
