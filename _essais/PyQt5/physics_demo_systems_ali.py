# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 07:27:21 2023

@author: Villou
"""
import sys

from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QLabel, QPushButton, QVBoxLayout

import graphicalLEnsE as gL
"""
from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap, QImage
from PyQt5 import QtCore

import numpy as np
from pyqtgraph import PlotWidget, plot, mkPen
from signal_processing.signal_processing import generate_sinus_time

import sys  # We need sys so that we can pass argv to QApplication
import os
"""




"""
MainWindow class
"""
class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__(parent=None)
        ''' Main Window parameters '''
        self.setWindowTitle("Ma première application PyQt")
        self.setGeometry(100, 100, 500, 200)
        self.mainWidget = QWidget()
        self.setCentralWidget(self.mainWidget)
        
        ''' Graphical elements '''
        self.gainALI = gL.sliderBlock("GAIN ALI", action=self.updateFC)
        self.gainALI.setPercent(True, 50)
        self.gbwALI = gL.sliderBlock("GBW ALI", action=self.updateFC)
        self.gbwALI.setUnits('Hz')
        self.gbwALI.setPercent(True, 20)
        self.fcALI = gL.labelBlock('Cut Freq')
        self.fcALI.setUnits('Hz')
        
        ''' Layout Manager '''
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.gainALI)
        self.layout.addWidget(self.gbwALI)
        self.layout.addWidget(self.fcALI)
        self.mainWidget.setLayout(self.layout)
    
    def updateFC(self):
        print('FC')
        #self.gbw = self.gbwALI.getSliderValue()
        #self.gain = self.gainALI.getSliderValue()
        
    def closeEvent(self, event):
        QApplication.quit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())