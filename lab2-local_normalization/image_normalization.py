import matplotlib.pyplot as plt
from numpy import clip

from integral_image import (
    compute_integral_image,
    window_sum,
)


def normalize_image(image, integral_image, integral_image_square,
                    grid_size_h, grid_size_v, new_mean, new_dispersion):
    """Local brightness normalizaiton of rectangular blocks of image
    by new mean and dispersion values using image integral representation

    Parameters
    ----------
    image : numpy 2d array
        Input image
    integral_image: numpy 2d array
        Integral representation of image
    integral_image_square: numpy 2d array
        Integral representation of image, where intensities are squared
    grid_size: int
        Size in pixels of rectangle (currently square)
    new_mean:
        Mean value for intensities in normalized image
    new_dispersion:
        Dispersion value for intensities in normalized image

    Returns
    -------
    numpy 2d array
        Normalized image
    """
    normalized_image = image.copy()
    height, width = image.shape
    for i in range(0, height, grid_size_v):
        for j in range(0, width, grid_size_h):
            window = [j, i, grid_size_h, grid_size_v]
            mean = window_sum(
                integral_image, window) / (grid_size_h * grid_size_v)
            square_mean = window_sum(
                integral_image_square, window) / (grid_size_h * grid_size_v)
            dispersion = square_mean - (mean ** 2)

            for pixel_i in range(i, i + grid_size_v):
                for pixel_j in range(j, j + grid_size_h):
                    if dispersion == 0.0:
                        normalized_image[pixel_i, pixel_j] = new_mean
                    else:
                        normalized_image[pixel_i, pixel_j] = \
                            clip((image[pixel_i, pixel_j] - mean) * \
                            new_dispersion / dispersion + new_mean, 0, 255)
    return normalized_image
