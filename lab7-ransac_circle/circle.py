from numpy import (
    random,
    linspace,
    pi,
    cos,
    sin,
    argmax,
    linalg,
    array,
    dot,
)
from pylab import (
    plot,
    grid,
    gca,
    show,
    figure,
)


def generate_circle():
    """Generate a set of points that form a circle with gaussian noise

    Returns
    -------
    list of numbers
        x-coordinates of points on noised circle
    list of numbers
        y coordinates of points on noised circle
    """
    t = linspace(0, 2 * pi, 100)  # evently spaced angles
    xc = 3 * random.rand()  # x-coordinate of center of circle
    yc = 3 * random.rand()  # y-coordinate of center of circle
    r = 2 * random.rand() + 0.5  # radius of circle

    x = r * cos(t) + random.normal(scale=1.0/7, size=len(t)) + xc
    y = r * sin(t) + random.normal(scale=1.0/7, size=len(t)) + yc
    return x, y


def get_three_random_points(x, y):
    """Select a random subset of 3 points of the original data
    This subset is called the hypothetical inliers

    Parameters
    ----------
    x: list of numbers
        x-coordinates of points on noised circle
    y: list of numbers
        y coordinates of points on noised circle

    Returns
    -------
    list of tuples (number, number)
        List of 3 random points (x, y) from the original data
    """
    point_indices = random.randint(low=0, high=len(x), size=3)
    points = [(x[index], y[index]) for index in point_indices]
    return points


def estimate_model(random_points):
    """Fit a model to the set of hypothetical inliers
    Find circle center and radius

    Parameters
    ----------
    random_points: list of tuples (number, number)
        List of 3 random points (x, y) from the original data

    Returns
    -------
    number
        x-coordinate of circle center
    number
        y-coordinate of circle center
    number
        circle radius
    """
    A = []
    for point in random_points:
        A.append([point[0] ** 2 + point[1] ** 2, point[0], point[1], 1])
    A = array(A)

    M1 = linalg.det(A[:, array([False, True, True, True])])
    M2 = linalg.det(A[:, array([True, False, True, True])])
    M3 = linalg.det(A[:, array([True, True, False, True])])
    M4 = linalg.det(A[:, array([True, True, True, False])])

    if M1 == 0:
        return 0, 0, 0

    x0 = 0.5 * M2 / M1
    y0 = -0.5 * M3 / M1

    r = (x0 ** 2 + y0 ** 2 + M4 / M1) ** 0.5
    return x0, y0, r


def distance_to_circle(x, y, x0, y0, r):
    """Calculate distance from the point to the circle

    Parameters
    ----------
    x: number
        x-coordinate of the point
    y: number
        y-coordinate of the point
    x0: number
        x-coordinate of the circle center
    y0: number
        y-coordinate of the circle center
    r: number
        circle radius

    Returns
    -------
    number
        Distance from point (x, y) to the circle with
        center in (x0, y0) and radius r
    """
    return abs((x - x0) ** 2 + (y - y0) ** 2 - r ** 2)


def test_data_against_model(best_circle, x, y, x0, y0, r, threshold):
    """Test all data against the fitted model
    Those points that fit the estimated model well,
    according to distance to the circle,
    are considered as part of the consensus set

    Parameters
    ----------
    best_circle: (unsigned int, number, number, number)
        (
            consensus set size,
            x-coordinate of circle center,
            y-coordinate of circle center,
            circle radius
        )
    x: number
        x-coordinate of the point
    y: number
        y-coordinate of the point
    x0: number
        x-coordinate of the circle center
    y0: number
        y-coordinate of the circle center
    r: number
        circle radius
    threshold: number
        Maximum allowable distance from point to circle,
        when the point is considered as an inlier

    Returns
    -------
    (unsigned int, number, number, number)
        best circle tuple
    """
    consensus_set_size = 0
    for x_, y_ in zip(x, y):
        d = distance_to_circle(x_, y_, x0, y0, r)
        if d < threshold:
            consensus_set_size += 1
    if consensus_set_size > best_circle[0]:
        best_circle = (consensus_set_size, x0, y0, r)
    return best_circle


def ransac_iteration(x, y, best_circle, T):
    """Iteration of RANSAC algorithm

    Parameters
    ----------
    x: list of numbers
        x-coordinates of points of noised circle
    y: list of numbers
        y-coordinates of points of noised circle
    best_circle: (unsigned int, number, number, number)
        (
            consensus set size,
            x-coordinate of circle center,
            y-coordinate of circle center,
            circle radius
        )

    Returns
    -------
    (unsigned int, number, number, number)
        best circle tuple
    """
    points = get_three_random_points(x, y)
    x0, y0, r = estimate_model(points)
    if r is not 0:
        best_circle = test_data_against_model(
            best_circle, x, y, x0, y0, r, threshold
        )
    return best_circle


if __name__ == "__main__":
    fig = figure()
    ax = fig.add_subplot(1, 1, 1)

    # geterate points for that form noised circle
    x, y = generate_circle()
    # initialize tuple for best circle: (# of inliers, x0, y0, r)
    best_circle = (0, 0, 0, 0)
    threshold = 0.5
    for _ in range(100):
        best_circle = ransac_iteration(x, y, best_circle, threshold)

    i, x0, y0, r = best_circle
    print("Number of inliers for the best model: {}".format(i))

    # plot the best circle
    t = linspace(0, 2 * pi, 100)
    x_best = r * cos(t) + x0
    y_best = r * sin(t) + y0
    plot(x_best, y_best, 'r')

    # plot the points of noised circle
    for p_x, p_y in zip(x, y):
        if distance_to_circle(p_x, p_y, x0, y0, r) < threshold:
            # plot inliers
            plot(p_x, p_y, "bo")
        else:
            # plot outliers
            plot(p_x, p_y, "co")
    grid(True)
    gca().set_aspect('equal', adjustable='box')
    show()
