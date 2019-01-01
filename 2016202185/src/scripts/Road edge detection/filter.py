import matplotlib.pyplot as plt
import pylab
import numpy as np
import math
from PIL import Image

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

def convolve(img,template):
    h = template.shape[0] // 2
    w = template.shape[1] // 2
    img = np.pad(img, ((h, h), (w, w),(0, 0)), 'constant')
    res_b = solve(img[:,:,0],template)
    res_g = solve(img[:,:,1],template)
    res_r = solve(img[:,:,2],template)
    res = np.dstack([res_b,res_g,res_r])
    return res

def solve(img,template):         
    template_heigh = template.shape[0]
    template_width = template.shape[1]
    conv_heigh = img.shape[0] - template.shape[0] + 1
    conv_width = img.shape[1] - template.shape[1] + 1
    conv = np.zeros((conv_heigh,conv_width),dtype = 'uint8')
    for i in range(conv_heigh):
        for j in range(conv_width):
            conv[i][j] = (img[i:i + template_heigh,j:j + template_width ]*template).sum()
    return conv

if __name__=='__main__':
    img = plt.imread("test.jpg")
    sigma  = 1.5
    plt.imshow(img)
    plt.show()
    template = gettemplate(sigma)
    res = convolve(img,template)
    im=Image.fromarray(res)
    plt.imshow(im)
    plt.imsave("res.jpg",res)
    plt.show()