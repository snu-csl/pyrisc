# The PyRISC Project

## Introduction

The PyRISC project aims at providing various RISC-V toolset written in Python for educational purposes. It includes the RISC-V instruction set simulator and pipelined RISC-V processor simulators. All the simulators accept the executable file compiled with the standard GNU toolchain that supports RV32I base instruction set. Some of instructions are intentionally left unimplemented for class projects.

## The PyRISC Project Subdirectories

Currently, the following tools are available:

* `./sim`: A RISC-V instruction set simulator for RV32I base instruction set
* `./pipe5`: A simulator for 5-stage pipelined RISC-V processor implementation with RV32I instruction set
* `./asm`: Makefile, linker script, and examples for building PyRISC-compatible RISC-V executable files

Please see the README file in each subdirectory for more information.


## Prerequisites

The PyRISC toolset requires Python version 3.6 or higher. In addition, the PyRISC toolset depends on Python modules such as `numpy` and `pyelftools`. These modules can be installed on Ubuntu 18.04LTS as follows:

```
$ sudo apt-get install python3-numpy python3-pyelftools
```

## Building PyRISC-compatible RISC-V GNU toolchain

In order to work with the PyRISC toolset, you need to build a RISC-V GNU toolchain for the RV32I instruction set. To build the RISC-V toolchain on your machine (on either Linux or MacOS), please take the following steps.

### 1. Install prerequisite packages first

For Ubuntu 18.04LTS, perform the following command:
```
$ sudo apt-get install autoconf automake autotools-dev curl libmpc-dev
$ sudo apt-get install libmpfr-dev libgmp-dev gawk build-essential bison flex
$ sudo apt-get install texinfo gperf libtool patchutils bc zlib1g-dev libexpat-dev
```

If your machine runs MacOS, perform the following command:
```
$ brew install gawk gnu-sed gmp mpfr libmpc isl zlib expat
```

### 2. Download the RISC-V GNU Toolchain from Github

```
$ git clone --recursive https://github.com/riscv/riscv-gnu-toolchain
```

### 3. Configure the RISC-V GNU toolchain

```
$ cd riscv-gnu-toolchain
$ mkdir build
$ cd build
$ ../configure --prefix=/opt/riscv --with-arch=rv32i
```

### 4. Compile and install them.


```
$ sudo make
```
Note that they are installed in the path given as the prefix, i.e. `/opt/riscv` in this example.

### 5. Add `/opt/riscv/bin` in your `PATH`

```
$ export PATH=/opt/riscv/bin:$PATH
```

## License

PyRISC is offered under the terms of the Open Source Initiative BSD 3-Clause License. More information about this license can be found [here](http://opensource.org/licenses/BSD-3-Clause).


---

Jin-Soo Kim<br>
Systems Software and Architecture Laboratory<br>
Seoul National University<br>
http://csl.snu.ac.kr<br>
