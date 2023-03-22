# -*- coding: utf-8 -*-
"""
Demo application : basics signals and Fourier transform

Author : Julien VILLEMEJANE
Laboratoire d Enseignement Experimental - Institut d Optique Graduate School
Created on 11/mar/2023

@author: julien.villemejane
"""

from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.uic import loadUi

import numpy as np
from pyqtgraph import PlotWidget, plot, mkPen
from signal_processing.signal_processing import generate_sinus_time

import sys  # We need sys so that we can pass argv to QApplication
import os


"""
MainWindow class
"""
class MainWindow(QMainWindow):

    
    def __init__(self):
        super().__init__(parent=None)
        loadUi("Demo_signals_fft.ui", self)
        
        """ Signal Widget """
        self.plotSignalWidget = PlotWidget(title='Time-dependent signal ')
        self.leftLayout.addWidget(self.plotSignalWidget)
        self.plotSignalWidget.setBackground('w')
        
        self.sin1Widget.setStyleSheet("background-color:lightblue;");
        self.sin2Widget.setStyleSheet("background-color:lightgreen;");

        self.pen = mkPen(color=(128, 128, 0), width=5)
        
        """ FFT Widget """
        self.plotFFTWidget = PlotWidget(title='Fourier Transform / Frequency-dependent')
        self.rightLayout.addWidget(self.plotFFTWidget)
        self.plotFFTWidget.setBackground('w')        
        
        max_freq = self.freq1Slider.maximum()
        self.plotFFTWidget.setXRange(-max_freq, max_freq, padding=0)  

        self.plotFFTWidget.setYRange(-.1, 1.1, padding=0)
        
        """ Sampling Widget """
        self.sampFreqValues = ['125', '250', '500', '1000', '5000', '10000']
        self.samplingFreqCombo.addItems(self.sampFreqValues)
        self.samplesValues = ['10000', '5000', '1000', '500', '100', '50', '10']
        self.samplesCombo.addItems(self.samplesValues)
            
        """ Initial values for data generation """
        self.samples = 2000
        self.sampling_freq = 1000
        self.sin_freq1 = 20
        self.sin_freq2 = 0
        self.freq1Slider.setValue(self.sin_freq1)
        self.freq1Value.setText(f'{self.sin_freq1} Hz')
        if(self.onSig2.isChecked()):
            self.freq2Slider.setValue(self.sin_freq2)
            self.freq2Value.setText(f'{self.sin_freq2} Hz')
        else:
            self.freq2Value.setText(f'OFF')
        
        """ Signals generation"""
        self.time, self.signal, self.freq, self.s_fft = self.generate_signals()
        self.plotSig = self.plotSignalWidget.plot(self.time, self.signal, pen=self.pen)
        self.plotFFT = self.plotFFTWidget.plot(self.freq, self.s_fft, pen=self.pen)
        
        """ Events """        
        self.refreshPlotsBt.clicked.connect(self.refreshGraph)
        self.freq1Slider.valueChanged.connect(self.freqChanged)
        self.freq2Slider.valueChanged.connect(self.freqChanged)
        self.onSig2.stateChanged.connect(self.freqChanged)
        self.samplingFreqCombo.currentIndexChanged.connect(self.freqChanged)
        self.samplesCombo.currentIndexChanged.connect(self.freqChanged)
        
        self.refreshGraph()

    def freqChanged(self):
        self.refreshGraph()
        
        
    def refreshGraph(self):
        """ Collecting new values """        
        self.sampling_freq = int(self.samplingFreqCombo.currentText())
        self.samples = int(self.samplesCombo.currentText())
        self.sin_freq1 = self.freq1Slider.value()
        self.freq1Value.setText(f'{self.sin_freq1} Hz')
        if(self.onSig2.isChecked()):
            self.sin_freq2 = self.freq2Slider.value()
            self.freq2Value.setText(f'{self.sin_freq2} Hz')
        else:
            self.freq2Value.setText(f'OFF')
            
        
        """ Signals generation"""
        self.time, self.signal, self.freq, self.s_fft = self.generate_signals()
        """ Zoom for displaying """
        freq_half = int(self.samples/2)        
        max_freq = self.freq1Slider.maximum()
        f_range = max_freq / self.sampling_freq * self.samples
        if(f_range > self.samples/2):
            f_range = int(self.samples/2)
        else:
            f_range = int(f_range)
        
        self.freq = self.freq[freq_half-f_range:freq_half+f_range]
        self.s_fft = self.s_fft[freq_half-f_range:freq_half+f_range]
        
        """ Displaying data """
        self.plotSignalWidget.removeItem(self.plotSig)
        self.plotSig = self.plotSignalWidget.plot(self.time, self.signal, pen=self.pen)
        self.plotFFTWidget.removeItem(self.plotFFT)
        self.plotFFT = self.plotFFTWidget.plot(self.freq, self.s_fft, pen=self.pen)
    
    def generate_signals(self):
        final_time = self.samples / self.sampling_freq
        time = np.linspace(0, final_time, self.samples)
        
        dataSig = generate_sinus_time(self.sin_freq1, time)
        if(self.onSig2.isChecked()):
            dataSig+= generate_sinus_time(self.sin_freq2, time)
        
        freq = np.fft.fftfreq(self.samples, time[1]-time[0])
        freq = np.fft.fftshift(freq)
        dataFFT = np.abs(np.fft.fftshift(np.fft.fft(dataSig)))/self.samples
        return time, dataSig, freq, dataFFT
    
    def closeEvent(self, event):
        QApplication.quit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())