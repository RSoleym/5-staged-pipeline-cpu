5-Stage Pipelined RISC CPU (FPGA)

Author: Ramtin Soleymani

Overview:

A custom 5-stage pipelined RISC CPU implemented in SystemVerilog, targeting the Basys 3 (Artix-7) FPGA.
The design follows a Harvard architecture and focuses on correct pipelining, control flow, and hazard handling.

Pipeline:

IF - Instruction Fetch

ID - Instruction Decode

EX - Execute / Branch

MEM - Data Memory

WB - Write Back

ISA (v1):

LOAD, STORE

ADD, ADDI, SUB, AND

BEQ, JMP

MOV

8 general-purpose registers (R0-R7)

32-bit registers and instructions


Assembly -> Machine Code Workflow

This CPU project is supported by a custom Python-scripted assembler that converts an assembly program into hexadecimal machine code making it suitible for CPU’s instruction memory.

The assembler: (check /docs/operand_format.png for formating)

Reads assembly code from a .asm file (asm_instr.asm).

Checks if instructions lines exceed 2kb instruction memory.

Splits the assmbly key words and numbers into a 2d array (removing '#', ',', ';', '[]').

If Key words match CPU's ISA, Register Length convert into string binary.

Garantees values do not exceed 32 bit unsigned, instruction memory does not exceed current number of instruction lines, and data memory does not exceed 4kb.

adds all the string values of the binary, converts into hex, and stores them in a .hex file (hex_instr.hex).

Status: 

ASM -> HEX Assembler Completed
CPU datapath and piepline stages in progress

Target: FPGA-based implementation with instruction-level verification.