第二次展示实现了图像识别和语音控制两部分功能。


图像识别：

代码见 人脸识别代码/，其中
1. XBG_face_detect.py 基于OpenCV自带的haar人脸特征分离器进行人脸检测
2. XBG_face_image.py 基于Ulib和Face_Recognition的使用hog/cnn方法对静态照片进行人脸识别
3. XBG_face_video.py 基于Ulib和Face_Recognition的使用hog/cnn方法对实时视频进行人脸识别
4. encodings.pickle 有120张白敬亭和120张魏大勋照片得到的两位人脸特征集
5. haarcascade_frontalface_default.xml 使用的haar人脸分离器特征池
6. output.avi 对白敬亭和魏大勋人脸视频进行识别的结果输出


语音控制：

基于DTW和GMM-HMM识别“前”、“后”、“左”、“右”、“停”五个指令，通过电脑蓝牙发送给小车蓝牙，从而控制小车的运动。

代码见 语音控制代码/，其中
1. recognition-DTW.ipynb 基于DTW的语音识别
2. recognition-GMMHMM.ipynb 基于GMM-HMM的语音识别
3. go.csv, back.csv, left.csv, right.csv, stop.csv 计算好的DTW模板库
4. models.pkl 训练好的GMM-HMM模型
5. BlueTooth.ipynb 蓝牙通讯
6. records 训练集
7. test.wav 测试音频
8. function 拷到Arduino上的代码 
