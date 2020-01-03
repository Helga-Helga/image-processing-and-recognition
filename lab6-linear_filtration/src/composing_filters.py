from numpy import (
    zeros,
    ones,
    full,
    exp,
    pi,
)
from scipy.ndimage import convolve


def shift_left(image, size):
    """Shift image left by 1 pixel

    Parameters
    ----------
    image : numpy 2d array
        Input monochrome image
    size : unsigned int
        Number of rows and columns of a square linear filter

    Returns
    -------
    numpy 2d array
        Filter matrix
    numpy 2d array
        Result of image filtration
    """
    shift_left_filter = zeros((size, size))
    horizontal_index = (size - 1) / 2
    shift_left_filter[int(horizontal_index), size - 1] = 1
    return shift_left_filter, convolve(image, shift_left_filter)


def shift_right(image, size):
    """Shift image right by 1 pixel

    Parameters
    ----------
    image : numpy 2d array
        Input monochrome image
    size : unsigned int
        Number of rows and columns of a square linear filter

    Returns
    -------
    numpy 2d array
        Filter matrix
    numpy 2d array
        Result of image filtration
    """
    shift_right_filter = zeros((size, size))
    horizontal_index = (size - 1) / 2
    shift_right_filter[int(horizontal_index), 0] = 1
    return shift_right_filter, convolve(image, shift_right_filter)


def shift_up(image, size):
    """Shift image up by 1 pixel

    Parameters
    ----------
    image : numpy 2d array
        Input monochrome image
    size : unsigned int
        Number of rows and columns of a square linear filter

    Returns
    -------
    numpy 2d array
        Filter matrix
    numpy 2d array
        Result of image filtration
    """
    shift_up_filter = zeros((size, size))
    vertical_index = (size - 1) / 2
    shift_up_filter[size - 1, int(vertical_index)] = 1
    return shift_up_filter, convolve(image, shift_up_filter)


def shift_down(image, size):
    """Shift image down by 1 pixel

    Parameters
    ----------
    image : numpy 2d array
        Input monochrome image
    size : unsigned int
        Number of rows and columns of a square linear filter

    Returns
    -------
    numpy 2d array
        Filter matrix
    numpy 2d array
        Result of image filtration
    """
    shift_down_filter = zeros((size, size))
    vertical_index = (size - 1) / 2
    shift_down_filter[0, int(vertical_index)] = 1
    return shift_down_filter, convolve(image, shift_down_filter)


def box_filter(image, size):
    """Bluring with a box filter

    Parameters
    ----------
    image : numpy 2d array
        Input monochrome image
    size : unsigned int
        Number of rows and columns of a square linear filter

    Returns
    -------
    numpy 2d array
        Filter matrix
    numpy 2d array
        Result of image filtration
    """
    box_filter = ones((size, size)) / size ** 2
    return box_filter, convolve(image, box_filter)


def sharpening(image, size):
    """Sharpening image:
    - accentuates differences with local average
    - known as Laplacian

    Parameters
    ----------
    image : numpy 2d array
        Input monochrome image
    size : unsigned int
        Number of rows and columns of a square linear filter

    Returns
    -------
    numpy 2d array
        Filter matrix
    numpy 2d array
        Result of image filtration
    """
    first_part = zeros((size, size))
    center_index = int((size - 1) / 2)
    first_part[center_index, center_index] = 1
    sharpening_filter = first_part - box_filter(image, size)[0]
    return sharpening_filter, image + convolve(image, sharpening_filter)


def smoothing(image, size, r):
    """Smoothing image
    All filter elements are equal to 1 / (2r + 1)^2.
    Drawback: all pixels on any distance from the processed pixel
    have the same impact on the result

    Parameters
    ----------
    image : numpy 2d array
        Input monochrome image
    size : unsigned int
        Number of rows and columns of a square linear filter
    r: number
        Parameter for calculating filter values

    Returns
    -------
    numpy 2d array
        Filter matrix
    numpy 2d array
        Result of image filtration
    """
    smoothing_filter = full((size, size), 1 / (2 * r + 1) ** 2)
    return smoothing_filter, convolve(image, smoothing_filter)


