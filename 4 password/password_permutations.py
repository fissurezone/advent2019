class DigitsMismatchError(Exception): pass


def digits_list(int_str):
    return [int(digit) for digit in int_str]


def monotonic_ceiling(digits):
    if len(digits) < 2:
        return digits
    if digits[0] > digits[1]:
        return [digits[0] - 1] + [9] * (len(digits) - 1)
    return digits[:1] + monotonic_ceiling(digits[1:])


def monotonic_floor(digits):
    if len(digits) < 2:
        return digits
    if digits[0] > digits[1]:
        return [digits[0]] * len(digits)
    return digits[:1] + monotonic_floor(digits[1:])


def count_permutations_dynamic(start_list, end_list, paired=False, trail=[]):
    cardinality = len(start_list)
    if cardinality == 0:
        print (trail, 1)
        yield ''.join([str(x) for x in trail])
        return

    msd_start = start_list[0]
    msd_end = end_list[0]
    if cardinality == 1:
        if paired:
            print (trail, msd_start, msd_end, msd_end-msd_start+1)
            for num in range(msd_start, msd_end+1):
                yield ''.join([str(x) for x in trail+[num]])
                return

    print(trail, start_list, end_list)
    if paired:
        if msd_start == msd_end:
            yield from count_permutations_dynamic(start_list[1:], end_list[1:], True, trail+[msd_start])
        else:
            yield from count_permutations_dynamic(start_list[1:], [9]*(cardinality-1), True, trail+[msd_start])
            for msd in range(msd_start+1, msd_end):
                yield from count_permutations_dynamic([msd]*(cardinality-1), [msd]+[9]*(cardinality-2), True,
                                                      trail+[msd])
            yield from count_permutations_dynamic([msd_end]*(cardinality-1), end_list[1:], True, trail+[msd_end])
    elif cardinality >= 2:
        if msd_start == start_list[1]:
            yield from count_permutations_dynamic(start_list[2:], [9]*(cardinality-2), True, trail+[msd_start]*2)
        for msd in range(msd_start+1, msd_end):
            yield from count_permutations_dynamic([msd]*(cardinality-2), [msd]+[9]*(cardinality-3), True, trail+[msd]*2)
        if msd_end > msd_start:
            yield from count_permutations_dynamic([msd_end]*(cardinality-2), end_list[2:], True, trail+[msd_end]*2)

        if msd_start < 9:
            yield from count_permutations_dynamic([max(msd_start+1, start_list[1])]*(cardinality-1),
                                                  [9]*(cardinality-1), False, trail+[msd_start])
        for msd in range(msd_start+1, msd_end):
            yield from count_permutations_dynamic([msd+1]*(cardinality-1), [9]*(cardinality-1), False, trail+[msd])
        if msd_start < msd_end < end_list[1]:
            yield from count_permutations_dynamic([min(msd_end+1, end_list[1])]*(cardinality-1), [9]*(cardinality-1),
                                                  False, trail+[msd_end])
    return


def ordinal(digits):
    return sum(digit * 10 ** (6-idx-1) for idx, digit in enumerate(digits))


def has_adjacent_repeated_digits(digits):
    for left, right in zip(digits, digits[1:]):
        if left == right:
            return True
    return False


def increment(digits):
    idx = 5
    overflow = 1
    while idx >= 0 and overflow > 0:
        digits[idx] += overflow
        overflow = digits[idx] // 10
        digits[idx] = digits[idx] % 10
        idx -= 1
    idx = 5
    while idx >= 0 and digits[idx] == 0:
        idx -= 1
    return digits[:idx+1] + [digits[idx]] * (5 - idx)


def permutations(start_digits, end_digits):
    while ordinal(start_digits) <= ordinal(end_digits):
        if has_adjacent_repeated_digits(start_digits):
            yield start_digits
        start_digits = increment(start_digits)


def permutations_with_exactly_pair(start_digits, end_digits):
    for digits in permutations(start_digits, end_digits):
        if has_exactly_pair_adjacent_repeated(digits):
            yield digits


def has_exactly_pair_adjacent_repeated(digits):
    match_length = 0
    for left, right in zip(digits, digits[1:]):
        if left == right:
            match_length += 1
        elif match_length == 1:
            return True
        else:
            match_length = 0
    if match_length == 1:
        return True
    return False


if __name__ == '__main__':
    range_string = '264793-803935'
    start, end = range_string.split('-', 2)
    if len(start) != len(end):
        raise DigitsMismatchError('Lengths of start and end do not match.')

    start = monotonic_floor(digits_list(start))
    end = monotonic_ceiling(digits_list(end))
    nums = permutations(start, end)
    print('Part 1: ', sum(1 for n in nums))

    nums = permutations_with_exactly_pair(start, end)
    print('Part 2: ', sum(1 for n in nums))
