from functools import reduce
from operator import mul

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


def unit_slope(dx, dy):
    sign_x = 1 if dx > 0 else -1
    sign_y = 1 if dy > 0 else -1
    if dx == 0:
        return 0, sign_y
    if dy == 0:
        return sign_x, 0
    dx = list(prime_factorial(dx))
    dy = list(prime_factorial(dy))
    for i in dx[:]:
        if i in dy:
            dx.remove(i)
            dy.remove(i)
    return sign_x * prod(dx), sign_y * prod(dy)


if __name__ == '__main__':
    matrix = []
    with open('input.txt') as f:
        for line in f:
            if line:
                matrix.append([mark == '#' for mark in line.strip()])
    for row in matrix:
        print(''.join('#' if aster else '.' for aster in row))
    height = len(matrix)
    width = len(matrix[0])
    asteroids = set((x, y) for y in range(height) for x in range(width) if matrix[y][x])

    detections = {tup: 0 for tup in asteroids}
    for (x, y) in asteroids:
        other_asteroids = asteroids - set(((x, y),))
        slopes = set(unit_slope(ox - x, oy - y) for (ox, oy) in other_asteroids)
        detections[(x, y)] = len(slopes)

    max_visibility_location = max(detections, key=detections.get)
    print('Part 1 : {}'.format(detections[max_visibility_location]))
