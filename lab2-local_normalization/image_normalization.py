import matplotlib.pyplot as plt
from numpy import clip
from statistics import mean

from integral_image import (
    compute_integral_image,
    window_sum,
)


def average_intensity(intensities):
    """Calculation of average intensity value among list elements

    Parameters
    ----------
    intensities : list of integers
        list of intensities for pixel

    Returns
    -------
    int
        Average intensity from the list
    """
    if len(intensities) == 1:
        return clip(intensities, 0, 255)
    return clip(round(mean(intensities)), 0, 255)


def normalize_image(image, integral_image, integral_image_square,
                    grid_size_h, grid_size_v, intersection_area,
                    new_mean, new_dispersion):
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
    grid_size_h: int
        Height in pixels of rectangle
    grid_size_v: int
        Width in pixels of rectangle
    intersection_area: int
        Width and height of intersected area between two neighbor rectangles
    new_mean:
        Mean value for intensities in normalized image
    new_dispersion:
        Dispersion value for intensities in normalized image

    Returns
    -------
    numpy 2d array
        Normalized image
    """
    height, width = image.shape

    # create matrix of lists for normalized intensities
    # new intensity for a pixel will be
    # an average intensity of corresponding list
    normalized_intensities = []
    for i in range(height):
        normalized_intensities.append([])
        for j in range(width):
            normalized_intensities[i].append([])

    for i in range(0, height, grid_size_v - intersection_area):
        if i + grid_size_v >= height:
            i = height - grid_size_v
        for j in range(0, width, grid_size_h - intersection_area):
            if j + grid_size_h >= width:
                j = width - grid_size_h
            window = [j, i, grid_size_h, grid_size_v]
            mean = window_sum(
                integral_image, window) / (grid_size_h * grid_size_v)
            square_mean = window_sum(
                integral_image_square, window) / (grid_size_h * grid_size_v)
            dispersion = square_mean - (mean ** 2)

            for pixel_i in range(i, i + grid_size_v):
                for pixel_j in range(j, j + grid_size_h):
                    if dispersion == 0.0:
                        normalized_intensities[pixel_i][pixel_j].append(
                            new_mean)
                    else:
                        normalized_intensities[pixel_i][pixel_j].append(
                            (image[pixel_i, pixel_j] - mean) *
                            new_dispersion / dispersion + new_mean)

    normalized_image = image.copy()
    for i in range(height):
        for j in range(width):
            normalized_image[i, j] = average_intensity(
                normalized_intensities[i][j])
    return normalized_image
