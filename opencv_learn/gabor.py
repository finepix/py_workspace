from skimage import data, filters
import matplotlib.pyplot as plt

img = data.camera()

filter_real, filter_image = filters.gabor(img, frequency=0.7)

fig, (x, y, z) = plt.subplots(ncols=3, figsize=(15, 6))
x.imshow(img)
y.imshow(filter_real, cmap="gray")
z.imshow(filter_image, cmap="gray")

plt.figure(figsize=(30, 8))

plt.subplot(131)
plt.imshow(img)

plt.subplot(132)
plt.imshow(filter_real)

plt.subplot(133)
plt.imshow(filter_image)

plt.tight_layout()
plt.show()
