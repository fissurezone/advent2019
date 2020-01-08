import math


def load_fuel(mass):
    return math.floor(mass / 3) - 2


def total_fuel(mass):
    if mass < 9:
        return 0
    fuel_mass = math.floor(mass / 3) - 2
    return fuel_mass + total_fuel(fuel_mass)

if __name__ == '__main__':
    def get_loads():
        with open('input.txt') as f:
            for mass in f:
                mass = mass.strip()
                if mass:
                    yield int(mass)

    print('part 1: {}'.format(sum(load_fuel(load) for load in get_loads())))
    print('part 2: {}'.format(sum(total_fuel(load) for load in get_loads())))
