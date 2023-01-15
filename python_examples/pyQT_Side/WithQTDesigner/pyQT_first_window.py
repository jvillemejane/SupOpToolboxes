# -*- coding: utf-8 -*-
"""
First application with pyQT5 / Spyder 
    Interface designed with QT Designer - mainWindow.ui

Author : Julien VILLEMEJANE
Laboratoire d Enseignement Experimental - Institut d Optique Graduate School
Created on Sat Jan 14 20:34:05 2023

@author: julien.villemejane
"""

import sys

from PyQt5.QtWidgets import (
    QApplication, QDialog, QMainWindow, QMessageBox
)
from PyQt5.uic import loadUi

class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi("mainWindow.ui", self)
        self.tryMeButton.clicked.connect(self.tryMeButtonPressed)
        
    
    def tryMeButtonPressed(self):
        self.tryMeButton.setText('Text Changed')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())
