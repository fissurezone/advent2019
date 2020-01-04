from computer import run

if __name__ == '__main__':
    with open('input.txt') as f:
        diagnostic_test = [int(x) for x in f.readline().strip().split(',')]
        run(diagnostic_test, 0)
