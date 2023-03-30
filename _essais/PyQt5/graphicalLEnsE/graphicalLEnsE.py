# -*- coding: utf-8 -*-
"""
Signal Processing libraries of functions

Author : Julien VILLEMEJANE
Laboratoire d Enseignement Experimental - Institut d Optique Graduate School
Version : 1.0 - 2022-12-01
"""

import numpy as np

from PyQt5.QtWidgets import (QWidget, 
                             QGridLayout, QVBoxLayout, 
                             QLabel, QSlider, QLineEdit, QPushButton, 
                             QMessageBox, QCheckBox)
from PyQt5.QtCore import Qt, pyqtSignal, QObject, QRect

from pyqtgraph import PlotWidget, plot, mkPen

styleH1 = "font-size:20px; padding:10px; color:Navy; border-top: 1px solid Navy;"
styleH = "font-size:18px; padding:10px; color:Navy;"
styleV = "font-size:14px; padding:5px; "


"""
Graph1D class
"""
class graph1D(QWidget):
    
    def __init__(self, name=''):
        super().__init__() 
        self.name = name
        ''' '''
        self.yRangeMin = -1
        self.yRangeMax = 1
        self.xRangeMin = 0
        self.xRangeMax = 1
        self.length = 1001
        self.legendBottom = ''
        self.legend = []
        self.pen = []
        self.pen.append(mkPen(color=(80, 128, 80), width=3))
        self.pen.append(mkPen(color=(128, 192, 0), width=6))
        self.pen.append(mkPen(color=(80, 80, 128), width=3))
        self.pen.append(mkPen(color=(0, 128, 192), width=6))
        self.pen.append(mkPen(color=(128, 80, 80), width=3))
        self.pen.append(mkPen(color=(192, 128, 0), width=6))
        self.nbSignal = 1
        ''' Layout '''
        self.plotLayout = QVBoxLayout()
        self.setLayout(self.plotLayout)
        ''' Graph section '''
        self.plotSection = PlotWidget()
        self.plotLayout.addWidget(self.plotSection)
        
        self.plotSection.setBackground('black')
        
        #self.plotSection.setYRange(self.yRangeMin, self.yRangeMax, padding=0)
        self.plotSection.setLabel('bottom', self.legendBottom)
        self.xData = np.linspace(self.xRangeMin, self.xRangeMax, self.length)
        self.yData = np.sin(self.xData)
        
        self.refreshGraph()
        
    def setYRange(self, ymin, ymax):
        self.yRangeMin = ymin
        self.yRangeMax = ymax
        self.plotSection.setYRange(self.yRangeMin, self.yRangeMax, padding=0)
        
    
    def setData(self, x, y):
        self.xData = x
        self.yData = y
        
        try:
            self.nbSignal = x.shape[1]
            pass
        except Exception:
            self.nbSignal = 1
            pass
                
    def refreshGraph(self, logX=False, logY=False):
        """ Displaying data """
        self.plotSection.clear()
        self.plotSection.addLegend()
        self.plotSection.showGrid(x = True, y = True, alpha = 1.0)
        # Test the shape of the data to plot different curves
        
        if(self.nbSignal > 1):
            for k in range(self.nbSignal):
                if(self.legend):
                    self.plotSection.plot(self.xData[:,k], self.yData[:,k], 
                                      pen=self.pen[k], name=self.legend[k])
                else:
                    self.plotSection.plot(self.xData[:,k], self.yData[:,k], 
                                      pen=self.pen[k])
            self.plotSection.setLogMode(logX, logY)
        else:
            self.plotSection.plot(self.xData, self.yData, pen=self.pen[1])
            self.plotSection.setLogMode(logX, logY)       
    
    def setLegend(self, legends):
        self.legend = legends
        

