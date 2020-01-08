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
    t = linspace(0, 2 * pi, 100)  # evently spaced angles
    xc = 3 * random.rand()  # x-coordinate of center of circle
    yc = 3 * random.rand()  # y-coordinate of center of circle
    r = 2 * random.rand() + 0.5  # radius of circle

    x = r * cos(t) + random.normal(scale=1.0/7, size=len(t)) + xc
    y = r * sin(t) + random.normal(scale=1.0/7, size=len(t)) + yc
    return x, y


def get_three_random_points(x, y):
    point_indices = random.randint(low=0, high=len(x), size=3)
    points = [(x[index], y[index]) for index in point_indices]
    return points


def estimate_model(random_points):
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
    return abs((x - x0) ** 2 + (y - y0) ** 2 - r ** 2)


def vote_for_circle(circles, x, y, x0, y0, r, T):
    good_points = 0
    for x_, y_ in zip(x, y):
        d = distance_to_circle(x_, y_, x0, y0, r)
        if d < T:
            good_points += 1
    circles.append((good_points, x0, y0, r))
    return circles


def ransac_iteration(x, y, circles):
    points = get_three_random_points(x, y)
    x0, y0, r = estimate_model(points)
    if r is not 0:
        circles = vote_for_circle(circles, x, y, x0, y0, r, T)
    return circles


if __name__ == "__main__":
    fig = figure()
    ax = fig.add_subplot(1, 1, 1)
    x, y = generate_circle()
    circles = []
    T = 0.5
    for _ in range(1000):
        ransac_iteration(x, y, circles)

    best_circle_index = argmax(list(zip(*circles))[0])
    i, x0, y0, r = circles[best_circle_index]
    print(i)

    t = linspace(0, 2 * pi, 100)
    x_best = r * cos(t) + x0
    y_best = r * sin(t) + y0
    plot(x_best, y_best, 'r')

    for p_x, p_y in zip(x, y):
        if distance_to_circle(p_x, p_y, x0, y0, r) < T:
            plot(p_x, p_y, "bo")
        else:
            plot(p_x, p_y, "co")
    grid(True)
    gca().set_aspect('equal', adjustable='box')
    show()
