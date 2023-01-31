# -*- coding: utf-8 -*-
"""
Script for generating AM modulated signal

Author : Julien VILLEMEJANE
Laboratoire d Enseignement Experimental - Institut d Optique Graduate School
Created on Mon Jan 31 16:10:05 2023

@author: julien.villemejane
"""

import numpy as np
import matplotlib.pyplot as plt


Fs = 1e4  # sampling frequency
samples_number = 1e3
time = np.arange(0, samples_number/Fs, 1/Fs)

## Generate carrier signal
carrier_freq = 1000
carrier_signal = np.sin(2*np.pi*time*carrier_freq) 
plt.figure()
plt.plot(time,carrier_signal)
plt.title('Carrier signal - f = 1kHz')
plt.xlabel('Time (s)')
plt.ylabel('Signal (V)')

## Generate modulation signal
modul_freq = 60
modul_signal = np.sin(2*np.pi*time*modul_freq)
plt.plot(time, modul_signal)

am_signal = modul_signal * carrier_signal
plt.plot(time, am_signal)

plt.show()

# Zero padding
zeros_pad = np.zeros(3*int(samples_number))
am_signal_zero = np.concatenate((am_signal, zeros_pad))

# FFT
freq = np.linspace(0, Fs, int(samples_number))
freq_zero = np.linspace(0, Fs, 4*int(samples_number))
am_signal_tf = np.fft.fft(am_signal)
am_signal_tf_zero = np.fft.fft(am_signal_zero)
plt.figure()
plt.plot(freq, np.abs(am_signal_tf))
plt.plot(freq_zero, np.abs(am_signal_tf_zero))
