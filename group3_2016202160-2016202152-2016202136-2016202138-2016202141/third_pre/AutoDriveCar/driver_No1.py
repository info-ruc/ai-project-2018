import sys
import numpy as np
import cv2


from moudle import NeuralNetwork
from driver_helper import *

class VideoStreamHandler():
    nn = NeuralNetwork()
    nn.load_model("saved_model/nn_model.xml")

    rc_car = RCControl("COM5")

    video = 'http://192.168.43.1:8080/video'  # 此处@后的ipv4 地址需要修改为自己的地址
    capture = cv2.VideoCapture(video)

    def handle(self):
        try:
            # stream video frames one by one
            while True:
                success, image = self.capture.read()
                img_encode = cv2.imencode('.jpg', image)[1]
                data_encode = np.array(img_encode)
                str_encode = data_encode.tostring()

                gray = cv2.imdecode(np.frombuffer(str_encode, dtype=np.uint8), cv2.IMREAD_GRAYSCALE)

                height, width = gray.shape
                roi = gray[int(height / 2):height, :]

                cv2.imshow('image', image)
                # cv2.imshow('mlp_image', roi)

                # reshape image
                image_array = roi.reshape(1, int(height / 2) * width).astype(np.float32)

                # neural network makes prediction
                prediction = self.nn.predict(image_array)

                self.rc_car.steer(prediction)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    print("car stopped")
                    self.rc_car.stop()
                    break
        finally:
            cv2.destroyAllWindows()
            sys.exit()

if __name__ == '__main__':
    t = VideoStreamHandler()
    t.handle()