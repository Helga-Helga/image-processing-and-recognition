from numpy import (
    exp,
    dot,
    ix_,
    average,
    transpose,
    tile,
    repeat,
    arange,
    resize,
)
from operator import itemgetter


def bilateral_filter(image, window_height, window_width, sigma_d, sigma_r):
    """Denoising image with bilateral filter

    Parameters
    ----------
    image : numpy 2d array
        Input image
    window_height: int
        Half of window height (radius)
    window_width: int
        Half of window width (radius)
    sigma_d: float
        Smoothing parameter for distance between pixels
    sigma_r: float
        Smoothing parameter for difference between intensities

    Returns
    -------
    numpy 2d array
        Denoised image with bilateral filter
    """
    filtered_image = image.copy()
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            print("Pricessing pixel ({}, {})".format(i, j))
            # coordinates of window for x axis
            window_x = arange(max(0, i - window_height),
                              min(image.shape[0], i + window_height + 1))
            # coordinates of window for y axis
            window_y = arange(max(0, j - window_width),
                              min(image.shape[1], j + window_width + 1))
            # array of pairs <x, y> from <window_x, window_y>
            pr = transpose([tile(window_x, len(window_y)),
                            repeat(window_y, len(window_x))])
            # part of image under filter
            image_window = image[ix_(window_x, window_y)]

            intensity_part = (image[i, j] - image_window) ** 2 / (2 * sigma_r)
            distance_part = resize(
                (([i, j] - pr) ** 2).sum(axis=1) / (2 * sigma_d),
                (intensity_part.shape))
            weights = exp(-distance_part - intensity_part)
            filtered_image[i, j] = average(image_window, weights=weights)
    return filtered_image
