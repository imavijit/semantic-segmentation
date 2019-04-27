from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication,QWidget, QVBoxLayout, QPushButton, QFileDialog , QLabel, QTextEdit
import sys
from PyQt5.QtGui import QPixmap
import cv2
import os
from tkinter import *


from lib.maskBorder import maskBorder

class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.title = "Semantic Segmentation"
        self.top = 200
        self.left = 500
        self.width = 300
        self.height = 100

        self.InitWindow()


    def InitWindow(self):
        #self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        vbox = QVBoxLayout()
        self.label = QLabel("Semantic Segmentation")
        vbox.addWidget(self.label)
        self.btn1 = QPushButton("Open Image")
        self.btn1.clicked.connect(self.getImage)
        vbox.addWidget(self.btn1)
        self.setLayout(vbox)
        self.show()

    def on_scroll(x, y, dx, dy):
        print('Scrolled {0}'.format('down' if dy < 0 else 'up'))


    def getImage(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file','c:\\', "Image files (*.jpg *.gif *.png)")
        imagePath = fname[0]
        print(imagePath)
        img = cv2.imread(imagePath,-1)
        maskBorder(imagePath)

        #cv2.imshow('image',img)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()
        #pixmap = QPixmap(imagePath)
        #self.label.setPixmap(QPixmap(pixmap))
        #self.resize(pixmap.width(), pixmap.height())



App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())
