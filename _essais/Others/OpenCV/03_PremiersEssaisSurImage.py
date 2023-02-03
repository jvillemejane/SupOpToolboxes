import cv2 as cv
import numpy as np
import sys

# Create a black image - 512x512 images - RGB layers
img = np.zeros((512,512,3), np.uint8)

# Draw a diagonal blue line with thickness of 5 px
cv.line(img,(0,0),(511,511),(255,0,0),5)

# Draw a rectangle - top-left-corner to bottom-right-corner - RGB color
cv.rectangle(img,(384,0),(510,128),(0,255,0),3)
# Draw a circle - center - diameter - RGB color
cv.circle(img,(447,63), 63, (0,0,255), -1)

# Text in an image
font = cv.FONT_HERSHEY_SIMPLEX
cv.putText(img,'OpenCV',(10,500), font, 2,(255,255,255),2,cv.LINE_AA)

cv.imshow("Drawing", img)