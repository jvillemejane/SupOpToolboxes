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
import cv2

#%%  Meshgrid generation
x = np.linspace(-1,1,1000)  # Grille en X
y = np.linspace(-1,1,1000)  # Grille en Y
xx, yy = np.meshgrid(x,y) #Nous permet d'obtenir une "grille" 2D à partir de deux arrays


#%%  Function to display
def generate_sine(xx, yy, freq=1, alpha=0):
    return (1+np.sin(freq*(xx*np.sin(alpha)+yy*np.cos(alpha))))/2

def generate_square(xx, yy, freq=1, alpha=0):
    image = 255*(1+np.sin(freq*(xx*np.sin(alpha)+yy*np.cos(alpha))))/2
    th, im_th = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY)
    print(th)
    return im_th
    
    


#%%  Display
image = 255*generate_sine(xx, yy, freq=60, alpha=np.pi/12)
image = image.astype(int)
plt.figure()
plt.title("Tramage Sinus")
plt.imshow(image)

image_s = generate_square(xx, yy, freq = 200, alpha=np.pi/12)/255
plt.figure()
plt.title("Tramage Carre")
plt.imshow(image_s)

#%% FFT
tf_image = np.fft.fftshift(np.fft.fft2(image))
plt.figure()
plt.imshow(np.abs(tf_image), cmap='gray')
plt.title("TF Tramage Sinus")
plt.show()

tf_image_s = np.fft.fftshift(np.fft.fft2(image_s))
plt.figure()
plt.imshow(np.log(np.abs(tf_image_s)), cmap='gray')
plt.title("TF Tramage Carre")

plt.show()
