from computer import run_sub_routine

if __name__ == '__main__':
    with open('input.txt') as f:
        code = [int(x) for x in f.readline().strip().split(',')]
    print('Part 1: {}'.format(run_sub_routine(code, 1)[0]))
    print('Part 1: {}'.format(run_sub_routine(code, 2)[0]))
