# -*- coding: utf-8 -*-
"""
Closed-Loop System / TD11

Author : Julien VILLEMEJANE
Laboratoire d Enseignement Experimental - Institut d Optique Graduate School
Created on 17/mar/2023

@author: julien.villemejane
"""

import control as ct
from matplotlib import pyplot as plt
import numpy as np

# Frequency vector
f = np.logspace(0,5,1001)
w = 2*np.pi*f
# Time vector
t = np.linspace(0,2e-2, 1001)


'''
First order initial system
H0 = 0.5
tau = 2ms
'''
H0 = 0.5
tau = 2e-3

FTBO = ct.tf([H0], [tau, 1])
FTBO_freq, FTBO_freq_sigM, FTBO_freq_sigP = ct.bode(FTBO, omega=w, plot=True)
FTBO_time, FTBO_step = ct.step_response(FTBO, T=t)

'''
Feedback 1 - No correction
C = 1
B = 1
'''
FTBF_B1_C1_I0 = ct.feedback(FTBO, 1)
FTBF_1_freq, FTBF_1_freq_sigM, FTBF_1_freq_sigP = ct.bode(FTBF_B1_C1_I0, omega=w, plot=True)
FTBF_1_time, FTBF_1_step = ct.step_response(FTBF_B1_C1_I0, T=t)


'''
Feedback 1 - Proportionnal correction
C = G (G = 10)
B = 1
'''
G = 10
FTBF_B1_CG_I0 = ct.feedback(G * FTBO, 1)
FTBF_2_freq, FTBF_2_freq_sigM, FTBF_2_freq_sigP = ct.bode(FTBF_B1_CG_I0, omega=w, plot=True)
FTBF_2_time, FTBF_2_step = ct.step_response(FTBF_B1_CG_I0, T=t)


'''
Feedback 1 - Proportionnal and integral correction
C = G + 1/(taui*p) (G = 10, taui = 3e-5)
B = 1
'''
taui = 3e-5
Cpi = ct.tf([1], [taui, 0])

FTBF_B1_CG_I1 = ct.feedback((G+Cpi) * FTBO, 1)
FTBF_3_freq, FTBF_3_freq_sigM, FTBF_3_freq_sigP = ct.bode(FTBF_B1_CG_I1, omega=w, plot=True)
FTBF_3_time, FTBF_3_step = ct.step_response(FTBF_B1_CG_I1, T=t)