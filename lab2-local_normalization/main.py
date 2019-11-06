from utils import rgb2gray
from image_normalization import normalize_image

import os
import sys
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.image as mpimg

sys.path.insert(1, '../lab1-histogram')

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

ax_grid = fig.add_subplot(spec[0, 1])
ax_grid.set_title('Rectangle blocks')
normalized_image = normalize_image(input_image, 500, 128, 1000)
ax_grid.imshow(normalized_image, cmap=plt.get_cmap('gray'))

ax_normalized_image = fig.add_subplot(spec[0, 2])
ax_normalized_image.set_title('Normalized image')
ax_normalized_image.imshow(input_image, cmap=plt.get_cmap('gray'))

for ax in [ax_original_image, ax_grid, ax_normalized_image]:
    ax.set_axis_off()

plt.show()
