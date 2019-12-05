import os
import sys
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from numpy import full

sys.path.insert(1, '../lab1-histogram')
from utils import rgb2gray
from morphological_operations import (
    dilation,
    erosion,
    closing,
    opening,
    get_edges,
)

if len(sys.argv) > 1:
    image_path = sys.argv[1]
    if os.path.exists(image_path):
        input_image = rgb2gray(mpimg.imread(image_path))
    else:
        raise Exception('Bad image path')
else:
    raise Exception('Usage: python main.py image_path')

fig = plt.figure()
spec = fig.add_gridspec(ncols=3, nrows=2)

ax_original_image = fig.add_subplot(spec[0, 0])
ax_original_image.set_title('Original image')
ax_original_image.imshow(input_image, cmap=plt.get_cmap('gray'))

s = full((5, 5), 1)

ax_dilated_image = fig.add_subplot(spec[0, 1])
dilated_image = dilation(input_image, s)
ax_dilated_image.set_title('Dilated image')
ax_dilated_image.imshow(dilated_image, cmap=plt.get_cmap('gray'))

ax_erosed_image = fig.add_subplot(spec[0, 2])
erosed_image = erosion(input_image, s)
ax_erosed_image.set_title('Erosed image')
ax_erosed_image.imshow(erosed_image, cmap=plt.get_cmap('gray'))

ax_closed_image = fig.add_subplot(spec[1, 0])
closed_image = closing(input_image, s)
ax_closed_image.set_title('Closed image')
ax_closed_image.imshow(closed_image, cmap=plt.get_cmap('gray'))

ax_opened_image = fig.add_subplot(spec[1, 1])
opened_image = opening(input_image, s)
ax_opened_image.set_title('Opened image')
ax_opened_image.imshow(opened_image, cmap=plt.get_cmap('gray'))

ax_edges = fig.add_subplot(spec[1, 2])
edges = get_edges(input_image, s)
ax_edges.set_title('Edges')
ax_edges.imshow(edges, cmap=plt.get_cmap('gray'))

for ax in [ax_original_image,
           ax_dilated_image, ax_erosed_image,
           ax_closed_image, ax_opened_image, ax_edges]:
    ax.set_axis_off()

plt.show()
