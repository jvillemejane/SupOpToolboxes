# -*- coding: utf-8 -*-
"""
Demo application : photonics / diffraction and Airy

Author : Julien VILLEMEJANE
Laboratoire d Enseignement Experimental - Institut d Optique Graduate School
Created on 18/mar/2023

@author: julien.villemejane
"""

from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QFileDialog
from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap, QImage, QPainter, QDoubleValidator
from PyQt5 import QtCore
import cv2

import numpy as np
from scipy.special import j1
from pyqtgraph import PlotWidget, plot, mkPen, PColorMeshItem

import sys  # We need sys so that we can pass argv to QApplication
import os

def isfloat(num):
    if(num is None): 
        return False 
    else: 
        try:
            float(num)
            return True
        except ValueError:
            return False


def diffraction_trou(x, y, d, L0, lam, D):
    eta = np.pi*d*np.sqrt(x**2+y**2)/(lam*D)
    return (4*L0*(j1(eta)/eta)**2)


"""
MainWindow class
"""
class MainWindow(QMainWindow):

    
    def __init__(self):
        super().__init__(parent=None)
        loadUi("./data/Demo_physics_airy.ui", self)
        
        imageSize = self.imageDisplay.size()
        self.imageWidth = imageSize.width()
        self.imageHeight = imageSize.height()
        self.pen = mkPen(color=(128, 128, 0), width=2)
        self.maxMean = 200
        self.simuDisplay = False
        ''' Logo LEnsE '''
        imageSize = self.lense_logo.size()
        logo = QPixmap("./data/IOGS-LEnsE-logo.jpg")
        logo = logo.scaled(imageSize.width(), imageSize.height(), QtCore.Qt.KeepAspectRatio)
        self.lense_logo.setPixmap(logo)
                
        """ Opening image """
        self.initImage()
        
        """ Airy Section """
        self.plotSection = PlotWidget()
        self.sectionLayout.addWidget(self.plotSection)
        self.plotSection.setBackground('w')
        self.plotSection.setYRange(0, 255, padding=0)
        self.plotSection.setXRange(0, self.imageOrW-1, padding=0)
        self.plotSection.setLabel('bottom', 'Position in px')
                
        """ """
        self.originSlider.setMaximum(self.imageOrW//10)
        self.originSlider.setMinimum(-self.imageOrW//10)
        self.origin = 0
        self.originSlider.setValue(self.origin)
        self.originValue.setText(f'{self.origin} px')
        
        self.opticalParams.setStyleSheet("background-color:#A4E1DA;");
        self.cameraParams.setStyleSheet("background-color:#CAE1A4;");
        self.positionParams.setStyleSheet("background-color:#E1AFA4;");
        
        self.distSlider.setMinimum(-100)
        self.distSlider.setMaximum(100)
        self.distSlider.setValue(0)
        self.distReal = 0
        self.distRealValue.setText(f'{self.distReal} cm')

        self.diamSlider.setMinimum(-100)
        self.diamSlider.setMaximum(100)
        self.diamSlider.setValue(0)
        self.diamReal = 0
        self.diamRealValue.setText(f'{self.diamReal} mm')

        self.lambdaSlider.setMinimum(-100)
        self.lambdaSlider.setMaximum(100)
        self.lambdaSlider.setValue(0)
        self.lambdaReal = 0
        self.lambdaRealValue.setText(f'{self.lambdaReal} nm')
        
        self.intensitySlider.setMinimum(-100)
        self.intensitySlider.setMaximum(100)
        self.intensitySlider.setValue(0)
        self.intensityRealValue.setText(f'{self.maxIntensity}')
        
        self.refreshGraph()
       
        """ Events """        
        self.positionSlider.valueChanged.connect(self.verticalChanged)
        self.meanSlider.valueChanged.connect(self.verticalChanged)
        self.logCheck.stateChanged.connect(self.verticalChanged)
        self.cameraBtn.clicked.connect(self.axisChanged)
        self.opticalBtn.clicked.connect(self.opticalUpdated)
        self.originSlider.valueChanged.connect(self.axisChanged)
        self.distSlider.valueChanged.connect(self.opticalChanged)
        self.diamSlider.valueChanged.connect(self.opticalChanged)
        self.lambdaSlider.valueChanged.connect(self.opticalChanged)
        self.intensitySlider.valueChanged.connect(self.opticalChanged)
        self.fileBt.clicked.connect(self.openFileImage)

    def initImage(self, fileName = ""):
        """ Opening image """
        if(fileName == ""):
            self.openImage("./data/airy_1mm.bmp")
        else:
            self.openImage(fileName)
        self.processRatio()
        """ Resizing image """
        self.resizeDispImage()
        """ Position Slider update """
        self.positionSlider.setMaximum(self.imageOrH) # depending on the height of the image
        self.positionSlider.setMinimum(1)
        
        """ Find Max intensity in gray image """
        self.maxIntensity = np.max(self.image)
        self.maxIntensityInd = np.argmax(self.image) // self.imageOrW 
        """ Set position of the slider to the maximum intensity line"""
        self.position = self.maxIntensityInd
        self.positionValue.setText(f'{self.position} px')
        self.positionSlider.setValue(self.maxIntensityInd)
        """ Mean Slider update """
        if((self.maxIntensityInd > self.maxMean) and (self.imageOrH-self.maxIntensityInd) > self.maxMean):
            self.meanSlider.setMaximum(self.maxMean)
        else:
            value = np.minimum(self.maxIntensityInd, self.imageOrH-self.maxIntensityInd)
            self.meanSlider.setMaximum(value)
        self.mean = int(self.meanSlider.value())
        self.meanValue.setText(f'{self.mean} px')
        
        """ Updating display of the image """
        self.updateImage()        

    def openFileImage(self):
        self.openFileNameDialog()
        self.initImage(self.fileName)
        self.refreshGraph()
    
    def openFileNameDialog(self):
        self.dlg = QFileDialog()
        options = QFileDialog.Options()
        options |= QFileDialog.FileMode.ExistingFiles
        self.fileName, _ = self.dlg.getOpenFileName(self,
                        "QFileDialog.getOpenFileName()", "",
                        "Images (*.png *.jpg *.bmp)", options=options)
        if self.fileName:
            # file name with extension
            self.realFileName = os.path.basename(self.fileName)
            self.openFileLabel.setText(os.path.splitext(self.realFileName)[0])
    
    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self,"QFileDialog.getOpenFileNames()", "","All Files (*);;Python Files (*.py)", options=options)
        if files:
            print(files)
    
    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","All Files (*);;Text Files (*.txt)", options=options)
        if fileName:
            print(fileName)
        self.openFileLabel.setText('Opening !')
                    

    def processRatio(self):
        self.scaleHeight = self.imageOrH / self.imageHeight
        self.ratioValue.setText(f'{np.round(self.scaleHeight, decimals=2)}')
    
    def resizeDispImage(self):
        self.newDim = (self.imageWidth, self.imageHeight)
        self.image_res = cv2.resize(self.image, self.newDim)
        self.pmap_res = QImage(self.image_res, self.imageWidth, self.imageHeight, self.imageWidth, QImage.Format_Grayscale8)     
        self.pmap_res = QPixmap(self.pmap_res)

    def openImage(self, imageName):
        self.image = cv2.imread(imageName, cv2.IMREAD_GRAYSCALE)
        self.imageOrW = self.image.shape[1]     # width of the original image
        self.imageOrH = self.image.shape[0]     # height of the original image

    def opticalUpdated(self):
        self.distSlider.setValue(0)
        self.diamSlider.setValue(0)
        self.lambdaSlider.setValue(0)
        self.opticalChanged()

    def opticalChanged(self):
        ''' Test Distance '''
        self.distance = self.distEdit.text()
        self.distance = self.testFloatValue(self.distance, "Distance")
        ''' Test Diameter '''
        self.diameter = self.diamEdit.text()
        self.diameter = self.testFloatValue(self.diameter, "Diameter")
        ''' Test WaveLength '''
        self.waveLength = self.lambdaEdit.text()
        self.waveLength = self.testFloatValue(self.waveLength, "WaveLength")
        ''' Intensity '''
        self.intensity = np.round(self.maxIntensity*(1+self.intensitySlider.value()/200.0), decimals=1)
        self.intensityRealValue.setText(f'{self.intensity}')
        ''' Updating values '''
        if((isfloat(self.distance)) and (isfloat(self.diameter)) and (isfloat(self.waveLength))):
            self.simuDisplay = True
            self.distance = np.round(self.distance*(1+self.distSlider.value()/1000.0), decimals=2)
            self.distRealValue.setText(f'{self.distance} cm')
            self.diameter = np.round(self.diameter*(1+self.diamSlider.value()/1000.0), decimals=2)
            self.diamRealValue.setText(f'{self.diameter} mm')            
            self.waveLength = np.round(self.waveLength*(1+self.lambdaSlider.value()/1000.0), decimals=2)
            self.lambdaRealValue.setText(f'{self.waveLength} nm')  
            k = self.diameter*1e-3/(self.distance*1e-2*self.waveLength*1e-9)
            J = (2*j1(np.pi*k*self.x_axis)/(np.pi*k*self.x_axis))**2
            self.simu = self.intensity*J
            ''' Simulated Airy '''
            self.simulatedAiry()
        else:
            self.simuDisplay = False
        self.refreshGraph()

    def simulatedAiry(self):
        min_ax = (-(self.imageOrW)+self.maxIntensityInd+self.origin)/2*self.taille_pix*1e-6
        max_ax = ((self.imageOrW)+self.maxIntensityInd+self.origin)/2*self.taille_pix*1e-6
        self.x_axis = np.linspace(min_ax, max_ax, self.imageOrW)
        min_ay = -(self.imageOrH)/2*self.taille_pix*1e-6
        max_ay = +(self.imageOrH)/2*self.taille_pix*1e-6
        self.y_axis = np.linspace(min_ay, max_ay, self.imageOrH)
        self.xx, self.yy = np.meshgrid(self.x_axis,self.y_axis) 
        print(self.diameter)
        self.zz = diffraction_trou(self.xx, self.yy, self.diameter*1e-3, 255, self.waveLength*1-9, self.distance*1e-2)
        maxZZ = np.max(self.zz) 
        self.zz2 = (self.zz / maxZZ * 255)
        self.zz3 = np.log10(self.zz2).astype(np.uint8)

        simuSize = self.simulationDisplay.size()
        simuWidth = simuSize.width()
        simuHeight = simuSize.height()
        newSimuDim = (simuWidth, simuHeight)
        self.simu_res = cv2.resize(self.zz3, newSimuDim)


        self.pmap_simu_res = QImage(self.simu_res, simuWidth, simuHeight, simuWidth, QImage.Format_Grayscale8)     
        self.pmap_simu_res = QPixmap(self.pmap_simu_res)
        
        """ Displaying image and line """
        self.simulationDisplay.setPixmap(self.pmap_simu_res)
        self.simulationDisplay.repaint()        

        
    def testFloatValue(self, value, message):
        if(value != ""):
            if(isfloat(value)):
                return float(value)
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText(f"Not a number - {message}")
                msg.setWindowTitle("Not a Number Value")
                msg.exec_()
                return
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText(f"Empty Value - {message}")
            msg.setWindowTitle("Empty Value")
            msg.exec_()
            return

    def axisChanged(self):
        self.origin = self.originSlider.value()
        self.originValue.setText(f'{self.origin} px')
        self.taille_pix = self.pixelEdit.text()
        self.taille_pix = self.testFloatValue(self.taille_pix, "Pixel Size")
        if(isfloat(self.taille_pix)):
            min_ax = (-(self.imageOrW)+self.maxIntensityInd+self.origin)/2*self.taille_pix*1e-6
            max_ax = ((self.imageOrW)+self.maxIntensityInd+self.origin)/2*self.taille_pix*1e-6
            self.x_axis = np.linspace(min_ax, max_ax, self.imageOrW)
        if(self.simuDisplay):
            self.opticalChanged()
        self.refreshGraph()

    def updateImage(self):
        self.image_line = np.array(self.image)
        """ Log scale on the image """
        if(self.logCheck.isChecked()):
            self.image_line = np.log(0.99*self.image_line+1)
            self.image_line = self.image_line / np.max(self.image_line) * 255
            self.image_line = np.trunc(self.image_line).astype('uint8')
        self.image_line[self.position-2:self.position+2,:] = 255
        
        if(self.mean != 0):
            self.image_line[(self.position-self.mean)-2:(self.position-self.mean)+2,:] = 200
            self.image_line[(self.position+self.mean)-2:(self.position+self.mean)+2,:] = 200
    
        self.image_res = cv2.resize(self.image_line, self.newDim)
        self.pmap_res = QImage(self.image_res, self.imageWidth, self.imageHeight, self.imageWidth, QImage.Format_Grayscale8)     
        self.pmap_res = QPixmap(self.pmap_res)
        
        """ Displaying image and line """
        self.imageDisplay.setPixmap(self.pmap_res)
        self.imageDisplay.repaint()


    def verticalChanged(self):
        """ Collecting new values """ 
        self.position = int(self.positionSlider.value())
        self.positionValue.setText(f'{self.position} px')
        self.mean = int(self.meanSlider.value())
        self.meanValue.setText(f'{self.mean} px')
        """ Limits verification """
        if(self.position-self.mean < 0):
            self.mean = self.position
        if(self.position+self.mean > self.imageOrH-1):
            self.mean = self.imageOrH-1-self.position
        self.meanSlider.setValue(self.mean)
        """ Refresh Graph """
        self.refreshGraph()
       
        
    def refreshGraph(self):
        """ Updatind Display of image """
        self.updateImage()
        """ Displaying data """
        self.plotSection.clear()
        if(isfloat(self.pixelEdit.text())):
            self.plotSection.setXRange(self.x_axis[0], self.x_axis[self.imageOrW-1], padding=0)
            self.plotSection.plot(self.x_axis, self.image[self.position-1,:], pen=self.pen)
            self.plotSection.setLabel('bottom', 'Position in m')
        else:
            self.plotSection.plot(self.image[self.position-1,:], pen=self.pen)
            self.plotSection.setXRange(0, self.imageOrW-1, padding=0)
            self.plotSection.setLabel('bottom', 'Position in px')
        
        if(self.mean != 0):
            penMean = mkPen(color=(255, 0, 128), width=2)
            meanValue = np.mean(self.image[self.position-self.mean:self.position+self.mean, :],axis=0)
            if(isfloat(self.pixelEdit.text())):
                self.plotSection.plot(self.x_axis, meanValue, pen=penMean)
            else:
                self.plotSection.plot(meanValue, pen=penMean)
        
        if(self.simuDisplay):
            penSimu = mkPen(color=(128, 0, 255), width=2)
            self.plotSection.plot(self.x_axis, self.simu, pen=penSimu)
    
    def closeEvent(self, event):
        QApplication.quit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
