from numpy import (
    zeros,
    argmax,
)


def get_intensity_probabilities(histogram):
    probabilities = zeros(256)
    for intensity in range(256):
        probabilities[intensity] = histogram[intensity] / sum(histogram)
    return probabilities


def get_total_group_probabilities(intensity_probabilities):
    total_probabilities = zeros(256)
    total_probabilities[0] = intensity_probabilities[0]
    for threshold in range(1, 256):
        total_probabilities[threshold] = \
            total_probabilities[threshold - 1] + \
            intensity_probabilities[threshold]
    return total_probabilities


def get_mean_group_values(intensity_probabilities, total_group_probabilities):
    mu1 = zeros(256)
    mu2 = zeros(256)
    for threshold in range(256):
        for intensity in range(threshold + 1):
            mu1[threshold] += \
                intensity * intensity_probabilities[intensity] / \
                total_group_probabilities[threshold]
        for intensity in range(threshold + 1, 256):
            mu2[threshold] += \
                intensity * intensity_probabilities[intensity] / \
                (1 - total_group_probabilities[threshold])
    return mu1, mu2


def get_intergroup_dispersions(total_group_probabilities, mu1, mu2):
    intergroup_dispersions = zeros(256)
    for threshold in range(256):
        intergroup_dispersions[threshold] = \
            total_group_probabilities[threshold] * \
            (1 - total_group_probabilities[threshold]) * \
            (mu1[threshold] - mu2[threshold]) ** 2
    return intergroup_dispersions


def get_optimal_threshold(histogram):
    intensity_probabilities = get_intensity_probabilities(histogram)
    total_group_probabilities = get_total_group_probabilities(
        intensity_probabilities)
    mu1, mu2 = get_mean_group_values(intensity_probabilities,
                                     total_group_probabilities)
    intergroup_dispersions = get_intergroup_dispersions(
        total_group_probabilities, mu1, mu2)
    return argmax(intergroup_dispersions)
