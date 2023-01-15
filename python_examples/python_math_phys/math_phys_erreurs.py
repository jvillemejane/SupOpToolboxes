# -*- coding: utf-8 -*-
"""
Math and Physics examples, including calculation error

Author : Julien VILLEMEJANE
Laboratoire d Enseignement Experimental - Institut d Optique Graduate School
Version : 1.0 - 2022-12-01

Adapted from Francois Marquier / ENS Paris-Saclay
@author: julien.villemejane
"""

import numpy as np

# Erreur relative de 2**-52 (mantisse) et incertitude de l'ordre de 2**-54
# Cours Physique Numérique (c) François Marquier / ENS Paris-Saclay
print(0.1+0.2-0.3)

print(2 - 1 - 1)
print(2. - 1.1 - 0.9)


# Nombres complexes
k = (1j)**2
print(k)
print(type(k))


# Erreur et pas de nombre sur certains calculs
# Cours Physique Numérique (c) François Marquier / ENS Paris-Saclay
print(np.sqrt(-1))
print((-1)**0.5)