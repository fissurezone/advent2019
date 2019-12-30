def get_line_segments(path, srart_x=0, start_y=0):
    horizontals = []  # [((left, right), Y), ...]
    verticals = []  # [(X, (bottom, top)), ...]
    x = start_x, y = start_y
    for line_segment in path.split(','):
        direction = line_segment[0]
        magnitude = int(line_segment[1:])
        if direction == 'D' or direction == 'L':
            magnitude = -magnitude
        
        if direction == 'D' or direction == 'U':
            start = y
            end = y + magnitude
            verticals.push((x, (min(start, end), max(start, end))))
            y = end
        elif direction == 'L' or direction == 'R':
            start = x
            end = x + magnitude
            horizontals.push(((min(start, end), max(start, end)), y))
            x = end
        return horizontals, verticals

def get_intersections(horizontals, verticals):
    # horizontals: [((left, right), Y), ...]
    # verticals: [(X, (bottom, top)), ...]
    horizontals = horizontals.sort(key=lambda x: x[0][1])
    verticals = verticals.sort(key=lambda x: x[0])
    
    points = []  # [(x, y), ...]

def get_path_intersections(path1, path2):
    lines = {0: {'horizontals': [], 'verticals': []},
             1: {'horizontals': [], 'verticals': []}}
    #

def manhattan_distance(x, y):
    # https://en.wikipedia.org/wiki/Taxicab_geometry
    return abs(x) + abs(y)

if __name__ == '__main__':
    with open('input.txt') as f:
        paths = [x.strip() for x in f.readlines()]