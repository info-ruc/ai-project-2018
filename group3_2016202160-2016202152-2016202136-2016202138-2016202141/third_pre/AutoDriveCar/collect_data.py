import numpy as np
import cv2
import pygame
from pygame.locals import *
import time
import os
import serial


class CollectTrainingData(object):

    def __init__(self, input_size):

        # 开启ip摄像头
        video = 'http://192.168.43.1:8080/video'  # 此处@后的ipv4 地址需要修改为自己的地址
        self.capture = cv2.VideoCapture(video)

        # connect to a seral port
        self.send_inst = True

        self.input_size = input_size

        # create labels
        self.k = np.zeros((4, 4), 'float')
        for i in range(4):
            self.k[i, i] = 1

        pygame.init()
        pygame.display.set_mode((250, 250))

    def collect(self):

        saved_frame = 0
        total_frame = 0

        # collect images for training
        print("Start collecting images...")
        print("Press 'q' or 'x' to finish...")
        start = cv2.getTickCount()

        X = np.empty((0, self.input_size))
        y = np.empty((0, 4))
        # stream video frames one by one
        try:
            frame = 1
            while self.send_inst:
                success, image = self.capture.read()
                image = cv2.resize(image, (240, 320), interpolation=cv2.INTER_CUBIC)
                img_encode = cv2.imencode('.jpg', image)[1]
                data_encode = np.array(img_encode)
                str_encode = data_encode.tostring()

                image = cv2.imdecode(np.frombuffer(str_encode, dtype=np.uint8), cv2.IMREAD_GRAYSCALE)

                # select lower half of the image
                height, width = image.shape
                #height=1080   width=1920
                roi = image[int(height / 2):height, :]

                cv2.imshow('roi',roi)

                # reshape the roi image into a vector
                temp_array = roi.reshape(1, int(height / 2) * width).astype(np.float32)

                frame += 1
                total_frame += 1

                # get input from human driver
                for event in pygame.event.get():
                    if event.type == KEYDOWN:
                        key_input = pygame.key.get_pressed()

                        # complex orders
                        if key_input[pygame.K_UP] and key_input[pygame.K_RIGHT]:
                            print("Forward Right")
                            X = np.vstack((X, temp_array))
                            y = np.vstack((y, self.k[1]))
                            saved_frame += 1


                        elif key_input[pygame.K_UP] and key_input[pygame.K_LEFT]:
                            print("Forward Left")
                            X = np.vstack((X, temp_array))
                            y = np.vstack((y, self.k[0]))
                            saved_frame += 1


                        elif key_input[pygame.K_DOWN] and key_input[pygame.K_RIGHT]:
                            print("Reverse Right")


                        elif key_input[pygame.K_DOWN] and key_input[pygame.K_LEFT]:
                            print("Reverse Left")


                        # simple orders
                        elif key_input[pygame.K_UP]:
                            print("Forward")
                            saved_frame += 1
                            X = np.vstack((X, temp_array))
                            y = np.vstack((y, self.k[2]))


                        elif key_input[pygame.K_DOWN]:
                            print("Reverse")


                        elif key_input[pygame.K_RIGHT]:
                            print("Right")
                            X = np.vstack((X, temp_array))
                            y = np.vstack((y, self.k[1]))
                            saved_frame += 1


                        elif key_input[pygame.K_LEFT]:
                            print("Left")
                            X = np.vstack((X, temp_array))
                            y = np.vstack((y, self.k[0]))
                            saved_frame += 1


                        elif key_input[pygame.K_x] or key_input[pygame.K_q]:
                            print("exit")

                            break

                    elif event.type == pygame.KEYUP:
                        print('njnx')

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            # save data as a numpy file
            file_name = str(int(time.time()))
            directory = "training_data"
            if not os.path.exists(directory):
                os.makedirs(directory)
            try:
                np.savez(directory + '/' + file_name + '.npz', train=X, train_labels=y)
            except IOError as e:
                print(e)

            end = cv2.getTickCount()
            # calculate streaming duration
            print("Streaming duration: , %.2fs" % ((end - start) / cv2.getTickFrequency()))

            print(X.shape)
            print(y.shape)
            print("Total frame: ", total_frame)
            print("Saved frame: ", saved_frame)
            print("Dropped frame: ", total_frame - saved_frame)

        finally:
            print('end!')


if __name__ == '__main__':
    # vector size, half of the image
    s = 120*320

    ctd = CollectTrainingData(s)
    ctd.collect()
