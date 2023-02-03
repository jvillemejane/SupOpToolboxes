import cv2 as cv
import sys

img = cv.imread("ciel_mer.jpg")

if img is None:
    sys.exit("Could not read the image.")
cv.imshow("Display window", img)

k = cv.waitKey(0)