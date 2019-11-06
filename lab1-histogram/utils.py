from numpy import (
    dot,
    zeros,
)


def rgb2gray(image):
    if len(image.shape) > 2:
        return dot(
            image[..., :3], [0.2989, 0.5870, 0.1140]
        ).round().astype(int)
    else:
        return image


def calculate_histogram(image):
    histogram = zeros(256)
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            histogram[image[i, j]] += 1
    return histogram


def threshold_binarization(image, threshold):
    binarized_image = image.copy()
    for i in range(binarized_image.shape[0]):
        for j in range(binarized_image.shape[1]):
            binarized_image[i][j] = int(binarized_image[i][j] >= threshold)
    return binarized_image
