# -*- coding: utf-8 -*-
"""
Signal Processing / Signal generation and Amplitude Modulation Simulation

Author : Julien VILLEMEJANE
Laboratoire d Enseignement Experimental - Institut d Optique Graduate School
Version : 1.0 - 2022-12-01
"""

from signal_processing import *
import matplotlib.pyplot as plt

test_signal()

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

## Generate modulation carrier sine
carrier = generate_sinus_time(2000, t)
am_sig = carrier * signal

plt.figure()
plt.plot(t, am_sig)
plt.title('Amplitude Modulation - fcarrier = 2kHz')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude (V)')
plt.show()

# Calculate FFT of the modulated signal
f, tf_mod = calculate_FFT_1D(am_sig, 1e4)
plt.figure()
plt.plot(f, np.abs(tf_mod))
plt.title('Fourier Transform of the modulated signal')
plt.show()

## Demodulation
am_sig_dem = carrier * am_sig

plt.figure()
plt.plot(t, am_sig_dem)
plt.title('Amplitude DeModulation - fcarrier = 2kHz')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude (V)')
plt.show()

# Calculate FFT of the modulated signal
f, tf_demod = calculate_FFT_1D(am_sig_dem, 1e4)
plt.figure()
plt.plot(f, np.abs(tf_demod))
plt.title('Fourier Transform of the demodulated signal')
plt.show()