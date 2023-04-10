# -*- coding: utf-8 -*-
"""
Physics Demo / Linear Amplifier 1st order model and control system

Author : Julien VILLEMEJANE
Laboratoire d Enseignement Experimental - Institut d Optique Graduate School
Version : 1.0 - 2022-12-01
"""
import sys
import numpy as np

from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget, 
                             QLabel, QPushButton, 
                             QVBoxLayout, QHBoxLayout, QGridLayout)

import graphicalLEnsE as gL
import systemSimu as sS
import control as ct


'''
MainWindow class
'''
class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__(parent=None)
        
        RT = 1e5
        Re = 1e6
        Ce = 120
        Cphd = 70
        
        
        ''' Main Window parameters '''
        self.setWindowTitle("Ma première application PyQt")
        self.setGeometry(100, 100, 1000, 800)
        self.mainWidget = QWidget()
        self.setCentralWidget(self.mainWidget)
        
        ''' Graphical elements '''
        # ALI
        self.gainALI = gL.sliderBlock("Gain ALI")
        self.gainALI.setPercent(True, 50)
        self.gbwALI = gL.sliderBlock("GBW ALI")
        self.gbwALI.setUnits('Hz')
        self.gbwALI.setPercent(True, 50)
        self.fcALI = gL.labelBlock('Cut Freq')
        self.fcALI.setUnits('Hz')
        
        self.labelALI = gL.titleBlock('ALI parameters')        
        self.labelALI.setMaximumWidth(300)
        self.labelALI.setStyleSheet("font-size:22px; font-weight:bold; padding:10px; color:Navy;")
        
        # Measurement
        self.labelMeasure = gL.titleBlock('Measurement')
        self.reLabel = gL.titleBlock('Osc. Resistance')
        self.reBack = gL.sliderBlock("Value")
        self.reBack.setValue(Re)
        self.reBack.setPercent(True, 90)
 
        self.cCLabel = gL.titleBlock('Cable capacitance')
        self.cCBack = gL.sliderBlock("Value (pF)")
        self.cCBack.setValue(Ce)
        self.cCBack.setPercent(True, 90)   
 
        # Photodetection
        self.labelPhD = gL.titleBlock('Photodetection')
        self.rtLabel = gL.titleBlock('Resistance RT')
        self.rtBack = gL.sliderBlock("Value")
        self.rtBack.setValue(RT)
        self.rtBack.setPercent(True, 90)
 
        self.cphdLabel = gL.titleBlock('diode capacitance')
        self.cphdBack = gL.sliderBlock("Value (pF)")
        self.cphdBack.setValue(Cphd)
        self.cphdBack.setPercent(True, 90)   
        
        
        ''' Layout Manager '''
        self.mainLayout = QGridLayout()
        self.mainWidget.setLayout(self.mainLayout)
        # Left area / ALI Parameters
        self.mainLayout.addWidget(self.labelALI, 0, 0)
        self.mainLayout.addWidget(self.gainALI, 1, 0, 3, 1)
        self.mainLayout.addWidget(self.gbwALI, 4, 0, 3, 1)
        self.mainLayout.addWidget(self.fcALI, 7, 0)
        # Center area / Graph
        self.graphT = gL.graph1D('Time dependent')
        self.graphF = gL.graph1D('Freq dependent')
        self.mainLayout.addWidget(self.graphT, 0, 1, 7, 1)
        self.mainLayout.addWidget(self.graphF, 7, 1, 7, 1)
        # Right Area / Feedback
        self.mainLayout.addWidget(self.labelMeasure, 0, 2)
        self.mainLayout.addWidget(self.reLabel, 1, 2)
        self.mainLayout.addWidget(self.reBack, 2, 2, 2, 1)
        self.mainLayout.addWidget(self.cCLabel, 4, 2)
        self.mainLayout.addWidget(self.cCBack, 5, 2, 2,1)
        
        self.mainLayout.addWidget(self.labelPhD, 7, 2)
        self.mainLayout.addWidget(self.rtLabel, 8, 2)
        self.mainLayout.addWidget(self.rtBack, 9, 2, 2, 1)
        self.mainLayout.addWidget(self.cphdLabel, 11, 2)
        self.mainLayout.addWidget(self.cphdBack, 12, 2, 2,1)
    
        self.mainLayout.setColumnStretch(0, 1)
        self.mainLayout.setColumnStretch(1, 4)
        self.mainLayout.setColumnStretch(2, 1)
        for k in range(13):
            self.mainLayout.setRowStretch(k, 1)
        
        ''' Graph Legends '''
        legends = ['','ALI',
                   '','FeedBack',
                   '','Closed Loop']
        self.graphT.setLegend(legends)
        
        ''' Events '''
        self.gbwALI.asignal.connect(self.updateFC)
        self.gainALI.asignal.connect(self.updateFC)
        self.reBack.asignal.connect(self.updateFC)
        self.rtBack.asignal.connect(self.updateFC)
        self.cCBack.asignal.connect(self.updateFC)
        self.cphdBack.asignal.connect(self.updateFC)
        
        ''' model for simulation '''
        self.simu = sS.systemSimulation()
        self.phDsys = sS.photodetection()
        
    def updateFC(self, sig):
        self.gbw = self.gbwALI.getRealValue()
        self.gain = self.gainALI.getRealValue()
        self.fc = np.round(self.gbw / self.gain, decimals=4)
        self.fcALI.setValue(self.fc)
        timeData, timeSignal, timeDataZ, timeSignalZ, freqData, freqSignalM = self.updateModel()
        self.updateGraph(timeData, timeSignal, timeDataZ, timeSignalZ, freqData, freqSignalM)
    
    def updateModel(self):
        ''' Simulation parameters '''
        samplesT = 1001
        self.simu.setTimeParams(0, 0.0002, samplesT)
        samplesF = 1001
        freqMax = sS.higherPowerOfK(self.phDsys.AOP.getGBW(), 10) + 2
        self.simu.setFreqParams(0, freqMax, samplesF)
        
        nbSignal = 6
        
        timeData = np.zeros((samplesT, nbSignal))
        timeSignal = np.ones((samplesT, nbSignal))
        timeDataZ = np.zeros((samplesT, nbSignal))
        timeSignalZ = np.ones((samplesT, nbSignal))
        freqData = np.zeros((samplesT, nbSignal))
        freqSignalM = np.ones((samplesT, nbSignal))
        
        ''' Open Loop ALI '''
        # Initial model - text 
        self.phDsys.AOP.setGain(self.gainALI.getUserValue())
        self.phDsys.AOP.setGBW(self.gbwALI.getUserValue())
        self.aliInitTF = self.phDsys.AOP.transferFunction()
        self.simu.setModel(self.aliInitTF)
        timeData[:,0], timeSignal[:,0] = self.simu.timeResponse()
        freqData[:,0], freqSignalM[:,0], freqSignalInitP = self.simu.freqResponse()
        
        # Slider model
        self.phDsys.AOP.setGain(self.gainALI.getRealValue())
        self.phDsys.AOP.setGBW(self.gbwALI.getRealValue())
        self.aliTF = self.phDsys.AOP.transferFunction()
        self.simu.setModel(self.aliTF)
        timeData[:,1], timeSignal[:,1] = self.simu.timeResponse()
        freqData[:,1], freqSignalM[:,1], freqSigP = self.simu.freqResponse()

        ''' FeedBack '''
        # Init
        self.phDsys.setCe(self.cCBack.getUserValue()*1e-12)
        self.phDsys.setCphd(self.cphdBack.getUserValue()*1e-12)
        self.phDsys.setRe(self.reBack.getUserValue())
        self.phDsys.setRt(self.rtBack.getUserValue())
        sysTF = self.phDsys.transferFunctionSimple()
        self.simu.setModel(sysTF)
        timeData[:,2], timeSignal[:,2] = self.simu.timeResponse()
        freqData[:,2], freqSignalM[:,2], freqSigP = self.simu.freqResponse()
        # Slider
        self.phDsys.setCe(self.cCBack.getRealValue()*1e-12)
        self.phDsys.setCphd(self.cphdBack.getRealValue()*1e-12)
        self.phDsys.setRe(self.reBack.getRealValue())
        self.phDsys.setRt(self.rtBack.getRealValue())
        sysTF = self.phDsys.transferFunctionSimple()
        self.simu.setModel(sysTF)
        timeData[:,3], timeSignal[:,3] = self.simu.timeResponse()
        freqData[:,3], freqSignalM[:,3], freqSigP = self.simu.freqResponse()
        
        freqSignalM[:,2] = freqSignalM[:,2] / 100
        freqSignalM[:,3] = freqSignalM[:,3] / 100
        
        ''' Complete System '''
        self.phDsys.AOP.setGain(self.gainALI.getUserValue())
        self.phDsys.AOP.setGBW(self.gbwALI.getUserValue())
        self.phDsys.setCe(self.cCBack.getUserValue()*1e-12)
        self.phDsys.setCphd(self.cphdBack.getUserValue()*1e-12)
        self.phDsys.setRe(self.reBack.getUserValue())
        self.phDsys.setRt(self.rtBack.getUserValue())
        sysCompletTF = self.phDsys.transferFunction()
        self.simu.setModel(sysCompletTF)
        timeData[:,4], timeSignal[:,4] = self.simu.timeResponse()
        freqData[:,4], freqSignalM[:,4], freqSigP = self.simu.freqResponse()
        
        self.phDsys.AOP.setGain(self.gainALI.getRealValue())
        self.phDsys.AOP.setGBW(self.gbwALI.getRealValue())
        self.phDsys.setCe(self.cCBack.getRealValue()*1e-12)
        self.phDsys.setCphd(self.cphdBack.getRealValue()*1e-12)
        self.phDsys.setRe(self.reBack.getRealValue())
        self.phDsys.setRt(self.rtBack.getRealValue())       
        sysCompletTF = self.phDsys.transferFunction()
        self.simu.setModel(sysCompletTF)
        timeData[:,5], timeSignal[:,5] = self.simu.timeResponse()
        freqData[:,5], freqSignalM[:,5], freqSigP = self.simu.freqResponse()
                
        freqSignalM[:,4] = freqSignalM[:,4] / 100
        freqSignalM[:,5] = freqSignalM[:,5] / 100

        return timeData, timeSignal, timeDataZ, timeSignalZ, freqData, freqSignalM
    
    def updateGraph(self, timeData, timeSignal, timeDataZ, timeSignalZ, freqData, freqSignalM):
        # Step response
        self.graphT.setData(timeData, timeSignal)
        ymax = self.gainALI.getMaxValue()*1.5
        self.graphT.setYRange(-0.1, ymax)
        self.graphT.refreshGraph()
        
        '''
        # Step Response - Normalization
        maxValue = np.max(timeSignal, axis=0)
        timeSignal2 = timeSignal / maxValue
        self.graphT2.setData(timeData, timeSignal2)
        self.graphT2.refreshGraph()
        '''
        
        # Frequency response
        self.graphF.setData(freqData, 20*np.log10(freqSignalM))
        ymax = 20*np.log10(self.gainALI.getMaxValue())+ 40
        self.graphF.setYRange(-40, ymax)
        self.graphF.refreshGraph(logX=True)        

    def closeEvent(self, event):
        QApplication.quit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())