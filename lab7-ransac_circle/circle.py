from numpy import (
    random,
    linspace,
    pi,
    cos,
    sin,
    argmax,
)
from pylab import (
    plot,
    grid,
    gca,
    show,
    figure,
)
from matplotlib import animation


def generate_circle():
    t = linspace(0, 2 * pi, 100)  # evently spaced angles
    xc = 3 * random.rand()  # x-coordinate of center of circle
    yc = 3 * random.rand()  # y-coordinate of center of circle
    r = 2 * random.rand() + 0.5  # radius of circle

    x = r * cos(t) + random.normal(scale=1.0/7, size=len(t)) + xc
    y = r * sin(t) + random.normal(scale=1.0/7, size=len(t)) + yc
    return x, y


def get_two_random_points(x, y):
    point_indices = random.randint(low=0, high=len(x), size=2)
    points = [(x[index], y[index]) for index in point_indices]
    return points


def find_h_and_k(random_points):
    h = sum(list(zip(*random_points))[0]) / len(random_points)
    k = sum(list(zip(*random_points))[1]) / len(random_points)
    return h, k


def distance_to_circle(x, y, h, k, r):
    return abs((x - h) ** 2 + (y - k) ** 2 - r ** 2)


def vote_for_circle(circles, x, y, h, k, r, T):
    good_points = 0
    for x_, y_ in zip(x, y):
        d = distance_to_circle(x_, y_, h, k, r)
        if d < T:
            good_points += 1
    circles.append((good_points, h, k, r))
    return circles


def ransac_iteration(x, y, circles):
    points = get_two_random_points(x, y)
    h, k = find_h_and_k(points)
    r = 2 * random.random_sample()
    circles = vote_for_circle(circles, x, y, h, k, r, T)
    return circles


if __name__ == "__main__":
    fig = figure()
    ax = fig.add_subplot(1, 1, 1)
    x, y = generate_circle()
    circles = []
    T = 1
    for _ in range(1000):
        ransac_iteration(x, y, circles)

    best_circle_index = argmax(list(zip(*circles))[0])
    i, h, k, r = circles[best_circle_index]
    print(i)

    t = linspace(0, 2 * pi, 100)
    x_best = r * cos(t) + h
    y_best = r * sin(t) + k
    plot(x_best, y_best, 'r')

    plot(x, y, 'o')
    grid(True)
    gca().set_aspect('equal', adjustable='box')
    show()
