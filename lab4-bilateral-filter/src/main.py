import os
import sys
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from numpy import full

sys.path.insert(1, '../lab1-histogram')
from utils import rgb2gray
from noise import noise_image
from bilateral_filter import bilateral_filter

if len(sys.argv) > 1:
    image_path = sys.argv[1]
    if os.path.exists(image_path):
        input_image = rgb2gray(mpimg.imread(image_path))
    else:
        raise Exception('Bad image path')
else:
    raise Exception('Usage: python main.py image_path')

fig = plt.figure()
spec = fig.add_gridspec(ncols=3, nrows=1)

ax_original_image = fig.add_subplot(spec[0, 0])
ax_original_image.set_title('Original image')
ax_original_image.imshow(input_image, cmap=plt.get_cmap('gray'))

ax_noised_image = fig.add_subplot(spec[0, 1])
ax_noised_image.set_title('Noised image')
noised_image = noise_image(input_image, 0, 20)
ax_noised_image.imshow(noised_image, cmap=plt.get_cmap('gray'))

ax_resulting_image = fig.add_subplot(spec[0, 2])
ax_resulting_image.set_title('Resulting image')
resulting_image = bilateral_filter(noised_image, 10, 10, 40 ** 2, 40 ** 2)
ax_resulting_image.imshow(resulting_image, cmap=plt.get_cmap('gray'))

for ax in [ax_original_image, ax_noised_image, ax_resulting_image]:
    ax.set_axis_off()

plt.show()
