# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 07:27:21 2023

@author: Villou
"""
import sys
import numpy as np

from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget, 
                             QLabel, QPushButton, 
                             QVBoxLayout, QHBoxLayout)

import graphicalLEnsE as gL
from pyqtgraph import PlotWidget, plot, mkPen


class graphWidget(QWidget):
    def __init__(self, name=''):
        super().__init__()    
        self.plotLayout = QVBoxLayout()
        self.setLayout(self.plotLayout)
        
        self.plotSection = PlotWidget()
        self.plotLayout.addWidget(self.plotSection)

"""
MainWindow class
"""
class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__(parent=None)
        ''' Main Window parameters '''
        self.setWindowTitle("Ma première application PyQt")
        self.setGeometry(100, 100, 800, 600)
        self.mainWidget = QWidget()
        self.setCentralWidget(self.mainWidget)
        
        self.mainLayout = QHBoxLayout()
        self.mainWidget.setLayout(self.mainLayout)        
        
        # Right widget
        self.rightWidget = QWidget()
        self.rightLayout = QVBoxLayout()
        self.rightLayout.addWidget(gL.graph1D('Test'))
        #self.widgetPlot = graphWidget('Test')
        self.rightWidget.setLayout(self.rightLayout)
        
        # Left widget
        self.leftWidget = QWidget()
        self.leftLayout = QVBoxLayout()
        self.leftLayout.addWidget(QLabel('Left 1'))
        self.leftLayout.addWidget(QLabel('Left 2'))
        self.leftWidget.setLayout(self.leftLayout)
        
        
        # Main Layout
        self.mainLayout.addWidget(self.leftWidget)        
        self.mainLayout.addWidget(self.rightWidget)
        
        
        
    def closeEvent(self, event):
        QApplication.quit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())