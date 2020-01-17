import itertools

if __name__ == '__main__':
    matrix = []
    with open('input.txt') as f:
        for line in f:
            if line:
                matrix.append([mark == '#' for mark in line.strip()])
    for row in matrix:
        print(''.join('#' if aster else '.' for aster in row))
    height = len(matrix)
    width = len(matrix[0])
    asteroids = set((x, y) for y in range(height) for x in range(width) if matrix[y][x])
    print(asteroids)

    detections = {tup: 0 for tup in asteroids}
    for (x, y) in asteroids:
        other_asteroids = asteroids - set(((x, y),))
        axial_visibility_flags = {'vertical': [0, 0], 'horizontal': [0, 0]}

        for idx, axial_iterable in enumerate(range(x), range(x+1, width)):
            for vertical_index in axial_iterable:
                if (vertical_index, y) in other_asteroids:
                    axial_visibility_flags['vertical'][idx] = 1
                    other_asteroids.remove((vertical_index, y))

        for idx, axial_iterable in enumerate(range(y), range(y+1, width)):
            for horizontal_index in axial_iterable:
                if (x, horizontal_index) in other_asteroids:
                    axial_visibility_flags['horizontal'][idx] = 1
                    other_asteroids.remove((x, horizontal_index))

        detections[(x, y)] += sum(sum(flags) for flags in axial_visibility_flags.values())

        while other_asteroids:
            (other_x, other_y) = other_asteroids.pop()
            delta_x = x - other_x
            delta_y = y - other_y



