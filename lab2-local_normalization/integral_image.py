from numpy import zeros


def compute_integral_image(image, power=1):
    """Image integral representation computing

    Parameters
    ----------
    image : numpy 2d array
        Input image
    power: int
        Power of intensities to sum

    Returns
    -------
    numpy 2d array
        Integral representation of image
    """
    return (image ** power).cumsum(axis=0).cumsum(axis=1)


def window_sum(integral_image, window):
    """Compute sum of intensities in given window using integral representation

    Parameters
    ----------
    integral_image : numpy 2d array
        Integral representation of image
    window: list of 4 int values
        Contains coordinate of the top left pixel of window
        and size of the window

    Returns
    -------
    int
        Sum of intensities in image window
    """
    x = window[0]
    y = window[1]
    width = window[2]
    height = window[3]

    image_height, image_width = integral_image.shape

    if width is 0 and height is 0:
        return 0

    result = 0

    if y + height - 1 < image_height and x + width - 1 < image_width:
        result += integral_image[y + height - 1, x + width - 1]

    if y + height - 1 < image_height and x > 0:
        result -= integral_image[y + height - 1, x - 1]

    if y > 0 and x + width - 1 < image_width:
        result -= integral_image[y - 1, x + width - 1]

    if y > 0 and x > 0:
        result += integral_image[y - 1, x - 1]

    return result
