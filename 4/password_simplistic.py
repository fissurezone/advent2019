
def has_monotonic_digits(digits):
    for left, right in zip(digits, digits[1:]):
        if left > right:
            return False
    return True


def has_adjacent_repeated_digits(digits):
    for left, right in zip(digits, digits[1:]):
        if left == right:
            return True
    return False


def permutations(lower, upper):
    for num in range(lower, upper+1):
        digits = [int(digit) for digit in str(num)]
        if has_monotonic_digits(digits) and has_adjacent_repeated_digits(digits):
            yield num


if __name__ == '__main__':
    range_string = '264793-803935'
    start, end = (int(s) for s in range_string.split('-', 2))
    passwords = list(permutations(start, end))
    print(len(passwords))
