# -*- coding: utf-8 -*-
"""
Created on Sat Mar  4 13:56:46 2023

@author: Villou
"""

import pandas
from matplotlib import pyplot as plt
import numpy as np
import time

# Lecture avec Pandas
df = pandas.read_csv('test_oscillo_sin_2k_2Vpp_4k.csv', header=2, nrows=4000)
v_time = df['Time(s)']
v_signal = df['Volt(V)']

v_time = np.linspace(0,1,4000)
f0 = 100
v_signal = np.sin(2 * np.pi * f0 * v_time)


n_max = 400


# Calcul iteratif
v_time_imp = np.zeros(n_max)

start1 = time.time()

for k in range(100):
    for i in range(n_max):
        v_time_imp[i] = v_time[i]
end1 = time.time()
elapsed1 = end1 - start1
print(f'Temps d\'exécution (100 exécutions) : {elapsed1:.8}ms')

# Calcul matriciel
v_time_mat = np.zeros(n_max)

start2 = time.time()
for k in range(int(1e4)):
    v_time_mat[0:n_max] = v_time[0:n_max]
end2 = time.time()
elapsed2 = end2 - start2
elapsed2 = elapsed2
print(f'Temps d\'exécution (10^4 executions) : {elapsed2:.8}ms')