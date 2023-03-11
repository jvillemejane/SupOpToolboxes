# -*- coding: utf-8 -*-
"""
First application with pyQtGraph / Spyder in PyQt5 graphical QMainWindow

Author : Julien VILLEMEJANE
Laboratoire d Enseignement Experimental - Institut d Optique Graduate School
Created on Sat Jan 28 20:34:05 2023

@author: julien.villemejane
@see https://www.pythonguis.com/tutorials/plotting-pyqtgraph/
@see https://www.aranacorp.com/fr/afficher-un-signal-dans-pyqt-avec-pyqtgraph/
"""

from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (
    QApplication, QDialog, QMainWindow, QMessageBox, QWidget
)
from PyQt5.uic import loadUi

import sys
import numpy as np

SAMPLES = 10

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__(parent=None)
        loadUi("IHM_PyQtGraph_v1_inPyQt.ui", self)
        self.refreshBt.clicked.connect(self.refreshGraph)

        
        self.plotWidget = pg.PlotWidget()
        self.mainLayout.addWidget(self.plotWidget)
        
        self.x = np.linspace(0, SAMPLES, SAMPLES)
        self.data = np.random.random_sample(size=SAMPLES)

        self.plotWidget.setBackground('w')
        self.plotWidget.setYRange(0, 1, padding=0)

        self.pen = pg.mkPen(color=(255, 0, 0), width=5)
        self.plot1 = self.plotWidget.plot(self.x, self.data, pen=self.pen)
        
    def refreshGraph(self):
        print("refresh")
        self.plotWidget.removeItem(self.plot1)
        self.data = np.random.random_sample(size=SAMPLES)
        self.plot1 = self.plotWidget.plot(self.x, self.data, pen=self.pen)

    def closeEvent(self, event):
        QApplication.quit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())