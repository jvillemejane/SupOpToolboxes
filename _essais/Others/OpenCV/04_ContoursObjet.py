import cv2 as cv
import numpy as np
import sys

# Open image
img = cv.imread("objets.png")
if img is None:
    sys.exit("Could not read the image.")
cv.imshow("Display window", img)

# Pause
cv.waitKey(0)

# convert the image to grayscale format
img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
cv.imshow("Display window", img_gray)

# Pause
cv.waitKey(0)

# apply binary thresholding
treshold = 200
ret, thresh = cv.threshold(img_gray, treshold, 255, cv.THRESH_BINARY)

# visualize the binary image
cv.imshow('Binary image', thresh)
cv.waitKey(0)
cv.imwrite('objets_bin.png', thresh)
cv.destroyAllWindows()

# detect the contours on the binary image using cv2.CHAIN_APPROX_NONE
contours, hierarchy = cv.findContours(image=thresh, mode=cv.RETR_TREE, method=cv.CHAIN_APPROX_NONE)

# draw contours on the original image
image_copy = img.copy()
cv.drawContours(image=image_copy, contours=contours, contourIdx=-1, color=(0, 255, 0), thickness=2, lineType=cv.LINE_AA)

# see the results
cv.imshow('None approximation', image_copy)
cv.waitKey(0)
cv.imwrite('objets_contours.png', image_copy)
cv.destroyAllWindows()
