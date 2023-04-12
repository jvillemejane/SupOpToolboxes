#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module Outils Numériques / Semestre 5 / Institut d'Optique

Génération d'images 2D

Created on 08/Apr/2023

@author: LEnsE / IOGS / Palaiseau
@author: Julien Villemejane
"""

import numpy as np
from matplotlib import pyplot as plt

#%%  Meshgrid generation
x = np.linspace(-1,1,1000)  # Grille en X
y = np.linspace(-1,1,1000)  # Grille en Y
xx, yy = np.meshgrid(x,y) #Nous permet d'obtenir une "grille" 2D à partir de deux arrays


#%%  Function to display
def generate_sine(xx, yy, freq=1, alpha=0):
    return np.sin(freq*(xx*np.sin(alpha)+yy*np.cos(alpha)))
    
image = generate_sine(xx, yy, freq = 50, alpha=np.pi/12)

#%% Display image
plt.figure()
plt.imshow(image)

#%%  FFT of the image
tf_image = np.fft.fftshift(np.fft.fft2(image))

plt.figure()
plt.imshow(np.abs(tf_image))