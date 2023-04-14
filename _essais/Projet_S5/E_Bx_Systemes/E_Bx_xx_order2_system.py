#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module Systèmes-Photonique / Semestre 5 / Institut d'Optique

Système du 2nd ordre

Created on 14/Apr/2023

@author: LEnsE / IOGS / Palaiseau
@author: Julien Villemejane
"""

import numpy as np
from matplotlib import pyplot as plt
import control as ct


#%% Low pass Model
w = np.logspace(2, 6, 1001)
t = np.linspace(0, 1, 1001)

# frequency
fc = 2000
wc = 2*np.pi*fc
# damping factor
m10 = np.sqrt(2)/2
m09 = m10/2
m08 = m10/4
m11 = 2*m10
m12 = 4*m10
m00 = -m08
# static gain
G0 = 1


tf08 = ct.tf([G0],[1/(wc*wc), 2*m08/wc, 1])
tf09 = ct.tf([G0],[1/(wc*wc), 2*m09/wc, 1])
tf10 = ct.tf([G0],[1/(wc*wc), 2*m10/wc, 1])
tf11 = ct.tf([G0],[1/(wc*wc), 2*m11/wc, 1])
tf12 = ct.tf([G0],[1/(wc*wc), 2*m12/wc, 1])

tf00 = ct.tf([G0],[1/(wc*wc), 2*m00/wc, 1])

tf_m08, tf_p08, w = ct.bode_plot(tf08, omega=w, plot=False)
tf_m09, tf_p09, w = ct.bode_plot(tf09, omega=w, plot=False)
tf_m10, tf_p10, w = ct.bode_plot(tf10, omega=w, plot=False)
tf_m11, tf_p11, w = ct.bode_plot(tf11, omega=w, plot=False)
tf_m12, tf_p12, w = ct.bode_plot(tf12, omega=w, plot=False)

tf_m00, tf_p00, w = ct.bode_plot(tf00, omega=w, plot=False)

plt.figure()
plt.plot(w, 20*np.log10(tf_m10))
plt.plot(w, 20*np.log10(tf_m11))
plt.plot(w, 20*np.log10(tf_m09))
plt.plot(w, 20*np.log10(tf_m12))
plt.plot(w, 20*np.log10(tf_m08))
plt.xscale('log')
plt.show()


plt.figure()
plt.plot(w, 20*np.log10(tf_m10))
plt.plot(w, 20*np.log10(tf_m00))
plt.xscale('log')
plt.show()