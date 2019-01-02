import matplotlib.pyplot as plt
import pylab
import cv2
import numpy as np
import math
def gettemplate(sig):
    a = np.zeros((5,5))
    s = 0.0
    sigma = sig
    for i in range(5):
        for j in range(5):
            t = -((i - 2)*(i - 2) + (j - 2)*(j - 2)) / (2 * sigma*sigma)
            a[i][j]= math.exp(t)
            s += a[i][j]
    res = a/s
    return res

def grayfy(img):
    gray = np.zeros((img.shape[0],img.shape[1]))
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            gray[i][j] =0.299*img[i][j][2]+0.587*img[i][j][1]+0.114*img[i][j][0]
    return gray 

if __name__=='__main__':
    img = cv2.imread("test.jpg")
    if img.ndim == 3:
        img = grayfy(img)
    #plt.imshow(img,cmap = 'gray')
    #pylab.show()

    template1 = np.array([[ -1,0, 1],
                        [ -2, 0, 2],
                        [ -1, 0, 1]])
    template2 = np.array([[ -1,-2, -1],
                        [ 0, 0, 0],
                        [ 1, 2, 1]])
    template3 = np.array([[-2,-4,-4,-4,-2],
                        [-4,0,8,0,-4],
                        [-4,8,24,8,-4],
                        [-4,0,8,0,-4],
                        [-2,-4,-4,-4,-2]])
    sigma = 1.5
    template = gettemplate(sigma)
    after_filter = cv2.filter2D(img,-1,template)
    #plt.imshow(after_filter, cmap ='gray') 
    #plt.imsave("after_filter.jpg",after_filter,cmap ='gray')
    #pylab.show()
    

    Gx = cv2.filter2D(after_filter,-1,template2)
    Gy = cv2.filter2D(after_filter,-1,template1)
    #plt.imshow(Gx, cmap ='gray') 
    #plt.imsave("Gx.jpg",Gx,cmap ='gray')
    #pylab.show()
    #plt.imshow(Gy, cmap ='gray') 
    #plt.imsave("Gy.jpg",Gy,cmap ='gray')
    #pylab.show()
    G1 = np.zeros(Gx.shape,np.float64)
    D = np.zeros(Gx.shape,np.float64)
    for i in range(Gx.shape[0]):
        for j in range(Gy.shape[1]):
            G1[i][j] = math.sqrt(Gx[i][j] ** 2 + Gy[i][j] ** 2)
            D[i][j] = math.fabs(math.atan2(Gx[i][j],Gy[i][j])*180/math.pi)
    #print(D)
    #plt.imshow(G1, cmap ='gray') 
    #plt.imsave("G1.jpg",G1, cmap ='gray')
    #pylab.show()

    G2 = cv2.filter2D(after_filter,-1,template3)
    #plt.imshow(G2, cmap ='gray') 
    #plt.imsave("G2.jpg",G2, cmap ='gray')
    #pylab.show()

    newimg = np.zeros(G1.shape)
    for i in range(1, newimg.shape[0] - 1, 1):
        for j in range(1, newimg.shape[1] - 1, 1):
            if 0 <= D[i][j] <= 22.5 or 157.5 <= D[i][j] <= 180:
                if G1[i][j - 1] < G1[i][j] and G1[i][j] > G1[i][j + 1]:
                    newimg[i][j] = G1[i][j]
                else:
                    newimg[i][j] = 0
            elif 22.5 <= D[i][j] <= 67.5:
                if G1[i - 1][j + 1] < G1[i][j] and G1[i][j] > G1[i + 1][j - 1]:
                    newimg[i][j] = G1[i][j]
                else:
                    newimg[i][j] = 0
            elif 67.5 <= D[i][j] <= 112.5:
                if G1[i - 1][j] < G1[i][j] and G1[i][j] > G1[i + 1][j]:
                    newimg[i][j] = G1[i][j]
                else:
                    newimg[i][j] = 0
            elif 112.5 <= D[i][j] <= 157.5:
                if G1[i - 1][j - 1] < G1[i][j] and G1[i][j] > G1[i + 1][j + 1]:
                    newimg[i][j] = G1[i][j]
                else:
                    newimg[i][j] = 0
    #plt.imshow(newimg, cmap ='gray') 
    #plt.imsave("newimg.jpg",newimg, cmap ='gray')
    #pylab.show()

    newimg2 = np.zeros(newimg.shape)
    high_threshold = 60
    low_threshold = 30
    for i in range(newimg.shape[0]):
        for j in range(newimg.shape[1]):
            if newimg[i][j] >= high_threshold:
                newimg2[i][j] = 255
            elif newimg[i][j] <= low_threshold:
                newimg2[i][j] = 0
            else:
                if 0 < i < newimg.shape[0] - 1 and 0 < j < newimg.shape[1] - 1:
                    if 0 <= D[i][j] <= 22.5 and 157.5 <= D[i][j] <= 180:
                        if newimg[i][j - 1] > high_threshold or newimg[i][j + 1] > high_threshold:
                            newimg2[i][j] = 255
                        else:
                            newimg2[i][j] = 0
                    elif 22.5 <= D[i][j] <= 67.5:
                        if newimg[i - 1][j + 1] > high_threshold or newimg[i + 1][j - 1] > high_threshold:
                            newimg2[i][j] = 255
                        else:
                            newimg2[i][j] = 0
                    elif 67.5 <= D[i][j] <= 112.5:
                        if newimg[i - 1][j] > high_threshold or newimg[i + 1][j] > high_threshold:
                            newimg2[i][j] = 255
                        else:
                            newimg2[i][j] = 0
                    elif 112.5 <= D[i][j] <= 167.5:
                        if newimg[i - 1][j - 1] > high_threshold or newimg[i + 1][j + 1] > high_threshold:
                            newimg2[i][j] = 255
                        else:
                            newimg2[i][j] = 0
    #plt.imshow(newimg2, cmap ='gray') 
    #plt.imsave("newimg2.jpg",newimg2, cmap ='gray')
    #pylab.show()

    queue = []
    flag = np.zeros((newimg2.shape[0],newimg2.shape[1]), np.bool)
    newimg3 = np.zeros(newimg2.shape)
    for i in range(1,newimg2.shape[0]-1):
        for j in range(1,newimg2.shape[1]-1):
            flag = 0
            if newimg2[i][j]>low_threshold and newimg2[i][j]<high_threshold:
                for p in range(-1,2,1):
                    for q in range(-1,2,1):
                        if newimg2[i+p][j+q]>high_threshold:
                            flag=1
            if newimg2[i][j]<low_threshold:
                newimg3[i][j] = 0
            elif flag == 1:
                queue.append((i,j))
                flag[i][j] = True
                newimg3[i][j] = newimg2[i][j]
                while len(queue) > 0:
                    temps = queue[0]
                    del queue[0]
                    for p in range(-1, 2, 1):
                        for q in range(-1, 2, 1):
                            i1 = temps[0] + p
                            j1 = temps[1] + q
                            if low_threshold < newimg2[i1][j1] < high_threshold and not flag[i1][j1]:
                                queue.append((i1, j1))
                                flag[i1][j1] = True
                                newimg3[i1][j1] = newimg2[i1][j1]
            else:
                newimg3[i][j] = 255
    plt.imshow(newimg3, cmap ='gray') 
    plt.imsave("canny_test.jpg",newimg3, cmap ='gray')
    pylab.show()
