import scipy.signal as sig
import matplotlib.pyplot as plt
import numpy as np

#Simulation Parameters
x0 = [0,0]
start = 0
stop = 30
step = 1
t = np.arange(start,stop,step)
K = 3
T = 4

# State-space Model
A = [[-1/T, 0],
[0, 0]]
B = [[K/T],
[0]]
C = [[1, 0]]
D = 0
sys = sig.StateSpace(A, B, C, D)

# Step Response
t, y = sig.step(sys, x0, t)

# Plotting
plt.plot(t, y)
plt.title("Step Response")
plt.xlabel("t")
plt.ylabel("y")
plt.grid()
plt.show()