# -*- coding: utf-8 -*-
"""
Created on Thu Dec 27 21:01:06 2018

@author: 啊花花
"""

from skimage import io,transform
import tensorflow as tf
import numpy as np
import time
import schedule
from PIL import ImageGrab

direction_dict = {0:'back',1:'left',2:'right',3:'stop',4:'up'}

w=100
h=100
c=3

def screen():
    im = ImageGrab.grab((20,120,620,560))#截图
    im.save('D:\Image\image4/'+str(c)+'.jpg','JPEG')#图片存储
    


def read_one_image(path):
    img = io.imread(path)
    
    img = transform.resize(img,(w,h))
    return np.asarray(img)

def test_one_image(path):
    with tf.Session() as sess:
        
        data = []
        data1 = read_one_image(path)
        data.append(data1)
        
        saver = tf.train.import_meta_graph('modle/model3.ckpt.meta')
        saver.restore(sess,tf.train.latest_checkpoint('modle/'))
        graph = tf.get_default_graph()
        x = graph.get_tensor_by_name("x:0")
        feed_dict = {x:data}
        
        logits = graph.get_tensor_by_name("logits_eval:0")
        classification_result = sess.run(logits,feed_dict)
        
        print(classification_result)
        print(tf.argmax(classification_result,1).eval())
        output = []
        output = tf.argmax(classification_result,1).eval()
        for i in range(len(output)):
            print("第",i+1,"张图预测:"+flower_dict[output[i]])
    
    

if __name__ == '__main__':
    
    c = 0
    schedule.every(1).seconds.do(screen)
    while True:
    #c = input()
        print(c)
        schedule.run_pending()
        path = 'D:\Image\image4/'+str(c)+'.jpg'
        test_one_image(path)
        #object_detection('D:\Image\image4/'+str(c)+'.jpg',"MobileNetSSD_deploy.prototxt.txt","MobileNetSSD_deploy.caffemodel",0.2)
        c += 1
        if c>10000:
            break
        time.sleep(1)