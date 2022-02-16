import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
import sys
from PIL import Image


def removegreen(num):
    image = cv.imread('nobols/frame ('+str(num)+').png', cv.IMREAD_UNCHANGED)
    original = image.copy()

    l = int(max(5, 6))
    u = int(min(6, 6))

    ed = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    edges = cv.GaussianBlur(image, (21, 51), 3)
    edges = cv.cvtColor(edges, cv.COLOR_BGR2GRAY)
    edges = cv.Canny(edges, l, u)

    _, thresh = cv.threshold(edges, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5, 5))
    mask = cv.morphologyEx(thresh, cv.MORPH_CLOSE, kernel, iterations=4)

    data = mask.tolist()
    sys.setrecursionlimit(10**8)
    for i in range(len(data)):
        for j in range(len(data[i])):
            if data[i][j] != 255:
                data[i][j] = -1
            else:
                break
        for j in range(len(data[i])-1, -1, -1):
            if data[i][j] != 255:
                data[i][j] = -1
            else:
                break
    image = np.array(data)
    image[image != -1] = 255
    image[image == -1] = 0

    mask = np.array(image, np.uint8)

    result = cv.bitwise_and(original, original, mask=mask)
    result[mask == 0] = 255
    cv.imwrite('bg.png', result)

    image = Image.open('bg.png')
    image.convert("RGBA")
    datas = image.getdata()

    newData = []
    for item in datas:
        if item[0] == 255 and item[1] == 255 and item[2] == 255:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)

    image.putdata(newData)
    image.save("sinfondo/grame"+str(num)+".png", "PNG")

    print('Imagen #'+str(num)+' procesada!')


def removeres(num, comp):
    image_path = 'sinfondo/grame'+str(num)+'.png'
    bgcolor1 = [5, 253, 33]  # Codigo BGR del fondo
    bgcolor2 = [255, 255, 255]  # Codigo BGR del fondo

    img = cv.imread(image_path)
    img = cv.cvtColor(img, cv.COLOR_BGR2BGRA)

    img[np.all(img == bgcolor1 + [255], axis=2)] = [0, 0, 0, 0]
    img[np.all(img == bgcolor2 + [255], axis=2)] = [0, 0, 0, 0]

    cv.imwrite('sinfondo/frame'+comp+str(num)+'.png', img)

    print('Imagen #'+comp+str(num)+' REprocesada!')


for i in range(300):
    removegreen(i+1)

for i in range(1, 10):
    removeres(i, '00')

for i in range(10, 100):
    removeres(i, '0')

for i in range(100, 301):
    removeres(i, '')
