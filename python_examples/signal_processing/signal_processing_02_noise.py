# -*- coding: utf-8 -*-
"""
Signal Processing / Noise generation and spectral analysis

Author : Julien VILLEMEJANE
Laboratoire d Enseignement Experimental - Institut d Optique Graduate School
Version : 1.0 - 2022-12-14
"""

from signal_processing import generate_sinus_freq, calculate_FFT_1D, generate_noise, generate_sinus_time
import matplotlib.pyplot as plt
import numpy as np


## Generate sine waveforms
t, sine = generate_sinus_freq(100, 1e4, 10)
sine2 = generate_sinus_time(250, t)
signal = 5*sine + sine2
plt.figure()
plt.plot(t, signal)
plt.title('Initial signal')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude (V)')
plt.show()

# Calculate FFT of the signal
f, tf_sine = calculate_FFT_1D(signal, 1e4)
plt.figure()
plt.plot(f, np.abs(tf_sine))
plt.title('Fourier Transform of the initial signal')
plt.show()

## Generate noise
noise = generate_noise(len(signal))
A_noise = 5.0
noise_sig = signal + A_noise * noise

# Display only noise
plt.figure()
plt.plot(t, noise)
plt.title('Noise Generation')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude (V)')
plt.show()

# Calculate FFT of the noise
f, tf_mod = calculate_FFT_1D(noise, 1e4)
plt.figure()
plt.plot(f, np.abs(tf_mod))
plt.title('Fourier Transform of the noise')
plt.show()

# Histogram of the noise signal


# Display of the noisy signal
plt.figure()
plt.plot(t, noise_sig)
plt.title('Noise Generation')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude (V)')
plt.show()

# Calculate FFT of the noisy signal
f, tf_mod = calculate_FFT_1D(noise_sig, 1e4)
plt.figure()
plt.plot(f, np.abs(tf_mod))
plt.title('Fourier Transform of the noised signal')
plt.show()
