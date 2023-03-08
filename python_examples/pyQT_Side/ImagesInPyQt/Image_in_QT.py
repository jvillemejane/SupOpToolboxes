# -*- coding: utf-8 -*-
'''
Image in QLabel via QPixMap

This application requires the following Python libraries : 
    opencv2, numpy, PyQt5
This application requires the Image_in_QT.ui file (QTDesigner)

Author : Julien VILLEMEJANE
Laboratoire d Enseignement Experimental - Institut d Optique Graduate School
Version : 1.0 - 2023-03-08
'''

#   Libraries to import
# Graphical interface
from PyQt5 import QtGui
from PyQt5.QtWidgets import ( QApplication, QMainWindow )
from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap, QImage

# Standard
import numpy as np
import cv2
import sys

#-----------------------------------------------------------------------------------------------


class MainWindow(QMainWindow):
    '''
    
    '''
    
    def __init__(self):
        '''
        

        Returns
        -------
        None.

        '''
        super().__init__(parent=None)
        
        # Graphical interface
        loadUi("Image_in_QT.ui", self)
        self.refreshBt.clicked.connect(self.refreshGraph)
        self.closeBt.clicked.connect(self.closeApp)

        self.refreshGraph()
        
    def refreshGraph(self):
        '''
        Refresh the frame with a new image.

        Returns
        -------
        None.

        '''
        print("refresh")
        
        #image=cv2.imread('python.png')
        image = np.random.randint(255, size=(144, 144),dtype=np.uint8)
        print(type(image))
        image = QImage(image, image.shape[1],image.shape[0], image.shape[1], QImage.Format_Grayscale8)

        pix = QPixmap(image)
        self.cameraDisplay.setPixmap(QtGui.QPixmap(pix))
                
    
    
    def closeApp(self):
        self.close()
        self.closeEvent(None)
        
    def closeEvent(self, event):
        QApplication.quit()
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