"""
TitleBlock class
"""
class titleBlock(QWidget):
    tBsignal = pyqtSignal(str)
    
    def __init__(self, title='', checkBox=False):
        super().__init__()
        self.title = title
        self.enabled = True
        self.checkBox = checkBox
        ''' Layout Manager '''
        self.layout = QGridLayout()
        ''' Graphical Objects '''
        self.name = QLabel(self.title)
        self.name.setMaximumWidth(300)
        self.name.setStyleSheet(styleH1)
        self.checkB = QCheckBox('EN')
        self.checkB.setStyleSheet(styleV)
        ''' Adding GO into the widget layout '''
        self.layout.addWidget(self.name, 1, 0)  # Position 1,0 / one cell
        if(self.checkBox):
            self.layout.addWidget(self.checkB, 1, 1)
            self.checkB.toggled.connect(self.checkedBox)
        self.setLayout(self.layout)
    
    def setTitle(self, value):
        self.title = value 
        self.name.setText(self.title)
        
    def checkedBox(self):
        self.tBsignal.emit('tB')
    
    def isChecked(self):
        return self.checkB.isChecked()
    
    def setChecked(self, value):
        self.checkB.setCheckState(value)


"""
LabelBlock class
"""
class labelBlock(QWidget):
    lBsignal = pyqtSignal(str)
    
    def __init__(self, name='', checkBox=False):
        super().__init__()
        self.units = ''
        self.realValue = ''
        self.enabled = True
        self.checkBox = checkBox
        ''' Layout Manager '''
        self.layout = QGridLayout()
        ''' Graphical Objects '''
        self.name = QLabel(name)
        self.name.setMaximumWidth(200)
        self.value = QLabel('')
        self.value.setMaximumWidth(300)
        self.name.setStyleSheet(styleH1)
        self.value.setStyleSheet(styleH)
        self.checkB = QCheckBox('EN')
        ''' Adding GO into the widget layout '''
        self.layout.addWidget(self.name, 1, 0)  # Position 1,0 / one cell
        self.layout.addWidget(self.value, 1, 1)  # Position 1,1 / one cell
        if(self.checkBox):
            self.layout.addWidget(self.checkB, 1, 2)
            self.checkB.toggled.connect(self.checkedBox)
        self.setLayout(self.layout)
    
    def setValue(self, value):
        self.realValue = value 
        self.updateDisplay()
    
    def setUnits(self, units):
        self.units = units

    def updateDisplay(self):
        displayValue = self.realValue
        displayUnits = self.units
        if(self.realValue / 1000 >= 1):
            displayValue = self.realValue / 1000
            displayUnits = 'k'+self.units
        if(self.realValue / 1e6 >= 1):
            displayValue = self.realValue / 1e6
            displayUnits = 'M'+self.units
            
        textT = f'{displayValue} {displayUnits}'
        self.value.setText(textT)
        
    def checkedBox(self):
        self.lBsignal.emit('lB')


