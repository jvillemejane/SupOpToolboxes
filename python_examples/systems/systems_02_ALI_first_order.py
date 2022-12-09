# -*- coding: utf-8 -*-
"""
Linear Amplifier - First order model

Author : Julien VILLEMEJANE
Laboratoire d Enseignement Experimental - Institut d Optique Graduate School
Version : 1.0 - 2022-12-01
"""

import numpy as np
import matplotlib.pyplot as plt
import control

## Linear Amplifier Low-Pass model - First order
#       H(jw) = Ad / (1 + jw/wc)
Ad = 1e5 # V/V - differential gain
funitaire = 1e6 # Hz
fc = funitaire / Ad
wc = fc * np.pi * 2


## Frequency response - Using control library
### Open-loop model
num = [Ad]
den = [1./wc, 1.]
sys_ALI_OL = control.tf(num, den)
print(sys_ALI_OL)

# Step response
T, yout = control.step_response(sys_ALI_OL)
plt.figure()
plt.plot(T, yout)
plt.grid(which='both')
plt.ylabel('u(t) in V')
plt.xlabel('Time (s)')
plt.title('Step response of a linear amplifier')
plt.show()

# Bode response
f = np.logspace(-2,8,101)
plt.figure()
mag, phase, om = control.bode_plot(sys_ALI_OL, 2*np.pi*f, plot=True, Hz=True)
plt.show()



### Closed-loop with a wire / Voltage follower
num_FB = [1.]
den_FB = [1.]
sys_FB = control.tf(num_FB, den_FB)
sys_CL = control.feedback(sys_ALI_OL, sys_FB)
print(sys_CL)

# Bode response
plt.figure()
mag, phase, om = control.bode_plot(sys_ALI_OL, 2*np.pi*f, plot=True, Hz=True)
mag_FB, phase_FB, om_FB = control.bode_plot(sys_CL, 2*np.pi*f, plot=True, Hz=True)
plt.show()