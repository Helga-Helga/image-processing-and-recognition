import matplotlib.pyplot as plt

from integral_image import (
    compute_integral_image,
    window_sum,
)


def normalize_image(image, integral_image, grid_size, new_mean, new_dispersion):
    """Local brightness normalizaiton of rectangular blocks of image
    by new mean and dispersion values using image integral representation

    Parameters
    ----------
    image : numpy 2d array
        Input image
    integral_image: numpy 2d array
        Integral representation of image
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
    for i in range(0, height, grid_size):
        for j in range(0, width, grid_size):
            window = [j, i, grid_size, grid_size]
            mean = window_sum(integral_image, window) / pow(grid_size, 2)
            dispersion = sum(
                (pow(image[y, x] - mean, 2)
                    for y in range(i, i + grid_size)
                    for x in range(j, j + grid_size))
                ) / (pow(grid_size, 2) - 1)

            for pixel_i in range(i, i + grid_size):
                for pixel_j in range(j, j + grid_size):
                    normalized_image[pixel_i, pixel_j] = \
                        (image[pixel_i, pixel_j] - mean) * \
                        new_dispersion / dispersion + new_mean
    return normalized_image
