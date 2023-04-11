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
def generate_sine(xx, yy, freqx=1, freqy=1):
    return np.sin(xx)
    

#%%  Display
fig = plt.figure(figsize=(15,10))
ax = plt.axes(projection="3d")
surf = ax.plot_surface(xx, yy, generate_sine(xx, yy))
plt.title("Figure 3D")
plt.show()
 