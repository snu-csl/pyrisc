# The PyRISC Project
# A RISC-V Instruction Set Simulator

## Introduction

This directory contains "__snurisc__", an implementation of RISC-V instruction set simulator in Python. __snurisc__ supports most of RV32I base instruction set.

## Machine Model

### Supported Instructions

Among the 40 instructions defined in the RV32I base instruction set, __snurisc__ supports the following 31 instructions:

* ALU instructions: `lui`, `auipc`, `addi`, `slti`, `sltiu`, `xori`, `ori`, `andi`, `slli`, `srli`, `srai`, `add`, `sub`, `sll`, `slt`, `sltu`, `xor`, `srl`, `sra`, `or`, `and`
* Memory access instructions: `lw`, `sw`
* Control transfer instructions: `jal`, `jalr`, `beq`, `bne`, `blt`, `bge`, `bltu`, `bgeu`

### Special Instruction

* `ebreak`: The `ebreak` instruction is used to return control to a debugging environment. In __snurisc__, we use the `ebreak` instruction to stop the execution of the simulator.

### Unsupported Instructions

The following RV32I instructions are not supported in __snurisc__:

* `fence`: The `fence` instruction is used to order device I/O and memory accesses.
* `ecall`: The `ecall` instruction is originally used to make a service request to the execution environment. We reserve this instruction to simulate some of system calls in a future extension.

### Unimplemented Instructions

The following instructions are intentionally left unimplemented for future class projects.

* `lb`, `lh`, `lbu`, `lhu`, `sb`, `sh`

### Memory

The target machine is assumed to have separate Instruction Memory (imem) and Data Memory (dmem), whose sizes are 64KB each. imem starts at memory address 0x80000000 followed by dmem. Hence, the valid memory regions are 0x80000000 ~ 0x8000ffff for imem, and 0x80010000 ~ 0x8001ffff for dmem. The stack pointer should be initialized to 0x80020000 by the startup code.

## Running __snurisc__

First, you need to install Python modules, `numpy` and `elftools`, to run __snurisc__. Please refer to the top-level PyRISC [README.md](https://github.com/snu-csl/pyrisc/blob/master/README.md) file for installation steps for these modules.

Basically, __snurisc__ requires the name of the executable file to run, as shown in the following. You can print various log information each cycle or at the end of the program execution by using the `-l` argument. You can also configure the simulator to print logs after a certain number of cycles by using the `-c` argument.

```
SNURISC: A RISC-V Instruction Set Simulator in Python
Usage: ./snurisc.py [-l n] [-c m] filename
        filename: RISC-V executable file name
        -l sets the desired log level n (default: 1)
           0: shows no output message
           1: dumps registers at the end of the execution
           2: dumps registers and data memory at the end of the execution
           3: 2 + shows instruction executed in each cycle
           4: 3 + shows full information for each instruction
           5: 4 + dumps registers for each cycle
           6: 5 + dumps data memory for each cycle
        -c shows logs after cycle m (default: 0, only effective for log level 3 or higher)
```

## Building an Executable File

__snurisc__ accepts a RISC-V executable file compiled by the standard RISC-V GNU toolchain that supports the RV32I base instruction set. In order to build the RISC-V GNU toolchain for use with __snurisc__, please refer to the [README.md](https://github.com/snu-csl/pyrisc/blob/master/README.md) in the PyRISC top-level directory.

There are several restrictions when an executable file is built from a RISC-V assembly program on __snurisc__.
1. The text section should begin at the memory address 0x80000000, which is the start address of the Instruction Memory (imem).
2. Similarly, the data section should begin at the memory address 0x80010000 which is the start address of the Data Memory (dmem).
3. The entry point to the code should be explicitly marked with the `_start` label. It is used to initialize the `pc` register before the program is executed.
4. No standard C startup code or libraries should be linked to the executable file.

In order to meet these requirements, we provide Makefile and linker script that can be used to build PyRISC-compatible RISC-V executable files. They are available in the ``../asm`` directory.

Note that, unlike the "golden standard" RISC-V instruction set simulator [spike](https://github.com/riscv/riscv-isa-sim), __snurisc__ does not support Privileged instructions nor HTIF (Host-Target Interface). Hence, any program on __snurisc__ should not rely on application execution environment such as [pk](https://github.com/riscv/riscv-pk).


---
Jin-Soo Kim<br>
Systems Software and Architecture Laboratory<br>
Seoul National University<br>
http://csl.snu.ac.kr
