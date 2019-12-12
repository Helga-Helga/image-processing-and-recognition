from numpy import exp


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
            print(i, j)
            numerator = 0.0
            denominator = 0.0
            for k in range(i - window_height, i + window_height + 1):
                if k < 0 or k >= image.shape[0]:
                    continue
                for l in range(j - window_width, j + window_width + 1):
                    if l < 0 or l >= image.shape[1]:
                        continue
                    w = exp(-((i - k) ** 2 + (j - l) ** 2) /
                            (2 * sigma_d) -
                            ((image[i, j] - image[k, l]) ** 2) /
                            (2 * sigma_r))
                    numerator += image[k, l] * w
                    denominator += w
            filtered_image[i, j] = numerator / denominator
    return filtered_image
