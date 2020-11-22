# The PyRISC Project
# SNURISC5: A 5-Stage Pipelined RISC-V Simulator

## Introduction

This directory contains "__snurisc5__", an implementation of 5-stage pipelined RISC-V instruction set simulator in Python. __snurisc5__ supports most of RV32I base instruction set.

## Machine Model

### Supported Instructions

Among the 40 instructions defined in the RV32I base instruction set, __snurisc5__ supports the following 31 instructions:

* ALU instructions: `lui`, `auipc`, `addi`, `slti`, `sltiu`, `xori`, `ori`, `andi`, `slli`, `srli`, `srai`, `add`, `sub`, `sll`, `slt`, `sltu`, `xor`, `srl`, `sra`, `or`, `and`
* Memory access instructions: `lw`, `sw`
* Control transfer instructions: `jal`, `jalr`, `beq`, `bne`, `blt`, `bge`, `bltu`, `bgeu`

### Special Instruction

* `ebreak`: The `ebreak` instruction is used to return control to a debugging environment. In __snurisc5__, we use the `ebreak` instruction to stop the execution of the simulator.

### Unsupported Instructions

The following RV32I instructions are not supported in __snurisc5__:

* `fence`: The `fence` instruction is used to order device I/O and memory accesses.
* `ecall`: The `ecall` instruction is originally used to make a service request to the execution environment. 

### Unimplemented Instructions

The following instructions are intentionally left unimplemented for future class projects.

* `lb`, `lh`, `lbu`, `lhu`, `sb`, `sh`

### Memory

The target machine is assumed to have separate Instruction Memory (imem) and Data Memory (dmem), whose sizes are 64KB each. imem starts at memory address 0x80000000 followed by dmem. Hence, the valid memory regions are 0x80000000 ~ 0x8000ffff for imem, and 0x80010000 ~ 0x8001ffff for dmem. The stack pointer should be initialized to 0x80020000 by the startup code.

## Pipeline implementation

