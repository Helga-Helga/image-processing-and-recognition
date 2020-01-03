import os
import sys
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from numpy import full
from scipy.ndimage import convolve

sys.path.insert(1, '../lab1-histogram')
from utils import rgb2gray
from composing_filters import *

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

filter, resulting_image = sobel_filter(input_image)

ax_filter = fig.add_subplot(spec[0, 1])
ax_filter.set_title('Filter')
ax_filter.imshow(filter, cmap=plt.get_cmap('gray'))

ax_resulting_image = fig.add_subplot(spec[0, 2])
ax_resulting_image.set_title('Resulting image')
ax_resulting_image.imshow(resulting_image, cmap=plt.get_cmap('gray'))

for ax in [ax_original_image, ax_filter, ax_resulting_image]:
    ax.set_axis_off()

plt.show()
