from numpy import (
    random,
    clip,
    round,
)


def noise_image(image, mean, sigma):
    """Adding Gaussian noise to image

    Parameters
    ----------
    image : numpy 2d array
        Input image
    mean: float
        Mean ("centre") of the distribution
    sigma: float
        Standard deviation (spread or "width") of the distribution

    Returns
    -------
    numpy 2d array
        Image with Gaussian noise
    """
    noise = random.normal(mean, sigma, image.shape)
    return clip(round(image + noise), 0, 255)
