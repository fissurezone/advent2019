from computer import run_sub_routine, run_until_next_input
from itertools import permutations


def amplifier_series(amp, phases):
    signal = 0
    for phase in phases:
        signal = run_sub_routine(amp[:], 0, *(phase, signal))[0]
    return signal


def amplifier_loop(amp, phases):
    amplifier_coroutines = [run_until_next_input(amp[:], 0) for _ in phases]
    for amp, phase in zip(amplifier_coroutines, phases):
        next(amp)
        amp.send(phase)

    signal = 0
    first_loop = True
    while amplifier_coroutines:
        stopped_amps = []
        for idx, amp in enumerate(amplifier_coroutines):
            try:
                # each amplifier expects 2 inputs and generates one output for next amp in loop
                if not first_loop:  # phase (already sent) counts as input 1 of first loop
                    amp.send(signal)
                signal = amp.send(signal)
            except StopIteration:
                stopped_amps.append(idx)

        first_loop = False
        for amp_idx in reversed(stopped_amps):
            amplifier_coroutines.pop(amp_idx)
    return signal


def phase_permutations(phases=range(5)):
    yield from permutations(phases, 5)


if __name__ == '__main__':
    with open('input.txt') as f:
        code = [int(x) for x in f.readline().strip().split(',')]
    print('part 1: {}'.format(max(amplifier_series(code[:], phases) for phases in phase_permutations())))
    print('part 2: {}'.format(max(amplifier_loop(code[:], phases) for phases in phase_permutations(range(5,10)))))
