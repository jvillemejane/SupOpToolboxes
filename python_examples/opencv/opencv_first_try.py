# -*- coding: utf-8 -*-
"""
First application with OpenCV 
    Opening an image file
    

Author : Julien VILLEMEJANE
Laboratoire d Enseignement Experimental - Institut d Optique Graduate School
Created on Sat Jan 14 20:34:05 2023

@author: julien.villemejane

@see http://www.python-simple.com/python-opencv/detection-aretes.php
"""


import cv2
import numpy as np

img = cv2.imread('med_bottle_example__.jpg', 0)  # 0 = grayscale, 1 = rgb

cv2.imshow('My Image', img)    # Show the image in a window called 'Mon Image'

cv2.waitKey(0)              # Wait until a key is pressed
cv2.destroyAllWindows()     # destroy all the opened images

print(img.shape)


## Binary Threshold
_, thresh = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY)

cv2.imshow('Image threshold', thresh)    # Show the image in a window called 'Mon Image'

cv2.waitKey(0)              # Wait until a key is pressed
cv2.destroyAllWindows()     # destroy all the opened images


## Kernel for morphological transforms
kernel_3 = np.ones((3, 3), np.uint8)
kernel_5 = np.ones((5, 5), np.uint8)

## Erosion
img_erod_3 = cv2.erode(img, kernel_3)
cv2.imwrite('image_erod_3.png', img_erod_3)

img_erod_5 = cv2.erode(img, kernel_5)
cv2.imwrite('image_erod_5.png', img_erod_5)

## Dilatation
img_dila_3 = cv2.dilate(img, kernel_3)
cv2.imwrite('image_dila_3.png', img_dila_3)

img_dila_5 = cv2.dilate(img, kernel_5)
cv2.imwrite('image_dila_5.png', img_dila_5)

## Opening
img_open_3 = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel_3)
cv2.imwrite('image_open_3.png', img_open_3)
img_open_5 = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel_5)
cv2.imwrite('image_open_5.png', img_open_5)

## Closing
img_clos_3 = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel_3)
cv2.imwrite('image_clos_3.png', img_open_3)
img_clos_5 = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel_5)
cv2.imwrite('image_clos_5.png', img_open_5)

## Gradient
img_grad_3 = cv2.morphologyEx(img, cv2.MORPH_GRADIENT, kernel_3)
cv2.imwrite('image_grad_3.png', img_grad_3)
img_grad_5 = cv2.morphologyEx(img, cv2.MORPH_GRADIENT, kernel_5)
cv2.imwrite('image_grad_5.png', img_grad_5)

## Gradient with another kernel
new_kernel_3 = np.zeros((3,3), np.uint8)
new_kernel_3[:,1] = 1
new_kernel_3[1,:] = 1
print(new_kernel_3)
img_grad_n_3 = cv2.morphologyEx(img, cv2.MORPH_GRADIENT, new_kernel_3)
cv2.imwrite('image_grad_n_3.png', img_grad_n_3)