def gaussian_filter(image, size, sigma):
    """Smoothing image with Gaussian filter
    Impact of a pixel decreases proportionally to square distance to it

    Parameters
    ----------
    image : numpy 2d array
        Input monochrome image
    size : unsigned int
        Number of rows and columns of a square linear filter
    sigma: number
        Dispersion

    Returns
    -------
    numpy 2d array
        Filter matrix
    numpy 2d array
        Result of image filtration
    """
    gaussian_filter = zeros((size, size))
    center_index = int((size - 1) / 2)
    for i in range(-center_index, center_index + 1):
        for j in range(-center_index, center_index + 1):
            gaussian_filter[i + center_index, j + center_index] = exp(
                -(i ** 2 + j ** 2) / (2 * sigma ** 2)
            )
    gaussian_filter /= (2 * pi * sigma ** 2)
    return gaussian_filter, convolve(image, gaussian_filter)


def contrast_enhancing_filter(image, size):
    """Contrast enhancing filter:
    - center value of filter is bigger than 1
    - the sum of all elements of filter equals to 1

    Parameters
    ----------
    image : numpy 2d array
        Input monochrome image
    size : unsigned int
        Number of rows and columns of a square linear filter

    Returns
    -------
    numpy 2d array
        Filter matrix
    numpy 2d array
        Result of image filtration
    """
    contrast_enhancing_filter = zeros((size, size))
    center_index = int((size - 1) / 2)
    contrast_enhancing_filter[center_index, 0] = -1
    contrast_enhancing_filter[center_index, -1] = -1
    contrast_enhancing_filter[0, center_index] = -1
    contrast_enhancing_filter[-1, center_index] = -1
    contrast_enhancing_filter[center_index, center_index] = 5
    return contrast_enhancing_filter, image + convolve(
        image, contrast_enhancing_filter)


def prewitt_filter_x(image):
    """Differential Prewitt filter for x coordinate
    The sum of filter elements is equal to 0

    Parameters
    ----------
    image : numpy 2d array
        Input monochrome image

    Returns
    -------
    numpy 2d array
        Filter matrix
    numpy 2d array
        Result of image filtration
    """
    prewitt_filter_x = zeros((3, 3))
    prewitt_filter_x[:, 0] = -1
    prewitt_filter_x[:, 2] = 1
    prewitt_filter_x /= 3
    return prewitt_filter_x, convolve(image, prewitt_filter_x)


def prewitt_filter_y(image):
    """Differential Prewitt filter for y coordinate
    The sum of filter elements is equal to 0

    Parameters
    ----------
    image : numpy 2d array
        Input monochrome image

    Returns
    -------
    numpy 2d array
        Filter matrix
    numpy 2d array
        Result of image filtration
    """
    prewitt_filter_y = zeros((3, 3))
    prewitt_filter_y[0, :] = -1
    prewitt_filter_y[2, :] = 1
    prewitt_filter_y /= 3
    return prewitt_filter_y, convolve(image, prewitt_filter_y)


def prewitt_filter(image):
    """Differential Prewitt filter for both x and y coordinates

    Parameters
    ----------
    image : numpy 2d array
        Input monochrome image

    Returns
    -------
    numpy 2d array
        Filter matrix
    numpy 2d array
        Result of image filtration
    """
    filter_x, resulting_image_x = prewitt_filter_x(image)
    filter_y, resulting_image_y = prewitt_filter_y(image)
    resulting_image = (resulting_image_x ** 2 + resulting_image_y ** 2) ** 0.5
    filter = (filter_x ** 2 + filter_y ** 2) ** 0.5
    return filter, resulting_image


def sobel_filter_x(image):
    """Differential Sobel filter for x coordinate
    The sum of filter elements is equal to 0

    Parameters
    ----------
    image : numpy 2d array
        Input monochrome image

    Returns
    -------
    numpy 2d array
        Filter matrix
    numpy 2d array
        Result of image filtration
    """
    sobel_filter_x = zeros((3, 3))
    sobel_filter_x[:, 0] = -1
    sobel_filter_x[1, 0] = -2
    sobel_filter_x[:, 2] = 1
    sobel_filter_x[1, 2] = 2
    sobel_filter_x /= 4
    return sobel_filter_x, convolve(image, sobel_filter_x)


def sobel_filter_y(image):
    """Differential Sobel filter for y coordinate
    The sum of filter elements is equal to 0

    Parameters
    ----------
    image : numpy 2d array
        Input monochrome image

    Returns
    -------
    numpy 2d array
        Filter matrix
    numpy 2d array
        Result of image filtration
    """
    sobel_filter_y = zeros((3, 3))
    sobel_filter_y[0, :] = -1
    sobel_filter_y[0, 1] = -2
    sobel_filter_y[2, :] = 1
    sobel_filter_y[2, 1] = 2
    sobel_filter_y /= 4
    return sobel_filter_y, convolve(image, sobel_filter_y)


