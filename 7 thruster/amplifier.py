from computer import run_sub_routine
from itertools import permutations


def amplifier_series(amp, phases):
    signal = 0
    for phase in phases:
        print(phases, signal)
        signal = run_sub_routine(amp[:], 0, *(phase, signal))[0]
        print(signal)
    return signal


def phase_permutations(phases=range(5)):
    yield from permutations(phases, 5)

if __name__ == '__main__':
    with open('input.txt') as f:
        code = [int(x) for x in f.readline().strip().split(',')]
    print('part 1: {}'.format(max(amplifier_series(code[:], phases) for phases in phase_permutations())))
