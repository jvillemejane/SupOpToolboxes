#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module Outils Numériques / Semestre 5 / Institut d'Optique

Résolution de systèmes linéaires

Created on 08/Apr/2023

@author: LEnsE / IOGS / Palaiseau
@author: Julien Villemejane
"""

import numpy as np

''' 
Find x1 and x2 where

x1 + x2 = 210
1.5 * x1 + 3 * x2 = 540
'''
a = np.array([[1, 1], [1.5, 3.0]])
b = np.array([210, 540])

# Solve a.X = b <=> X = a^-1 * b
# Using inverse of a matrix is long and less accurate
x = np.linalg.inv(a).dot(b)
print(x)

# Using solve from Numpy
x = np.linalg.solve(a,b)
print(x)