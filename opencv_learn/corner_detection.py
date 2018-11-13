import cv2
from skimage import data
import numpy as np


def corner_detect(im):
    """
            角点检测，使用Harris Corner检测算法
    :param im:
    :return:
    """
    gray = cv2.cvtColor(im, cv2.COLOR_RGB2GRAY)

    gray = np.float32(gray)
    dst = cv2.cornerHarris(gray, 2, 3, 0.04)

    dst = cv2.dilate(dst, None)

    # Threshold for an optimal value, it may vary depending on the image.
    im[dst > 0.01 * dst.max()] = [0, 0, 255]

    return im


if __name__ == '__main__':
    img = data.astronaut()

    img = corner_detect(img)

    cv2.imshow('corner detect ', img)
    if cv2.waitKey(0) & 0xff == 27:
        cv2.destroyAllWindows()
