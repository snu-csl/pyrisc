# The PyRISC Project
# Sample Build Scripts

## Introduction

This directory contains Makefile and linker script (`link.ld`) to show how to build PyRISC-compatible RISC-V executable files. We also provide several sample RISC-V assembly programs that can be used to verify the correctness of pipelined RISC-V simulators. Note that you are allowed to use all the RISC-V pseudo-instructions such as `li`, `mv`, `call`, `ret`, etc. supported by the GNU toolchain.

## RISC-V programs

This directory contains the following RISC-V assembly programs and their pre-compiled executable binaries.

* `fib.s`: computes the Fibonacci number. 
* `sum100.s`: computes the sum of integers from 1 to 100.
* `forward.s`: shows a sequence of instructions that have data dependences among them.
* `branch.s`: shows a case for mispredicted branch.
* `loaduse.s`: shows an example of load-use data hazard.

## Building the executable file

To build the PyRISC-compatible RISC-V executable file, just type `make`. Each assembly file is compiled using 32-bit RISC-V compiler that supports RV32I RISC-V instruction set. For the given object file(s), the executable binary is generated using the linker script named `link.ld`. The linker script is used to place each section in the predefined memory address. Note that you should build the RISC-V GNU Toolchain first as specified in the PyRISC top-level [README.md](https://github.com/snu-csl/pyrisc/blob/master/README.md) file.

```
$ make
riscv32-unknown-elf-gcc -c -Og -march=rv32i -mabi=ilp32 -static   fib.s -o fib.o
riscv32-unknown-elf-gcc -T./link.ld -nostdlib -nostartfiles -o fib fib.o
riscv32-unknown-elf-objdump -D --section=.text --section=.data fib > fib.objdump
riscv32-unknown-elf-gcc -c -Og -march=rv32i -mabi=ilp32 -static   sum100.s -o sum100.o
riscv32-unknown-elf-gcc -T./link.ld -nostdlib -nostartfiles -o sum100 sum100.o
riscv32-unknown-elf-objdump -D --section=.text --section=.data sum100 > sum100.objdump
riscv32-unknown-elf-gcc -c -Og -march=rv32i -mabi=ilp32 -static   loaduse.s -o loaduse.o
riscv32-unknown-elf-gcc -T./link.ld -nostdlib -nostartfiles -o loaduse loaduse.o
riscv32-unknown-elf-objdump -D --section=.text --section=.data loaduse > loaduse.objdump
riscv32-unknown-elf-gcc -c -Og -march=rv32i -mabi=ilp32 -static   forward.s -o forward.o
riscv32-unknown-elf-gcc -T./link.ld -nostdlib -nostartfiles -o forward forward.o
riscv32-unknown-elf-objdump -D --section=.text --section=.data forward > forward.objdump
riscv32-unknown-elf-gcc -c -Og -march=rv32i -mabi=ilp32 -static   branch.s -o branch.o
riscv32-unknown-elf-gcc -T./link.ld -nostdlib -nostartfiles -o branch branch.o
riscv32-unknown-elf-objdump -D --section=.text --section=.data branch > branch.objdump
```

## Running the executable file

Just type `make run` to run the executable file `fib` on the __snurisc__ instruction set simulator. You can see that the `a0` register has the value 8 at the end of the simulation which is the result of `fib(5)`.

```
$ make run
../sim/snurisc.py -l 1 fib
Loading file fib
Execution completed
Registers
=========
zero ($0): 0x00000000    ra ($1):   0x8000000c    sp ($2):   0x80020000    gp ($3):   0x00000000
tp ($4):   0x00000000    t0 ($5):   0x00000000    t1 ($6):   0x00000000    t2 ($7):   0x00000000
s0 ($8):   0x00000000    s1 ($9):   0x00000000    a0 ($10):  0x00000008    a1 ($11):  0x00000000
a2 ($12):  0x00000000    a3 ($13):  0x00000000    a4 ($14):  0x00000000    a5 ($15):  0x00000001
a6 ($16):  0x00000000    a7 ($17):  0x00000000    s2 ($18):  0x00000000    s3 ($19):  0x00000000
s4 ($20):  0x00000000    s5 ($21):  0x00000000    s6 ($22):  0x00000000    s7 ($23):  0x00000000
s8 ($24):  0x00000000    s9 ($25):  0x00000000    s10 ($26): 0x00000000    s11 ($27): 0x00000000
t3 ($28):  0x00000000    t4 ($29):  0x00000000    t5 ($30):  0x00000000    t6 ($31):  0x00000000
162 instructions executed in 162 cycles. CPI = 1.000
Data transfer:    42 instructions (25.93%)
ALU operation:    74 instructions (45.68%)
Control transfer: 46 instructions (28.40%)
```

## Disassembling the executable files

The disassembled files are also automatically created during `make` using the `riscv32-unknown-elf-objdump` command. Please refer to `*.objdump` files.

```
$ cat fib.objdump

fib:     file format elf32-littleriscv


Disassembly of section .text:

80000000 <_start>:
80000000:       80020137                lui     sp,0x80020
80000004:       00500513                li      a0,5
80000008:       008000ef                jal     ra,80000010 <fib>
8000000c:       00100073                ebreak

80000010 <fib>:
80000010:       00100793                li      a5,1
80000014:       04a7d263                bge     a5,a0,80000058 <Exit>
80000018:       ff010113                addi    sp,sp,-16 # 8001fff0 <_end+0xfff0>
8000001c:       00112623                sw      ra,12(sp)
80000020:       00812423                sw      s0,8(sp)
80000024:       00912223                sw      s1,4(sp)
80000028:       00050413                mv      s0,a0
8000002c:       fff50513                addi    a0,a0,-1
80000030:       fe1ff0ef                jal     ra,80000010 <fib>
80000034:       00050493                mv      s1,a0
80000038:       ffe40513                addi    a0,s0,-2
8000003c:       fd5ff0ef                jal     ra,80000010 <fib>
80000040:       00a48533                add     a0,s1,a0
80000044:       00c12083                lw      ra,12(sp)
80000048:       00812403                lw      s0,8(sp)
8000004c:       00412483                lw      s1,4(sp)
80000050:       01010113                addi    sp,sp,16
80000054:       00008067                ret

80000058 <Exit>:
80000058:       00100513                li      a0,1
8000005c:       00008067                ret
```

---

Jin-Soo Kim<br>
Systems Software and Architecture Laboratory<br>
Seoul National University<br>
http://csl.snu.ac.kr<br>
