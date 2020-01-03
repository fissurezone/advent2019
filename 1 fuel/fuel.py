import math


def fuel_required(mass):
    return math.floor(mass / 3) - 2

if __name__ == '__main__':
    fuel = 0
    with open('input.txt') as f:
        for mass in f:
            mass = mass.strip()
            if mass:
                fuel += fuel_required(int(mass))
    print(fuel)