# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 07:27:21 2023

@author: Villou
"""
import sys

from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QLabel, QPushButton, QVBoxLayout
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
        
        ''' Graphical Elements '''
        self.my_label = QLabel('<h1>Mon application est geniale</h1>')
        self.my_button = QPushButton("Appuyez !")
        ''' Layout Manager '''
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.my_label)
        self.layout.addWidget(self.my_button)
        self.mainWidget.setLayout(self.layout)
        ''' Events '''
        self.my_button.clicked.connect(self.buttonClicked)
    
    def buttonClicked(self):
        self.my_button.setText("! INACTIF !")
        self.my_button.setEnabled(False)
    
    def closeEvent(self, event):
        QApplication.quit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())