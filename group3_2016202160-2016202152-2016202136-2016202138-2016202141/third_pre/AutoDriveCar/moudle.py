import cv2
import numpy as np
import glob
import sys
import time
import os
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split


def load_data(input_size, path):
    print("Loading training data...")
    start = time.time()

    # load training data
    X = np.empty((0, input_size))
    y = np.empty((0, 4))
    training_data = glob.glob(path)

    # if no data, exit
    if not training_data:
        print("Data not found, exit")
        sys.exit()

    for single_npz in training_data:
        with np.load(single_npz) as data:
            train = data['train']  # 拍到的照片
            train_labels = data['train_labels']  # 照片对应的标签
        X = np.vstack((X, train))
        y = np.vstack((y, train_labels))
        print(y)

    print('Image array shape: ', X.shape)
    print('Label array shape: ', y.shape)

    end = time.time()
    print("Loading data duration: %.2fs" % (end - start))

    # train validation split, 7:3
    return train_test_split(X, y, test_size=0.3)


class NeuralNetwork(object):
    def __init__(self):
        self.model = None

    def create(self, layer_sizes):
        # create a neural network
        self.model = cv2.ml.ANN_MLP_create()  # 建立模型
        self.model.setLayerSizes(layer_sizes)  # 设置层数，输入38400层（像素320*240），输出层4（上下左右四个方向），以及中间层32
        self.model.setTrainMethod(cv2.ml.ANN_MLP_BACKPROP)  # 设置训练方式为反向传播
        self.model.setActivationFunction(cv2.ml.ANN_MLP_SIGMOID_SYM, 2, 1)  # 设置激活函数为SIGMOID，其实就这一个可以选
        self.model.setTermCriteria((cv2.TERM_CRITERIA_COUNT, 100, 0.01))  # 设置终止条件

    def train(self, X, y):
        # set start time
        start = time.time()

        print("Training ...")
        self.model.train(np.float32(X), cv2.ml.ROW_SAMPLE, np.float32(y)) #开始训练，cv2.ml.ROW_SAMPLE代表每一行是一个样本

        # set end time
        end = time.time()
        print("Training duration: %.2fs" % (end - start))

    def evaluate(self, X, y):
        ret, resp = self.model.predict(X)  # resp=[[0. 0. 1. 0.]...]
        prediction = resp.argmax(-1)  # resp.argmax返回的是最大元素所在的列号（如：最大元素出现在第2列）
        true_labels = y.argmax(-1)
        accuracy = np.mean(prediction == true_labels)
        return accuracy

    def save_model(self, path):
        directory = "saved_model"
        if not os.path.exists(directory):
            os.makedirs(directory)
        self.model.save(path)
        print("Model saved to: " + "'" + path + "'")


    def load_model(self, path):
        if not os.path.exists(path):
            print("Model 'nn_model.xml' does not exist, exit")
            sys.exit()
        self.model = cv2.ml.ANN_MLP_load(path)

    def predict(self, X):
        ret, resp = self.model.predict(X)
        return resp.argmax(-1)
