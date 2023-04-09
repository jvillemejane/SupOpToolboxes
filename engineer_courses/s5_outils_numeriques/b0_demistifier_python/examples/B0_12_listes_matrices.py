#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module Outils Numériques / Semestre 5 / Institut d'Optique

Listes et matrices

Created on 08/Apr/2023

@author: LEnsE / IOGS / Palaiseau
@author: Julien Villemejane
"""

import numpy as np

''' List (list) / classe native de Python '''

my_list = [1, 2, 3, 5]
print(f'my_list = {my_list}')
print(type(my_list))

print(f'\tlength of my_list = {len(my_list)} \n')

my_list_2 = my_list * 2
print(f'my_list_2 = {my_list_2}')
print(type(my_list_2))

print(f'\tlength of my_list_2 = {len(my_list_2)}\n')

''' Matrice (array) / classe de la bibliothèque Numpy '''

my_array = np.array([1, 2, 3, 5])
print(f'my_array = {my_array}')
print(type(my_array))

print(f'\tlength of my_array = {len(my_array)}\n')

my_array_2 = my_array * 2
print(f'my_array_2 = {my_array_2}')
print(type(my_array_2))

print(f'\tlength of my_array_2 = {len(my_array_2)}\n')