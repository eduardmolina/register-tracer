import re


INSTRUCTION_PATTERN = '^(\w*)  (\D+) (.+,)? ?(.*)'
DISPLACEMENT_PATTERN = '\[(\w+)\+.*\]'


class Instruction(object):

    def __init__(self, rip, instruction, opcode, operand1, operand2):
        self.instruction = instruction
        self.rip = rip
        self.opcode = opcode
        self.operand1 = operand1
        self.operand2 = operand2


def get_file_content(file_path):
    
    content = []
    with open(file_path) as f:
        content = f.readlines()

    return content


def parse_instruction(instruction):

    def parse_opcode(raw_opcode):
        return raw_opcode.split(' ')

    rip = '0x0'
    opcode = ''
    operand1 = ''
    operand2 = ''
    if 'dword ptr' not in instruction and \
        (match := re.match(INSTRUCTION_PATTERN, instruction)):

        groups = match.groups()
        rip = groups[0]
        
        opcode_info = parse_opcode(groups[1])
        if len(opcode_info) == 1:
            operand1 = groups[2] if groups[2] else ''
        else:
            operand1 = opcode_info[1]

        opcode = opcode_info[0]
        operand2 = groups[3]
    else:
        print(f'Instruction not parsed: {instruction}')

    return Instruction(
        rip,
        instruction,
        opcode,
        operand1.replace(',', ''),
        operand2)


def parse_instructions(instructions):
    return [*map(
        lambda i: parse_instruction(i.replace('\n', '')), instructions)]


def find_last_operand_attribution_index(operand, instructions):

    index = -1
    for i, instruction in enumerate(reversed(instructions)):

        if operand == instruction.operand1:
            index = len(instructions) - i - 1
            break

    return index


def has_displacement(operand):
    return re.match(DISPLACEMENT_PATTERN, operand)


def get_register_from_operand(operand, match):
    
    register = ''
    if match:
        register = match.groups()[0]

    return register


def track_register_from(start_index, instructions):

    tracking_instructions = []
    tracking_registers = [instructions[start_index].operand1]
    
    for instruction in reversed(instructions[:start_index + 1]):
    
        tracking_register = instruction.operand1 if instruction.operand1 \
            else instruction.operand2
        if tracking_register in tracking_registers:

            tracking_instructions.append(instruction)

            if instruction.opcode == 'mov' or instruction.opcode == 'lea':
                tracking_registers.remove(tracking_register)

            register2 = instruction.operand2
            displacement_match = has_displacement(register2)
            if displacement_match:
                register2 = get_register_from_operand(register2, displacement_match)

            if register2 not in tracking_registers:
                tracking_registers.append(register2)

    return reversed(tracking_instructions)


def run(dump_path, register):
    file_content = get_file_content(dump_path)
    instructions = parse_instructions(file_content)
    last_index = find_last_operand_attribution_index(register, instructions)
    tracking_instructions = track_register_from(last_index, instructions)

    for instruction in tracking_instructions:
        print(instruction.instruction)


if __name__ == '__main__':

    dump_path = input('Dump path: ')
    register = input('Register to track: ')
    
    run(dump_path, register)
