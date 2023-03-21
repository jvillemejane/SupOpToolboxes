# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 16:52:37 2023

@author: Villou
"""

import time

import numpy as np
import matplotlib.pyplot as plt
from scipy.special import j1

min_ax = (-(1280))/2*5.3*1e-6
max_ax = ((1280))/2*5.3*1e-6
x_axis = np.linspace(min_ax, max_ax, 1280)
min_ay = (-(1024))/2*5.3*1e-6
max_ay = ((1024))/2*5.3*1e-6
y_axis = np.linspace(min_ay, max_ay, 1024)
xx, yy = np.meshgrid(x_axis,y_axis) 

def diffraction_trou(x, y, d, L0, lam, D):
    eta = np.pi*d*np.sqrt(x**2+y**2)/(lam*D)
    return (4*L0*(j1(eta)/eta)**2)

zz = diffraction_trou(xx, yy, 1e-3, 1, 632e-9, 1e-1)

z_max = np.argmax(zz) // 1280

plt.figure()
plt.imshow(np.log10(zz))

plt.figure()
plt.plot(zz[z_max,:])

