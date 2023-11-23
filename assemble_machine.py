
inst_lst = ["NOP", "LDI", "LDS", "STS", "MOV", "JMP", "INC", "DEC", "CLR", "ADD", "SUB", "AND", "OR", "XOR", "NOT"]
inst_code = ["0000", "0001", "0010", "0011", "0100", "0101", "0110", "0111", "1000", "1001", "1010", "1011", "1100", "1101", "1110"]


def assemble_machine(instruction):
    func_lst = [NOP, LDI, LDS, STS, MOV, JMP, INC, DEC, CLR, ADD, SUB, AND, OR, XOR, NOT]
    opcode = instruction.split(" ")[0].upper()
    return func_lst[inst_lst.index(opcode)](instruction)  # return a list of bytes (as a string)


def opcode_binary(instruction):
    return inst_code[inst_lst.index(instruction.split(" ")[0].upper())]


def str_binary(num_str, bin_len):
    num = bin(eval(num_str))[2:]
    if len(num) < bin_len:
        num = ("0" * (bin_len - len(num))) + num
    return num


def NOP(instruction):
    return [opcode_binary(instruction) + "0000"]


def LDI(instruction):
    opcode = opcode_binary(instruction)
    register = str_binary(instruction[instruction.index(" ") + 2:instruction.index(",")], 4)
    value = str_binary(instruction[instruction.index(",") + 1:], 8)
    return [opcode + register, value]


def LDS(instruction):
    opcode = opcode_binary(instruction)
    register = str_binary(instruction[instruction.index(" ") + 2:instruction.index(",")], 4)
    address = str_binary(instruction[instruction.index(",") + 1:], 8)
    return [opcode + register, address]


def STS(instruction):
    opcode = opcode_binary(instruction)
    register = str_binary(instruction[instruction.index(",") + 2:], 4)
    address = str_binary(bin(eval(instruction[instruction.index(" ") + 1:instruction.index(",")])), 8)
    return [opcode + register, address]


def MOV(instruction):
    opcode = opcode_binary(instruction)
    register_dst = str_binary(instruction[instruction.index(" ") + 2:instruction.index(",")], 4)
    register_src = str_binary(instruction[(instruction.index(",") + 2):], 4)
    return [opcode + "0000", register_dst + register_src]


def JMP(instruction):
    opcode = opcode_binary(instruction)
    address = str_binary(instruction[instruction.index(" ") + 1:], 8)
    return [opcode + "0000", address]


def INC(instruction):
    opcode = opcode_binary(instruction)
    register = str_binary(instruction[instruction.index(" ") + 2:], 4)
    return [opcode + register]


def DEC(instruction):
    opcode = opcode_binary(instruction)
    register = str_binary(instruction[instruction.index(" ") + 2:], 4)
    return [opcode + register]


def CLR(instruction):
    opcode = opcode_binary(instruction)
    register = str_binary(instruction[instruction.index(" ") + 2:], 4)
    return [opcode + register]


def ADD(instruction):
    opcode = opcode_binary(instruction)
    register_dst = str_binary(instruction[instruction.index(" ") + 2:instruction.index(",")], 4)
    register_src = str_binary(instruction[(instruction.index(",") + 2):], 4)
    return [opcode + "0000", register_dst + register_src]


def SUB(instruction):
    opcode = opcode_binary(instruction)
    register_dst = str_binary(instruction[instruction.index(" ") + 2:instruction.index(",")], 4)
    register_src = str_binary(instruction[(instruction.index(",") + 2):], 4)
    return [opcode + "0000", register_dst + register_src]


def AND(instruction):
    opcode = opcode_binary(instruction)
    register_dst = str_binary(instruction[instruction.index(" ") + 2:instruction.index(",")], 4)
    register_src = str_binary(instruction[(instruction.index(",") + 2):], 4)
    return [opcode + "0000", register_dst + register_src]


def OR(instruction):
    opcode = opcode_binary(instruction)
    register_dst = str_binary(instruction[instruction.index(" ") + 2:instruction.index(",")], 4)
    register_src = str_binary(instruction[(instruction.index(",") + 2):], 4)
    return [opcode + "0000", register_dst + register_src]


def XOR(instruction):
    opcode = opcode_binary(instruction)
    register_dst = str_binary(instruction[instruction.index(" ") + 2:instruction.index(",")], 4)
    register_src = str_binary(instruction[(instruction.index(",") + 2):], 4)
    return [opcode + "0000", register_dst + register_src]


def NOT(instruction):
    opcode = opcode_binary(instruction)
    register = str_binary(instruction[instruction.index(" ") + 2:], 4)
    return [opcode + register]
