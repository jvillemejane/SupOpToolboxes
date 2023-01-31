# -*- coding: utf-8 -*-
"""
Linear regression - Airy disk diameter depending on diffraction hole diameter

Author : Julien VILLEMEJANE
Laboratoire d Enseignement Experimental - Institut d Optique Graduate School
Created on Mon Jan 31 16:10:05 2023

@author: julien.villemejane
@see: http://www.python-simple.com/python-scipy/fitting-regression.php
@see: https://moncoachdata.com/blog/regression-lineaire-avec-python/
"""

import numpy as np
import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression 


## Examples value - not real datas
hole_diameter_mm = np.array([1, 2, 5,10])
airy_disk_diameter_um = np.array([10.2, 4.8, 1.9, 0.99])

plt.figure()
plt.title('Linear Regression using Numpy')
plt.scatter(1/hole_diameter_mm, airy_disk_diameter_um, c = 'red', marker='+')
plt.xlabel('inverse of diffraction hole diameter ( mm-1 )')
plt.ylabel('airy disk diameter (um)')


## Linear Regression
# Méthode FIT polynomial avec Numpy
fit = np.polyfit(1/hole_diameter_mm, airy_disk_diameter_um, 1) # régression d'ordre 1
# a x + b
a = fit[0]
b = fit[1]

reg_lin = a * (1/hole_diameter_mm) + b

plt.plot(1/hole_diameter_mm, reg_lin)

# Méthode sklearn
# Data reshape
hole_diameter_mm_sk = hole_diameter_mm.reshape(-1,1)
airy_disk_diameter_um_sk = airy_disk_diameter_um.reshape(-1,1)
# Regression
reg = LinearRegression(fit_intercept=True, normalize=False, copy_X=True)
reg.fit(1/hole_diameter_mm_sk, airy_disk_diameter_um_sk)
a_sk = reg.coef_
b_sk = reg.intercept_

reg_lin = a_sk * (1/hole_diameter_mm) + b_sk

plt.figure()
plt.title('Linear Regression using SKlearn')
plt.scatter(1/hole_diameter_mm, airy_disk_diameter_um, c = 'red', marker='+')
plt.xlabel('inverse of diffraction hole diameter ( mm-1 )')
plt.ylabel('airy disk diameter (um)')

plt.plot(1/hole_diameter_mm, reg_lin)
