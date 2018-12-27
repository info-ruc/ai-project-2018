# test_model.py
from PIL import ImageGrab
import numpy as np
from grabscreen import grab_screen
import cv2
import time
from directkeys import PressKey,ReleaseKey, W, A, S, D
from alexnet import alexnet
from getkeys import key_check
import pyautogui
import tflearn
import tensorflow as tf
import random
import time
import os
import six.moves.urllib as urllib
import sys
import tarfile
import zipfile
from collections import defaultdict
from io import StringIO
from matplotlib import pyplot as plt
from PIL import Image
sys.path.append("object_detection")
from utils import label_map_util
from utils import visualization_utils as vis_util

WIDTH = 160
HEIGHT = 90
LR = 1e-4
EPOCHS = 120
MODEL_NAME = 'pygta5-car-{}-{}-{}-epochs.model'.format(LR, 'alexnetv2',EPOCHS)

MODEL_NAME2 = 'ssd_mobilenet_v1_coco_11_06_2017'
PATH_TO_CKPT = MODEL_NAME2 + '/frozen_inference_graph.pb'
PATH_TO_LABELS = os.path.join('object_detection/data', 'mscoco_label_map.pbtxt')

t_time = 0.005

def straight():
##    if random.randrange(4) == 2:
##        ReleaseKey(W)
##    else:
    PressKey(W)
    ReleaseKey(A)
    ReleaseKey(D)

def left():
    PressKey(W)
    PressKey(A)
    #ReleaseKey(W)
    ReleaseKey(D)
    #ReleaseKey(A)
    time.sleep(t_time)
    ReleaseKey(A)

def right():
    PressKey(W)
    PressKey(D)
    ReleaseKey(A)
    #ReleaseKey(W)
    #ReleaseKey(D)
    time.sleep(t_time)
    ReleaseKey(D)
    
    
model = alexnet(WIDTH, HEIGHT, LR)
model.load(MODEL_NAME)
def main():
    # last_time = time.time()
    for i in list(range(4))[::-1]:
        print(i+1)
        time.sleep(1)

    paused = False
    NUM_CLASSES = 90
    detection_graph = tf.Graph()
    with detection_graph.as_default():
        od_graph_def = tf.GraphDef()
        with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')

    label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
    categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
    category_index = label_map_util.create_category_index(categories)

    def load_image_into_numpy_array(image):
        (im_width, im_height) = image.size
        return np.array(image.getdata()).reshape(
            (im_height, im_width, 3)).astype(np.uint8)

    IMAGE_SIZE = (12, 8)
    with detection_graph.as_default():
        with tf.Session(graph=detection_graph) as sess:
            while(True):
                
                if not paused:
                    # 800x600 windowed mode
                    #screen =  np.array(ImageGrab.grab(bbox=(0,40,800,640)))


                    screen = grab_screen(region=(0,40,800,640))

                    screen1 = cv2.resize(screen, (800,640))
                    image_np = cv2.cvtColor(screen1, cv2.COLOR_BGR2RGB)
                    image_np_expanded = np.expand_dims(image_np, axis=0)
                    image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
                    boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
                    scores = detection_graph.get_tensor_by_name('detection_scores:0')
                    classes = detection_graph.get_tensor_by_name('detection_classes:0')
                    num_detections = detection_graph.get_tensor_by_name('num_detections:0')
                    (boxes, scores, classes, num_detections) = sess.run(
                        [boxes, scores, classes, num_detections],
                        feed_dict={image_tensor: image_np_expanded})
                    vis_util.visualize_boxes_and_labels_on_image_array(
                        image_np,
                        np.squeeze(boxes),
                        np.squeeze(classes).astype(np.int32),
                        np.squeeze(scores),
                        category_index,
                        use_normalized_coordinates=True,
                        line_thickness=8)
                    cv2.imshow('window',image_np)
                    # print('loop took {} seconds'.format(time.time()-last_time))
                    # last_time = time.time()
                    screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
                    screen = cv2.resize(screen, (160,90))

                    prediction = model.predict([screen.reshape(160,90,1)])[0]
                    print(prediction)

                    turn_thresh = .75
                    fwd_thresh = 0.6

                    if prediction[1] > fwd_thresh:
                        straight()
                        # print("!")
                    elif prediction[0] > turn_thresh:
                        left()
                        # print("<")
                    elif prediction[2] > turn_thresh and prediction[2] < 0.95 :
                        right()
                        # print(">")
                    else:
                        straight()
                        # print("!!!")

                keys = key_check()

                # p pauses game and can get annoying.
                if 'T' in keys:
                    if paused:
                        paused = False
                        time.sleep(1)
                    else:
                        paused = True
                        ReleaseKey(A)
                        ReleaseKey(W)
                        ReleaseKey(D)
                        time.sleep(1)
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    cv2.destroyAllWindows()
                    break
main()       
