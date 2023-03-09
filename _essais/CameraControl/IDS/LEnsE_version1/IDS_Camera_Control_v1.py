# -*- coding: utf-8 -*-
'''
IDS Camera simple application control
(except XS and USB3 versions)
    - Finding cameras on USB2 ports
    - Showing live pictures from camera

This application is based on pyueye library and IDS Camera drivers need to be installed
This application requires the following Python libraries : 
    opencv2, numpy, PyQt5
This application requires the LEnsE_version1.ui file (QTDesigner)

Author : Julien VILLEMEJANE
Laboratoire d Enseignement Experimental - Institut d Optique Graduate School
Version : 1.0 - 2023-03-08
'''

#   Libraries to import
# Camera
from pyueye import ueye
import camera
# Graphical interface
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (
    QApplication, QDialog, QMainWindow, QMessageBox, QWidget
)
from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap, QImage

# Standard
import numpy as np
import cv2
import sys

#-----------------------------------------------------------------------------------------------


class MainWindow(QMainWindow):
    '''
    Graphical Interface for IDS Camera control class
    '''
    
    def __init__(self):
        '''
        Constructor of the MainWindow class

        Returns
        -------
        None.

        '''
        super().__init__(parent=None)
        
        # Camera
        self.camera = None 
        self.max_width = 0
        self.max_height = 0     
        
        # Graphical interface
        loadUi("LEnsE_version1.ui", self)
        self.cameraInfo.setText('LEnsE')
        self.cameraExposureInfo.setText('Exposure : NO CAMERA')
        self.refreshBt.setEnabled(False)
        self.initListCamera()
        self.refreshBt.clicked.connect(self.refreshGraph)
        self.connectBt.clicked.connect(self.connectCamera)
        self.closeBt.clicked.connect(self.closeApp)
        self.refreshListBt.clicked.connect(self.initListCamera)
        
        # Other variables
        self.frameWidth = self.cameraDisplay.width()
        self.frameHeight = self.cameraDisplay.height()
        
        
    def refreshGraph(self):
        '''
        Refresh the frame with a new image.

        Returns
        -------
        None.

        '''
        array = self.camera.get_image()
        X, Y, W, H = self.camera.get_aoi()
        frame = np.reshape(array,(W, H, -1))
        frame = cv2.resize(frame, dsize=(self.frameWidth, self.frameHeight), interpolation=cv2.INTER_CUBIC)
        image = QImage(frame, frame.shape[1],frame.shape[0], frame.shape[1], QImage.Format_Grayscale8)
        pmap = QPixmap(image)
        self.cameraDisplay.setPixmap(pmap)
        
    
    def initListCamera(self):
        '''
        Initialize the list of the USB IDS Camera connected to the computer

        Returns
        -------
        Complete the list box of the graphical interface with the list of cameras.

        '''
        self.nb_cam = camera.get_nb_of_cam()
        self.cameraInfo.setText('Cam Nb = '+str(self.nb_cam))
        if(self.nb_cam > 0):
            self.cameraList = camera.get_cam_list() 
            self.cameraListCombo.clear()
            for i in range(self.nb_cam):
                cam = self.cameraList[i]
                self.cameraListCombo.addItem(f'{cam[2]} (SN : {cam[1]})')
                
    def connectCamera(self):
        '''
        Event link to the connect button of the GUI.

        Returns
        -------
        None.

        '''
        self.connectBt.setEnabled(False)
        self.refreshBt.setEnabled(True)
        self.connectBt.setText('Connected')
        
        self.selectedCamera = self.cameraListCombo.currentIndex()
        self.camera = camera.uEyeCamera(self.selectedCamera)
        
        self.max_width = self.camera.get_sensor_max_width()
        self.max_height = self.camera.get_sensor_max_height()
        self.camera.set_exposure(0.9)
        self.cameraExposureInfo.setText(f'Exposure : {self.camera.get_exposure()} ms')
        self.camera.set_colormode(ueye.IS_CM_MONO8)
        self.camera.set_aoi(0, 0, self.max_width-1, self.max_height-1)
        self.camera.alloc()
        self.camera.capture_video()
        self.refreshGraph()
    
    def closeApp(self):
        self.close()
        self.closeEvent(None)
        
    def closeEvent(self, event):
        if(self.camera != None):
            self.camera.stop_camera()
        QApplication.quit()

        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
