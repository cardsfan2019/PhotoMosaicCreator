import numpy as np
import os
import matplotlib.pylab as plt
import math
import cv2
from PIL import Image
import imageio

large_image = plt.imread("large_image/large.JPG")

large_image = cv2.resize(large_image, (2560, 1440))
(full_y, full_x, full_depth) = large_image.shape
small_images = np.load("image_comp.npy")
(num_images, height, width, depth) = small_images.shape

average_rgbs = []
res = round(full_y / height)

pixels = 0
scale = 1

for i in range(num_images):
    r = 0
    g = 0
    b = 0
    for j in range(height):
        for l in range(width):
            pixel = small_images[i][j][l]
            r = r + pixel[0]
            g = g + pixel[1]
            b = b + pixel[2]

    average_rgbs.append([
            math.floor(r/(height*width)), 
            math.floor(g/(height*width)), 
            math.floor(b/(height*width))
        ])

average_rgbs = np.asarray(average_rgbs)

broken_down_large = []

startX = 0
startY = 0

currentImage = 0
numImages = round((res / scale) * (res / scale))

for im in range(numImages): #stores blocks of the large image individually in an array
    col = [] #initialize new col to store rows
    for i in range(round(height * scale)):
        row = [] #initialize new row to store individual pixels (r, g, b)
        for j in range(round(width * scale)):
            row.append(large_image[i + startY][j + startX]) #append pixel rgb to the row
        col.append(row) #append row of pixels to the column
    broken_down_large.append(col) #append col of rows to the broken down large image
    if (im + 1) % round(res / scale) == 0: #if the end of the row is reached, move down and back to the beginning
        startX = 0
        startY = round(startY + (height * scale))
    else: #otherwise move to the right
        startX = round(startX + (width * scale))



for im in broken_down_large:
    im = np.asarray(im)
    im = cv2.resize(im, (width, height))


broken_down_large_average_rgbs = []

for im in broken_down_large:
    r = 0
    g = 0
    b = 0
    for j in range(round(height * scale)):
        for l in range(round(width * scale)):
            pixel = im[j][l]
            r = r + pixel[0]
            g = g + pixel[1]
            b = b + pixel[2]

    broken_down_large_average_rgbs.append([
            math.floor(r/(height*width)), 
            math.floor(g/(height*width)), 
            math.floor(b/(height*width))
        ])

broken_down_large_average_rgbs = np.asarray(broken_down_large_average_rgbs)

closest_match = []

for i in range(len(broken_down_large_average_rgbs)):
    minimum = 255 * 3
    minimumLocation = 0
    for j in range(len(average_rgbs)):
        lr = broken_down_large_average_rgbs[i][0]
        lg = broken_down_large_average_rgbs[i][1]
        lb = broken_down_large_average_rgbs[i][2]

        sr = average_rgbs[j][0]
        sg = average_rgbs[j][1]
        sb = average_rgbs[j][2]

        difference = (((lr-sr)/255.0)**2 + ((lg-sg)/255.0)**2 + ((lb-sb)/255.0)**2) * 255
        if difference < minimum:
            minimumLocation = j
            minimum = difference
    closest_match.append(minimumLocation)
print("Starting assembly of large image ----------------------------------------------")
final_image = np.zeros((full_y, full_x, full_depth), dtype=int)

largeImageStartX = 0
largeImageStartY = 0

iteration = 1
for image in closest_match: #stores the index of the closest picture to the original
    print(largeImageStartX, ",", largeImageStartY)
    image = cv2.resize(small_images[image], (round(width * scale), round(height * scale)))
    for i in range(round(height * scale)):
        for j in range(round(width * scale)):
            final_image[largeImageStartY + i][largeImageStartX + j] = image[i][j]
    if largeImageStartX == full_x - round((width * scale)):
        largeImageStartX = 0
        largeImageStartY = round(largeImageStartY + (height * scale))
    else:
        largeImageStartX = round(largeImageStartX + (width * scale))

imageio.imwrite('mosaic.jpg', final_image)