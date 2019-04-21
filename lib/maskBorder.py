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

def line_drawing(event,x,y,flags,param):
    global pt1_x,pt1_y,drawing,drawing2

    if event==cv2.EVENT_LBUTTONDOWN:
        drawing=True
        drawing2=False
        pt1_x,pt1_y=x,y
        print("Working5")

    elif event==cv2.EVENT_RBUTTONDOWN:
        drawing2=True
        drawing=False
        pt1_x,pt1_y=x,y
        print("Working6")

    elif event==cv2.EVENT_MOUSEMOVE:
        if drawing==True:
            cv2.line(img,(pt1_x,pt1_y),(x,y),color=(255,255,0),thickness=3)
            pt1_x,pt1_y=x,y
            print("Working")
        elif drawing2==True:
            cv2.line(img,(pt1_x,pt1_y),(x,y),color=(0,255,255),thickness=3)
            pt1_x,pt1_y=x,y
            print("Working2")

    elif event==cv2.EVENT_LBUTTONUP:
        drawing=False
        cv2.line(img,(pt1_x,pt1_y),(x,y),color=(255,255,0),thickness=3)
        print("Working3")

    elif event==cv2.EVENT_RBUTTONUP:
        drawing2=False
        cv2.line(img,(pt1_x,pt1_y),(x,y),color=(0,255,255),thickness=3)
        print("Working4")



def maskBorder(imagePath):
    tresh_min = 100
    tresh_max = 255
    real_img = cv2.imread(imagePath)
    rootImagePath = imagePath[:-7]
    testImagePath = rootImagePath + "seg.png"
    print(testImagePath)

    exists = os.path.isfile(testImagePath)

    if exists:
        mask = cv2.imread(testImagePath)
        mask2 = cv2.cvtColor(mask, cv2.COLOR_RGB2GRAY)
        (thresh, mask2) = cv2.threshold(mask2, tresh_min, tresh_max, 0)
        #plt.imshow(mask2)
        #plt.show()

        plt.subplot(121)
        plt.imshow(mask, cmap='Greys_r', interpolation='none')

        border = cv2.copyMakeBorder(mask2, 1, 1, 1, 1, cv2.BORDER_CONSTANT, value=0 )
        contours, hierarchy = cv2.findContours(border, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        real_img = cv2.imread(imagePath)
        contour_img = cv2.drawContours(real_img, contours, -1, (255,0,0), 3)
        img = contour_img
        cv2.namedWindow('test draw')
        cv2.setMouseCallback('test draw',line_drawing)

        while(1):
            #cv2.imshow("result",real_img)
            #img = contour_img
            #cv2.namedWindow('test draw')
            cv2.imshow('test draw',img)
            #cv2.setMouseCallback('test draw',line_drawing)
            #cv2.setMouseCallback('test draw',line_drawing)
            if cv2.waitKey(1) & 0xFF == 27:
                break
        cv2.destroyAllWindows()

    else:
        print("The mask of the selected image doesn't exist in the directory.")
        root = Tk()
        var = StringVar()
        label = Message( root, textvariable = var, relief = RAISED )
        var.set("The mask of the selected image doesn't exist in the directory.")
        label.pack()
        root.mainloop()
