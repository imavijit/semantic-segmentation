import numpy as np
import cv2
import matplotlib.pyplot as plt
import os
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox
import sys
from tkinter import *


drawing , drawing2 = False , False
pt1_x , pt1_y = None , None
img = None
brushSize = 5
bright, contrast = 0, 127

def line_drawing(event,x,y,flags,param):
    global pt1_x,pt1_y,drawing,drawing2, img
    global brushSize

    if event==cv2.EVENT_LBUTTONDOWN:
        drawing=True
        drawing2=False
        pt1_x,pt1_y=x,y

    elif event==cv2.EVENT_RBUTTONDOWN:
        drawing2=True
        drawing=False
        pt1_x,pt1_y=x,y

    elif event==cv2.EVENT_MOUSEMOVE:
        if drawing==True:
            cv2.line(img,(pt1_x,pt1_y),(x,y),color=(255,0,0),thickness=brushSize)
            pt1_x,pt1_y=x,y

        elif drawing2==True:
            cv2.line(img,(pt1_x,pt1_y),(x,y),color=(0,255,0),thickness=brushSize)
            pt1_x,pt1_y=x,y

    elif event==cv2.EVENT_LBUTTONUP:
        drawing=False
        cv2.line(img,(pt1_x,pt1_y),(x,y),color=(255,0,0),thickness=brushSize)

    elif event==cv2.EVENT_RBUTTONUP:
        drawing2=False
        cv2.line(img,(pt1_x,pt1_y),(x,y),color=(0,255,0),thickness=brushSize)

    elif event==cv2.EVENT_MOUSEWHEEL:
        if flags < 0:
            if brushSize >= 2:
                brushSize = brushSize - 1
        else:
            if brushSize <= 10:
                brushSize = brushSize + 1


def maskBorder(imagePath):
    global img, brushSize, bright, contrast
    tresh_min = 100
    tresh_max = 255
    real_img = cv2.imread(imagePath)
    rootImagePath = imagePath[:-7]
    testImagePath = rootImagePath + "seg.png"
    resultPath = rootImagePath[:-12] + "results/" +  rootImagePath[-12:]  + "img_result.png"
    print(resultPath)
    existsResult = os.path.isfile(resultPath)
    exists = os.path.isfile(testImagePath)

    if exists and testImagePath != imagePath:
        if existsResult:
            testImagePath = resultPath
            print(testImagePath)
        mask = cv2.imread(testImagePath)
        mask2 = cv2.cvtColor(mask, cv2.COLOR_RGB2GRAY)
        (thresh, mask2) = cv2.threshold(mask2, tresh_min, tresh_max, 0)

        plt.subplot(121)
        plt.imshow(mask, cmap='Greys_r', interpolation='none')

        border = cv2.copyMakeBorder(mask2, 1, 1, 1, 1, cv2.BORDER_CONSTANT, value=0 )
        contours, hierarchy = cv2.findContours(border, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        real_img = cv2.imread(imagePath)
        bordered_image = contour_img = cv2.drawContours(real_img, contours, -1, (0,0,0), 3)
        cv2.namedWindow('test draw')
        cv2.namedWindow('test draw',-1)
        cv2.createTrackbar('bright', 'test draw', bright, 2*127, funcBrightContrast)
        cv2.createTrackbar('contrast', 'test draw', contrast, 2*127, funcBrightContrast)

        while cv2.getWindowProperty('test draw', 0) >= 0:
            img = bordered_image
            img = funcBrightContrast()
            cv2.imshow('test draw',img)
            #scrollEvent()
            cv2.setMouseCallback('test draw',line_drawing)
            path = imagePath[:-19]
            name = imagePath[-19:-4]
            dir = path + "results/" + name + '_result.png'
            imageMask = img
            image = cv2.imread(testImagePath)
            h,w = img.shape[:2]
            keyCode = cv2.waitKey(50)
            '''
            if keyCode == ord('u'):
                print("zoom in")
                bordered_image = cv2.pyrUp(bordered_image,dstsize = (2*w,2*h))
            elif keyCode == ord('d'):
                print("zoom out")
                bordered_image = cv2.pyrDown(bordered_image,dstsize = (int(w/2),int(h/2)))
            '''
        finalmask(image,imageMask)
        cv2.imwrite(dir, image)
        cv2.destroyAllWindows()

    else:
        print("The mask of the selected image doesn't exist in the directory.")
        root = Tk()
        var = StringVar()
        label = Message( root, textvariable = var, relief = RAISED )
        var.set("The mask of the selected image doesn't exist in the directory.")
        label.pack()
        root.mainloop()

def finalmask(image,imageMask):
    global img
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
        #green
            if imageMask[i][j][0] == 0 and imageMask[i][j][1] == 255 and imageMask[i][j][2] == 0:
                image[i][j] = 255
        #blue
            elif imageMask[i][j][0] == 255 and imageMask[i][j][1] == 0 and imageMask[i][j][2] == 0:
                image[i][j] = 0
            else:
                image[i][j] = image[i][j]


def funcBrightContrast(bright=0,contrast=0):
    global img
    bright = cv2.getTrackbarPos('bright', 'test draw')
    contrast = cv2.getTrackbarPos('contrast', 'test draw')
    img = apply_brightness_contrast(img,bright,contrast)
    return img
def apply_brightness_contrast(input_img, brightness = 0, contrast = 127):
    bright = map(brightness, 0, 255, -127, 127)
    contrast = map(contrast, 0, 254, -127, 127)

    if brightness != 0:
        if brightness > 0:
            shadow = brightness
            highlight = 255
        else:
            shadow = 0
            highlight = 255 + brightness
        alpha_b = (highlight - shadow)/255
        gamma_b = shadow
        buf = cv2.addWeighted(input_img, alpha_b, input_img, 0, gamma_b)
    else:
        buf = input_img.copy()

    if contrast != 0:
        f = float(131 * (contrast + 127)) / (127 * (131 - contrast))
        alpha_c = f
        gamma_c = 127*(1-f)
        buf = cv2.addWeighted(buf, alpha_c, buf, 0, gamma_c)
    return buf

def map(x, in_min, in_max, out_min, out_max):
    return int((x-in_min) * (out_max-out_min) / (in_max-in_min) + out_min)
