# -*- coding: utf-8 -*-
"""
Second application to send and receive data from a Nucleo board
based on PyQt5 Window
    

Author : Julien VILLEMEJANE
Laboratoire d Enseignement Experimental - Institut d Optique Graduate School
Created on Tue Jan 26 20:34:05 2023

@author: julien.villemejane
"""

from serial import Serial
import serial.tools.list_ports

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (
    QApplication, QDialog, QMainWindow, QMessageBox, QWidget
)
from PyQt5.uic import loadUi


class MyWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi("Python_to_Nucleo_ihm_v1.ui", self)
        # To obtain the list of the communication ports
        self.ports = serial.tools.list_ports.comports()
        self.ports.sort()
        # To clear the list on the window
        self.comPortList.clear()
        # To add all the communication ports to the list
        for port, desc, hwid in sorted(self.ports):
            self.comPortList.addItem(f"{port} [{desc}]")
        # To link click to actions
        self.connectBt.clicked.connect(self.connectToNucleo)
        self.appQuitBt.clicked.connect(self.quitApp)
        self.ledOnBt.clicked.connect(self.switchOnLed)
        self.ledOffBt.clicked.connect(self.switchOffLed)
        # To create an empty serial connection
        self.serNuc = Serial()
        self.connected = 0
            
    def __del__(self):
        self.serNuc.close()
    
    def connectToNucleo(self):
        if(self.connected == 0):
            self.selectPort = self.ports[self.comPortList.currentIndex()].name
            self.serNuc = Serial(self.selectPort, 115200)
            self.connected = 1
            self.connectBt.setEnabled(False)
            self.ledOnBt.setEnabled(True)
            self.ledOffBt.setEnabled(True)
            self.lenseLabel.setText(f"Connected to {self.selectPort}")
            
    def quitApp(self):
        self.serNuc.close()
        self.close()
        
    def switchOnLed(self):
        if(self.connected):
            self.serNuc.write(bytes('a','utf-8'))
            while self.serNuc.inWaiting() != 0:
                pass
            self.data = self.serNuc.read(1)
            self.lenseLabel.setText(f"Switch On Led ({self.data})")

    def switchOffLed(self):
        if(self.connected):
            self.serNuc.write(bytes('e','utf-8'))
            while self.serNuc.inWaiting() != 0:
                pass
            self.data = self.serNuc.read(1)
            self.lenseLabel.setText(f"Switch Off Led ({self.data})")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    win = MyWindow()
    win.show()
    sys.exit(app.exec())