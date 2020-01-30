from functools import reduce
from operator import mul
from heapq import heappush, nsmallest
from math import pi, atan2

RAD_2_PI = 2 * pi
primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71]


def prod(iterable):
    return reduce(mul, iterable, 1)


def prime_factorial(n):
    n = abs(n)
    if n == 1:
        yield 1
    else:
        for i in primes:
            if i * i > n:
                break
            while n % i == 0:
                n //= i
                yield i
            if n == 1:
                break
        if n > 1:
            yield n


def scale_and_slope_fraction(dx, dy):
    sign_x = 1 if dx > 0 else -1
    sign_y = 1 if dy > 0 else -1
    if dx == 0:
        return abs(dy), 0, sign_y
    if dy == 0:
        return abs(dx), sign_x, 0

    dx = list(prime_factorial(dx))
    dy = list(prime_factorial(dy))
    scale = []
    for factor in dx[:]:
        if factor in dy:
            dx.remove(factor)
            dy.remove(factor)
            scale.append(factor)
    return prod(scale), sign_x * prod(dx), sign_y * prod(dy)


def slope_fraction(dx, dy):
    _, unit_dx, unit_dy = scale_and_slope_fraction(dx, dy)
    return unit_dx, unit_dy


def angle_to_y_axis(dx, dy):
    return (RAD_2_PI + atan2(dx, dy)) % RAD_2_PI


if __name__ == '__main__':
    matrix = []
    with open('input.txt') as f:
        for line in f:
            if line:
                matrix.append([mark == '#' for mark in line.strip()])

    height = len(matrix)
    width = len(matrix[0])
    max_dim = max(height, width)
    asteroids = set((x, y) for y in range(height) for x in range(width) if matrix[height-y-1][x])
    detections = {tup: 0 for tup in asteroids}
    for (x, y) in asteroids:
        other_asteroids = asteroids - set(((x, y),))
        slopes = set(slope_fraction(ox - x, oy - y) for (ox, oy) in other_asteroids)
        detections[(x, y)] = len(slopes)

    max_visibility_location = max(detections, key=detections.get)
    print('Part 1 : {}'.format(detections[max_visibility_location]))

    asteroids.remove(max_visibility_location)
    y_axis_angle_wise_asteroids = {}
    for x, y in asteroids:
        delta_x = x - max_visibility_location[0]
        delta_y = y - max_visibility_location[1]
        scale, slope_x, slope_y = scale_and_slope_fraction(delta_x, delta_y)
        angle = angle_to_y_axis(slope_x, slope_y)
        if angle in y_axis_angle_wise_asteroids:
            heappush(y_axis_angle_wise_asteroids[angle], (scale, x, y))
        else:
            y_axis_angle_wise_asteroids[angle] = [(scale, x, y)]

    for y, row in enumerate(matrix):
        print(''.join('X' if x == max_visibility_location[0] and y == max_visibility_location[1] else
                      '#' if aster else '.' for x, aster in enumerate(row)))
    scan_wise_asteroids = []
    for angle in sorted(y_axis_angle_wise_asteroids.keys()):
        for idx, (_, x, y) in enumerate(nsmallest(max_dim, y_axis_angle_wise_asteroids[angle])):
            heappush(scan_wise_asteroids, (idx, angle, (x, y)))

    x_200, inv_y_200 = nsmallest(200, scan_wise_asteroids)[-1][2]
    y_200 = height - inv_y_200 - 1
    print('Part 2 : {}'.format((x_200 * 100) + y_200))
