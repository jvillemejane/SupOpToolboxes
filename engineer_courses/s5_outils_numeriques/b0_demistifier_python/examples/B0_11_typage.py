#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module Outils Numériques / Semestre 5 / Institut d'Optique

Types de données

Created on 08/Apr/2023

@author: LEnsE / IOGS / Palaiseau
@author: Julien Villemejane
"""

''' Meme variable, types différents '''

k = 1
print(f'k = {k}')
print(type(k))

k = 0.1
print(f'k = {k}')
print(type(k))

k = '1'
print(f'k = {k}')
print(type(k))

''' Transtypage '''

m = int(k)
print(f'm = {m}')
print(type(m))


''' Tout est une question d'octets '''

b = b'\x61\x41\x42'
print(b)
print(type(b))

b = b.decode('UTF-8')
print(b)