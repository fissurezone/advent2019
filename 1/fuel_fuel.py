import math


def fuel_required(mass):
    if mass < 9:
        return 0
    fuel_mass = math.floor(mass / 3) - 2
    return fuel_mass + fuel_required(fuel_mass)

if __name__ == '__main__':
    fuel = 0
    with open('input.txt') as f:
        for mass in f:
            mass = mass.strip()
            if mass:
                fuel += fuel_required(int(mass))
    print(fuel)