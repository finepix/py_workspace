from skimage.feature import local_binary_pattern
from skimage import data
import cv2
import matplotlib.pyplot as plt

radius = 2
n_points = 8 * radius

image = data.astronaut()
image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

image_lbp = local_binary_pattern(image_gray, n_points, radius)

# fig, (x, y) = plt.subplots(ncols=2)
#
# x.imshow(image)
# y.imshow(image_lbp)
plt.figure(figsize=(20, 8))

plt.subplot(121)
plt.imshow(image[:, :, ::-1])

plt.subplot(122)
plt.imshow(image_lbp)

plt.tight_layout()
plt.show()
