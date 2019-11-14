import os
import sys
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from numpy import full

sys.path.insert(1, '../lab1-histogram')
from utils import rgb2gray
from morphological_operations import dilation

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

ax_dilated_image = fig.add_subplot(spec[0, 1])
s = full((5, 5), 0)
dilated_image = dilation(input_image, s)
ax_dilated_image.imshow(dilated_image, cmap=plt.get_cmap('gray'))

for ax in [ax_original_image, ax_dilated_image]:
    ax.set_axis_off()

plt.show()
