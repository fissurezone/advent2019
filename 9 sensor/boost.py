from computer import run

if __name__ == '__main__':
    with open('input.txt') as f:
        code = [int(x) for x in f.readline().strip().split(',')]
    run(code)
