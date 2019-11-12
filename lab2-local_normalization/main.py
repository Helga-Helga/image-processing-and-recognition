import os
import sys
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.image as mpimg

from matplotlib.widgets import Button

sys.path.insert(1, '../lab1-histogram')
from utils import rgb2gray
from image_normalization import normalize_image
from utils2 import (
    get_factors,
    get_lists_intersection,
)
from integral_image import compute_integral_image

if len(sys.argv) > 1:
    image_path = sys.argv[1]
    if os.path.exists(image_path):
        input_image = rgb2gray(mpimg.imread(image_path))
    else:
        raise Exception('Bad image path')
else:
    raise Exception('Usage: python main.py image_path')

fig = plt.figure()
spec = fig.add_gridspec(ncols=2, nrows=1)

ax_original_image = fig.add_subplot(spec[0, 0])
ax_original_image.set_title('Original image')
ax_original_image.imshow(input_image, cmap=plt.get_cmap('gray'))

ax_normalized_image = fig.add_subplot(spec[0, 1])
ax_normalized_image.set_title('Normalized image')

integral_image = compute_integral_image(input_image)
integral_image_square = compute_integral_image(input_image, 2)
normalized_image = normalize_image(
    input_image, integral_image, integral_image_square, 100, 200, 100)
ax_normalized_image.imshow(normalized_image, cmap=plt.get_cmap('gray'))

for ax in [ax_original_image, ax_normalized_image]:
    ax.set_axis_off()

plt.show()
