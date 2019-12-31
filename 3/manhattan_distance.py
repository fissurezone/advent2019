def line_segments(path, start_x=0, start_y=0):
    horizontals = []  # [((left, right), Y), ...]
    verticals = []  # [(X, (bottom, top)), ...]
    x = start_x
    y = start_y

    for line_segment in path.split(','):
        direction = line_segment[0]
        magnitude = int(line_segment[1:])

        if direction == 'D' or direction == 'L':
            magnitude = -magnitude
        
        if direction == 'D' or direction == 'U':
            end = y + magnitude
            verticals.append({'x': x, 'left': min(y, end), 'right': max(y, end)})
            y = end
        elif direction == 'L' or direction == 'R':
            end = x + magnitude
            horizontals.append({'bottom': min(x, end), 'top': max(x, end), 'y': y})
            x = end

    return {'horizontals': horizontals, 'verticals': verticals}


def orthogonal_intersections(horizontals, verticals):
    """ yield (x,y) co-ordinates where any vertical line intersects any horizontal line
    """
    for level in horizontals:
        for normal in verticals:
            if level['bottom'] <= normal['x'] <= level['top'] and normal['left'] <= level['y'] <= normal['right']:
                yield normal['x'], level['y']


def path_intersections(path1, path2):
    lines = []
    for path in (path1, path2):
        lines.append(line_segments(path))
    for idx in (0, 1):
        yield from orthogonal_intersections(lines[idx]['horizontals'], lines[1-idx]['verticals'])


def manhattan_distance(x, y):
    # https://en.wikipedia.org/wiki/Taxicab_geometry
    return abs(x) + abs(y)


def intersection_distances(path1, path2):
    for x, y in path_intersections(path1, path2):
        yield manhattan_distance(x, y)

if __name__ == '__main__':
    with open('input.txt') as f:
        paths = [x.strip() for x in f.readlines()]
        print(min(intersection_distances(*paths)))
