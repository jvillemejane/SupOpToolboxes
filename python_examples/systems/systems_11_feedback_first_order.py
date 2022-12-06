# -*- coding: utf-8 -*-
"""
Systems - Feedback with zero and first order system

Author : Julien VILLEMEJANE
Laboratoire d Enseignement Experimental - Institut d Optique Graduate School
Version : 1.0 - 2022-12-01
"""

import numpy as np
import matplotlib.pyplot as plt
import control

t = np.linspace(0, 0.5, 1001)
f = np.logspace(-2, 4, 1001)

## Open Loop system
G_OL = 1.0
t_OL = 0.01
num_OL = [G_OL]
den_OL = [t_OL, 1.]
sys_OL = control.tf(num_OL, den_OL)
print(sys_OL)

## Feedback System
G_FB = 10.0
t_FB = 0.05
num_FB = [G_FB]
den_FB = [t_FB, 1.]
sys_FB = control.tf(num_FB, den_FB)
print(sys_FB)

## Step and frequency responses
# Step response
T_OL, yout_OL = control.step_response(sys_OL, t)
T_FB, yout_FB = control.step_response(sys_FB, t)
plt.figure()
plt.plot(T_FB, yout_FB, label='Feedback System')
plt.plot(T_OL, yout_OL, label='Open-Loop System')
plt.grid(which="both")
plt.ylabel('u(t) in V')
plt.xlabel("Time (s)")
plt.title("Step response of the feedback system")
plt.show()

# Frequency response
plt.figure()
mag_FB, phase_FB, om = control.bode_plot(sys_FB, 2*np.pi*f, plot=True, Hz=True, label='FeedBack System')
mag_OL, phase_OL, om = control.bode_plot(sys_OL, 2*np.pi*f, plot=True, Hz=True, label='Open-Loop System')
plt.xlabel("Frequency (Hz)")
plt.title("Frequency Response")
plt.legend()
plt.show()

## Closed System
sys_CL = control.feedback(sys_OL, sys_FB)
plt.figure()
mag_FB, phase_FB, om = control.bode_plot(sys_FB, 2*np.pi*f, plot=True, Hz=True, label='FeedBack System')
mag_OL, phase_OL, om = control.bode_plot(sys_OL, 2*np.pi*f, plot=True, Hz=True, label='Open-Loop System')
mag_CL, phase_CL, om = control.bode_plot(sys_CL, 2*np.pi*f, plot=True, Hz=True, label='Global Closed Loop System')
plt.xlabel("Frequency (Hz)")
plt.title("Frequency Response")
plt.legend()
plt.show()


# Step response
T_CL, yout_CL = control.step_response(sys_CL, t)
plt.figure()
plt.plot(T_CL, yout_CL, label='Global System')
plt.grid(which="both")
plt.ylabel('u(t) in V')
plt.xlabel("Time (s)")
plt.title("Step response of the global system")
plt.show()