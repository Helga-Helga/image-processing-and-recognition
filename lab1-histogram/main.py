import matplotlib
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.image as mpimg
from matplotlib.widgets import Slider
from matplotlib.ticker import AutoMinorLocator

input_image = mpimg.imread("original_image.jpg")

fig = plt.figure(constrained_layout=True)
widths = [2, 2, 2]
heights = [2, 4, 0.25]
spec = fig.add_gridspec(ncols=3, nrows=3,
                        width_ratios=widths, height_ratios=heights)

gs = fig.add_gridspec(3, 3)

ax_original_image = fig.add_subplot(spec[0, 0])
ax_original_image.set_title('Original image')
ax_original_image.imshow(input_image)

ax_histogram_binarization = fig.add_subplot(spec[0, 1])
ax_histogram_binarization.set_title('Histogram binarization')
ax_histogram_binarization.imshow(input_image)

ax_otsus_binarization = fig.add_subplot(spec[0, 2])
ax_otsus_binarization.set_title('Otsu\'s binarization')
ax_otsus_binarization.imshow(input_image)

ax_histogram = fig.add_subplot(spec[1, :])
ax_histogram.set_title('Histogram')
vertical_line = plt.axvline(x=0)
ax_histogram.set_xlim([0, 255])
ax_histogram.xaxis.set_minor_locator(AutoMinorLocator(50))

ax_slider = fig.add_subplot(spec[2, :])
slider = Slider(ax_slider, 'Threshold', 0, 255, valinit=0, valfmt='%0.0f')


def update(val):
    current_threshrold = int(slider.val)
    vertical_line.set_xdata(current_threshrold)


slider.on_changed(update)

for ax in [ax_original_image,
           ax_histogram_binarization,
           ax_otsus_binarization,
           ax_slider]:
    ax.set_axis_off()

plt.show()
