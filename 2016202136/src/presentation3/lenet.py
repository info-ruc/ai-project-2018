#coding=utf-8
import os
import numpy as np
import tensorflow as tf
import cv2
from tensorflow.contrib.layers import flatten
from sklearn.utils import shuffle


# 数据文件夹
data_dir = "pic"
# 训练还是测试
train = True
# 模型文件路径
model_path = "model/try"


# 从文件夹读取图片和标签到numpy数组中
# 标签信息在文件名中，例如1_40.jpg表示该图片的标签为1
def read_data(data_dir):
    datas = []
    labels = []
    fpaths = []
    for fname in os.listdir(data_dir):
        fpath = os.path.join(data_dir, fname)
        fpaths.append(fpath)
        image = cv2.imread(fpath)
        pic = cv2.resize(image, (32, 32), interpolation=cv2.INTER_AREA)
        data = np.array(pic) / 255.0
        datas.append(data)
    label = [[2 for z in range(485)], [0 for x in range(485, 1006)], [1 for y in range(1006, 1608)]]
    for ll in label:
        labels.extend(ll)
    datas = np.array(datas)
    labels = np.array(labels)

    print("shape of datas: {}\tshape of labels: {}".format(datas.shape, labels.shape))
    return fpaths, datas, labels


fpaths, datas, labels = read_data(data_dir)

# 计算有多少类图片
num_classes = len(set(labels))


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


def evaluate(X_data, y_data):
    num_examples = len(X_data)
    total_accuracy = 0
    sess = tf.get_default_session()
    for offset in range(0, num_examples, BATCH_SIZE):
        batch_x, batch_y = X_data[offset:offset+BATCH_SIZE], y_data[offset:offset+BATCH_SIZE]
        accuracy = sess.run(accuracy_operation, feed_dict={x: batch_x, y: batch_y})
        total_accuracy += (accuracy * len(batch_x))
    return total_accuracy / num_examples


x = tf.placeholder(tf.float32, (None, 32, 32, 3))
y = tf.placeholder(tf.int32, (None))
one_hot_y = tf.one_hot(y, 43)  # 一个值化为一个概率分布的向量

rate = 0.002
EPOCHS = 50
BATCH_SIZE = 200

logits = LeNet(x)
# 计算交叉熵 交叉熵得到的值一定是正数，其次是预测结果越准确值越小
cross_entropy = tf.nn.softmax_cross_entropy_with_logits_v2(labels=one_hot_y, logits=logits)
loss_operation = tf.reduce_mean(cross_entropy)  # 求平均值
optimizer = tf.train.AdamOptimizer(learning_rate=rate)
# optimizer = tf.train.GradientDescentOptimizer(rate)  # 梯度下降优化器
training_operation = optimizer.minimize(loss_operation)  # 最小化交叉熵

# 比较两者是否相同 argmax axis：0表示按列，1表示按行
correct_prediction = tf.equal(tf.argmax(logits, 1), tf.argmax(one_hot_y, 1))
prediction = tf.argmax(logits, 1)
accuracy_operation = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))  # cast转换类型
saver = tf.train.Saver()


with tf.Session() as sess:

    if train:
        print("训练模式")
        # 如果是训练，初始化参数
        sess.run(tf.global_variables_initializer())
        # 定义输入和Label以填充容器，训练时dropout为0.25
        datas, labels = shuffle(datas, labels)
        train_feed_dict = {
            x: datas,
            y: labels,
        }
        for step in range(300):
            _, mean_loss_val = sess.run([training_operation, accuracy_operation], feed_dict=train_feed_dict)

            if step % 10 == 0:
                print("step = {}\taccuracy = {}".format(step, mean_loss_val))
        saver.save(sess, model_path)
        print("训练结束，保存模型到{}".format(model_path))
    else:
        print("测试模式")
        # 如果是测试，载入参数
        saver.restore(sess, model_path)
        print("从{}载入模型".format(model_path))
        # label和名称的对照关系
        label_name_dict = {
            0: "turn left",
            1: "stop",
            2: "forward"
        }
        # 定义输入和Label以填充容器，测试时dropout为0
        test_feed_dict = {
            x: datas,
            y: labels,
        }
        predicted_labels_val = sess.run(prediction, feed_dict=test_feed_dict)
        # 真实label与模型预测label
        for fpath, real_label, predicted_label in zip(fpaths, labels, predicted_labels_val):
            # 将label id转换为label名
            # real_label_name = label_name_dict[real_label]
            bal = [[0 for x in range(10)], [1 for y in range(10, 20)], [2 for z in range(20, 30)]]
            real_label_name = []
            for x in bal:
                real_label_name.extend(x)
            predicted_label_name = label_name_dict[predicted_label]
            # print("{}\t{} => {}".format(fpath, real_label_name, predicted_label_name))
            print(predicted_label_name)











