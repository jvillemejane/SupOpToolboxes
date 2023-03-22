# -*- coding: utf-8 -*-
"""
Demo application : basics signals and Fourier transform

Author : Julien VILLEMEJANE
Laboratoire d Enseignement Experimental - Institut d Optique Graduate School
Created on 11/mar/2023

@author: julien.villemejane
"""

from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap, QImage
from PyQt5 import QtCore


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
        loadUi("./data/Demo_signals_fft_convolution.ui", self)
        ''' Logo LEnsE '''
        self.lense_logo.resize(300, 200)
        imageSize = self.lense_logo.size()
        logo = QPixmap("./data/IOGS-LEnsE-logo.jpg")
        logo = logo.scaled(imageSize.width(), imageSize.height(), QtCore.Qt.KeepAspectRatio)
        self.lense_logo.setPixmap(logo)
        
        """ Window Size """
        self.width = self.size().width()
        self.height = self.size().height()
        
        self.freqOffsetLabel.setStyleSheet('background-color: lightgreen')
        self.samplesNumberLabel.setStyleSheet('background-color: lightblue')
        
        """ """
        self.maxNumber = 1001
        self.offsetSlider.setMinimum(-100)
        self.offsetSlider.setMaximum(100)
        self.offsetSlider.setValue(0)
        self.offset = self.offsetSlider.value()
        self.offsetValue.setText(f'{self.offset}')
        self.numberSlider.setMinimum(10)
        self.numberSlider.setMaximum(self.maxNumber//20)
        self.numberSlider.setValue(self.maxNumber//20)
        self.number = self.numberSlider.value()
        self.numberValue.setText(f'{self.number}')
        
        """ Signal Widget """
        self.plotSignalWidget = PlotWidget(title='Sinus Cardinal')
        self.signalLayout.addWidget(self.plotSignalWidget)
        self.plotSignalWidget.setBackground('w')
        self.plotSignalWidget.setYRange(-0.3, 1.1)
        
        
        """ Events """        
        self.offsetSlider.valueChanged.connect(self.freqChanged)
        self.numberSlider.valueChanged.connect(self.freqChanged)
        self.onSig.stateChanged.connect(self.freqChanged)
        self.absSig.stateChanged.connect(self.freqChanged)
        self.resetBt.clicked.connect(self.resetGraph)
        
        self.refreshGraph()

    def freqChanged(self):
        self.refreshGraph()
        
    def resetGraph(self):
        self.offset = 0
        self.offsetValue.setText(f'{self.offset}')
        self.offsetSlider.setValue(self.offset)
        self.number = self.maxNumber // 20
        self.numberValue.setText(f'{self.number}')
        self.numberSlider.setValue(self.number)
        self.absSig.setChecked(False)
        self.onSig.setChecked(False)
        self.refreshGraph()
        
        
    def refreshGraph(self):
        """ Collecting new values """        
        self.offset = (self.offsetSlider.value() / 10.0)
        self.offsetValue.setText(f'{self.offset}')
        self.number = self.numberSlider.value()
        self.numberValue.setText(f'{self.number}')
        
        """ Signals generation"""
        self.x, self.signal, self.xFT, self.signalFT = self.generate_signals()
        
        """ Displaying data """
        self.plotSignalWidget.clear()
        penSinC = mkPen(color=(128, 128, 0), width=3)
        penSinCFT = mkPen(color=(0, 0, 255), width=4)
        
        self.plotSignalWidget.plot(self.x, self.signal, pen=penSinC)
        if(self.onSig.isChecked()):
            self.plotSignalWidget.plot(self.xFT, self.signalFT, pen=penSinCFT)
    
    def generate_signals(self):
        x = np.linspace(-10, 10, self.maxNumber)
        y = np.sinc(x + self.offset)
        if(self.absSig.isChecked()):
            y = np.abs(y)
        if(self.onSig.isChecked()):
            x2 = np.linspace(-10, 10, self.number)
            y2 = np.sinc(x2 + self.offset)
            if(self.absSig.isChecked()):
                y2 = np.abs(y2)
        else:
            x2 = 0
            y2 = 0
        return x, y, x2, y2
    
    def closeEvent(self, event):
        QApplication.quit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())