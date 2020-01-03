from operator import add, mul


def store_input():
    return int(input("Enter an integer: "))


def print_output(val):
    print(val)


class ParseError(Exception):
    pass


def computer(arr, program_counter):
    if program_counter >= len(arr):
        raise ParseError("Program ended without explicit halt")

    def value_by_mode(param, mode):
        if mode == 0:
            return arr[param]  # position mode
        return param  # immediate mode

    def input_operator(operator, param1, mode1):
        arr[param1] = operator()

    def output_operator(operator, param1, mode1):
        value_by_mode(param1, mode1)
        operator(arr[param1])

    def binary_operator(operator, param1, param2, param3, mode1, mode2, mode3):
        val1 = value_by_mode(param1, mode1)
        val2 = value_by_mode(param2, mode2)
        arr[param3] = operator(val1, val2)

    def jump_operator(predicate, param1, mode1):
        #value_by_mode(param1, mode1)
        pass

    operator_map = {
        1: (binary_operator, 3, add),
        2: (binary_operator, 3, mul),
        3: (input_operator, 1, store_input),
        4: (output_operator, 1, print_output)
    }
    
    opcode = arr[program_counter]
    parameter_modes = str(opcode // 100)[::-1]  # in reverse order of parameters
    opcode = opcode % 100

    if opcode == 99:
        return
    elif 1 <= opcode <= 8:
        operator_type, arg_count, operator_func = operator_map[opcode]
        if len(arr) <= program_counter + arg_count:
            raise ParseError("Missing required arguments for opcode: {}".format(opcode))

        modes = {'mode{}'.format(idx+1): 0 for idx in range(arg_count)}
        modes.update({'mode{}'.format(idx+1): int(digit) for idx, digit in enumerate(parameter_modes)})
        next_pointer = operator_type(operator_func, *arr[program_counter + 1:program_counter + arg_count + 1], **modes)
        return computer(arr, next_pointer or program_counter + arg_count + 1)
    else:
        raise ParseError("Unknown opcode: {}".format(opcode))

if __name__ == '__main__':
    diagnostic_test = []
    with open('input.txt') as f:
        diagnostic_test = [int(x) for x in f.readline().strip().split(',')]
        computer(diagnostic_test, 0)
