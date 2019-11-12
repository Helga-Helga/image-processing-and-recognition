from numpy import array

from integral_image import (
    window_sum,
    compute_integral_image,
)


def test_window_sum():
    image = array([[4, 25, 235, 74, 245, 34],
                   [45, 54, 43, 2, 4, 64],
                   [32, 23, 243, 2, 4, 23],
                   [13, 124, 251, 143, 23, 53]])
    integral_image = compute_integral_image(image)
    assert window_sum(integral_image, [0, 0, 2, 2]) == 128
    assert window_sum(integral_image, [2, 2, 3, 2]) == 666
    assert window_sum(integral_image, [0, 0, 0, 0]) == 0
