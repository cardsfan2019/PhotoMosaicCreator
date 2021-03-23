import numpy as np
import os
import matplotlib.pylab as plt
from PIL import Image
import cv2
import numpy as np
NUM_IMAGES = 3

small_image_names = os.listdir("small_images/")

small_images = []

i = 0

def rename():
    for image in small_image_names:
        os.rename("small_images/" + image, "small_images/image_" + str(i) + ".JPG")
        print(i)
        i = i + 1

small_image_names = os.listdir("small_images/")

for image in small_image_names:
    if (i < NUM_IMAGES):
        temp = Image.open("small_images/" + image)
        temp = np.asarray(temp)
        final = cv2.resize(temp, (60, 40))
        small_images.append(np.array(final))
        print(i)
    i = i + 1
small_images = np.asarray(small_images)

np.save("image_comp", small_images)