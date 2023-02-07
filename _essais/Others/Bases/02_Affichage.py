import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

image = Image.open('airy_2mm.bmp')
plt.figure()
plt.imshow(image, cmap='gray')
plt.show()
pts = plt.ginput(1)

print(pts)