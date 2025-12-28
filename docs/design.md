Registers:

R0-R7 (R0 is always preset to 1)

32-Bits


BRAM:

2kB for Instruction

4kB for Data


Instructions:

000000 -> Register Format

000001 -> LOAD: Loads a value from address into register

000010 -> STORE: Stores a register into an address

000011 -> ADD: Adds two registers

000100 -> ADDI: Adds one register with one Immidiate Value

000101 -> SUB: Subtracts two registers

000110 -> AND: Returns one if the bit by bit values are one 

000111 -> BEQ: compares two registers if true then jumps to an address

001000 -> JMP: Jump to an address

001001 -> MOV: copies register to a register




Vivado stores the data in Instruction RAM, starting from address zero.
CPU Fetch, reads the Instructions using an increment from 0.


Instruction Fetch -> Instruction Decode -> Execute -> Memory Access -> Write Back


Instruction Fetch: 

- Increment Program Counter 

- Reads instruction set from the instruction address (Send Instruction Decode)


Instruction Decode: 

- Turn the instruction words into 4 Bit op-code

- ADD, SUB, AND, BEQ is for ALU

- JMP is for branch decision

- LOAD, STORE is for data handling

- MOV is for register handling 

 

Execute:

- ALU does the operations and sends the results to register handling, if BEQ is true sends the data to branch decision

- branch decision changes the Program counter to the designed instruction address 


Memory Access:

- data handling either loads or stores memory


Write Back:

- register handling updates the desired register



Source Modules:

cpu_fpga_top.sv

cpu_top.sv

if_stage.sv

id_stage.sv

alu.sv

ex_branch.sv 

mem_stage.sv

wb_stage.sv

pipeline_reg.sv

hazard_handle.sv

instr_mem.sv

data_mem.sv