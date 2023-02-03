import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt

# Define Transfer Function
num1 = np.array([3])
num2 = np.array([2, 1])
num = np.convolve(num1, num2)
den1 = np.array([3, 1])
den2 = np.array([5, 1])
den = np.convolve(den1, den2)
H = signal.TransferFunction(num, den)
print ('H(s) =', H)

# Frequencies
w_start = 0.01
w_stop = 10
step = 0.01
N = int ((w_stop-w_start )/step) + 1
w = np.linspace (w_start , w_stop , N)

# Bode Plot
w, mag, phase = signal.bode(H, w)
plt.figure()
plt.subplot (2, 1, 1)
plt.semilogx(w, mag) # Bode Magnitude Plot
plt.title("Bode Plot")
plt.grid(b=None, which='major', axis='both')
plt.grid(b=None, which='minor', axis='both')
plt.ylabel("Magnitude (dB)")
plt.subplot (2, 1, 2)
plt.semilogx(w, phase) # Bode Phase plot
plt.grid(b=None, which='major', axis='both')
plt.grid(b=None, which='minor', axis='both')
plt.ylabel("Phase (deg)")
plt.xlabel("Frequency (rad/sec)")
plt.show()