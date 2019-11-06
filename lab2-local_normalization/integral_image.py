from numpy import zeros


def compute_integral_image(image):
    """Image integral representation computing

    Parameters
    ----------
    image : numpy 2d array
        Input image

    Returns
    -------
    numpy 2d array
        Integral representation of image
    """
    height, width = image.shape
    integral_image = zeros((height, width))

    for i in range(height):
        for j in range(width):
            sum_in_line = zeros(width)
            sum_in_line[j] = image[i, j]
            if j > 0:
                sum_in_line[j] += sum_in_line[j - 1]

            integral_image[i, j] = sum_in_line[j]
            if i > 0:
                integral_image[i, j] += integral_image[i - 1, j]

    return integral_image


def window_sum(integral_image, window, mean=0):
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
