#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module Outils Numériques / Semestre 5 / Institut d'Optique

Calcul symbolique SymPy
- better vizualization in Jupyter Notebook

Created on 15/Apr/2023

@author: LEnsE / IOGS / Palaiseau
@author: Julien Villemejane
@see : https://www.youtube.com/watch?v=-SdIZHPuW9o

NEXT Solving Differential Equation
@see : https://www.youtube.com/watch?v=MM3cBamj1Ms
"""

import sympy as sp
from sympy import *

#%% Definition of symbols
x, y, t = sp.symbols('x y t')
# x and y consider as variables
print(x**2)

f,g,h,m = sp.symbols('f g h m', cls=sp.Function) 
# f, g, h and m consider as functions
f=f(x)


#%% Rational number
print(sp.Rational(3,2))  # 3/2

#%% Function of x and y
f = x**2 + y

print(f.subs(x, 4))



#%% Solve limits of an expression
# First function
g = sp.sin(x/2 + sp.sin(x))
print(g)
lg = sp.limit(g, x, sp.pi)
print(lg)

# Second function with limit in 0+
h = 2*sp.exp(1/x)/(sp.exp(1/x)+1)
print(h)
lhplus = sp.limit(h, x, 0, dir='+')
print(lhplus)
# Second function with limit in 0-
lhmoins = sp.limit(h, x, 0, dir='-')
print(lhmoins)

# Third function with limit in +infinite
m = (sp.cos(x)-1)/x
print(f'Value in x=1 = {m.subs(x, 1)}')
lm = sp.limit(m, x, sp.oo)
print(f'Limit in +inf = {lm}')


#%% Derivatives
print('\nDerivatives !!')
dfx = sp.diff(f, x)
print(dfx)

# Derivative with abstract expression
k, l = sp.symbols('k l', cls=sp.Function)
k = k(x)
l = l(x + k)
dfkl = sp.diff(l, x)
print(dfkl)

#%% Integral
print('\nIntegral !!')
inte_f = sp.integrate(f, x)
print(inte_f)

# with definite value
f = sp.exp(x)/(sp.sqrt(sp.exp(2*x)+9))
inte_f = sp.integrate(f, (x, 0, sp.log(4)))
print(inte_f)

g = x**10*sp.exp(x)
inte_g = sp.integrate(g, (x, 1, t))
print(inte_g)

#%% Series
print('\nSeries !!')
n = sp.symbols('n')

s1 = 6/(4**n)
sums1 = sp.Sum(s1, (n, 0, sp.oo))
print(sums1)
value_sums1 = sums1.doit()  
# .n() if we want an approximative value
print(value_sums1)


#%% Vectors
print('\nVectors !!')
u,v,u1, u2, u3, v1,v2,v3 = sp.symbols('u v u_1 u_2 u_3 v_1 v_2 v_3')

u = sp.Matrix([u1, u2, u3])
v = sp.Matrix([v1, v2, v3])

w = 2*u+v
print(w)

# Dot products
w = u.dot(v)
print(w)

# Norm of a vector
print(u.norm())

# Projection of the u vector on v
proj_v_u = u.dot(v)/v.norm()**2 * v
print(proj_v_u)


