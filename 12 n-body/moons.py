from itertools import combinations
from functools import reduce


def gravity_time_step(bodies, dimensions=('x', 'y', 'z')):
    # update velocities
    for body_a, body_b in combinations(bodies, 2):
        for dim in dimensions:
            if body_a[dim] < body_b[dim]:
                body_a['v'+dim] += 1
                body_b['v'+dim] -= 1
            elif body_a[dim] > body_b[dim]:
                body_a['v'+dim] -= 1
                body_b['v'+dim] += 1
    # update positions
    for body in bodies:
        for dim in dimensions:
            body[dim] += body['v'+dim]


def total_energy(bodies):
    total = 0
    for body in bodies:
        potential_energy = sum(abs(body[dim]) for dim in ('x', 'y', 'z'))
        kinetic_energy = sum(abs(body[dim]) for dim in ('vx', 'vy', 'vz'))
        total += potential_energy * kinetic_energy
    return total


def dimension_wise_hash_generator(dimensions=('x', 'y', 'z')):
    position_dimensions = [dim for dim in ('x', 'y', 'z') if dim in dimensions]
    velocity_dimensions = ['v'+dim for dim in ('x', 'y', 'z') if dim in dimensions]
    dimensions = position_dimensions + velocity_dimensions

    def hash_function(bodies):
        return tuple(body[dim] for body in bodies for dim in dimensions)
    return hash_function


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def lcm(a, b):
    return a * b // gcd(a, b)


def lcm_multi(*args):
    return reduce(lcm, args)


if __name__ == '__main__':
    with open('input.txt') as f:
        lines = [line.strip() for line in f]

    moons = []
    for line in lines:
        dims = [expr.split('=') for expr in line.strip('<>').split(', ')]
        moon = {dim: int(val) for dim, val in dims}
        moon.update({'vx': 0, 'vy': 0, 'vz': 0})
        moons.append(moon)

    for idx in range(1000):
        gravity_time_step(moons)
    print('Part 1 : {}'.format(total_energy(moons)))

    periods = {}
    for dim in ('x', 'y', 'z'):
        dimension_hash = dimension_wise_hash_generator((dim,))
        dimension_moons = [{dim: moon[dim], 'v'+dim: moon['v'+dim]} for moon in moons]
        dimension_set = set(dimension_hash(dimension_moons))
        steps = 0
        while True:
            gravity_time_step(dimension_moons, (dim,))
            steps += 1
            step_hash = dimension_hash(dimension_moons)
            if step_hash in dimension_set:
                break
            else:
                dimension_set.add(step_hash)
        periods[dim] = steps - 1

    print('Part 2 : {}'.format(lcm_multi(*periods.values())))
