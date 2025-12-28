import sys
import os



BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
file_path_asm = os.path.join(PROJECT_ROOT, "programs", "asm_instr.asm")
file_path_hex = os.path.join(PROJECT_ROOT, "programs", "hex_instr.hex")


max_reg_mem = 65535
max_instr_mem = 512
max_data_mem = 0x0FFC

register_format_opcode = "000000"

instr_string = ["LOAD", "STORE", "ADD", "ADDI", "SUB", "AND", "BEQ", "JMP", "MOV"]
reg_string = ["R0", "R1", "R2", "R3", "R4", "R5", "R6", "R7"]

instr_bin = ["000001", "000010", "000011", "000100", "000101", "000110", "000111", "001000", "001001"]
reg_bin = ["00000", "00001", "00010", "00011", "00100", "00101", "00110", "00111"]
asm_lines = []


def reg_bin_format(reg):
    if reg in reg_string:
        return reg_bin[reg_string.index(reg)]
    else:
        print("Error: Unknown Register Command.")
        sys.exit(1)

def instr_bin_format(opcode):
    if opcode in instr_string:
        return instr_bin[instr_string.index(opcode)]
    else:
        print("Error: Unknown Instruction Command.")
        sys.exit(1)

def instr_format(asm_instr):
    if asm_instr in ["LOAD", "STORE", "BEQ", "ADDI"]:
        return "Immediate"
    elif asm_instr in ["ADD", "SUB", "AND", "MOV"]:
        return "Register"
    elif asm_instr == "JMP":
        return "Jump"
    else:
        print("Error: Unknown Instruction Command.")
        sys.exit(1)


def reg_format(reg1, reg2, reg3, func_code):
    if func_code == "MOV":
        return register_format_opcode + reg_bin_format(reg1) + reg_bin_format(reg2) + "00000" + instr_bin_format(func_code)
    else:
        return register_format_opcode + reg_bin_format(reg1) + reg_bin_format(reg2) + reg_bin_format(reg3) + instr_bin_format(func_code)

def immediate_format(op_code, reg1, reg2, immediate):
    if op_code in ["ADDI", "BEQ"]:
        return instr_bin_format(op_code) + reg_bin_format(reg1) + reg_bin_format(reg2) + immediate
    elif op_code in ["LOAD", "STORE"]:
        return instr_bin_format(op_code) + reg_bin_format(reg1) + "00000" + immediate

def jump_format(op_code, word_address):
    return instr_bin_format(op_code) + word_address

with open(file_path_asm, 'r') as file:
    for line in file:
        stripped_line = line.strip()
        if stripped_line and (not stripped_line.startswith(';') and not stripped_line.startswith('#')):
            stripped_line = stripped_line.split(';')[0].strip()
            asm_lines.append(stripped_line)

if len(asm_lines) > max_instr_mem:
    print("Error: Exceeded maximum instruction memory.")
    sys.exit(1)

parsed_lines = []

for line in asm_lines:
    clean_line = line.replace(",", "")
    parts = clean_line.split()
    parsed_lines.append(parts)


for i in range(len(parsed_lines)):
    asm_instr = parsed_lines[i][0]

    if instr_format(asm_instr) == "Register":
        if (asm_instr == "MOV" and len(parsed_lines[i]) == 3) or (asm_instr != "MOV" and len(parsed_lines[i]) == 4):
            if asm_instr == "MOV":
                reg1 = parsed_lines[i][1]
                reg2 = parsed_lines[i][2]
                binary_string_instr = reg_format(reg1, reg2, "Null", asm_instr)
            else:
                reg1 = parsed_lines[i][1]
                reg2 = parsed_lines[i][2]
                reg3 = parsed_lines[i][3]
                binary_string_instr = reg_format(reg1, reg2, reg3, asm_instr)
        else:
            print("Error: Too Many Arguements.")
            sys.exit(1)       
    elif instr_format(asm_instr) == "Immediate":
        if (asm_instr == "ADDI" and len(parsed_lines[i]) == 4) or (asm_instr != "ADDI" and len(parsed_lines[i]) == 3) or (asm_instr == "BEQ" and len(parsed_lines[i]) == 4):
            if asm_instr == "ADDI":
                reg1 = parsed_lines[i][1]
                reg2 = parsed_lines[i][2]
                try:
                    im_int_value = int(parsed_lines[i][3], 0)
                except ValueError:
                    print("Error: Wrong Immediate Format")
                    sys.exit(1)

                if im_int_value < 0 or im_int_value > max_reg_mem:
                    print("Error: Wrong Memory Format.")
                    sys.exit(1)       
                else:
                    im_str_value = format(im_int_value, '016b') 

                binary_string_instr = immediate_format(asm_instr, reg1, reg2, im_str_value)
            elif asm_instr == "BEQ":
                reg1 = parsed_lines[i][1]
                reg2 = parsed_lines[i][2]
                try:
                    im_int_value = int(parsed_lines[i][3], 0)
                except ValueError:
                    print("Error: Wrong Immediate Format")
                    sys.exit(1)

                if im_int_value < 0 or im_int_value > (len(asm_lines) * 4 - 4) or im_int_value % 4 != 0:
                    print("Error: Wrong Memory Format.")
                    sys.exit(1)
                else:
                    im_str_value = format(im_int_value, '016b') 

                binary_string_instr = immediate_format(asm_instr, reg1, reg2, im_str_value)
            elif asm_instr == "LOAD" or asm_instr == "STORE":
                reg1 = parsed_lines[i][1]
                if parsed_lines[i][2].startswith('[') and parsed_lines[i][2].endswith(']'):
                    im_int_value = int(parsed_lines[i][2].strip("[]"), 0)

                    if im_int_value < 0 or im_int_value > max_data_mem or im_int_value %4 !=0:
                        print("Error: Wrong Memory Format.")
                        sys.exit(1)       
                    else:
                        im_str_value = format(im_int_value, '016b') 
                else:
                    print("Error: Wrong Immediate Format")
                    sys.exit(1)    

                binary_string_instr = immediate_format(asm_instr, reg1, "Null", im_str_value)
        else:
            print("Error: Too Many Arguements.")
            sys.exit(1)   
    elif instr_format(asm_instr) == "Jump":
        if len(parsed_lines[i]) == 2:
            try:
                im_int_value = int(parsed_lines[i][1], 0)
            except ValueError:
                print("Error: Wrong Immediate Format")
                sys.exit(1)

            if im_int_value < 0 or im_int_value > (len(asm_lines) * 4 - 4) or im_int_value %4 !=0:
                print("Error: Wrong Memory Format.")
                sys.exit(1)       
            else:
                im_str_value = format(im_int_value, '026b') 
           
            binary_string_instr = jump_format(asm_instr, im_str_value)
        else:
            print("Error: Too Many Arguements.")
            sys.exit(1)


    hex_string_instr = format(int(binary_string_instr, 2), '08X')

    parsed_lines[i] = hex_string_instr


with open(file_path_hex, 'w') as file:
    for line in parsed_lines:
        file.write(line + '\n')
