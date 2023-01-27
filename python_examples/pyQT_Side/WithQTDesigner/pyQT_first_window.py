# -*- coding: utf-8 -*-
"""
First application with pyQT5 / Spyder 
    Interface designed with QT Designer - mainWindow.ui
    This example requires the mainWindow.ui file (created on QTDesigner)

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
    """
    A class to manage a main Window of a QT Application (QT5)
    
    This class is based on QMainWindow class from pyQT5.
    It's a simple example with a window designed with QTDesigner (mainWindow.ui)
    The Try Me button text changes when you click on it.
    ...

    Attributes
    ----------
    tryMeButton: QButton
        a button that can be clicked - coming from the mainWindow.ui design

    Methods
    -------
    tryMeButtonPressed()
        Changes the text of the TryMe button when it press
    """
    
    def __init__(self, parent=None):
        """
        Initializes the main window of the application

        Parameters
        ----------
        parent : argv from sys
            Default is None.

        Returns
        -------
        None.

        """
        super().__init__(parent)
        loadUi("mainWindow.ui", self)
        self.tryMeButton.clicked.connect(self.tryMeButtonPressed)
        
    
    def tryMeButtonPressed(self):
        """
        Modifies text of TryMe button when it press

        Returns
        -------
        None.

        """
        self.tryMeButton.setText('Text Changed')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())
