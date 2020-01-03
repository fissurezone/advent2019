def line_segments(path, start_x=0, start_y=0):
    horizontals = []  # [{left, right, Y}, ...]
    verticals = []  # [{X, top, bottom}, ...]
    x = start_x
    y = start_y
    cumulative = 0

    for idx, line_segment in enumerate(path.split(',')):
        direction = line_segment[0]
        segment = {'idx': idx, 'trailing': cumulative, 'direction': direction}

        magnitude = int(line_segment[1:])
        if direction == 'D' or direction == 'L':
            magnitude = -magnitude

        if direction == 'D' or direction == 'U':
            end = y + magnitude
            segment.update({'bottom': min(y, end), 'top': max(y, end), 'x': x})
            verticals.append(segment)
            y = end
        elif direction == 'L' or direction == 'R':
            end = x + magnitude
            segment.update({'left': min(x, end), 'right': max(x, end), 'y': y})
            horizontals.append(segment)
            x = end
        cumulative += abs(magnitude)

    return {'horizontals': horizontals, 'verticals': verticals}


def orthogonal_intersections(horizontals, verticals):
    """ yield (x,y) co-ordinates where any vertical line intersects any horizontal line
    """
    for level in horizontals:
        for normal in verticals:
            if normal['bottom'] <= level['y'] <= normal['top'] and level['left'] <= normal['x'] <= level['right']:
                if level['idx'] == normal['idx'] == 0:
                    continue
                yield level, normal


def path_intersections(path1, path2):
    yield from orthogonal_intersections(path1['horizontals'], path2['verticals'])
    yield from orthogonal_intersections(path2['horizontals'], path1['verticals'])


def manhattan_distance(level, normal):
    # https://en.wikipedia.org/wiki/Taxicab_geometry
    return abs(normal['x']) + abs(level['y'])


def signal_distance(level, normal):
    level_dist = (level['right'] - normal['x'] if level['direction'] == 'L' else normal['x'] - level['left'])
    normal_dist = (normal['top'] - level['y'] if normal['direction'] == 'D' else level['y'] - normal['bottom'])
    return level['trailing'] + normal['trailing'] + level_dist + normal_dist


def intersection_distance(distance_func, path1, path2):
    for level, normal in path_intersections(path1, path2):
        yield distance_func(level, normal)

if __name__ == '__main__':
    with open('input.txt') as f:
        paths = [line_segments(x.strip()) for x in f.readlines()]
        print('part 1: ', min(intersection_distance(manhattan_distance, *paths)))
        print('part 2: ', min(intersection_distance(signal_distance, *paths)))