def sobel_filter(image):
    """Differential Sobel filter for both x and y coordinates

    Parameters
    ----------
    image : numpy 2d array
        Input monochrome image

    Returns
    -------
    numpy 2d array
        Filter matrix
    numpy 2d array
        Result of image filtration
    """
    filter_x, resulting_image_x = sobel_filter_x(image)
    filter_y, resulting_image_y = sobel_filter_y(image)
    resulting_image = (resulting_image_x ** 2 + resulting_image_y ** 2) ** 0.5
    filter = (filter_x ** 2 + filter_y ** 2) ** 0.5
    return filter, resulting_image


def roberts_filter_x(image, size):
    """Differential Roberts filter for x coordinate
    It approximates partial derivative

    Parameters
    ----------
    image : numpy 2d array
        Input monochrome image
    size: unsigned int
        Can be 2 or 3: size of square pixels (number or rows and columns)

    Returns
    -------
    numpy 2d array
        Filter matrix
    numpy 2d array
        Result of image filtration
    """
    if size == 2:
        roberts_filter_x = zeros((2, 2))
        roberts_filter_x[0, 0] = -1
        roberts_filter_x[1, 1] = 1
    elif size == 3:
        roberts_filter_x = zeros((3, 3))
        roberts_filter_x[0, 0] = -1
        roberts_filter_x[1, 0] = -1
        roberts_filter_x[0, 1] = -1
        roberts_filter_x[1, 2] = 1
        roberts_filter_x[2, 1] = 1
        roberts_filter_x[2, 2] = 1
    else:
        raise("Unsupported filter size. Try 2 or 3")
    return roberts_filter_x, convolve(image, roberts_filter_x)


def roberts_filter_y(image, size):
    """Differential Roberts filter for y coordinate
    It approximates partial derivative

    Parameters
    ----------
    image : numpy 2d array
        Input monochrome image
    size: unsigned int
        Can be 2 or 3: size of square pixels (number or rows and columns)

    Returns
    -------
    numpy 2d array
        Filter matrix
    numpy 2d array
        Result of image filtration
    """
    if size == 2:
        roberts_filter_y = zeros((2, 2))
        roberts_filter_y[0, 1] = -1
        roberts_filter_y[1, 0] = 1
    elif size == 3:
        roberts_filter_y = zeros((3, 3))
        roberts_filter_y[0, 1] = -1
        roberts_filter_y[0, 2] = -1
        roberts_filter_y[1, 2] = -1
        roberts_filter_y[1, 0] = 1
        roberts_filter_y[2, 0] = 1
        roberts_filter_y[2, 1] = 1
    else:
        raise("Unsupported filter size. Try 2 or 3")
    return roberts_filter_y, convolve(image, roberts_filter_y)


def roberts_filter(image, size):
    """Differential Roberts filter for both x and y coordinates

    Parameters
    ----------
    image : numpy 2d array
        Input monochrome image
    size: unsigned int
        Can be 2 or 3: size of square pixels (number or rows and columns)

    Returns
    -------
    numpy 2d array
        Filter matrix
    numpy 2d array
        Result of image filtration
    """
    filter_x, resulting_image_x = roberts_filter_x(image, size)
    filter_y, resulting_image_y = roberts_filter_y(image, size)
    resulting_image = (resulting_image_x ** 2 + resulting_image_y ** 2) ** 0.5
    filter = (filter_x ** 2 + filter_y ** 2) ** 0.5
    return filter, resulting_image


def laplacian_filter(image):
    """2d Laplacian operator
    It approximates the second partial derivatives

    Parameters
    ----------
    image : numpy 2d array
        Input monochrome image

    Returns
    -------
    numpy 2d array
        Filter matrix
    numpy 2d array
        Result of image filtration
    """
    laplacian_filter = zeros((3, 3))
    laplacian_filter[0, 1] = 1
    laplacian_filter[1, 0] = 1
    laplacian_filter[2, 1] = 1
    laplacian_filter[1, 2] = 1
    laplacian_filter[1, 1] = -4
    return laplacian_filter, image + convolve(image, laplacian_filter)
