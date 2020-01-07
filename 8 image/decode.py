import re

width = 25
height = 6
layer_size = width * height

if __name__ == '__main__':
    with open('input.txt') as f:
        digits = f.read().strip()
    bounds = range(0, len(digits)+1, layer_size)
    layers = [digits[start:end] for start, end in zip(bounds, bounds[1:])]

    def count_layer_digit(digit, layer_idx):
        return len(re.findall(str(digit), layers[layer_idx]))

    def count_layer_zeroes(layer_idx):
        return count_layer_digit(0, layer_idx)

    least_zeroes_layer = min(range(len(layers)), key=count_layer_zeroes)
    print('part 1: {}'.format(count_layer_digit(1, least_zeroes_layer) * count_layer_digit(2, least_zeroes_layer)))

    image = list(layers[0])
    for layer in layers[1:]:
        for idx, pixel in enumerate(layer):
            if image[idx] == '2':
                image[idx] = pixel
    print('part 2:')
    for row in range(height):
        print(''.join(image[row*width:(row+1)*width]).replace('0', ' ').replace('1', '*'))
