import numpy as np
import matplotlib.pyplot as plt
import control

## Creating the transfer function :
num1 = np.array([2])
den1 = np.array([5 , 1])
H1 = control.tf(num1, den1)

num2 = np.array([1])
den2 = np.array([3 , 1])
H2 = control.tf(num2, den2)

## Displaying the transfer function :
print ('H1(s) =', H1)
print ('H2(s) =', H2)

## Combination of transfer functions :
# Serie
Hs = control.series(H1, H2)
print ('Hs(s) = H1(s).H2(s) =', Hs)
# Parallele
Hp = control.parallel(H1, H2)
print ('Hp(s) = H1(s) + H2(s) =', Hp)

## Feedback combination of transfer functions :
Hf = control.feedback(H1, H2, sign=-1)
print ('Hf(s) = ', Hf)

## Collecting data from tf
(num_list, den_list) = control.tfdata(Hf)
# convert to numpy array
num_array = np.array(num_list)
num_array = num_array[0,0,:]
den_array = np.array(den_list)
den_array = den_array[0,0,:]

print('Num = ', num_array)
print('Den = ', den_array)


## Defining signals :
t0 = 0          # initial time
t1 = 20         # final time
dt = 0.01       # sampling time
nt = int ( t1 / dt ) + 1    # Number of points of sim time
t = np . linspace ( t0 , t1 , nt )      # time vector
u = 2* np . ones ( nt )                 # signal vector

## Simulation :
(t, y) = control.forced_response(Hs, t, u, X0 =0)        # X0 : initial state

## Plotting :
fig_width_cm = 24
fig_height_cm = 18
plt.figure (1 , figsize =( fig_width_cm /2.54 , fig_height_cm /2.54))
plt.subplot (2 , 1 , 1)
plt.plot (t, y, 'blue')
# plt.xlabel ( ’ t [ s ] ’)
plt.grid ()
plt.legend ( labels =('y',))
plt.subplot (2 , 1 , 2)
plt.plot (t, u, 'green')
plt.xlabel ('t [ s ]')
plt.grid ()
plt.legend ( labels =('u',))
plt.show()
# plt.savefig ('sim_tf.pdf')

## Poles and zeros of a transfer function :
(p, z) = control.pzmap(Hs)
print ('poles = ', p)
print ('zeros = ', z)
