import numpy as np
import matplotlib.pyplot as plt
import control

## Second order model :
m = 0.07
wc = 1e4
H0 = 5

## Low pass filter :
num1 = np.array([H0])
den1 = np.array([(1/wc)**2, 2*m/wc, 1])
H1 = control.tf(num1, den1)

print('H1(s) = ', H1)

## Frequency response (Bode diagram) :
w0 = wc/100
w1 = wc*100
nw = 1001
w = np.linspace(w0 ,w1 ,nw)
(mag, phase_rad, w) = control.bode_plot(H1, w)
mag_db = 20*np.log10(mag)

# plotting
plt.figure()
plt.subplot(2, 1, 1)
plt.semilogx(w, mag_db, 'blue')
plt.grid()
plt.legend(labels=('magnitude',))

plt.subplot(2, 1, 2)
plt.semilogx(w, phase_rad*180/np.pi, 'red')
plt.grid()
plt.xlabel('w[rad/s]')
plt.legend(labels=('phase [deg]',))

plt.show()

# Automatic plt
plt.figure()
(mag, phase_rad, w) = control.bode_plot(H1, w, dB=True, deg=True, margins=True)

## Margins :
( GM , PM , wg , wp ) = control.margin(H1)
print ('GM [1 ( not dB )] = ', GM)
print ('PM [ deg ] = ', PM)
print ('wg [ rad / s ] = ', wg)
print ('wp [ rad / s ] = ', wp)