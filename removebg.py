import cv2
import numpy as np

image_path = 'test.png'  # Path to the input image
bgcolor = [255, 255, 255]  # BGR value of background color.

img = cv2.imread(image_path)
img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)

img[np.all(img == bgcolor + [255], axis=2)] = [0, 0, 0, 0]
# File will be saved as output.png in the current directory.
cv2.imwrite('output.png', img)
