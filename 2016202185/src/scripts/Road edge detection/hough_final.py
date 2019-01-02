import numpy as np
import cv2
import math

def rgb2gray(rgb):
    return np.dot(rgb[..., :3], [0.299, 0.587, 0.114]).astype(np.uint8)

def hough_line(img,diag_len):
    # Rho and Theta ranges
    accumulator = np.zeros((2 * diag_len ,180 ), dtype=np.uint8)
    #print(accumulator.shape)
    # Vote in the hough accumulator
    for i in range(width):
        for j in range(height):
            if img[i,j]==255:
                for t in range(-90,90,1):
                # Calculate rho. diag_len is added for a positive index
                    tot = 2*t*math.pi/360
                    sin_tot = np.sin(tot)
                    cos_tot = np.cos(tot)
                    rho = int(diag_len + round(i*cos_tot + j*sin_tot))
                    accumulator[rho, t+90] += 1
    return accumulator

def add_line(img,rho,theta,diag_len):
    width = img.shape[1]
    theta = theta - 90
    rho = rho - diag_len
    tot = 2*theta*math.pi/360
    if theta == - 90:
        img = cv2.line(img,(rho,0),(rho,img.shape[0]),(255,0,0),2)
    elif theta == 0:
        img = cv2.line(img,(0,rho),(img.shape[1],rho),(255,0,0),2)
    else:
        sin_t = np.sin(tot)
        cos_t = np.cos(tot)
        x1 = 0
        y1 = int(round(rho/cos_t))
        x2 = width
        y2 = int(round((rho-width*sin_t)/cos_t))
        img = cv2.line(img,(x1,y1),(x2,y2),(255,0,0),2)
        #print(x1,y1,x2,y2)
    return img

if __name__ == '__main__':
    imgpath = 'canny_test.jpg'
    img1 = cv2.imread(imgpath)
    img2 = cv2.imread("test.jpg")
    img = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    width, height = img.shape
    diag_len = int(round(math.sqrt(width * width + height * height)))
    #print(diag_len)
    #print(img)
    #print(img.shape)
    accumulator = hough_line(img,diag_len)
    #print(accumulator.shape)
    N = np.max(accumulator)-50
    flag = 0
    for rho in range(accumulator.shape[0]):
        for theta in range(accumulator.shape[1]):
            if accumulator[rho,theta] > N:
                flag = 0
                if rho-100>0:
                    left = rho-100
                else:
                    left = 0
                if rho+100<accumulator.shape[0]:
                    right = rho+100
                else:
                    right= accumulator.shape[0]
                if theta - 10 >0:
                    up = theta
                else:
                    up = 0
                if theta+10 <180:
                    down = theta +10
                else:
                    down = 180
                for i in range(left,right,1):
                    for j in range(up,down,1):
                        if accumulator[i,j]>accumulator[rho,theta]:
                            img2 = add_line(img2,i,j,diag_len)
                            flag = 1
                if flag == 0:
                    img2 = add_line(img2,rho,theta,diag_len)
                #print(rho, theta,accumulator[rho,theta])
    #cv2.imshow('after_hough',img)
    cv2.imwrite('after_hough.jpg',img2)