# -*- coding: utf-8 -*-
"""
Signal Processing libraries of functions

Author : Julien VILLEMEJANE
Laboratoire d Enseignement Experimental - Institut d Optique Graduate School
Version : 1.0 - 2022-12-01
"""

from scipy import fftpack
import numpy as np
from numpy import random as rd


def test_signal():
    """
    test the integration of libraries in a python application.

    Returns
    -------
    int
        0 without any condition.

    """
    print('OK')
    return 0
    


def generate_sinus_freq(f, Fe, nb_per):
    """
    Generates Sine Waveform from 
    {frequency, sampling frequency,period number}

    Parameters
    ----------
    f : double
        frequency of the signal
    Fe : double
        sampling frequency.
    nb_per : integer
        number of periods of the signal.

    Returns
    -------
    t : 1-dimension vector - double
        time vector.
    signal : 1-dimension vector - double
        signal vector.

    """

    final_time = nb_per * 1/f
    samples = int(nb_per * Fe/f)
    t = np.linspace(0, final_time, samples)
    signal = np.sin(f * 2 * np.pi * t)
    return t, signal


def generate_sinus_time(f, time):
    """
    Generates Sine Waveform from 
    {frequency, time vector}

    Parameters
    ----------
    f : double
        frequency of the signal.
    time : 1-dimension vector - double
        time vector.

    Returns
    -------
    signal : 1-dimension vector - double
        signal vector.

    """
    if(f != 0):
        signal = np.sin(f * 2 * np.pi * time)
    else:
        signal = np.zeros(len(time))
    return signal


def calculate_FFT_1D(signal, Fe):
    """
    Calculates FFT from 
    {signal vector, sampling frequency}

    Parameters
    ----------
    signal : 1-dimension vector - double
        signal vector to calculate the FFT.
    Fe : double
        sampling frequency.

    Returns
    -------
    freq : 1-dimension vector - double
        frequency vector.
    TF : 1-dimension vector - complex
        complex Fourier Transform vector.

    """
    TF = fftpack.fft(signal)/len(signal)
    freq = fftpack.fftfreq(len(signal)) * Fe
    return freq, TF

def generate_noise(nb_samples):
    """
    Generates a random vector of {nb_samples} samples

    Parameters
    ----------
    nb_samples : int
        Size of the vector.

    Returns
    -------
    v_noise : 1-dimension vector - double
        Array of random floats of shape nb_samples.

    """
    v_noise = rd.random(nb_samples) - 0.5
    return v_noise