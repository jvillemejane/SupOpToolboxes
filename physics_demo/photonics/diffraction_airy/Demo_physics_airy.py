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
from PyQt5.QtGui import QPixmap, QImage

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
        
        """ Opening image """
        pmap = QPixmap("airy_1mm.bmp")s
        pmap = pmap.scaled(self.imageWidth, self.imageHeight)
        self.imageDisplay.setPixmap(pmap)
        self.positionSlider.setMaximum(self.imageHeight) # depending on the height of the image
        self.positionSlider.setMinimum(1)
        
        """ Airy Section """
        self.plotSection = PlotWidget()
        self.sectionLayout.addWidget(self.plotSection)
        self.plotSection.setBackground('w')
        self.plotSection.setYRange(0, 255, padding=0)
        
        self.opticalParams.setStyleSheet("background-color:lightblue;");
        self.pen = mkPen(color=(128, 128, 0), width=5)
       
        """ Events """        
        self.positionSlider.valueChanged.connect(self.verticalChanged)
        
        

    def verticalChanged(self):
        self.position = int(self.positionSlider.value())
        self.positionValue.setText(f'{self.position} px')
       
        
    def refreshGraph(self):
        print('refresh')
        """ Collecting new values """        
        
            
        
        """ Signals generation"""
        
        
        """ Displaying data """
        

    
    def closeEvent(self, event):
        QApplication.quit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
