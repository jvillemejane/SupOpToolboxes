# -*- coding: utf-8 -*-
"""
Images and processing

Author : Julien VILLEMEJANE
Laboratoire d Enseignement Experimental - Institut d Optique Graduate School
Created on Mon Jan 31 16:10:05 2023

@author: julien.villemejane
@see: http://www.python-simple.com/python-scipy/fitting-regression.php
@see: https://moncoachdata.com/blog/regression-lineaire-avec-python/
"""

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

img = Image.open('airy_2mm.bmp').convert('L')
img_data = np.asarray(img)

plt.imshow(img_data, cmap='hot')

# information about the image
height_data = img_data.shape[0]
width_data = img_data.shape[1]
print(f'H = {height_data} / W = {width_data}')

# finding index of the maximum value
max_data = np.argmax(img_data)
x_max = max_data % width_data
y_max = int(max_data / height_data)
print(f'Max index : X = {x_max} / Y = {y_max}')

# Slicing the image
y_slice = input('Select the slicing line : ')
slice_data = img_data[int(y_slice),:]
plt.figure()
plt.plot(slice_data)

# Mean on slicing
delta_mean = input('Select the number of line to mean :')
slice_mean_data = img_data[int(y_slice)-int(delta_mean):int(y_slice)+int(delta_mean),:]

plt.figure()
plt.imshow(slice_mean_data, cmap='hot')

slice_mean_slice = slice_mean_data.mean(axis=0)
plt.figure()
plt.plot(slice_mean_slice)