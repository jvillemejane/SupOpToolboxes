# -*- coding: utf-8 -*-
"""
Script for opening CSV files and plotting datas

Author : Julien VILLEMEJANE
Laboratoire d Enseignement Experimental - Institut d Optique Graduate School
Created on Mon Jan 31 16:10:05 2023

@author: julien.villemejane
"""

import numpy as np
import csv
import matplotlib.pyplot as plt

## Sans Numpy mais sortie = list !!!
# ouverture en lecture du fichier csv
with open('test_oscillo_AM_2k_400_50p_4k.csv', newline='') as fichier:
    # on crée un objet reader
    lecture = csv.reader(fichier, delimiter=',')

    # on transforme l'itérateur en liste:
    lignes = list(lecture)


print(type(lignes))
print(lignes[0])

## Avec Numpy
# Lecture des données au format str
data = np.genfromtxt('test_oscillo_AM_2k_400_50p_4k.csv', delimiter=',', skip_header = 3)
print(data)
time = data[:,1]
freq_sample = 1/(time[2]-time[1])
signal = data[:,2]

## Figure Signal temporel
plt.figure()
plt.plot(time, signal)
plt.title('Signal en fonction du temps')
plt.xlabel('Temps (s)')
plt.ylabel('Signal (V)')
plt.legend('Signal module')

## Calcul FFT et affichage
tf_signal = np.fft.fftshift(np.fft.fft(signal))
tf_freq = np.linspace(-freq_sample/2,freq_sample/2, len(time))
plt.figure()
plt.plot(tf_freq, np.abs(tf_signal))
plt.show()

freq_carry = float(input('Frequence de la porteuse ? '))
# Generation de la porteuse
sin_carry = np.sin(2*np.pi*freq_carry*time)
signal_mult = signal * sin_carry
# Figure signal multiplie
plt.figure()
plt.plot(time, signal_mult)
plt.title('Signal en fonction du temps')
plt.xlabel('Temps (s)')
plt.ylabel('Signal (V)')
plt.legend('Signal module')

# TF signal multiplie
tf_signal_mult = np.fft.fftshift(np.fft.fft(signal_mult))
plt.figure()
plt.plot(tf_freq, np.abs(tf_signal_mult))
plt.show()

# Filtrage / on garde la zone centrale
tf_signal_mult[0:1500] = 0
tf_signal_mult[2500:4000] = 0
plt.figure()
plt.plot(tf_freq, np.abs(tf_signal_mult))
plt.show()

signal_demod = np.fft.ifft(np.fft.fftshift(tf_signal_mult))
plt.figure()
plt.plot(time, signal_demod)
plt.show()