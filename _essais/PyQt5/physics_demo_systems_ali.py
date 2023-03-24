# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 07:27:21 2023

@author: Villou
"""
import sys
import numpy as np

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
        self.gainALI = gL.sliderBlock("GAIN ALI")
        self.gainALI.setPercent(True, 50)
        self.gbwALI = gL.sliderBlock("GBW ALI")
        self.gbwALI.setUnits('Hz')
        self.gbwALI.setPercent(True, 20)
        self.gbwALI.asignal.connect(self.updateFC)
        self.gainALI.asignal.connect(self.updateFC)
        self.fcALI = gL.labelBlock('Cut Freq')
        self.fcALI.setUnits('Hz')
        
        ''' Layout Manager '''
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.gainALI)
        self.layout.addWidget(self.gbwALI)
        self.layout.addWidget(self.fcALI)
        self.mainWidget.setLayout(self.layout)
    
    def updateFC(self, sig):
        self.gbw = self.gbwALI.getRealValue()
        self.gain = self.gainALI.getRealValue()
        self.fc = np.round(self.gbw / self.gain, decimals=2)
        self.fcALI.setValue(self.fc)
        
    def closeEvent(self, event):
        QApplication.quit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())