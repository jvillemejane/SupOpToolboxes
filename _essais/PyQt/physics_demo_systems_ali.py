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
Find the power of K just higher than N
'''
def higherPowerOfK(N, K):
    # Finding log of the element
    lg = int(np.log(N) / np.log(K))
    return lg + 1

'''
MainWindow class
'''
class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__(parent=None)
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
        self.gbwALI.setPercent(True, 70)
        self.fcALI = gL.labelBlock('Cut Freq')
        self.fcALI.setUnits('Hz')
        
        self.labelALI = gL.titleBlock('ALI parameters')        
        self.labelALI.setMaximumWidth(300)
        self.labelALI.setStyleSheet("font-size:22px; font-weight:bold; padding:10px; color:Navy;")
        
        # Feedback Gain
        self.labelFeedBack = gL.titleBlock('FeedBack Parameters')
        self.gainFeedBackLabel = gL.titleBlock('Simple Gain', checkBox=True)
        self.gainFeedBack = gL.sliderBlock("Gain")
        self.gainFeedBack.setPercent(True, 90)
        self.gainFeedBack.setEnabled(False)
        
        # Order 1 FeedBack
        self.order1FeedBackLabel = gL.titleBlock('Order 1', checkBox=True)
        self.order1gainFeedBack = gL.sliderBlock("Gain")
        self.order1gainFeedBack.setPercent(True, 50)
        self.order1gainFeedBack.setEnabled(False)
        self.order1fcFeedBack = gL.sliderBlock("Cut Freq")
        self.order1fcFeedBack.setPercent(True, 50)
        self.order1fcFeedBack.setEnabled(False)
        
        ''' Layout Manager '''
        self.mainLayout = QGridLayout()
        self.mainWidget.setLayout(self.mainLayout)
        # Left area / ALI Parameters
        self.mainLayout.addWidget(self.labelALI, 0, 0)
        self.mainLayout.addWidget(self.gainALI, 1, 0, 3, 1)
        self.mainLayout.addWidget(self.gbwALI, 4, 0, 3, 1)
        self.mainLayout.addWidget(self.fcALI, 7, 0)
        self.graphTZ = gL.graph1D('Time dependent - normalization')
        self.mainLayout.addWidget(self.graphTZ, 8, 0, 4, 1)
        # Center area / Graph
        self.graphT = gL.graph1D('Time dependent')
        self.graphT2 = gL.graph1D('Time dependent - normalization')
        self.graphF = gL.graph1D('Freq dependent')
        self.mainLayout.addWidget(self.graphT, 0, 1, 4, 1)
        self.mainLayout.addWidget(self.graphF, 4, 1, 4, 1)
        self.mainLayout.addWidget(self.graphT2, 8, 1, 4, 1)
        # Right Area / Feedback
        self.mainLayout.addWidget(self.labelFeedBack, 0, 2, 1,2)
        self.mainLayout.addWidget(self.gainFeedBackLabel, 1, 2)
        self.mainLayout.addWidget(self.gainFeedBack, 2, 2)
        self.mainLayout.addWidget(self.order1FeedBackLabel, 3, 2)
        self.mainLayout.addWidget(self.order1gainFeedBack, 4, 2)
        self.mainLayout.addWidget(self.order1fcFeedBack, 5, 2)
        
        self.mainLayout.setColumnStretch(0, 1)
        self.mainLayout.setColumnStretch(1, 3)
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
        self.gainFeedBackLabel.tBsignal.connect(self.updateFeedback)
        self.gainFeedBack.asignal.connect(self.updateFeedback)
        self.order1FeedBackLabel.tBsignal.connect(self.updateFeedback)
        self.order1gainFeedBack.asignal.connect(self.updateFeedback)
        self.order1fcFeedBack.asignal.connect(self.updateFeedback)
        
        ''' model for simulation '''
        self.simu = sS.systemSimulation()
        self.aliModel = sS.compALI()
        self.order1ModelLP = sS.firstOrderSystem()
        
    def updateFeedback(self, sig):
        self.gainFeedBack.setEnabled(False)
        self.order1fcFeedBack.setEnabled(False)
        self.order1gainFeedBack.setEnabled(False)
        if(self.gainFeedBackLabel.isChecked()):
            self.gainFeedBack.setEnabled(True)
            self.order1fcFeedBack.setEnabled(False)
            self.order1gainFeedBack.setEnabled(False)
        if(self.order1FeedBackLabel.isChecked()):
            self.gainFeedBack.setEnabled(False)
            self.order1fcFeedBack.setEnabled(True)
            self.order1gainFeedBack.setEnabled(True)
 
        timeData, timeSignal, timeDataZ, timeSignalZ, freqData, freqSignalM = self.updateModel()
        self.updateGraph(timeData, timeSignal, timeDataZ, timeSignalZ, freqData, freqSignalM)
    
        
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
        self.simu.setTimeParams(0, 0.1, samplesT)
        samplesF = 1001
        freqMax = higherPowerOfK(self.aliModel.getGBW(), 10) + 2
        self.simu.setFreqParams(0, freqMax, samplesF)
        
        if(self.gainFeedBackLabel.isChecked() or self.order1FeedBackLabel.isChecked()):
            nbSignal = 6
        else:
            nbSignal = 2
        
        timeData = np.zeros((samplesT, nbSignal))
        timeSignal = np.zeros((samplesT, nbSignal))
        timeDataZ = np.zeros((samplesT, nbSignal))
        timeSignalZ = np.ones((samplesT, nbSignal))
        freqData = np.zeros((samplesT, nbSignal))
        freqSignalM = np.zeros((samplesT, nbSignal))
        
        ''' Open Loop ALI '''
        # Initial model - text 
        self.aliModel.setGain(self.gainALI.getUserValue())
        self.aliModel.setGBW(self.gbwALI.getUserValue())
        self.aliInitTF = self.aliModel.transferFunction()
        self.simu.setModel(self.aliInitTF)
        timeData[:,0], timeSignal[:,0] = self.simu.timeResponse()
        freqData[:,0], freqSignalM[:,0], freqSignalInitP = self.simu.freqResponse()
        
        # Slider model
        self.aliModel.setGain(self.gainALI.getRealValue())
        self.aliModel.setGBW(self.gbwALI.getRealValue())
        self.aliTF = self.aliModel.transferFunction()
        self.simu.setModel(self.aliTF)
        timeData[:,1], timeSignal[:,1] = self.simu.timeResponse()
        freqData[:,1], freqSignalM[:,1], freqSigP = self.simu.freqResponse()


        ''' FeedBack Loop - Control '''
        if(self.gainFeedBackLabel.isChecked()): # Order 0 model / simple gain
            
            # Initial model - text 
            self.gainFB = self.gainFeedBack.getUserValue()
            self.modelInitFB = ct.tf([self.gainFB],[1])
            self.simu.setModel(self.modelInitFB)
            timeData[:,2], timeSignal[:,2] = self.simu.timeResponse()
            freqData[:,2], freqSignalM[:,2], freqSignalInitFBP = self.simu.freqResponse()
                
            # Slider model
            self.gainFB = self.gainFeedBack.getRealValue()
            self.modelFB = ct.tf([self.gainFB],[1])
            self.simu.setModel(self.modelFB)
            timeData[:,3], timeSignal[:,3] = self.simu.timeResponse()
            freqData[:,3], freqSignalM[:,3], freqSigFBP = self.simu.freqResponse()
            
            ## Control system
            self.closedLoopInit = ct.feedback(self.aliInitTF, self.modelInitFB)
            self.closedLoop = ct.feedback(self.aliTF, self.modelFB)
            self.simu.setModel(self.closedLoopInit)
            timeData[:,4], timeSignal[:,4] = self.simu.timeResponse()
            freqData[:,4], freqSignalM[:,4], freqSigInitCLP = self.simu.freqResponse()
            self.simu.setModel(self.closedLoop)
            timeData[:,5], timeSignal[:,5] = self.simu.timeResponse()
            freqData[:,5], freqSignalM[:,5], freqSigCLP = self.simu.freqResponse()
            
            ## Zoom figure
            self.simu.setTimeParams(0, 0.001, samplesT)
            self.aliModel.setGain(self.gainALI.getRealValue())
            self.aliModel.setGBW(self.gbwALI.getRealValue())
            self.aliTF = self.aliModel.transferFunction()
            self.simu.setModel(self.aliTF)
            timeDataZ[:,1], timeSignalZ[:,1] = self.simu.timeResponse()
            
            self.gainFB = self.gainFeedBack.getRealValue()
            self.modelFB = ct.tf([self.gainFB],[1])
            self.simu.setModel(self.modelFB)
            timeDataZ[:,3], timeSignalZ[:,3] = self.simu.timeResponse()
            
            self.closedLoop = ct.feedback(self.aliTF, self.modelFB)
            self.simu.setModel(self.closedLoop)
            timeDataZ[:,5], timeSignalZ[:,5] = self.simu.timeResponse()
            
        
        if(self.order1FeedBackLabel.isChecked()): # Order 1 model 
            # Initial model - text 
            self.gainFB = self.order1gainFeedBack.getUserValue()
            self.order1ModelLP.setGain(self.gainFB)
            self.fc = self.order1fcFeedBack.getUserValue()
            self.order1ModelLP.setCutFreq(self.fc)
            self.modelInitFB = self.order1ModelLP.transferFunction()
            self.simu.setModel(self.modelInitFB)
            timeData[:,2], timeSignal[:,2] = self.simu.timeResponse()
            freqData[:,2], freqSignalM[:,2], freqSignalInitFBP = self.simu.freqResponse()
                
            # Slider model
            self.gainFB = self.order1gainFeedBack.getRealValue()
            self.order1ModelLP.setGain(self.gainFB)
            self.fc = self.order1fcFeedBack.getRealValue()
            self.order1ModelLP.setCutFreq(self.fc)            
            self.modelFB = self.order1ModelLP.transferFunction()
            self.simu.setModel(self.modelInitFB)
            timeData[:,3], timeSignal[:,3] = self.simu.timeResponse()
            freqData[:,3], freqSignalM[:,3], freqSigFBP = self.simu.freqResponse()
            
            ''' A CHANGER !!! '''
            ## Control system
            self.closedLoopInit = ct.feedback(self.aliInitTF, self.modelInitFB)
            self.closedLoop = ct.feedback(self.aliTF, self.modelFB)
            self.simu.setModel(self.closedLoopInit)
            timeData[:,4], timeSignal[:,4] = self.simu.timeResponse()
            freqData[:,4], freqSignalM[:,4], freqSigInitCLP = self.simu.freqResponse()
            self.simu.setModel(self.closedLoop)
            timeData[:,5], timeSignal[:,5] = self.simu.timeResponse()
            freqData[:,5], freqSignalM[:,5], freqSigCLP = self.simu.freqResponse()
            
            ## Zoom figure
            self.simu.setTimeParams(0, 0.001, samplesT)
            self.aliModel.setGain(self.gainALI.getRealValue())
            self.aliModel.setGBW(self.gbwALI.getRealValue())
            self.aliTF = self.aliModel.transferFunction()
            self.simu.setModel(self.aliTF)
            timeDataZ[:,1], timeSignalZ[:,1] = self.simu.timeResponse()
            
            self.gainFB = self.gainFeedBack.getRealValue()
            self.modelFB = ct.tf([self.gainFB],[1])
            self.simu.setModel(self.modelFB)
            timeDataZ[:,3], timeSignalZ[:,3] = self.simu.timeResponse()
            
            self.closedLoop = ct.feedback(self.aliTF, self.modelFB)
            self.simu.setModel(self.closedLoop)
            timeDataZ[:,5], timeSignalZ[:,5] = self.simu.timeResponse()
        
        return timeData, timeSignal, timeDataZ, timeSignalZ, freqData, freqSignalM
    
    def updateGraph(self, timeData, timeSignal, timeDataZ, timeSignalZ, freqData, freqSignalM):
        # Step response
        self.graphT.setData(timeData, timeSignal)
        ymax = self.gainALI.getMaxValue()+0.1
        self.graphT.setYRange(-0.1, ymax)
        self.graphT.refreshGraph()
        
        # Step Response - Normalization
        maxValue = np.max(timeSignal, axis=0)
        timeSignal2 = timeSignal / maxValue
        self.graphT2.setData(timeData, timeSignal2)
        self.graphT2.refreshGraph()
        
        # Step Response - Zoom
        timeSignalZ2 = timeSignalZ / maxValue
        self.graphTZ.setData(timeDataZ, timeSignalZ2)
        self.graphTZ.setYRange(-0.1, 1.1)
        self.graphTZ.refreshGraph()        
        
        # Frequency response
        self.graphF.setData(freqData, 20*np.log10(freqSignalM))
        ymax = 20*np.log10(self.gainALI.getMaxValue())+20
        self.graphF.setYRange(-40, ymax)
        self.graphF.refreshGraph(logX=True)        

    def closeEvent(self, event):
        QApplication.quit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())