from numpy import (
    concatenate,
    zeros,
    delete,
)


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


def expand_image(image, height, width):
    """Add white borders around the image

    Parameters
    ----------
    image : numpy 2d array
        Input binary image
    height: int
        Number of rows to add at the beginning and at the end
    width: int
        Number of columns to add at the beginning and at the end

    Returns
    -------
    numpy 2d array
        Expanded image with white border
    """
    expanded_image = concatenate(
        ([[1] * image.shape[1]] * width, image), axis=0)
    expanded_image = concatenate(
        (expanded_image, [[1] * image.shape[1]] * width), axis=0)
    expanded_image = concatenate(
        ([[1] * height] * expanded_image.shape[0], expanded_image),
        axis=1)
    expanded_image = concatenate(
        (expanded_image, [[1] * height] * expanded_image.shape[0]),
        axis=1)
    return expanded_image


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
    dilated_image = expand_image(image, height // 2, width // 2)

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


def erosion(image, structural_element):
    """Binary image erosion

    Parameters
    ----------
    image : numpy 2d array
        Input binary image
    structural_element: numpy 2d array
        Binary filter with odd side sizes

    Returns
    -------
    numpy 2d array
        Erosed image by structural element
    """
    height, width = structural_element.shape

    # get center pixel intensity of structural element
    center_pixel = structural_element[height // 2, width // 2]

    indexes = get_filter_indexes(height, width)

    # add white borders
    erosed_image = expand_image(image, height // 2, width // 2)

    # go through image pixels
    for i in range(height // 2, image.shape[0] - height + 1):
        for j in range(width // 2, image.shape[1] - width + 1):
            number_of_errors = 0
            # go through filter pixels
            for s_i in range(height):
                for s_j in range(width):
                    # get corresponding image pixel coordinate
                    im_i = i + int(indexes[s_i, s_j, 0])
                    im_j = j + int(indexes[s_i, s_j, 1])
                    if image[im_i, im_j] != structural_element[s_i, s_j]:
                        number_of_errors += 1
            if number_of_errors > 0:
                erosed_image[i, j] = 1 - center_pixel
    return erosed_image


def closing(image, structural_element):
    """Binary image closing

    Parameters
    ----------
    image : numpy 2d array
        Input binary image
    structural_element: numpy 2d array
        Binary filter with odd side sizes

    Returns
    -------
    numpy 2d array
        Closed image by structural element as dilation and then erosion
    """
    return erosion((dilation(image, structural_element)), structural_element)


def opening(image, structural_element):
    """Binary image opening

    Parameters
    ----------
    image : numpy 2d array
        Input binary image
    structural_element: numpy 2d array
        Binary filter with odd side sizes

    Returns
    -------
    numpy 2d array
        Opened image by structural element as erosion and then dilation
    """
    return dilation((erosion(image, structural_element)), structural_element)

def get_edges(image, structural_element):
    """Get edges of image

    Parameters
    ----------
    image: numpy 2d array
        Input binary image
    structural_element: numpy 2d array
        Binary filter with odd side sizes

    Returns
    -------
    numpy 2d array
        Image that contains edges after
        substraction of erosed image from initial image
    """
    erosed_image = erosion(image, structural_element)
    height, width = structural_element.shape
    for i in range(height // 2):
        erosed_image = delete(erosed_image, 0, axis=0)
        erosed_image = delete(erosed_image, -1, axis=0)
    for j in range(width // 2):
        erosed_image = delete(erosed_image, 0, axis=1)
        erosed_image = delete(erosed_image, -1, axis=1)
    return image - erosed_image
