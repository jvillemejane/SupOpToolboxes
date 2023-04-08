#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module Outils Numériques / Semestre 5 / Institut d'Optique

Calculs scientifiques

Created on 08/Apr/2023

@author: LEnsE / IOGS / Palaiseau
@author: Julien Villemejane
"""

import numpy as np


''' Calculs simples '''

k = 3 - 2 - 1
print(f' k = {k}')

m = 0.3 - 0.2 - 0.1
print(f' m = {m} \n')


''' Format d'affichage '''

print(format(0.1, '.20f')+'\n')


''' Nombres complexes '''

c = (1j)**2
print(f'c = {c}')
print(f'type of c = {type(k)}\n')

print(f'sqrt(-1) = {np.sqrt(-1)}')
print(f'(-1) puis 0.5 = {(-1)**0.5}')
