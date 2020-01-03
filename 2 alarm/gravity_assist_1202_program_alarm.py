from operator import add, mul


class ParseError(Exception):
    pass


def computer(arr, instruction_pointer):
    if instruction_pointer >= len(arr):
        raise ParseError("Program ended without explicit halt")
    
    def binary_operator(operator, param1, param2, param3):
        arr[param3] = operator(arr[param1], arr[param2])
    
    operator_map = {
        1: (binary_operator, 3, add),
        2: (binary_operator, 3, mul),
        99: (None, 0, None)
    }
    
    opcode = arr[instruction_pointer]
    if opcode == 99:
        return
    elif 1 <= opcode <= 2:
        operator_type, arg_count, operator_func = operator_map[opcode]
        if len(arr) <= instruction_pointer + arg_count:
            raise ParseError("Missing required arguments for opcode: {}".format(opcode))
        operator_type(operator_func, *arr[instruction_pointer+1:instruction_pointer+arg_count+1])
        return computer(arr, instruction_pointer + arg_count + 1)
    else:
        raise ParseError("Unknown opcode: {}".format(opcode))


def gravity_assist_func(intcode, noun, verb):
    intcode[1] = noun
    intcode[2] = verb
    
    try:
        computer(intcode, 0)
    except ParseError as e:
        print(e)
    return intcode[0]

if __name__ == '__main__':
    gravity_assist = []
    with open('input.txt') as f:
        gravity_assist = [int(x) for x in f.readline().strip().split(',')]
    # part 1
        print('Part 1: ', gravity_assist_func(gravity_assist[:], 12, 2))
    # part 2
    print('Part 2:')
    for noun in range(100):
        for verb in range(100):
            if gravity_assist_func(gravity_assist[:], noun, verb) == 19690720:
                print(100 * noun + verb)