"""
SliderBlock class
"""
class sliderBlock(QWidget, QObject):
    asignal = pyqtSignal(str)
        
    def __init__(self, name="", percent=False):
        super(sliderBlock, self).__init__()

        ''' '''
        self.percent = percent
        self.minValue = 0
        self.maxValue = 100
        self.ratioSlider = 10.0
        self.realValue = 1
        self.enabled = True
        ''' Layout Manager '''
        self.layout = QGridLayout()
        ''' Graphical Objects '''
        self.name = QPushButton(name)
        self.userValue = QLineEdit()
        self.userValue.setMinimumWidth(100)
        self.userValue.setMaximumWidth(200)
        self.name.setStyleSheet(styleH)
        self.name.setMinimumWidth(100)        
        self.userValue.setMaximumWidth(300)
        self.userValue.setStyleSheet(styleH)
        self.value = QLabel('')
        self.value.setStyleSheet(styleV) 
        self.value.setMaximumWidth(300)
        self.slider = QSlider(Qt.Horizontal)
        self.minSlider = 0
        self.maxSlider = self.maxValue*self.ratioSlider
        self.sliderValue = self.realValue
        self.slider.setMinimum(self.minSlider)
        self.slider.setMaximum(self.maxSlider)
        self.slider.setValue(self.sliderValue)
        self.slider.setMinimumWidth(100)
        self.slider.setMaximumWidth(200)
        ''' '''
        self.units = ''
        
        ''' Adding GO into the widget layout '''
        self.layout.addWidget(self.name, 1, 0)  # Position 1,0 / one cell
        self.layout.addWidget(self.userValue, 1, 1)  # Position 1,1 / one cell
        self.layout.addWidget(self.value, 2, 0)  # Position 2,0 / one cell
        self.layout.addWidget(self.slider, 2, 1)  # Position 2,0 / one cell
        self.setLayout(self.layout)
        
        ''' Events '''      
        self.slider.valueChanged.connect(self.sliderChanged)
        self.name.clicked.connect(self.valueChanged)
        
        self.initBlock()

    def initBlock(self):
        self.userValue.setText('1')
        self.updateDisplay()
        
    def getName(self):
        return self.name
    
    def setName(self, name):
        self.name = name
        
    def setEnabled(self, value):
        self.enabled = value
        self.updateGUI()
        
    def updateGUI(self):
        self.slider.setEnabled(self.enabled)
        self.userValue.setEnabled(self.enabled)
        self.name.setEnabled(self.enabled)
        
    def isNumber(self, value, min='', max=''):
        minOk = False
        maxOk = False
        if(str(value).isnumeric()):
            if(min > max):
                min, max = max, min                
            if((min != '') and (int(value) >= min)):
                minOk = True
            if((max != '') and (int(value) <= max)):
                maxOk = True
            if(minOk != maxOk):
                return False
            else:
                return True                    
        else:
            return False
        
    def valueChanged(self, event):
        value = self.userValue.text()
        value2 = value.replace('.','',1)
        value2 = value2.replace('e','',1)
        value2 = value2.replace('-','',1)
        if(value2.isdigit()):
            self.realValue = float(value)
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText(f"Not a number")
            msg.setWindowTitle("Not a Number Value")
            msg.exec_()
            self.realValue = 1
            self.userValue.setText(str(self.realValue))
        self.sliderValue = self.realValue
        self.updateDisplay()
        self.slider.setValue(0)
        self.asignal.emit('S')    
    
    def sliderChanged(self, event):
        if(self.percent):
            self.sliderValue = self.realValue * (1 + (float(self.slider.value()) / (100.0) / self.ratioSlider))
            self.sliderValue = np.round(self.sliderValue, decimals=6)
        else:
            self.sliderValue = self.slider.value() / self.ratioSlider
        self.updateDisplay()
        self.asignal.emit('S')
    
    def setPercent(self, value, maxValue=100):
        self.percent = value
        self.minValue = -maxValue
        self.minSlider = self.minValue*self.ratioSlider
        self.maxValue = maxValue
        self.maxSlider = self.maxValue*self.ratioSlider
        self.slider.setMinimum(self.minSlider)
        self.slider.setMaximum(self.maxSlider)
        self.slider.setValue(0)
        
    def setMinMaxSlider(self, min, max):
        self.minSlider = min
        self.maxSlider = max
        self.minSlider = self.minValue*self.ratioSlider
        self.maxSlider = self.maxValue*self.ratioSlider
        self.slider.setMinimum(self.minSlider)
        self.slider.setMaximum(self.maxSlider)
    
    def setUnits(self, units):
        self.units = units
    
    def updateDisplay(self):
        displayValue = self.sliderValue
        displayUnits = self.units
        if(self.realValue / 1000 >= 1):
            displayValue = self.sliderValue / 1000
            displayUnits = 'k'+self.units
        if(self.realValue / 1e6 >= 1):
            displayValue = self.sliderValue / 1e6
            displayUnits = 'M'+self.units
            
        textT = f'{displayValue} {displayUnits}'
        self.value.setText(textT)        
    
    def getSliderValue(self):
        return self.slider.value()/self.ratioSlider
    
    def getRealValue(self):
        return self.sliderValue

    def getUserValue(self):
        return float(self.userValue.text())
    

    def getMaxValue(self):
        if(self.percent):
            maxValue = float(self.userValue.text()) * (1 + (float(self.maxSlider) / (100.0) / self.ratioSlider))
            maxValue = np.round(maxValue, decimals=6)
        else:
            maxValue = (float(self.userValue.text()) + self.maxSlider) / self.ratioSlider
        return maxValue

    def setValue(self, value):
        self.sliderValue = value
        self.userValue.setText(str(value))
        self.slider.setValue(value)
    
  
    
if __name__ == '__main__':
    print("PyQt5 - Graphical Elements / from LEnsE")