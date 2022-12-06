# -*- coding: utf-8 -*-
"""
Signal Processing libraries of functions

Author : Julien VILLEMEJANE
Laboratoire d Enseignement Experimental - Institut d Optique Graduate School
Version : 1.0 - 2022-12-01
"""

from scipy import fftpack
import numpy as np


def test_signal():
    """ test_signal displays OK and returns 0.
    
    This function is here to test the integration of libraries in a python application.
    
    :return: 0 without any condition
    """ 
    print('OK')
    return 0
    


def generate_sinus_freq(f, Fe, nb_per):
    """ generate_sinus_freq generates Sine Waveform from 
    {frequency, sampling frequency,period number}
    
    :f: frequency of the signal
    :Fe: sampling frequency
    :nb_per: number of periods of the signal
    :return: time vector, signal vector
    """
    final_time = nb_per * 1/f
    samples = int(nb_per * Fe/f)
    t = np.linspace(0, final_time, samples)
    signal = np.sin(f * 2 * np.pi * t)
    return t, signal

def generate_sinus_time(f, time):
    """ generate_sinus_time generates Sine Waveform from 
    {frequency, time vector}
    
    :f: frequency of the signal
    :time: time vector
    :return: signal vector
    """
    signal = np.sin(f * 2 * np.pi * time)
    return signal


def calculate_FFT_1D(signal, Fe):
    """ calculate_FFT_1D calculates FFT from 
    {signal vector, sampling frequency}
    need fftpack from Scipy Lib
    
    :signal: signal vector to calculate the FFT
    :Fe: sampling frequency
    :return: frequency vector, complex Fourier Transform vector
    """
    TF = fftpack.fft(signal)/len(signal)
    freq = fftpack.fftfreq(len(signal)) * Fe
    return freq, TF