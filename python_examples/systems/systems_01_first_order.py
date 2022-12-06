# -*- coding: utf-8 -*-
"""
Systems  simple examples

Author : Julien VILLEMEJANE
Laboratoire d Enseignement Experimental - Institut d Optique Graduate School
Version : 1.0 - 2022-12-01

Adapted from https://cpge.frama.io/fiches-cpge/Python/%C3%89quation%20diff%C3%A9rentielle/0-Equation%20diff%C3%A9rentielle/
"""

from scipy.integrate import solve_ivp
import numpy as np
import matplotlib.pyplot as plt
import control

# System constants
R = 1000  # Ohms
C = 0.001  # F
U = 10  # V

print('Time constant : ', R*C)

## Differential equation / Step response
# model of a RC circuit by differential equation
def du_dt(t, u):
    ''' model of a RC circuit by differential equation

    :t: time
    :u: voltage
    :return: du/dt of a RC circuit
    '''
    return (U-u)/(R*C)


t0 = 0      # starting time (in seconds)
tf = 7.0    # final time (in seconds)
u0 = 0      # initial condition for u

# Solving equation
voltage = solve_ivp(du_dt, [t0, tf], [u0], max_step=0.1)

# current calculation from previous solution
current = (U-voltage.y[0])/R


# Display voltage and current in the capacitor
plt.figure()
plt.plot(voltage.t, voltage.y[0], label="u(t)")
plt.plot(voltage.t, 1000*current, label="i(t)")
plt.ylabel('u(t) in V / i(t) in mA')
plt.xlabel("Time (s)")
plt.title("Step response of a RC circuit - U = 10V")
plt.grid(which="both")
plt.legend()
plt.show()


## Frequency response - Method 1 - Calculating transfer function
def tf_rc(f):
    ''' tf_rc is the transfer function of a first order RC system

    :f: frequency
    :return: value of the transfer function at f value
    '''
    w = 2*np.pi * f
    return 1/(1 + 1j*w/(R * C))

f = np.logspace(-2, 2, 101)
FT = 20 * np.log10(abs(tf_rc(f)))

# Display transfer function
plt.figure()
plt.title('Transfer function of a RC system')
plt.subplot(2, 1, 1)
plt.semilogx(f, FT, label="gain of TF(f)")
plt.grid(which="both")
plt.ylabel('Mag of TF (dB)')
plt.legend()
plt.subplot(2, 1, 2)
plt.semilogx(f, np.angle(tf_rc(f)), label="angle of TF(f)")
plt.xlabel('Frequency (Hz)')
plt.ylabel('Angle of TF (rad)')
plt.grid(which="both")
plt.legend()
plt.show()


## Frequency response - Method 2 - Using control library
num = [1.]
den = [1./(R*C), 1.]
sys = control.tf(num, den)
print(sys)

# Step response
T, yout = control.step_response(sys)
plt.figure()
plt.plot(T, yout)
plt.grid(which="both")
plt.ylabel('u(t) in V')
plt.xlabel("Time (s)")
plt.title("Step response of a RC circuit")
plt.show()

# Bode response
plt.figure()
mag, phase, om = control.bode_plot(sys, 2*np.pi*f, plot=True, Hz=True)
plt.show()

