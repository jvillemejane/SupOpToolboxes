# -*- coding: utf-8 -*-
"""
Demo application : photonics / diffraction and Airy

Author : Julien VILLEMEJANE
Laboratoire d Enseignement Experimental - Institut d Optique Graduate School
Created on 18/mar/2023

@author: julien.villemejane
"""

from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap, QImage, QPainter
from PyQt5 import QtCore
import cv2

import numpy as np
from pyqtgraph import PlotWidget, plot, mkPen
from signal_processing.signal_processing import generate_sinus_time

import sys  # We need sys so that we can pass argv to QApplication
import os



"""
MainWindow class
"""
class MainWindow(QMainWindow):

    
    def __init__(self):
        super().__init__(parent=None)
        loadUi("Demo_physics_airy.ui", self)
        
        imageSize = self.imageDisplay.size()
        self.imageWidth = imageSize.width()
        self.imageHeight = imageSize.height()
        self.pen = mkPen(color=(128, 128, 0), width=2)
        self.maxMean = 200
        
        imageSize = self.lense_logo.size()
        logo = QPixmap("./data/IOGS-LEnsE-logo.jpg")
        logo = logo.scaled(imageSize.width(), imageSize.height(), QtCore.Qt.KeepAspectRatio)
        self.lense_logo.setPixmap(logo)
        
        """ Opening image """
        self.openImage("./data/airy_1mm.bmp")
        self.processRatio()
        """ Resizing image """
        self.resizeDispImage()
        """ Position Slider update """
        self.positionSlider.setMaximum(self.imageOrH) # depending on the height of the image
        self.positionSlider.setMinimum(1)
        
        """ Find Max intensity in gray image """
        self.maxIntensity = np.argmax(self.image) // self.imageOrW 
        """ Set position of the slider to the maximum intensity line"""
        self.position = self.maxIntensity
        self.positionValue.setText(f'{self.position} px')
        self.positionSlider.setValue(self.maxIntensity)
        """ Mean Slider update """
        if((self.maxIntensity > self.maxMean) and (self.imageOrH-self.maxIntensity) > self.maxMean):
            self.meanSlider.setMaximum(self.maxMean)
        else:
            value = np.minimum(self.maxIntensity, self.imageOrH-self.maxIntensity)
            self.meanSlider.setMaximum(value)
        self.mean = int(self.meanSlider.value())
        self.meanValue.setText(f'{self.mean} px')
        
        """ Updating display of the image """
        self.updateImage()
        
        """ Airy Section """
        self.plotSection = PlotWidget()
        self.sectionLayout.addWidget(self.plotSection)
        self.plotSection.setBackground('w')
        self.plotSection.setYRange(0, 255, padding=0)
        self.plotSection.setXRange(0, 1279, padding=0)
        
        self.opticalParams.setStyleSheet("background-color:#A4E1DA;");
        self.meanParams.setStyleSheet("background-color:#CAE1A4;");
        self.positionParams.setStyleSheet("background-color:#E1AFA4;");
        self.refreshGraph()
       
        """ Events """        
        self.positionSlider.valueChanged.connect(self.verticalChanged)
        self.meanSlider.valueChanged.connect(self.verticalChanged)
        self.logCheck.stateChanged.connect(self.verticalChanged)
                    

    def processRatio(self):
        self.scaleHeight = self.imageOrH / self.imageHeight
        self.ratioValue.setText(f'{np.round(self.scaleHeight, decimals=2)}')
    
    def resizeDispImage(self):
        self.newDim = (self.imageWidth, self.imageHeight)
        self.image_res = cv2.resize(self.image, self.newDim)
        self.pmap_res = QImage(self.image_res, self.imageWidth, self.imageHeight, self.imageWidth, QImage.Format_Grayscale8)     
        self.pmap_res = QPixmap(self.pmap_res)

    def openImage(self, imageName):
        self.image = cv2.imread(imageName, cv2.IMREAD_GRAYSCALE)
        self.imageOrW = self.image.shape[1]     # width of the original image
        self.imageOrH = self.image.shape[0]     # height of the original image


    def updateImage(self):
        self.image_line = np.array(self.image)
        """ Log scale on the image """
        if(self.logCheck.isChecked()):
            self.image_line = np.log10(self.image_line+1)
            self.image_line = self.image_line / np.max(self.image_line) * 255
            self.image_line = np.trunc(self.image_line).astype('uint8')
        self.image_line[self.position-2:self.position+2,:] = 255
        
        if(self.mean != 0):
            self.image_line[(self.position-self.mean)-2:(self.position-self.mean)+2,:] = 200
            self.image_line[(self.position+self.mean)-2:(self.position+self.mean)+2,:] = 200
    
        self.image_res = cv2.resize(self.image_line, self.newDim)
        self.pmap_res = QImage(self.image_res, self.imageWidth, self.imageHeight, self.imageWidth, QImage.Format_Grayscale8)     
        self.pmap_res = QPixmap(self.pmap_res)
        
        """ Displaying image and line """
        self.imageDisplay.setPixmap(self.pmap_res)
        self.imageDisplay.repaint()


    def verticalChanged(self):
        """ Collecting new values """ 
        self.position = int(self.positionSlider.value())
        self.positionValue.setText(f'{self.position} px')
        self.mean = int(self.meanSlider.value())
        self.meanValue.setText(f'{self.mean} px')
        """ Limits verification """
        if(self.position-self.mean < 0):
            self.mean = self.position
        if(self.position+self.mean > self.imageOrH-1):
            self.mean = self.imageOrH-1-self.position
        self.meanSlider.setValue(self.mean)
        """ Refresh Graph """
        self.refreshGraph()
       
        
    def refreshGraph(self):
        """ Updatind Display of image """
        self.updateImage()
        """ Displaying data """
        self.plotSection.clear()
        self.plotSection.plot(self.image[self.position-1,:], pen=self.pen)
        
        if(self.mean != 0):
            penMean = mkPen(color=(255, 0, 128), width=2)
            meanValue = np.mean(self.image[self.position-self.mean:self.position+self.mean, :],axis=0)
            self.plotSection.plot(meanValue, pen=penMean)
    
    def closeEvent(self, event):
        QApplication.quit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
