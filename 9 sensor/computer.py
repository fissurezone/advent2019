from operator import add, mul, truth, lt, eq
from enum import Enum


class ParseError(Exception): pass


class WaitingInputSignal(Exception): pass


def read_int(*unused):
    del unused
    while True:
        try:
            return int(input("Enter an integer: "))
        except ValueError:
            print("Invalid base 10 integer.")
            pass


def print_value(val):
    print(val)


def true_option(val1, val2):
    return val2 if val1 != 0 else None


def false_option(val1, val2):
    return val2 if val1 == 0 else None


class ProcessState(object):
    def __init__(self, program_counter=0, relative_base=0):
        self.program_counter = program_counter
        self.relative_base = relative_base

    def __repr__(self):
        return '{}, {}'.format(self.program_counter, self.relative_base)


class ParameterMode(Enum):
    POSITION = 0
    IMMEDIATE = 1
    RELATIVE = 2


class OpCode(Enum):
    ADD = 1
    MULTIPLY = 2
    INPUT = 3
    OUTPUT = 4
    JUMP_IF_TRUE = 5
    JUMP_IF_FALSE = 6
    LESSER_THAN = 7
    GREATER_THAN = 8
    RELATIVE_BASE_OFFSET = 9
    HALT = 99


def _run_instruction(memory, process_state, input_op=read_int, output_op=print_value):
    def extend_memory_space(idx):
        if idx >= len(memory):
            memory.extend([0] * (idx + 1 - len(memory)))

    def read_memory(idx):
        extend_memory_space(idx)
        return memory[idx]

    def get_value_by_mode(param, mode):
        if mode == ParameterMode.POSITION:
            return read_memory(param)
        if mode == ParameterMode.RELATIVE:
            return read_memory(process_state.relative_base + param)
        return param  # immediate mode

    def store_memory(idx, mode, val):
        if mode == ParameterMode.RELATIVE:
            idx += process_state.relative_base
        extend_memory_space(idx)
        memory[idx] = int(val)

    def offset_relative_base(val):
        process_state.relative_base += val

    def unary_operator(operator, param1, mode1) -> None:
        val = get_value_by_mode(param1, mode1)
        res = operator(val)
        # (if operation returns a result) store result in same operation
        if res is not None:
            store_memory(param1, mode1, res)
    unary_operator.arg_count = 1

    def binary_jump_option_operator(operator, param1, param2, mode1, mode2) -> int:
        val1 = get_value_by_mode(param1, mode1)
        val2 = get_value_by_mode(param2, mode2)
        return operator(val1, val2)
    binary_jump_option_operator.arg_count = 2

    def binary_store_operator(operator, param1, param2, param3, mode1, mode2, mode3) -> None:
        store_memory(param3, mode3, binary_jump_option_operator(operator, param1, param2, mode1, mode2))
    binary_store_operator.arg_count = 3

    opcode_map = {
        OpCode.ADD: (binary_store_operator, add),
        OpCode.MULTIPLY: (binary_store_operator, mul),
        OpCode.INPUT: (unary_operator, input_op),
        OpCode.OUTPUT: (unary_operator, output_op),
        OpCode.JUMP_IF_TRUE: (binary_jump_option_operator, true_option),
        OpCode.JUMP_IF_FALSE: (binary_jump_option_operator, false_option),
        OpCode.LESSER_THAN: (binary_store_operator, lt),
        OpCode.GREATER_THAN: (binary_store_operator, eq),
        OpCode.RELATIVE_BASE_OFFSET: (unary_operator, offset_relative_base)
    }

    if process_state.program_counter >= len(memory):
        raise ParseError("Program ended without explicit halt")

    instruction = memory[process_state.program_counter]
    parameter_modes = str(instruction // 100)[::-1]  # in reverse order of parameters
    opcode = OpCode(instruction % 100)

    if opcode == OpCode.HALT:
        return None
    elif opcode in opcode_map:
        operator_type, operator_func = opcode_map[opcode]

        if len(memory) <= process_state.program_counter + operator_type.arg_count:
            raise ParseError("Missing required arguments for opcode: {}".format(opcode))

        modes = {'mode{}'.format(idx+1): ParameterMode.POSITION for idx in range(operator_type.arg_count)}
        modes.update({'mode{}'.format(idx+1): ParameterMode(int(digit)) for idx, digit in enumerate(parameter_modes)})
        args = memory[process_state.program_counter + 1: process_state.program_counter + operator_type.arg_count + 1]

        option_jump = operator_type(operator_func, *args, **modes)
        if option_jump is None:
            process_state.program_counter = process_state.program_counter + operator_type.arg_count + 1
        else:
            process_state.program_counter = option_jump
        return process_state
    else:
        raise ParseError("Unknown opcode: {}".format(opcode))


def run(arr, input_op=read_int, output_op=print_value, **proc_kw_args):
    proc_state = ProcessState(**proc_kw_args)
    while proc_state is not None:
        proc_state = _run_instruction(arr, proc_state, input_op=input_op, output_op=output_op)


def run_sub_routine(arr, *args, **proc_kw_args):
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

    run(arr, input_op=supply_input, output_op=output_builder, **proc_kw_args)
    return tuple(output_tuple)


def make_async_input_operator():
    input_queue = []

    def enqueue_integer_input(val):
        try:
            val = int(val)
        except ValueError:
            raise ValueError("Invalid integer input {}.".format(val))
        input_queue.append(val)

    def read_input_operator(*unused):
        del unused
        if input_queue:
            return input_queue.pop(0)
        else:
            raise WaitingInputSignal('')

    return read_input_operator, enqueue_integer_input


def make_async_output_operator():
    output_queue = []

    def has_output():
        return len(output_queue) > 0

    def dequeue_output():
        if not output_queue:
            return None
        return output_queue.pop(0)

    def store_output_operator(val):
        output_queue.append(val)

    return store_output_operator, has_output, dequeue_output


def run_until_next_input(arr, initial_input=None, **proc_kw_args):
    async_input_op, append_input = make_async_input_operator()
    async_output_op, has_output, get_output = make_async_output_operator()
    proc_state = ProcessState(**proc_kw_args)

    if initial_input is not None:
        append_input(initial_input)

    while proc_state is not None:
        try:
            proc_state = _run_instruction(arr, proc_state, input_op=async_input_op, output_op=async_output_op)
            while has_output():
                yield get_output()
        except WaitingInputSignal:
            append_input((yield))
            continue