The pipeline implementation of __snurisc5__ is based on a standard 5-stage pipelining architecture consisting of IF (Instruction Fetch), ID (Instruction Decode), EX (Execution), MM (Memory), and WB (Write Back) stages. The overall simulation architecture is inspired by the educational [Y86-64 processor simulator](http://csapp.cs.cmu.edu/3e/simguide.pdf) developed by Randal E. Bryant and David O. Hallaron. The internal microarchitecture of the 5-stage pipeline is largely based on the [riscv-sodor](https://github.com/ucb-bar/riscv-sodor) project, which provides educational microarchitectures for RISC-V ISA developed by UC Berkeley's Architecture Group. For overall pipeline architecture, please refer to the `snurisc5.pdf` file in this directory.

## Differences from the Textbook's 5-stage pipeline

The textbook, _Computer Organization and Design: RISC-V Edition_ (by David A. Patterson and John L. Hennessy, COD for short), shows an example of 5-stage RISC-V processor implementation for a subset of instructions such as `ld`, `sd`, `add`, `sub`, `and`, `or`, and `beq`. Please note that the implementation of __snurisc5__ has the following differences compared with the COD book.

* __32-bit RISC-V processor with support for RV32I ISA__: Although the COD book describes the 64-bit RISC-V CPU, __snurisc5__ is a 32-bit RISC-V CPU. Therefore, all the registers are 32-bit wide and 64-bit instructions such as `ld` and `sd` are not supported.

* __Data forwarding is handled in the ID stage__: In the COD book, forwarding detection logic is in the EX stage. At the beginning of the EX stage, the forwarding logic detects whether there are dependencies between the current instruction in the EX stage and any previous instructions. If there is a data hazard, the value from the previous instruction (either in MEM or in WB stage) is forwarded to the corresponding input of the ALU. On the contrary, __snurisc5__ detects any data hazard in the ID stage, and the value from previous instructions is forwarded to the ID stage.

* __Data is written to the register file at the end of the cycle__:  In the COD book, it is assumed that data is written to the register file during the first half of the cycle and it can be read during the last half of the cycle. In __snurisc5__, however, we assume that data is always written to the register file at the end of the WB stage. Therefore, a data value needs to be forwarded from WB to ID when the value is required by the instruction in the ID stage.

* __The branch outcome is determined at the end of EX stage__: In the COD book, the branch outcome is known at the MEM stage leading to 3-cycle penalty for mispredicted branch. Although the book suggests a way to move branch decision in the ID stage by using additional hardware, it requires more data forwarding paths. Instead, __snurisc5__ determines whether the branch is taken or not at the end of the EX stage. Therefore, __snurisc5__ requires 2-cycle penalty for mispredicted branch.

## Running __snurisc5__

First, you need to install Python modules, `numpy` and `pyelftools`, to run __snurisc__. Please refer to the top-level PyRISC [README.md](https://github.com/snu-csl/pyrisc/blob/master/README.md) file for installation steps for these modules.

Basically, __snurisc5__ requires the name of the executable file to run, as shown in the following. You can print various log information each cycle or at the end of the program execution by using the `-l` argument. You can also configure the simulator to print logs after a certain number of cycles by using the `-c` argument.

```
$ ./snurisc5.py
SNURISC5: A 5-stage Pipelined RISC-V ISA Simulator in Python
Usage: ./snurisc5.py [-l n] [-c m] filename
        filename: RISC-V executable file name
        -l sets the desired log level n (default: 4)
           0: shows no output message
           1: dumps registers at the end of the execution
           2: dumps registers and memory at the end of the execution
           3: 2 + shows instructions retired from the WB stage
           4: 3 + shows all the instructions in the pipeline
           5: 4 + shows full information for each instruction
           6: 5 + dumps registers for each cycle
           7: 6 + dumps data memory for each cycle
        -c shows logs after cycle m (default: 0, only effective for log level 3 or higher)
```

## Building an Executable File

__snurisc5__ accepts a RISC-V executable file compiled by the standard RISC-V GNU toolchain that supports the RV32I base instruction set. In order to build the RISC-V GNU toolchain for use with __snurisc5__, please refer to the [README.md](https://github.com/snu-csl/pyrisc/blob/master/README.md) in the PyRISC top-level directory.

There are several restrictions when an executable file is built from a RISC-V assembly program on __snurisc5__.
1. The text section should begin at the memory address 0x80000000, which is the start address of the Instruction Memory (imem).
2. Similarly, the data section should begin at the memory address 0x80010000 which is the start address of the Data Memory (dmem).
3. The entry point to the code should be explicitly marked with the `_start` label. It is used to initialize the `pc` register before the program is executed.
4. No standard C startup code or libraries should be linked to the executable file.

In order to meet these requirements, we provide Makefile and linker script that can be used to build PyRISC-compatible RISC-V executable files. They are available in the ``../asm`` directory.

Note that, unlike the "golden standard" RISC-V instruction set simulator [spike](https://github.com/riscv/riscv-isa-sim), __snurisc__ does not support Privileged instructions nor HTIF (Host-Target Interface). Hence, any program on __snurisc__ should not rely on application execution environment such as [pk](https://github.com/riscv/riscv-pk).

## Sample Run

The following shows the output of a sample run of `loaduse` program in the `../asm` directory with setting the log level to 5:

```
$ ./snurisc5.py -l 5 ../asm/loaduse
Loading file ../asm/loaduse
--------------------------------------------------
0 [IF] 0x80000000: lui    t0, 0x80010000         # inst=0x800102b7, pc_next=0x80000004
0 [ID] 0x00000000: BUBBLE                        # -
0 [EX] 0x00000000: BUBBLE                        # -
0 [MM] 0x00000000: BUBBLE                        # -
0 [WB] 0x00000000: BUBBLE                        # -
--------------------------------------------------
1 [IF] 0x80000004: addi   t6, zero, 3            # inst=0x00300f93, pc_next=0x80000008
1 [ID] 0x80000000: lui    t0, 0x80010000         # rd=5 rs1=2 rs2=0 op1=0x00000000 op2=0x80010000
1 [EX] 0x00000000: BUBBLE                        # -
1 [MM] 0x00000000: BUBBLE                        # -
1 [WB] 0x00000000: BUBBLE                        # -
--------------------------------------------------
2 [IF] 0x80000008: sw     t6, 0(t0)              # inst=0x01f2a023, pc_next=0x8000000c
2 [ID] 0x80000004: addi   t6, zero, 3            # rd=31 rs1=0 rs2=3 op1=0x00000000 op2=0x00000003
2 [EX] 0x80000000: lui    t0, 0x80010000         # 0x80010000 <- 0x80010000 (pass 2)
2 [MM] 0x00000000: BUBBLE                        # -
2 [WB] 0x00000000: BUBBLE                        # -
--------------------------------------------------
3 [IF] 0x8000000c: addi   t6, t6, 10             # inst=0x00af8f93, pc_next=0x80000010
3 [ID] 0x80000008: sw     t6, 0(t0)              # rd=0 rs1=5 rs2=31 op1=0x80010000 op2=0x00000000
3 [EX] 0x80000004: addi   t6, zero, 3            # 0x00000003 <- 0x00000000 + 0x00000003
3 [MM] 0x80000000: lui    t0, 0x80010000         # -
3 [WB] 0x00000000: BUBBLE                        # -
--------------------------------------------------
4 [IF] 0x80000010: lw     t6, 0(t0)              # inst=0x0002af83, pc_next=0x80000014
4 [ID] 0x8000000c: addi   t6, t6, 10             # rd=31 rs1=31 rs2=10 op1=0x00000003 op2=0x0000000a
4 [EX] 0x80000008: sw     t6, 0(t0)              # 0x80010000 <- 0x80010000 + 0x00000000
4 [MM] 0x80000004: addi   t6, zero, 3            # -
4 [WB] 0x80000000: lui    t0, 0x80010000         # R[5] <- 0x80010000
--------------------------------------------------
5 [IF] 0x80000014: addi   t6, t6, -1             # inst=0xffff8f93, pc_next=0x80000018
5 [ID] 0x80000010: lw     t6, 0(t0)              # rd=31 rs1=5 rs2=0 op1=0x80010000 op2=0x00000000
5 [EX] 0x8000000c: addi   t6, t6, 10             # 0x0000000d <- 0x00000003 + 0x0000000a
5 [MM] 0x80000008: sw     t6, 0(t0)              # M[0x80010000] <- 0x00000003
5 [WB] 0x80000004: addi   t6, zero, 3            # R[31] <- 0x00000003
--------------------------------------------------
6 [IF] 0x80000018: addi   t6, t6, -1             # inst=0xffff8f93, pc_next=0x8000001c
6 [ID] 0x80000014: addi   t6, t6, -1             # rd=31 rs1=31 rs2=31 op1=0x80010000 op2=0xffffffff
6 [EX] 0x80000010: lw     t6, 0(t0)              # 0x80010000 <- 0x80010000 + 0x00000000
6 [MM] 0x8000000c: addi   t6, t6, 10             # -
6 [WB] 0x80000008: sw     t6, 0(t0)              # -
--------------------------------------------------
7 [IF] 0x80000018: addi   t6, t6, -1             # inst=0xffff8f93, pc_next=0x8000001c
7 [ID] 0x80000014: addi   t6, t6, -1             # rd=31 rs1=31 rs2=31 op1=0x00000003 op2=0xffffffff
7 [EX] 0x80000014: BUBBLE                        # -
7 [MM] 0x80000010: lw     t6, 0(t0)              # 0x00000003 <- M[0x80010000]
7 [WB] 0x8000000c: addi   t6, t6, 10             # R[31] <- 0x0000000d
--------------------------------------------------
8 [IF] 0x8000001c: ebreak                        # inst=0x00100073, pc_next=0x80000020
8 [ID] 0x80000018: addi   t6, t6, -1             # rd=31 rs1=31 rs2=31 op1=0x00000002 op2=0xffffffff
8 [EX] 0x80000014: addi   t6, t6, -1             # 0x00000002 <- 0x00000003 + 0xffffffff
8 [MM] 0x80000014: BUBBLE                        # -
8 [WB] 0x80000010: lw     t6, 0(t0)              # R[31] <- 0x00000003
--------------------------------------------------
9 [IF] 0x80000020: (illegal)                     # inst=0x00000000, pc_next=0x80000024
9 [ID] 0x8000001c: ebreak                        # rd=0 rs1=0 rs2=1 op1=0x00000000 op2=0x00000000
9 [EX] 0x80000018: addi   t6, t6, -1             # 0x00000001 <- 0x00000002 + 0xffffffff
9 [MM] 0x80000014: addi   t6, t6, -1             # -
9 [WB] 0x80000014: BUBBLE                        # -
--------------------------------------------------
10 [IF] 0x80000024: (illegal)                     # inst=0x00000000, pc_next=0x80000028
10 [ID] 0x80000020: BUBBLE                        # -
10 [EX] 0x8000001c: ebreak                        # -
10 [MM] 0x80000018: addi   t6, t6, -1             # -
10 [WB] 0x80000014: addi   t6, t6, -1             # R[31] <- 0x00000002
--------------------------------------------------
11 [IF] 0x80000028: (illegal)                     # inst=0x00000000, pc_next=0x8000002c
11 [ID] 0x80000024: BUBBLE                        # -
11 [EX] 0x80000020: BUBBLE                        # -
11 [MM] 0x8000001c: ebreak                        # -
11 [WB] 0x80000018: addi   t6, t6, -1             # R[31] <- 0x00000001
--------------------------------------------------
12 [IF] 0x8000002c: (illegal)                     # inst=0x00000000, pc_next=0x80000030
12 [ID] 0x80000028: BUBBLE                        # -
12 [EX] 0x80000024: BUBBLE                        # -
12 [MM] 0x80000020: BUBBLE                        # -
12 [WB] 0x8000001c: ebreak                        # -
Execution completed
Registers
=========
zero ($0): 0x00000000    ra ($1):   0x00000000    sp ($2):   0x00000000    gp ($3):   0x00000000    
tp ($4):   0x00000000    t0 ($5):   0x80010000    t1 ($6):   0x00000000    t2 ($7):   0x00000000    
s0 ($8):   0x00000000    s1 ($9):   0x00000000    a0 ($10):  0x00000000    a1 ($11):  0x00000000    
a2 ($12):  0x00000000    a3 ($13):  0x00000000    a4 ($14):  0x00000000    a5 ($15):  0x00000000    
a6 ($16):  0x00000000    a7 ($17):  0x00000000    s2 ($18):  0x00000000    s3 ($19):  0x00000000    
s4 ($20):  0x00000000    s5 ($21):  0x00000000    s6 ($22):  0x00000000    s7 ($23):  0x00000000    
s8 ($24):  0x00000000    s9 ($25):  0x00000000    s10 ($26): 0x00000000    s11 ($27): 0x00000000    
t3 ($28):  0x00000000    t4 ($29):  0x00000000    t5 ($30):  0x00000000    t6 ($31):  0x00000001    
Memory 0x80010000 - 0x8001ffff
==============================
0x80010000:  03 00 00 00  (0x00000003)
8 instructions executed in 13 cycles. CPI = 1.625
Data transfer:    2 instructions (25.00%)
ALU operation:    5 instructions (62.50%)
Control transfer: 1 instructions (12.50%)
```

---
Jin-Soo Kim<br>
Systems Software and Architecture Laboratory<br>
Seoul National University<br>
http://csl.snu.ac.kr
