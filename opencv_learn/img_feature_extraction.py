import skimage
import matplotlib.pyplot as plt
import numpy as np
import cv2
from skimage import data, img_as_float, exposure


if __name__ == '__main__':
    img = data.astronaut()

    # cv2.imshow('ast', img)
    # cv2.waitKey(-1)

    img = img_as_float(img)
    cv2.imshow('ast', img)
    cv2.waitKey(-1)
