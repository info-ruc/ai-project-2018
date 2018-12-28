#coding=utf-8
import numpy as np
import tensorflow as tf
import cv2
from tensorflow.contrib.layers import flatten
import serial.tools.list_ports

plist = list(serial.tools.list_ports.comports())
ser = serial.Serial('COM4', 9600)

# 模型文件路径
model_path = "model/lenet"
rate = 0.002

vs = cv2.VideoCapture(0)
vs.open('http://192.168.43.1:8080/video')


def LeNet(x):
    mu = 0
    sigma = 0.1

    # Layer 1: Convolutional. Input = 32x32x3. Output = 28x28x6.
    # 形状为(5, 5) inchannel=3 outchannel=6 均值为mu 标准差为sigma的正态分布
    conv1_W = tf.Variable(tf.truncated_normal(shape=(5, 5, 3, 6), mean=mu, stddev=sigma))
    conv1_b = tf.Variable(tf.zeros(6))  # 偏移量
    # x做卷积的图片 conv1_W是卷积核 strides步长 padding补齐
    conv1 = tf.nn.conv2d(x, conv1_W, strides=[1, 1, 1, 1], padding='VALID') + conv1_b

    # Activation.
    conv1 = tf.nn.relu(conv1)

    # Pooling. Input = 28x28x6. Output = 14x14x6.
    conv1 = tf.nn.max_pool(conv1, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='VALID')

    # Layer 2: Convolutional. Output = 10x10x16.
    conv2_W = tf.Variable(tf.truncated_normal(shape=(5, 5, 6, 16), mean=mu, stddev=sigma))
    conv2_b = tf.Variable(tf.zeros(16))
    conv2 = tf.nn.conv2d(conv1, conv2_W, strides=[1, 1, 1, 1], padding='VALID') + conv2_b

    # Activation.
    conv2 = tf.nn.relu(conv2)

    # Pooling. Input = 10x10x16. Output = 5x5x16.
    conv2 = tf.nn.max_pool(conv2, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='VALID')

    # Flatten. Input = 5x5x16. Output = 400.
    fc0 = flatten(conv2)

    # Layer 3: Fully Connected. Input = 400. Output = 120.
    fc1_W = tf.Variable(tf.truncated_normal(shape=(400, 120), mean=mu, stddev=sigma))
    fc1_b = tf.Variable(tf.zeros(120))
    fc1 = tf.matmul(fc0, fc1_W) + fc1_b

    # Activation.
    fc1 = tf.nn.relu(fc1)

    # Layer 4: Fully Connected. Input = 120. Output = 84.
    fc2_W = tf.Variable(tf.truncated_normal(shape=(120, 84), mean=mu, stddev=sigma))
    fc2_b = tf.Variable(tf.zeros(84))
    fc2 = tf.matmul(fc1, fc2_W) + fc2_b

    # Activation.
    fc2 = tf.nn.relu(fc2)

    # Layer 5: Fully Connected. Input = 84. Output = 43.
    fc3_W = tf.Variable(tf.truncated_normal(shape=(84, 43), mean=mu, stddev=sigma))
    fc3_b = tf.Variable(tf.zeros(43))
    logits = tf.matmul(fc2, fc3_W) + fc3_b

    return logits


def detect_sign(frame):
    datas = []
    pic = cv2.resize(frame, (32, 32), interpolation=cv2.INTER_AREA)
    data = np.array(pic) / 255.0
    datas.append(data)
    datas = np.asarray(datas)

    predicted_labels_val = sess.run(prediction, feed_dict={x: datas})

    result = predicted_labels_val[0]
    print(label_name_dict[result])

    return result


x = tf.placeholder(tf.float32, (None, 32, 32, 3))
logits = LeNet(x)

prediction = tf.argmax(logits, 1)
saver = tf.train.Saver()

with tf.Session() as sess:
    saver.restore(sess, model_path)
    print("从{}载入模型".format(model_path))

    label_name_dict = {
        0: "turn left",
        1: "stop",
        2: "forward"
    }

    while True:
        ret, frame = vs.read()
        if not ret:
            break

        result = detect_sign(frame)
        if result == 0:
            ser.write('l'.encode())
        elif result == 1:
            ser.write('s'.encode())
        else:
            ser.write('f'.encode())

        cv2.imshow('monitor', frame)
        key = cv2.waitKey(10000) & 0xFF
        if key == 27:
            break











