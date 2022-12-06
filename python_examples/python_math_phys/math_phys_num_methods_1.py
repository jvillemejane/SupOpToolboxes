# -*- coding: utf-8 -*-
"""
Numerical methods examples
- root finding by bisection
- newton method

Author : Julien VILLEMEJANE
Laboratoire d Enseignement Experimental - Institut d Optique Graduate School
Version : 1.0 - 2022-12-01

Adapted from Francois Marquier / ENS Paris-Saclay
"""

import timeit
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import bisect, newton

import math_phys_methods as mpm

EPSILON = 1e-6

# Mathematical function definition f(x)
f = lambda x: np.cos(x) + np.sqrt(x+1)/3

# x vectors definition
x = np.linspace(0.,np.pi,200)

# display function
plt.plot(x,f(x))
plt.grid()
plt.show()

## BISECTION METHOD

# finding root by bisection (dichotomie in French)
x, n_ite = mpm.bisection(f, 2, 2.5, EPSILON)
print('Root = ',x, ' value of f = ', f(x), '/ nb iteration = ', n_ite)

# another possibility : bisect function, from scipy
x0 = bisect(f, 2, 2.5)
print('Root = ',x0, ' value of f = ', f(x0))

# Time execution measurement of both methods
# run same code 5 times to get measurable data
n = 5
# calculate total execution time
result_1 = timeit.timeit(stmt='mpm.bisection(f, 2, 2.5, EPSILON)', globals=globals(), number=n)
result_2 = timeit.timeit(stmt='bisect(f, 2, 2.5)', globals=globals(), number=n)
# get the average execution time
print(f"Execution time of first method is {result_1 / n} seconds")
print(f"Execution time of second method is {result_2 / n} seconds")


## NEWTON METHOD
# Derived function of F
df = lambda x: -np.sin(x) + 1/(6 * np.sqrt(x+1))

x_3, n_ite_3 = mpm.newton_find_root(f, df, 2.5, EPSILON)
print('Root = ',x_3, ' value of f = ', f(x_3), '/ nb iteration = ', n_ite_3)

# newton from scipy
x_4 = newton(f,2.5, fprime=df, tol=EPSILON)
print('Root = ',x_4, ' value of f = ', f(x_4))

# calculate total execution time
# run same code 5 times to get measurable data
n = 5
# calculate total execution time
result_3 = timeit.timeit(stmt='mpm.newton_find_root(f, df, 2.5, EPSILON)', globals=globals(), number=n)
result_4 = timeit.timeit(stmt='newton(f,2.5,df, tol=EPSILON)', globals=globals(), number=n)
# get the average execution time
print(f"Execution time of first method is {result_3 / n} seconds")
print(f"Execution time of second method is {result_4 / n} seconds")