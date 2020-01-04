from operator import add, mul, truth, lt, eq


def read_int(*unused):
    del unused  # match function type signature
    while True:
        try:
            return int(input("Enter an integer: "))
        except ValueError:
            print("Invalid base 10 integer.")
            pass


def print_value(val):
    print(val)
    return val


def true_option(val1, val2):
    return val2 if val1 else None


def false_option(val1, val2):
    return None if val1 else val2


class ParseError(Exception):
    pass


def run(arr, program_counter=0):
    if program_counter >= len(arr):
        raise ParseError("Program ended without explicit halt")

    def get_value_by_mode(param, mode):
        if mode == 0:
            return arr[param]  # position mode
        return param  # immediate mode

    def set_int_code(idx, val):
        arr[idx] = int(val)

    def unary_operator(operator, param1, mode1) -> None:
        val = get_value_by_mode(param1, mode1)
        res = operator(val)
        if mode1 == 0:  # set the result in position mode (immediate mode leaves nowhere to store the result)
            set_int_code(param1, res)
        return None
    unary_operator.arg_count = 1

    def binary_jump_operator(operator, param1, param2, mode1, mode2) -> int:
        val1 = get_value_by_mode(param1, mode1)
        val2 = get_value_by_mode(param2, mode2)
        return operator(val1, val2)
    binary_jump_operator.arg_count = 2

    def binary_store_operator(operator, param1, param2, param3, mode1, mode2, mode3) -> None:
        res = binary_jump_operator(operator, param1, param2, mode1, mode2)
        if mode3 == 0:
            set_int_code(param3, res)
        return None
    binary_store_operator.arg_count = 3

    operator_map = {
        1: (binary_store_operator, add),
        2: (binary_store_operator, mul),
        3: (unary_operator, read_int),
        4: (unary_operator, print_value),
        5: (binary_jump_operator, true_option),
        6: (binary_jump_operator, false_option),
        7: (binary_store_operator, lt),
        8: (binary_store_operator, eq)
    }

    opcode = arr[program_counter]
    parameter_modes = str(opcode // 100)[::-1]  # in reverse order of parameters
    opcode = opcode % 100

    if opcode == 99:
        return
    elif opcode in operator_map:
        operator_type, operator_func = operator_map[opcode]
        arg_count = operator_type.arg_count

        if len(arr) <= program_counter + arg_count:
            raise ParseError("Missing required arguments for opcode: {}".format(opcode))

        modes = {'mode{}'.format(idx+1): 0 for idx in range(arg_count)}
        modes.update({'mode{}'.format(idx+1): int(digit) for idx, digit in enumerate(parameter_modes)})
        option_jump = operator_type(operator_func, *arr[program_counter + 1:program_counter + arg_count + 1], **modes)
        run(arr, program_counter + arg_count + 1 if option_jump is None else option_jump)
    else:
        raise ParseError("Unknown opcode: {}".format(opcode))
