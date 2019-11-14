from numpy import concatenate, zeros


def get_filter_indexes(height, width):
    """Calculate indexes that are needed to add
    to image pixel coordinates around center pixel of the filter

    Parameters
    ----------
    height : int
        Filter height
    width: int
        Filter width

    Returns
    -------
    numpy 2d array
        Indexes in filter as signed distances from the center of filter
    """
    indexes = zeros((height, width, 2))
    for i in range(height):
        for j in range(width):
            indexes[i][j] = (i - height // 2, j - width // 2)
    return indexes


def dilation(image, structural_element):
    """Binary image dilation

    Parameters
    ----------
    image : numpy 2d array
        Input binary image
    structural_element: numpy 2d array
        Binary filter with odd side sizes

    Returns
    -------
    numpy 2d array
        Dilated image by structural element
    """
    height, width = structural_element.shape

    # get center pixel intensity of structural element
    center_pixel = structural_element[height // 2, width // 2]

    indexes = get_filter_indexes(height, width)

    # add white borders
    dilated_image = concatenate(
        ([[1] * image.shape[1]] * (width // 2), image), axis=0)
    dilated_image = concatenate(
        (dilated_image, [[1] * image.shape[1]] * (width // 2)), axis=0)
    dilated_image = concatenate(
        ([[1] * (height // 2)] * dilated_image.shape[0], dilated_image),
        axis=1)
    dilated_image = concatenate(
        (dilated_image, [[1] * (height // 2)] * dilated_image.shape[0]),
        axis=1)

    # go through image pixels
    for i in range(height // 2, image.shape[0] - height + 1):
        for j in range(width // 2, image.shape[1] - width + 1):
            if image[i, j] == center_pixel:
                # go through filter pixels
                for s_i in range(height):
                    for s_j in range(width):
                        if structural_element[s_i, s_j] == center_pixel:
                            # get corresponding image pixel coordinate
                            im_i = i + int(indexes[s_i, s_j, 0])
                            im_j = j + int(indexes[s_i, s_j, 1])

                            dilated_image[im_i, im_j] = center_pixel
    return dilated_image
