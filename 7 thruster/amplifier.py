from computer import run_sub_routine, run_until_next_input
from itertools import permutations


def amplifier_series(amp, phases):
    signal = 0
    for phase in phases:
        signal = run_sub_routine(amp[:], 0, *(phase, signal))[0]
    return signal


def amplifier_loop(amp, phases):
    coroutines = [run_until_next_input(amp[:], 0) for _ in phases]
    for coro in coroutines:
        next(coro)
    next_input = 0
    loop_count = 0
    while coroutines:
        stopped_in_current_loop = []
        for idx, (coro, phase) in enumerate(zip(coroutines, phases)):
            try:
                coro.send(phase if loop_count == 0 else next_input)
                next_input = coro.send(next_input)
            except StopIteration:
                stopped_in_current_loop.insert(0, idx)
        for idx in stopped_in_current_loop:
            coroutines.pop(idx)
        loop_count += 1
    return next_input


def phase_permutations(phases=range(5)):
    yield from permutations(phases, 5)

if __name__ == '__main__':
    with open('input.txt') as f:
        code = [int(x) for x in f.readline().strip().split(',')]
    print('part 1: {}'.format(max(amplifier_series(code[:], phases) for phases in phase_permutations())))
    print('part 2: {}'.format(max(amplifier_loop(code[:], phases) for phases in phase_permutations(range(5,10)))))
