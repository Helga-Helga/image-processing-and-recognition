import os
import sys
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.image as mpimg
from matplotlib.widgets import Slider
from matplotlib.ticker import AutoMinorLocator
from numpy import (
    arange,
    round,
)

from utils import (
    rgb2gray,
    calculate_histogram,
    threshold_binarization,
)
from otsus_binarization import get_optimal_threshold


if len(sys.argv) > 1:
    image_path = sys.argv[1]
    if os.path.exists(image_path):
        input_image = rgb2gray(mpimg.imread(image_path))
    else:
        raise Exception('Bad image path')
else:
    raise Exception('Usage: python main.py image_path')

histogram = calculate_histogram(input_image)


fig = plt.figure()
widths = [2, 2, 2]
heights = [2, 4, 0.25]
spec = fig.add_gridspec(ncols=3, nrows=3,
                        width_ratios=widths, height_ratios=heights)

ax_original_image = fig.add_subplot(spec[0, 0])
ax_original_image.set_title('Original image')
ax_original_image.imshow(input_image, cmap=plt.get_cmap('gray'))

ax_otsus_binarization = fig.add_subplot(spec[0, 2])
ax_otsus_binarization.set_title('Otsu\'s binarization')
otsus_threshold = get_optimal_threshold(histogram)
print("Optimal threshold using Otsu's algorihms:", otsus_threshold)
ax_otsus_binarization.imshow(
    threshold_binarization(input_image, otsus_threshold),
    cmap=plt.get_cmap('gray')
)

ax_threshold_binarization = fig.add_subplot(spec[0, 1])
ax_threshold_binarization.set_title('Threshold binarization')
ax_threshold_binarization.imshow(
    threshold_binarization(input_image, otsus_threshold),
    cmap=plt.get_cmap('gray')
)

ax_histogram = fig.add_subplot(spec[1, :])
ax_histogram.set_title('Histogram')
vertical_line = plt.axvline(x=otsus_threshold, color='red')
ax_histogram.set_xlim([0, 255])
plt.bar(arange(256), histogram, color='black')
ax_histogram.xaxis.set_minor_locator(AutoMinorLocator(50))

ax_slider = fig.add_subplot(spec[2, :])
slider = Slider(ax_slider, 'Threshold', 0, 255, valinit=otsus_threshold,
                valfmt='%0.0f', color='black')


def update(val):
    current_threshold = int(slider.val)
    vertical_line.set_xdata(current_threshold)
    ax_threshold_binarization.imshow(
        threshold_binarization(input_image, current_threshold),
        cmap=plt.get_cmap('gray')
    )


slider.on_changed(update)

for ax in [ax_original_image,
           ax_threshold_binarization,
           ax_otsus_binarization,
           ax_slider]:
    ax.set_axis_off()

plt.show()
