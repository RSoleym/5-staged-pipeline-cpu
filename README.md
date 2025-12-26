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

ADD, SUB, AND

BEQ, JMP

MOV

8 general-purpose registers (R0-R7)

32-bit registers and instructions

Status: In design / planning phase.

Target: FPGA-based implementation with instruction-level verification.
