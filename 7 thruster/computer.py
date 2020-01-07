from operator import add, mul, truth, lt, eq

class ParseError(Exception): pass
class WaitingInputSignal(Exception): pass


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


def run_step(arr, program_counter=0, input_op=read_int, output_op=print_value):
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
        3: (unary_operator, input_op),
        4: (unary_operator, output_op),
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
        return program_counter + arg_count + 1 if option_jump is None else option_jump
    else:
        raise ParseError("Unknown opcode: {}".format(opcode))


def run(arr, program_counter=0, input_op=read_int, output_op=print_value):
    while program_counter is not None:
        program_counter = run_step(arr, program_counter, input_op=input_op, output_op=output_op)


def run_sub_routine(arr, program_counter=0, *args):
    args = list(args)
    output_tuple = []

    def supply_input(*unused):
        del unused
        try:
            val = args.pop(0)
        except IndexError:
            raise TypeError("Missing required input argument.")
        try:
            val = int(val)
        except ValueError:
            raise ValueError("Invalid integer input {}.".format(val))
        return val

    def output_builder(val):
        output_tuple.append(val)
        return val

    run(arr, program_counter, input_op=supply_input, output_op=output_builder)
    return tuple(output_tuple)


def input_output_closure_generator(initial_input=None):
    input_queue = [initial_input]
    output_queue = []

    def enqueue_integer_input(val):
        global input_queue
        try:
            val = int(val)
        except ValueError:
            raise ValueError("Invalid integer input {}.".format(val))
        input_queue = val

    def dequeue_integer_output():
        if not output_queue:
            return None
        return output_queue.pop(0)

    def supply_input(*unused):
        del unused
        if input_queue:
            return input_queue.pop(0)
        else:
            raise WaitingInputSignal('')

    def output_builder(val):
        output_queue.append(val)
        return val

    return supply_input, output_builder, enqueue_integer_input, dequeue_integer_output


def run_until_next_input(arr, program_counter=0, initial_input=None):
    input_op, output_op, set_input, get_output = input_output_closure_generator(initial_input)
    while program_counter is not None:
        try:
            print(program_counter)
            program_counter = run_step(arr, program_counter, input_op=input_op, output_op=output_op)
            output = get_output()
            if output is not None:
                yield output
        except WaitingInputSignal:
            set_input((yield))
            continue
