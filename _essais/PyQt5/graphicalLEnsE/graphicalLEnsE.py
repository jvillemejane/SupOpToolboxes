# -*- coding: utf-8 -*-
"""
Signal Processing libraries of functions

Author : Julien VILLEMEJANE
Laboratoire d Enseignement Experimental - Institut d Optique Graduate School
Version : 1.0 - 2022-12-01
"""

import numpy as np

from PyQt5.QtWidgets import (QWidget, QGridLayout, QLabel, QSlider,
                             QLineEdit, QPushButton, QMessageBox)
from PyQt5.QtCore import Qt, pyqtSignal, QObject

styleH = "font-size:22px; padding:10px; color:Navy;"
styleV = "font-size:18px; padding:5px;"

"""
Signals class
"""
class Signals(QObject):
    asignal = pyqtSignal(str)

    def __init__(self):
        super(Signals, self).__init__()

    def sendSignal(self):
        self.asignal.emit('Hi, im a signal')

"""
LabelBlock class
"""
class labelBlock(QWidget):
    
    def __init__(self, name=""):
        super().__init__()
        self.units = ''
        self.realValue = ''
        ''' Layout Manager '''
        self.layout = QGridLayout()
        ''' Graphical Objects '''
        self.name = QLabel(name)
        self.value = QLabel('')
        self.name.setStyleSheet(styleH)
        self.value.setStyleSheet(styleH)
        ''' Adding GO into the widget layout '''
        self.layout.addWidget(self.name, 1, 0)  # Position 1,0 / one cell
        self.layout.addWidget(self.value, 1, 1)  # Position 1,1 / one cell
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
        ''' Layout Manager '''
        self.layout = QGridLayout()
        ''' Graphical Objects '''
        self.name = QPushButton(name)
        self.userValue = QLineEdit()
        self.name.setStyleSheet(styleH)
        self.name.setFixedWidth(200)
        self.userValue.setStyleSheet(styleH)
        self.value = QLabel('')
        self.value.setStyleSheet(styleV)
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setEnabled(False)
        self.minSlider = 0
        self.maxSlider = self.maxValue*self.ratioSlider
        self.sliderValue = self.realValue
        self.slider.setMinimum(self.minSlider)
        self.slider.setMaximum(self.maxSlider)
        self.slider.setValue(self.sliderValue)
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
        
    
    def getName(self):
        return self.name
    
    def setName(self, name):
        self.name = name
        
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
        self.slider.setEnabled(True)
        self.asignal.emit('T')
    
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
    
    def sliderChanged(self, event):
        if(self.percent):
            self.sliderValue = self.realValue * (1 + (float(self.slider.value()) / (100.0) / self.ratioSlider))
            self.sliderValue = np.round(self.sliderValue, decimals=2)
        else:
            self.sliderValue = self.slider.value() / self.ratioSlider
        self.updateDisplay()
        self.asignal.emit('S')
    
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
    
   